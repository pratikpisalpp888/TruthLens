'use client'

import { motion } from 'framer-motion'
import { Shield, Lock, CheckCircle, Eye, BarChart3 } from 'lucide-react'

export function TrustCompliance() {
  const pillars = [
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Offline-First Architecture',
      description: 'Zero data transmission. All analysis happens locally on-premise. Your data never leaves your servers.',
      color: 'from-[#00AEEF]',
    },
    {
      icon: <CheckCircle className="w-8 h-8" />,
      title: 'DPDP Compliant',
      description: 'Fully compliant with Digital Personal Data Protection Act 2023. User consent and data rights respected.',
      color: 'from-[#F58220]',
    },
    {
      icon: <Lock className="w-8 h-8" />,
      title: 'AES-256 Encryption',
      description: 'Military-grade encryption for all data at rest and in transit. Enterprise-grade security standards.',
      color: 'from-[#FDB913]',
    },
    {
      icon: <Eye className="w-8 h-8" />,
      title: 'Role-Based Access Control',
      description: 'Granular access permissions. Only authorized personnel can access specific application data.',
      color: 'from-[#003D6B]',
    },
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: 'Complete Audit Trail',
      description: 'Immutable logs of all access and modifications. Full compliance with regulatory requirements.',
      color: 'from-[#00AEEF]',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6 },
    },
  }

  return (
    <section className="relative w-full bg-gradient-to-b from-white to-[#003D6B] py-20 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold text-white mb-4">
            Built on <span className="text-[#FDB913]">Trust</span> & <span className="text-[#FDB913]">Compliance</span>
          </h2>
          <p className="text-lg text-gray-300 max-w-2xl mx-auto">
            Enterprise-grade security and regulatory compliance out of the box
          </p>
        </motion.div>

        {/* Trust Pillars */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-100px' }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6"
        >
          {pillars.map((pillar, i) => (
            <motion.div
              key={i}
              variants={itemVariants}
              className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:border-white/40 transition-all duration-300 group"
            >
              <motion.div
                className={`w-16 h-16 rounded-full bg-gradient-to-br ${pillar.color} to-transparent flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform duration-300`}
              >
                {pillar.icon}
              </motion.div>
              <h3 className="font-bold text-white text-lg mb-3">{pillar.title}</h3>
              <p className="text-gray-300 text-sm leading-relaxed">{pillar.description}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* Compliance Badges */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ delay: 0.6 }}
          className="mt-16 bg-white/10 backdrop-blur-sm rounded-xl p-8 border border-white/20"
        >
          <h3 className="text-2xl font-bold text-white text-center mb-8">Regulatory Certifications & Compliance</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-[#00AEEF]/20 flex items-center justify-center mx-auto mb-3">
                <Shield className="w-8 h-8 text-[#00AEEF]" />
              </div>
              <p className="font-semibold text-white text-sm">ISO 27001</p>
              <p className="text-xs text-gray-400">Information Security</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-[#F58220]/20 flex items-center justify-center mx-auto mb-3">
                <CheckCircle className="w-8 h-8 text-[#F58220]" />
              </div>
              <p className="font-semibold text-white text-sm">DPDP Act 2023</p>
              <p className="text-xs text-gray-400">Data Protection</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-[#FDB913]/20 flex items-center justify-center mx-auto mb-3">
                <Lock className="w-8 h-8 text-[#FDB913]" />
              </div>
              <p className="font-semibold text-white text-sm">RBI Guidelines</p>
              <p className="text-xs text-gray-400">Banking Regulation</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-white/10 flex items-center justify-center mx-auto mb-3">
                <BarChart3 className="w-8 h-8 text-white" />
              </div>
              <p className="font-semibold text-white text-sm">SOC 2 Type II</p>
              <p className="text-xs text-gray-400">Service Organization</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
