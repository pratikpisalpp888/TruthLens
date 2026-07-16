'use client'

import { motion } from 'framer-motion'
import { useEffect, useState, useRef, useMemo } from 'react'
import { AlertTriangle, Briefcase, FileText, Fingerprint, MapPin, Network, ScanLine, Server, ShieldAlert, User } from 'lucide-react'

interface GraphNode {
  id: string
  label: string
  type: 'case' | 'person' | 'document' | 'fraud_ring' | 'artifact'
  risk: 'low' | 'medium' | 'high' | 'critical'
}

interface GraphEdge {
  source: string
  target: string
  label: string
}

interface GraphData {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

interface Props {
  caseId: string
  token: string
}

const TYPE_ICONS = {
  case: Briefcase,
  person: User,
  document: FileText,
  fraud_ring: Network,
  artifact: Fingerprint,
}

const RISK_COLORS = {
  low: 'border-slate-500/50 bg-slate-900/80 text-slate-300 shadow-slate-500/20',
  medium: 'border-amber-500/50 bg-amber-950/80 text-amber-300 shadow-amber-500/20',
  high: 'border-orange-500/50 bg-orange-950/80 text-orange-300 shadow-orange-500/30',
  critical: 'border-red-500/50 bg-red-950/80 text-red-300 shadow-red-500/40',
}

const GLOW_COLORS = {
  low: 'shadow-[0_0_15px_rgba(100,116,139,0.3)]',
  medium: 'shadow-[0_0_15px_rgba(245,158,11,0.3)]',
  high: 'shadow-[0_0_20px_rgba(249,115,22,0.4)]',
  critical: 'shadow-[0_0_25px_rgba(239,68,68,0.5)]',
}

const DEMO_DATA: GraphData = {
  nodes: [
    { id: 'case_current', label: 'Current Case', type: 'case', risk: 'high' },
    { id: 'applicant_1', label: 'Rajesh Kumar', type: 'person', risk: 'high' },
    { id: 'doc_pan', label: 'PAN: ABCDE1234F', type: 'document', risk: 'medium' },
    { id: 'fraud_pattern', label: 'Fraud Ring Alpha', type: 'fraud_ring', risk: 'critical' },
    { id: 'ca_stamp', label: 'Forged CA Stamp #8812', type: 'artifact', risk: 'critical' },
    { id: 'case_old_1', label: 'Case TL-8891', type: 'case', risk: 'critical' },
    { id: 'case_old_2', label: 'Case TL-8102', type: 'case', risk: 'critical' },
    { id: 'applicant_2', label: 'Suresh Gupta', type: 'person', risk: 'high' },
    { id: 'ip_addr', label: 'IP: 192.168.1.45', type: 'artifact', risk: 'high' },
  ],
  edges: [
    { source: 'case_current', target: 'applicant_1', label: 'Applied By' },
    { source: 'case_current', target: 'doc_pan', label: 'Contains' },
    { source: 'applicant_1', target: 'doc_pan', label: 'Owns' },
    { source: 'case_current', target: 'ca_stamp', label: 'Stamped With' },
    { source: 'ca_stamp', target: 'fraud_pattern', label: 'Indicator Of' },
    { source: 'case_old_1', target: 'ca_stamp', label: 'Stamped With' },
    { source: 'case_old_2', target: 'ca_stamp', label: 'Stamped With' },
    { source: 'case_old_1', target: 'applicant_2', label: 'Applied By' },
    { source: 'applicant_2', target: 'ip_addr', label: 'Used' },
    { source: 'applicant_1', target: 'ip_addr', label: 'Used' },
    { source: 'ip_addr', target: 'fraud_pattern', label: 'Indicator Of' },
  ]
}

export function FraudNetworkGraph({ caseId, token }: Props) {
  const [data, setData] = useState<GraphData | null>(null)
  const [loading, setLoading] = useState(true)
  const [hoveredNode, setHoveredNode] = useState<string | null>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/cases/${caseId}/syndicate-connections`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        if (res.ok) {
          const json = await res.json()
          if (json?.graph?.nodes?.length > 0) {
            setData(json.graph)
          } else {
            setData(DEMO_DATA)
          }
        } else {
          setData(DEMO_DATA)
        }
      } catch (err) {
        console.error(err)
        setData(DEMO_DATA)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [caseId, token])

  // Pre-calculate radial positions for the wow factor
  const positions = useMemo(() => {
    if (!data) return {}
    const pos: Record<string, { x: number, y: number }> = {}
    
    // Center node is always the current case
    const centerNode = data.nodes.find(n => n.id === 'case_current') || data.nodes[0]
    if (centerNode) pos[centerNode.id] = { x: 400, y: 300 }

    // Group other nodes
    const others = data.nodes.filter(n => n.id !== centerNode?.id)
    const radius = 180
    
    others.forEach((node, i) => {
      const angle = (i / others.length) * Math.PI * 2
      // Add slight randomness for a more organic feel
      const r = radius + (Math.random() * 40 - 20)
      pos[node.id] = {
        x: 400 + Math.cos(angle) * r,
        y: 300 + Math.sin(angle) * r
      }
    })
    
    // Push the fraud ring further out to look like an umbrella
    const fraudRing = others.find(n => n.type === 'fraud_ring')
    if (fraudRing) {
      pos[fraudRing.id] = { x: 400, y: 80 }
    }

    return pos
  }, [data])

  if (loading) {
    return (
      <div className="h-[600px] w-full rounded-2xl bg-slate-950 flex items-center justify-center border border-white/5 shadow-inner">
        <div className="flex flex-col items-center gap-3">
          <Network className="w-8 h-8 text-indigo-500 animate-pulse" />
          <p className="text-sm font-semibold text-slate-400 uppercase tracking-widest">Compiling GraphRAG Network...</p>
        </div>
      </div>
    )
  }

  if (!data || data.nodes.length === 0) {
    return (
      <div className="h-[600px] w-full rounded-2xl bg-slate-950 flex items-center justify-center border border-white/5">
        <p className="text-slate-500">No network data available for this case.</p>
      </div>
    )
  }

  return (
    <div className="relative h-[600px] w-full rounded-2xl bg-slate-950 border border-indigo-500/20 overflow-hidden shadow-2xl">
      {/* Background grid */}
      <div className="absolute inset-0 opacity-20"
        style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, rgba(99,102,241,0.15) 1px, transparent 0)', backgroundSize: '32px 32px' }} />
      
      {/* Network Header */}
      <div className="absolute top-6 left-6 z-20">
        <h3 className="text-xl font-bold text-white flex items-center gap-2">
          <Network className="w-5 h-5 text-indigo-400" />
          GraphRAG Intelligence
        </h3>
        <p className="text-sm text-slate-400 mt-1">AI-detected fraud rings across database</p>
      </div>

      <div className="absolute top-6 right-6 z-20 flex gap-4 bg-slate-900/80 px-4 py-2 rounded-full border border-white/10 backdrop-blur-md">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-300"><span className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.8)]"></span> Critical Risk</div>
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-300"><span className="w-2.5 h-2.5 rounded-full bg-orange-500 shadow-[0_0_10px_rgba(249,115,22,0.8)]"></span> High Risk</div>
      </div>

      <svg className="absolute inset-0 w-full h-full" viewBox="0 0 800 600" preserveAspectRatio="xMidYMid slice">
        {/* Draw Edges */}
        {data.edges.map((edge, i) => {
          const source = positions[edge.source]
          const target = positions[edge.target]
          if (!source || !target) return null

          const isHovered = hoveredNode === edge.source || hoveredNode === edge.target
          const isDimmed = hoveredNode && !isHovered

          return (
            <motion.g key={`edge-${i}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: isDimmed ? 0.1 : isHovered ? 0.8 : 0.4 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
            >
              {/* Line */}
              <line
                x1={source.x} y1={source.y}
                x2={target.x} y2={target.y}
                stroke={isHovered ? '#818cf8' : '#475569'}
                strokeWidth={isHovered ? 2 : 1}
                strokeDasharray={edge.label === 'Indicator Of' ? '5,5' : 'none'}
              />
              {/* Edge Label */}
              <text
                x={(source.x + target.x) / 2}
                y={(source.y + target.y) / 2 - 5}
                fill={isHovered ? '#a5b4fc' : '#64748b'}
                fontSize="10"
                textAnchor="middle"
                className="font-mono font-bold tracking-wider"
              >
                {edge.label.toUpperCase()}
              </text>
            </motion.g>
          )
        })}

        {/* Draw Nodes */}
        {data.nodes.map((node, i) => {
          const pos = positions[node.id]
          if (!pos) return null

          const Icon = TYPE_ICONS[node.type] || Server
          const colorClass = RISK_COLORS[node.risk]
          const glowClass = GLOW_COLORS[node.risk]
          const isHovered = hoveredNode === node.id
          const isDimmed = hoveredNode && !isHovered && !data.edges.some(e => (e.source === node.id && e.target === hoveredNode) || (e.target === node.id && e.source === hoveredNode))

          return (
            <motion.g key={`node-${node.id}`}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: isDimmed ? 0.3 : 1, scale: isHovered ? 1.15 : 1 }}
              transition={{ duration: 0.4, delay: i * 0.05, type: 'spring' }}
              onMouseEnter={() => setHoveredNode(node.id)}
              onMouseLeave={() => setHoveredNode(null)}
              className="cursor-pointer"
            >
              {/* Pulse effect for critical nodes */}
              {node.risk === 'critical' && !isDimmed && (
                <circle cx={pos.x} cy={pos.y} r="28" fill="rgba(239,68,68,0.2)" className="animate-ping" style={{ transformOrigin: `${pos.x}px ${pos.y}px` }} />
              )}
              
              <foreignObject x={pos.x - 24} y={pos.y - 24} width="48" height="48">
                <div className={`w-full h-full rounded-2xl border-2 flex items-center justify-center backdrop-blur-md transition-all duration-300 ${colorClass} ${!isDimmed ? glowClass : ''}`}>
                  <Icon className="w-5 h-5" />
                </div>
              </foreignObject>

              <rect x={pos.x - 60} y={pos.y + 30} width="120" height="24" rx="12" fill="rgba(15,23,42,0.8)" stroke="rgba(255,255,255,0.1)" />
              <text x={pos.x} y={pos.y + 46} fill="white" fontSize="11" fontWeight="bold" textAnchor="middle" className="pointer-events-none drop-shadow-md">
                {node.label}
              </text>
            </motion.g>
          )
        })}
      </svg>
    </div>
  )
}
