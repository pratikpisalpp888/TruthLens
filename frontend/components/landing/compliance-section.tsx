'use client'

import { motion } from 'framer-motion'
import { WifiOff, Shield, FileCheck, Lock } from 'lucide-react'

export function ComplianceSection() {
  const features = [
    { icon: WifiOff, title: 'Offline-First', desc: 'Sensitive customer data never leaves bank premises. No cloud dependencies at runtime.' },
    { icon: Shield, title: 'DPDP Act Aligned', desc: 'Purpose limitation, consent management, data minimization, and full accountability.' },
    { icon: FileCheck, title: 'Complete Audit Trail', desc: 'Every action logged with timestamps. RBI inspection-ready from day one.' },
    { icon: Lock, title: 'Encrypted by Default', desc: 'AES-256 document encryption. Role-based access control. Sensitive data masking.' },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-50">
      <div className="max-w-7xl mx-auto">
        <div className="grid lg:grid-cols-[40%_60%] gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-6 tracking-tight">
              Built for <br/>Banking Reality
            </h2>
            <p className="text-lg text-slate-600 mb-8">
              Security, privacy, and compliance by design. We understand that bank data cannot be sent to public API endpoints.
            </p>
            <div className="inline-flex items-center gap-2 bg-green-50 text-green-700 px-4 py-2 rounded-full border border-green-200 font-semibold text-sm">
              <Shield className="w-4 h-4" /> Ready for internal deployment
            </div>
          </motion.div>

          <div className="grid sm:grid-cols-2 gap-6">
            {features.map((f, i) => {
              const Icon = f.icon
              return (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className="bg-white p-6 rounded-2xl shadow-sm border border-border"
                >
                  <Icon className="w-8 h-8 text-primary-600 mb-4" />
                  <h3 className="text-lg font-bold text-primary-900 mb-2">{f.title}</h3>
                  <p className="text-slate-600 text-sm leading-relaxed">{f.desc}</p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
}
