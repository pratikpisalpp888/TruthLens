import { create } from 'zustand'

export type AgentStatus = 'waiting' | 'working' | 'completed' | 'error'

export interface AgentState {
  id: string
  name: string
  status: AgentStatus
  progress: number
  subtask: string
  findings: string[]
  timeTaken?: string
}

interface FinalSummary {
  decision: string
  risk_category: string
  composite_score: number
  confidence: number
  summary: string
}

interface AnalysisState {
  isAnalyzing: boolean
  isComplete: boolean
  progress: number
  timeElapsed: number
  agents: Record<string, AgentState>
  feed: { id: string; type: 'info' | 'warning' | 'critical' | 'success' | 'system'; message: string; time: string }[]
  metrics: { docs: number; findings: number; critical: number; mismatches: number }
  finalSummary: FinalSummary | null
  ws: WebSocket | null
  
  startSimulation: (caseId: string, token: string) => void
  reset: () => void
}

const initialAgents: Record<string, AgentState> = {
  classifier: { id: 'classifier', name: 'Document Classifier', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  forensic: { id: 'forensic', name: 'Forensic Investigator', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  crossref: { id: 'crossref', name: 'Cross-Reference Agent', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  compliance: { id: 'compliance', name: 'Compliance Agent', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
  decision: { id: 'decision', name: 'Decision Agent', status: 'waiting', progress: 0, subtask: 'Waiting for input...', findings: [] },
}

const AGENT_LABELS: Record<string, string> = {
  classifier: 'Document Classifier',
  forensic: 'Forensic Investigator',
  crossref: 'Cross-Reference Agent',
  compliance: 'Compliance Agent',
  decision: 'Decision Agent',
}

export const useAnalysisStore = create<AnalysisState>((set, get) => ({
  isAnalyzing: false,
  isComplete: false,
  progress: 0,
  timeElapsed: 0,
  agents: { ...initialAgents },
  feed: [],
  metrics: { docs: 0, findings: 0, critical: 0, mismatches: 0 },
  finalSummary: null,
  ws: null,

  startSimulation: async (caseId: string, token: string) => {
    // Reset state fresh
    set({
      isAnalyzing: true,
      isComplete: false,
      progress: 0,
      timeElapsed: 0,
      agents: { ...initialAgents },
      feed: [],
      metrics: { docs: 0, findings: 0, critical: 0, mismatches: 0 },
      finalSummary: null,
    })
    
    const timer = setInterval(() => {
      set(state => ({ timeElapsed: state.timeElapsed + 1 }))
    }, 1000)

    const addFeed = (type: 'info' | 'warning' | 'critical' | 'success' | 'system', message: string) => {
      set(state => ({
        feed: [{ id: Date.now().toString() + Math.random(), type, message, time: 'just now' }, ...state.feed]
      }))
    }

    // Trigger analysis API
    try {
      const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const res = await fetch(`${BASE}/api/v1/cases/${caseId}/analyze`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) {
        addFeed('critical', `Failed to start analysis: HTTP ${res.status}`)
        clearInterval(timer)
        return
      }
    } catch (e) {
      addFeed('critical', 'Failed to connect to backend to trigger analysis')
      clearInterval(timer)
      return
    }

    // Connect WebSocket for live updates
    const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    const WS_URL = BASE_URL.replace(/^http/, 'ws')
    
    let ws: WebSocket
    try {
      ws = new WebSocket(`${WS_URL}/api/v1/cases/${caseId}/live-analysis`)
    } catch {
      addFeed('warning', 'Could not open WebSocket')
      clearInterval(timer)
      return
    }

    set({ ws })

    ws.onmessage = (event) => {
      let data: any
      try {
        data = JSON.parse(event.data)
      } catch {
        return
      }

      if (data.type === 'agent_progress') {
        const agent = data.agent as string
        const agentStatus = data.status as string
        const label = AGENT_LABELS[agent] || agent

        if (agentStatus === 'started') {
          set(state => ({
            agents: {
              ...state.agents,
              [agent]: {
                ...state.agents[agent],
                status: 'working',
                progress: 50,
                subtask: 'Analyzing...',
              },
            },
            progress: Math.min(state.progress + 15, 95),
          }))
          addFeed('system', `${label} started processing`)

        } else if (agentStatus === 'completed') {
          const result = data.data || {}
          set(state => ({
            agents: {
              ...state.agents,
              [agent]: {
                ...state.agents[agent],
                status: 'completed',
                progress: 100,
                subtask: 'Complete',
                timeTaken: 'done',
              },
            },
            metrics: {
              docs: result.docs_analyzed !== undefined ? result.docs_analyzed : state.metrics.docs,
              findings: result.anomalies !== undefined ? state.metrics.findings + result.anomalies : state.metrics.findings,
              critical: result.critical !== undefined ? state.metrics.critical + result.critical : state.metrics.critical,
              mismatches: result.mismatches !== undefined ? state.metrics.mismatches + result.mismatches : state.metrics.mismatches,
            }
          }))
          addFeed('success', `${label} finished`)
        }

      } else if (data.type === 'analysis_complete') {
        clearInterval(timer)
        const summary = data.summary || {}

        set({
          isComplete: true,
          progress: 100,
          finalSummary: {
            decision: summary.decision || 'flagged',
            risk_category: summary.risk_category || 'medium',
            composite_score: summary.composite_score ?? 0,
            confidence: summary.confidence ?? 0,
            summary: summary.summary || 'Analysis complete.',
          },
          metrics: {
            docs: summary.docs_analyzed ?? 0,
            findings: summary.anomalies ?? 0,
            critical: summary.critical ?? 0,
            mismatches: summary.mismatches ?? 0,
          },
          // Mark all agents as completed in case some missed their WS messages
          agents: Object.fromEntries(
            Object.entries(get().agents).map(([k, v]) => [
              k,
              v.status === 'waiting' ? { ...v, status: 'completed' as AgentStatus, progress: 100, subtask: 'Complete' } : v
            ])
          ),
        })
        addFeed('success', `✅ Analysis complete! Decision: ${(summary.decision || 'FLAGGED').toUpperCase()}`)
        ws.close()

      } else if (data.type === 'analysis_error') {
        clearInterval(timer)
        addFeed('critical', `Analysis error: ${data.error || 'Unknown error'}`)
        ws.close()
      }
    }

    ws.onerror = () => {
      addFeed('warning', 'WebSocket issue — switching to polling mode...')
    }

    ws.onclose = () => {
      // If WS closed before we got analysis_complete, start polling
      if (!get().isComplete) {
        addFeed('system', 'Connection dropped — polling for results...')
        _startPolling(caseId, token, addFeed, timer)
      }
    }
  },

  reset: () => {
    const ws = get().ws
    if (ws) {
      try { ws.close() } catch {}
    }
    set({
      isAnalyzing: false,
      isComplete: false,
      agents: { ...initialAgents },
      feed: [],
      progress: 0,
      timeElapsed: 0,
      ws: null,
      finalSummary: null,
      metrics: { docs: 0, findings: 0, critical: 0, mismatches: 0 },
    })
  },
}))

/** Poll /analysis-status every 4s until complete — fallback when WebSocket drops */
async function _startPolling(
  caseId: string,
  token: string,
  addFeed: (type: any, msg: string) => void,
  timer: ReturnType<typeof setInterval>
) {
  const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const store = useAnalysisStore.getState()

  let attempts = 0
  const MAX = 60 // 60 × 4s = 4 minutes max

  const poll = async () => {
    if (useAnalysisStore.getState().isComplete) return
    if (attempts++ >= MAX) {
      clearInterval(timer)
      addFeed('critical', 'Analysis timed out. Please check the case page.')
      return
    }

    try {
      const res = await fetch(`${BASE}/api/v1/cases/${caseId}/analysis-status`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const data = await res.json()

      if (data.status === 'completed' && data.summary) {
        clearInterval(timer)
        const summary = data.summary
        useAnalysisStore.setState({
          isComplete: true,
          progress: 100,
          finalSummary: {
            decision: summary.decision || 'flagged',
            risk_category: summary.risk_category || 'medium',
            composite_score: summary.composite_score ?? 0,
            confidence: summary.confidence ?? 0,
            summary: summary.summary || 'Analysis complete.',
          },
          metrics: {
            docs: summary.docs_analyzed ?? 0,
            findings: summary.anomalies ?? 0,
            critical: summary.critical ?? 0,
            mismatches: summary.mismatches ?? 0,
          },
          agents: Object.fromEntries(
            Object.entries(useAnalysisStore.getState().agents).map(([k, v]) => [
              k, v.status !== 'completed' ? { ...v, status: 'completed' as AgentStatus, progress: 100, subtask: 'Complete' } : v
            ])
          ),
        })
        addFeed('success', `✅ Analysis complete! Decision: ${(summary.decision || 'FLAGGED').toUpperCase()}`)
      }
    } catch {
      // network error — will retry next cycle
    }

    setTimeout(poll, 4000)
  }

  setTimeout(poll, 4000)
}
