import { useAuthStore } from "@/stores/auth-store";

export class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string;
  private onMessageCallback: ((data: any) => void) | null = null;

  constructor(endpoint: string) {
    const baseUrl = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";
    this.url = `${baseUrl}${endpoint}`;
  }

  connect() {
    const token = useAuthStore.getState().token;
    if (!token) return;

    this.ws = new WebSocket(`${this.url}?token=${token}`);

    this.ws.onmessage = (event) => {
      if (this.onMessageCallback) {
        try {
          const data = JSON.parse(event.data);
          this.onMessageCallback(data);
        } catch (e) {
          console.error("Failed to parse WebSocket message", e);
        }
      }
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error", error);
    };
  }

  onMessage(callback: (data: any) => void) {
    this.onMessageCallback = callback;
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}
