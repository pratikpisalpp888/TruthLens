'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { UserCircle, Bell, Shield, Sliders, Database, Key, Settings as SettingsIcon, Save, Upload, ShieldAlert, Zap, Globe, FileText } from 'lucide-react'
import { Button } from '@/components/ui/button'

const TABS = [
  { id: 'profile', label: 'My Profile', icon: UserCircle, group: 'User Preferences' },
  { id: 'notifications', label: 'Notifications', icon: Bell, group: 'User Preferences' },
  { id: 'security', label: 'Security', icon: Shield, group: 'User Preferences' },
  { id: 'thresholds', label: 'Risk Thresholds', icon: Sliders, group: 'Admin Settings' },
  { id: 'analysis', label: 'Analysis Config', icon: Zap, group: 'Admin Settings' },
  { id: 'system', label: 'System Config', icon: Database, group: 'Admin Settings' }
]

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('thresholds')

  return (
    <div className="max-w-6xl mx-auto pb-20 pt-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">System Settings</h1>
          <p className="text-slate-500 mt-1">Configure global parameters and user preferences</p>
        </div>
        <Button className="bg-primary hover:bg-primary-600 shadow-lg text-white font-bold h-10 px-6">
          <Save className="w-4 h-4 mr-2" /> Save All Changes
        </Button>
      </div>

      <div className="flex gap-8">
        
        {/* Vertical Tabs */}
        <div className="w-64 shrink-0">
          
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 px-3">Admin Settings</h3>
          <div className="space-y-1 mb-8">
            {TABS.filter(t => t.group === 'Admin Settings').map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-bold transition-all ${activeTab === tab.id ? 'bg-primary text-white shadow-md' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'}`}
              >
                <tab.icon className={`w-4 h-4 ${activeTab === tab.id ? 'text-primary-200' : 'text-slate-400'}`} />
                {tab.label}
              </button>
            ))}
          </div>

          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3 px-3">User Preferences</h3>
          <div className="space-y-1">
            {TABS.filter(t => t.group === 'User Preferences').map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-bold transition-all ${activeTab === tab.id ? 'bg-primary text-white shadow-md' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'}`}
              >
                <tab.icon className={`w-4 h-4 ${activeTab === tab.id ? 'text-primary-200' : 'text-slate-400'}`} />
                {tab.label}
              </button>
            ))}
          </div>

        </div>

        {/* Content Area */}
        <div className="flex-1">
          <AnimatePresence mode="wait">
            
            {activeTab === 'thresholds' && (
              <motion.div key="thresholds" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-6">
                
                <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-amber-100 text-amber-700 rounded-lg"><ShieldAlert className="w-5 h-5" /></div>
                    <div>
                      <h2 className="text-lg font-bold text-slate-900">Risk Score Thresholds</h2>
                      <p className="text-sm text-slate-500">Determine how cases are categorized based on their final trust score (0-100).</p>
                    </div>
                  </div>

                  <div className="space-y-6">
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <label className="text-sm font-bold text-slate-700">Critical Risk (Auto-Reject)</label>
                        <span className="text-sm font-bold text-red-600">0 - 15</span>
                      </div>
                      <input type="range" className="w-full accent-red-500" min="0" max="100" defaultValue="15" />
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <label className="text-sm font-bold text-slate-700">High Risk (Admin Review)</label>
                        <span className="text-sm font-bold text-amber-600">16 - 49</span>
                      </div>
                      <input type="range" className="w-full accent-amber-500" min="0" max="100" defaultValue="49" />
                    </div>

                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <label className="text-sm font-bold text-slate-700">Medium Risk (Officer Review)</label>
                        <span className="text-sm font-bold text-blue-600">50 - 79</span>
                      </div>
                      <input type="range" className="w-full accent-blue-500" min="0" max="100" defaultValue="79" />
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-blue-100 text-blue-700 rounded-lg"><Sliders className="w-5 h-5" /></div>
                    <div>
                      <h2 className="text-lg font-bold text-slate-900">Analysis Engine Layer Weights</h2>
                      <p className="text-sm text-slate-500">Distribute importance across the 5 analysis layers. Must equal 100%.</p>
                    </div>
                  </div>

                  <div className="space-y-5">
                    {[
                      { name: 'Document Authenticity (ELA/Metadata)', val: 25 },
                      { name: 'Cross-Document Consistency', val: 25 },
                      { name: 'ITR/Bank Math Validation', val: 25 },
                      { name: 'Fraud Pattern Matching', val: 15 },
                      { name: 'Regulatory Compliance Checks', val: 10 }
                    ].map(layer => (
                      <div key={layer.name} className="flex items-center gap-4">
                        <span className="w-56 text-sm font-medium text-slate-700">{layer.name}</span>
                        <input type="range" className="flex-1 accent-primary" min="0" max="100" defaultValue={layer.val} />
                        <span className="w-12 text-right font-bold text-slate-900">{layer.val}%</span>
                      </div>
                    ))}
                    
                    <div className="pt-4 mt-4 border-t border-slate-100 flex justify-end">
                      <span className="font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded">Total: 100%</span>
                    </div>
                  </div>
                </div>

              </motion.div>
            )}

            {activeTab === 'analysis' && (
              <motion.div key="analysis" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-6">
                
                <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="p-2 bg-purple-100 text-purple-700 rounded-lg"><Zap className="w-5 h-5" /></div>
                    <div>
                      <h2 className="text-lg font-bold text-slate-900">AI Model Configuration</h2>
                      <p className="text-sm text-slate-500">Set the underlying LLMs and vision models used for extraction and reasoning.</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Primary Reasoning Model</label>
                      <select className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none">
                        <option>Llama 3.1 8B (Local Quantized)</option>
                        <option>Mistral 7B Instruct</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Vision Model (OCR)</label>
                      <select className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none">
                        <option>Llava-1.5 7B</option>
                        <option>Tesseract OCR (Fallback)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Model Temperature (0.0 - 1.0)</label>
                      <input type="number" step="0.1" defaultValue="0.3" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                    </div>
                    <div className="flex items-center gap-3 pt-6">
                      <input type="checkbox" id="rag" defaultChecked className="w-4 h-4 text-primary" />
                      <label htmlFor="rag" className="text-sm font-medium text-slate-700">Enable CRAG (Self-Correction Loop)</label>
                    </div>
                  </div>
                </div>

              </motion.div>
            )}

            {activeTab === 'profile' && (
              <motion.div key="profile" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} className="space-y-6">
                
                <div className="bg-white rounded-2xl p-8 border border-slate-200 shadow-sm flex gap-8">
                  <div className="flex flex-col items-center">
                    <div className="w-32 h-32 bg-slate-200 rounded-full mb-4 flex items-center justify-center relative overflow-hidden group">
                      <UserCircle className="w-16 h-16 text-slate-400" />
                      <div className="absolute inset-0 bg-black/50 hidden group-hover:flex items-center justify-center cursor-pointer transition-all">
                        <Upload className="w-6 h-6 text-white" />
                      </div>
                    </div>
                    <span className="bg-amber-100 text-amber-700 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Administrator</span>
                  </div>

                  <div className="flex-1 grid grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Full Name</label>
                      <input type="text" defaultValue="System Admin" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Email</label>
                      <input type="email" defaultValue="admin@truthlens.local" disabled className="w-full border border-slate-200 bg-slate-50 text-slate-500 rounded-lg px-4 py-2 text-sm outline-none" />
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Department</label>
                      <input type="text" defaultValue="Fraud Control & Risk" className="w-full border border-slate-300 rounded-lg px-4 py-2 text-sm focus:border-primary outline-none" />
                    </div>
                    <div>
                      <label className="block text-sm font-bold text-slate-700 mb-2">Employee ID</label>
                      <input type="text" defaultValue="EMP-001" disabled className="w-full border border-slate-200 bg-slate-50 text-slate-500 rounded-lg px-4 py-2 text-sm outline-none" />
                    </div>
                  </div>
                </div>

              </motion.div>
            )}

          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
