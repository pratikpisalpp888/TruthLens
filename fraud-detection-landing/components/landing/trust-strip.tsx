'use client'

import { motion } from 'framer-motion'
import { Shield, Award, CheckCircle } from 'lucide-react'

export function TrustStrip() {
  const items = [
    { icon: Shield, text: 'RBI Compliant', subtext: 'Reserve Bank of India' },
    { icon: Award, text: 'NPCI Certified', subtext: 'National Payments Corp' },
    { icon: CheckCircle, text: 'ISO 27001', subtext: 'Information Security' },
  ]

  return (
    <section className="w-full bg-gradient-to-r from-[#00AEEF]/10 via-[#FDB913]/5 to-[#F58220]/10 py-16 px-4 sm:px-6 lg:px-8 border-y border-[#FDB913]/20">
      <div className="w-full max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {items.map((item, i) => {
            const Icon = item.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="flex items-center gap-4 text-center md:text-left"
              >
                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-[#00AEEF]/10 flex items-center justify-center">
                  <Icon className="w-6 h-6 text-[#00AEEF]" />
                </div>
                <div>
                  <p className="font-bold text-[#003D6B]">{item.text}</p>
                  <p className="text-xs text-gray-600">{item.subtext}</p>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
