import os

files = {
    "app/(protected)/audit/page.tsx": """'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Filter, Download, ShieldCheck, UserCircle, FileText, Settings, Key, AlertTriangle, Eye, Activity, ChevronRight, X, Terminal, Monitor, Lock, CheckCircle2, XCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'

const AUDIT_LOGS = [
  { id: 'evt-1', timestamp: '2025-01-15 11:47:32.456', user: 'Rahul Sharma', role: 'Officer', action: 'login', resource: 'User', resourceId: 'user-uuid', details: 'Successful login from Pune', ip: '192.168.1.45', device: 'Chrome/Win', status: 'Success', severity: 'Info', icon: Key },
  { id: 'evt-2', timestamp: '2025-01-15 11:45:18.234', user: 'Rahul Sharma', role: 'Officer', action: 'document_uploaded', resource: 'Document', resourceId: 'doc-uuid', details: 'Uploaded rajesh_itr.pdf', ip: '192.168.1.45', device: 'Chrome/Win', status: 'Success', severity: 'Info', icon: FileText },
  { id: 'evt-3', timestamp: '2025-01-15 11:44:52.789', user: 'Rahul Sharma', role: 'Officer', action: 'case_created', resource: 'Case', resourceId: 'TL-20250115-0847', details: 'Created new case for Rajesh Kumar', ip: '192.168.1.45', device: 'Chrome/Win', status: 'Success', severity: 'Info', icon: Activity },
  { id: 'evt-4', timestamp: '2025-01-15 11:32:15.123', user: 'System', role: 'System', action: 'analysis_completed', resource: 'Case', resourceId: 'TL-20250115-0851', details: 'Analysis completed in 87s', ip: '-', device: 'Backend', status: 'Success', severity: 'Success', icon: Monitor },
  { id: 'evt-5', timestamp: '2025-01-15 11:15:47.567', user: 'Priya Verma', role: 'Officer', action: 'case_decided', resource: 'Case', resourceId: 'TL-20250115-0834', details: 'Decided: FLAG_FOR_REVIEW', ip: '192.168.1.52', device: 'Chrome/Win', status: 'Success', severity: 'Warning', icon: ShieldCheck },
  { id: 'evt-6', timestamp: '2025-01-15 10:47:23.890', user: 'Admin User', role: 'Admin', action: 'settings_updated', resource: 'Settings', resourceId: 'risk-thresholds', details: 'Updated high risk threshold from 50 to 45', ip: '192.168.1.10', device: 'Chrome/Win', status: 'Success', severity: 'Info', icon: Settings },
  { id: 'evt-7', timestamp: '2025-01-15 10:30:11.345', user: 'Unknown', role: 'None', action: 'failed_login', resource: 'User', resourceId: '-', details: 'Failed login attempt for admin@bank.com', ip: '45.67.89.12', device: 'Unknown', status: 'Failed', severity: 'Critical', icon: AlertTriangle }
]

export default function AuditLogsPage() {
  const [selectedLog, setSelectedLog] = useState<any>(null)
  const [search, setSearch] = useState('')

  return (
    <div className="max-w-[1600px] mx-auto pb-20 relative h-[calc(100vh-64px)] overflow-hidden flex flex-col">
      
      {/* Header & Stats */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-white p-6 rounded-t-2xl shadow-sm border-b border-slate-200 shrink-0">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Audit Logs</h1>
            <span className="bg-emerald-100 text-emerald-700 border border-emerald-200 text-[10px] font-bold px-2 py-0.5 rounded flex items-center gap-1 uppercase tracking-wider">
              <ShieldCheck className="w-3 h-3" /> RBI Inspection Ready
            </span>
          </div>
          <p className="text-sm text-slate-500">Complete system activity trail</p>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="text-right mr-4 border-r border-slate-200 pr-4">
            <p className="text-xs text-slate-500 font-bold uppercase tracking-wider">Events Today</p>
            <p className="text-lg font-black text-slate-900">1,847</p>
          </div>
          <Button variant="outline" className="border-slate-200 text-slate-700 shadow-sm"><Filter className="w-4 h-4 mr-2" /> Filters</Button>
          <Button className="bg-primary hover:bg-primary-600 shadow-md text-white"><Download className="w-4 h-4 mr-2" /> Export Logs</Button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        
        {/* Main Log Table */}
        <div className="flex-1 bg-slate-50 flex flex-col overflow-hidden">
          
          <div className="p-4 border-b border-slate-200 bg-white flex justify-between items-center shrink-0">
            <div className="relative w-96">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input type="text" placeholder="Search logs, IPs, or users..." className="w-full pl-9 pr-4 py-2 border border-slate-200 rounded-lg text-sm outline-none focus:border-primary shadow-sm" value={search} onChange={(e) => setSearch(e.target.value)} />
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-500 flex items-center gap-2"><div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div> Live Monitoring Active</span>
            </div>
          </div>

          <div className="flex-1 overflow-auto custom-scrollbar">
            <table className="w-full text-left border-collapse min-w-[1200px]">
              <thead className="bg-slate-100 text-xs uppercase tracking-wider text-slate-500 font-bold sticky top-0 z-10 border-b border-slate-200 shadow-sm">
                <tr>
                  <th className="p-4 w-48">Timestamp</th>
                  <th className="p-4 w-56">User</th>
                  <th className="p-4 w-48">Action</th>
                  <th className="p-4 w-32">Resource</th>
                  <th className="p-4">Details</th>
                  <th className="p-4 w-32">IP Address</th>
                  <th className="p-4 w-24">Status</th>
                  <th className="p-4 w-20"></th>
                </tr>
              </thead>
              <tbody className="text-sm bg-white divide-y divide-slate-100">
                {AUDIT_LOGS.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50 transition-colors group">
                    <td className="p-4 font-mono text-xs text-slate-500 whitespace-nowrap">{log.timestamp}</td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <UserCircle className="w-4 h-4 text-slate-400" />
                        <span className="font-medium text-slate-900">{log.user}</span>
                        <span className={`text-[9px] px-1.5 py-0.5 rounded uppercase font-bold ${log.role === 'Admin' ? 'bg-amber-100 text-amber-700' : log.role === 'Officer' ? 'bg-blue-100 text-blue-700' : 'bg-slate-200 text-slate-600'}`}>{log.role}</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <div className="flex items-center gap-2">
                        <log.icon className="w-4 h-4 text-slate-400" />
                        <span className="font-mono text-xs text-slate-700">{log.action}</span>
                      </div>
                    </td>
                    <td className="p-4">
                      <span className="bg-slate-100 text-slate-600 text-[10px] px-2 py-1 rounded font-bold uppercase tracking-widest">{log.resource}</span>
                    </td>
                    <td className="p-4 text-slate-600 truncate max-w-xs">{log.details}</td>
                    <td className="p-4 font-mono text-xs text-slate-500">{log.ip}</td>
                    <td className="p-4">
                      {log.status === 'Success' ? (
                        <span className="flex items-center gap-1 text-emerald-600 text-xs font-bold"><CheckCircle2 className="w-3 h-3" /> Success</span>
                      ) : (
                        <span className="flex items-center gap-1 text-red-600 text-xs font-bold"><XCircle className="w-3 h-3" /> Failed</span>
                      )}
                    </td>
                    <td className="p-4 text-right">
                      <Button variant="ghost" size="sm" onClick={() => setSelectedLog(log)} className="text-primary hover:bg-primary-50 h-7 text-xs font-bold px-2">View</Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* JSON Metadata Slider */}
        <AnimatePresence>
          {selectedLog && (
            <motion.div 
              initial={{ x: '100%', opacity: 0 }} 
              animate={{ x: 0, opacity: 1 }} 
              exit={{ x: '100%', opacity: 0 }} 
              transition={{ type: "spring", damping: 25 }}
              className="absolute right-0 top-0 bottom-0 w-[550px] bg-white border-l border-slate-200 shadow-2xl z-20 flex flex-col"
            >
              <div className="p-6 border-b border-slate-200 flex justify-between items-start bg-slate-50/50">
                <div>
                  <h2 className="text-lg font-bold text-slate-900 mb-1 flex items-center gap-2">Event Details</h2>
                  <p className="text-xs text-slate-500 font-mono">ID: {selectedLog.id} • {selectedLog.timestamp}</p>
                </div>
                <button onClick={() => setSelectedLog(null)} className="p-2 hover:bg-slate-200 rounded-full text-slate-500 transition-colors">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-6">
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Actor</p>
                    <p className="font-bold text-slate-900">{selectedLog.user}</p>
                    <p className="text-xs text-slate-500">{selectedLog.ip} • {selectedLog.device}</p>
                  </div>
                  <div className="bg-slate-50 p-4 rounded-xl border border-slate-100">
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Resource</p>
                    <p className="font-bold text-slate-900">{selectedLog.resource}</p>
                    <p className="text-xs text-slate-500">{selectedLog.resourceId}</p>
                  </div>
                </div>

                <section>
                  <h3 className="text-sm font-bold text-slate-900 mb-3 border-b border-slate-100 pb-2 flex items-center gap-2"><Terminal className="w-4 h-4 text-slate-400" /> JSON Payload Metadata</h3>
                  <div className="bg-[#0B1121] rounded-xl p-5 text-slate-300 font-mono text-xs shadow-inner overflow-x-auto relative group">
                    <Button size="sm" variant="outline" className="absolute top-2 right-2 h-7 bg-white/10 border-white/20 text-white hover:bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity">Copy</Button>
                    <p className="text-slate-500">&#123;</p>
                    <p className="pl-4"><span className="text-blue-400">"event_id"</span>: <span className="text-emerald-400">"{selectedLog.id}"</span>,</p>
                    <p className="pl-4"><span className="text-blue-400">"timestamp"</span>: <span className="text-emerald-400">"{selectedLog.timestamp}"</span>,</p>
                    <p className="pl-4"><span className="text-blue-400">"action"</span>: <span className="text-emerald-400">"{selectedLog.action}"</span>,</p>
                    <p className="pl-4"><span className="text-blue-400">"actor"</span>: &#123;</p>
                    <p className="pl-8"><span className="text-blue-400">"user_id"</span>: <span className="text-emerald-400">"usr_9f8e7d"</span>,</p>
                    <p className="pl-8"><span className="text-blue-400">"role"</span>: <span className="text-emerald-400">"{selectedLog.role}"</span>,</p>
                    <p className="pl-8"><span className="text-blue-400">"ip_address"</span>: <span className="text-emerald-400">"{selectedLog.ip}"</span>,</p>
                    <p className="pl-8"><span className="text-blue-400">"user_agent"</span>: <span className="text-emerald-400">"Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."</span></p>
                    <p className="pl-4">&#125;,</p>
                    <p className="pl-4"><span className="text-blue-400">"request"</span>: &#123;</p>
                    <p className="pl-8"><span className="text-blue-400">"method"</span>: <span className="text-emerald-400">"POST"</span>,</p>
                    <p className="pl-8"><span className="text-blue-400">"endpoint"</span>: <span className="text-emerald-400">"/api/v1/auth/login"</span></p>
                    <p className="pl-4">&#125;</p>
                    <p className="text-slate-500">&#125;</p>
                  </div>
                </section>

                <section>
                  <h3 className="text-sm font-bold text-slate-900 mb-3 border-b border-slate-100 pb-2 flex items-center gap-2"><Lock className="w-4 h-4 text-slate-400" /> Compliance Notes</h3>
                  <div className="bg-blue-50 border border-blue-100 rounded-lg p-4 text-sm text-blue-900">
                    This log entry is cryptographically hashed and immutable per RBI guidelines. Retention period is set to 5 years.
                  </div>
                </section>

              </div>
              
              <div className="p-6 border-t border-slate-200 bg-slate-50 flex gap-3">
                <Button variant="outline" className="flex-1 border-slate-200 text-slate-700 bg-white hover:bg-slate-50">View Related Events</Button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </div>
  )
}
"""
}

def scaffold():
    for path, content in files.items():
        dir_path = os.path.dirname(path)
        os.makedirs(dir_path, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
if __name__ == "__main__":
    scaffold()
    print("Scaffolded Audit Logs Page.")
