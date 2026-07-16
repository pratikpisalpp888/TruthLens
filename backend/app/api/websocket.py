"""
TruthLens — WebSocket Router.

Real-time updates for analysis progress, notifications,
and live forensic processing status.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import structlog
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

logger = structlog.get_logger(__name__)
router = APIRouter()


class ConnectionManager:
    """
    WebSocket connection manager.

    Maintains active WebSocket connections and provides
    methods for broadcasting messages to subscribed clients.
    """

    def __init__(self) -> None:
        # Map of case_id -> list of active WebSocket connections
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, case_id: str) -> None:
        """
        Accept and register a new WebSocket connection.

        Args:
            websocket: The incoming WebSocket connection.
            case_id: The case ID to subscribe to.
        """
        await websocket.accept()
        if case_id not in self.active_connections:
            self.active_connections[case_id] = []
        self.active_connections[case_id].append(websocket)
        logger.info("ws.connected", case_id=case_id, total=len(self.active_connections[case_id]))

    def disconnect(self, websocket: WebSocket, case_id: str) -> None:
        """
        Remove a disconnected WebSocket from the registry.

        Args:
            websocket: The disconnected WebSocket.
            case_id: The case ID the connection was subscribed to.
        """
        if case_id in self.active_connections:
            self.active_connections[case_id].discard(websocket)
            if not self.active_connections[case_id]:
                del self.active_connections[case_id]
        logger.info("ws.disconnected", case_id=case_id)

    async def broadcast_to_case(self, case_id: str, message: dict[str, Any]) -> None:
        """
        Broadcast a message to all connections subscribed to a case.

        Args:
            case_id: The target case ID.
            message: The message payload to broadcast.
        """
        connections = self.active_connections.get(case_id, [])
        if connections:
            payload = json.dumps(message, default=str)
            dead_connections = []
            for connection in connections:
                try:
                    await connection.send_text(payload)
                except Exception:
                    dead_connections.append(connection)
            for dead in dead_connections:
                self.active_connections[case_id].discard(dead)

    async def broadcast_all(self, message: dict[str, Any]) -> None:
        """
        Broadcast a message to all connected clients.

        Args:
            message: The message payload to broadcast.
        """
        payload = json.dumps(message, default=str)
        for case_id, connections in list(self.active_connections.items()):
            dead = []
            for conn in connections:
                try:
                    await conn.send_text(payload)
                except Exception:
                    dead.append(conn)
            for d in dead:
                self.active_connections[case_id].discard(d)


# Global connection manager instance
manager = ConnectionManager()


@router.websocket("/ws/analysis/{case_id}")
async def analysis_websocket(
    websocket: WebSocket,
    case_id: str,
) -> None:
    """
    WebSocket endpoint for real-time analysis progress updates.

    Clients connect to this endpoint to receive live updates on:
    - Analysis start/progress/completion
    - Per-agent step notifications
    - Risk score updates
    - Error notifications

    Args:
        websocket: The WebSocket connection.
        case_id: The case ID to subscribe to.
    """
    await manager.connect(websocket, case_id)
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "case_id": case_id,
            "message": f"Subscribed to case {case_id} analysis updates.",
        })

        # Keep connection alive with ping/pong
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                # Send keepalive ping
                await websocket.send_json({"type": "ping"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, case_id)
    except Exception as exc:
        logger.error("ws.error", case_id=case_id, error=str(exc))
        manager.disconnect(websocket, case_id)


@router.websocket("/ws/notifications")
async def notifications_websocket(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for system-wide notifications.

    Provides alerts for:
    - New high-risk cases
    - System health changes
    - Admin broadcasts

    Args:
        websocket: The WebSocket connection.
    """
    await websocket.accept()
    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Connected to TruthLens notification stream.",
        })
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                msg = json.loads(data)
                if msg.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        logger.info("ws.notifications.disconnected")
