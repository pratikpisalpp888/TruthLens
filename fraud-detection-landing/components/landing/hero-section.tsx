'use client'

import { motion } from 'framer-motion'
import { CheckCircle2, Zap, Lock, BarChart3 } from 'lucide-react'

export function HeroSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8 },
    },
  }

  return (
    <section className="relative w-full bg-gradient-to-b from-[#E3F2FD] to-white py-20 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-[55%_45%] gap-12 items-center">
          {/* Left: Content (55%) */}
          <motion.div
            initial="hidden"
            animate="visible"
            variants={containerVariants}
            className="space-y-8"
          >
            {/* Main Heading */}
            <motion.div variants={itemVariants} className="space-y-3">
              <h1 className="text-5xl lg:text-6xl font-bold text-[#003D6B] leading-tight">
                Detect Fraud in <span className="text-[#00AEEF]">90 Seconds</span>
              </h1>
              <p className="text-lg text-gray-700 leading-relaxed">
                Enterprise-grade fraud detection with 7 intelligence layers. 100% offline, DPDP compliant, AES-256 encrypted. No data transmission.
              </p>
            </motion.div>

            {/* Government Badge */}
            <motion.div variants={itemVariants} className="inline-flex items-center gap-2 bg-yellow-50 border-2 border-[#FDB913] px-4 py-2 rounded-lg">
              <span className="text-xs font-bold text-[#FDB913]">🇮🇳</span>
              <span className="text-sm font-bold text-[#003D6B]">Government of India Undertaking</span>
            </motion.div>

            {/* Feature Buttons */}
            <motion.div variants={itemVariants} className="space-y-3">
              {[
                { icon: CheckCircle2, text: '99.8% Detection Accuracy', color: 'orange' },
                { icon: Zap, text: '<100ms Response Time', color: 'blue' },
                { icon: Lock, text: 'RBI & NPCI Compliant', color: 'yellow' },
                { icon: BarChart3, text: 'Real-Time Analytics Dashboard', color: 'navy' },
              ].map((feature, i) => {
                const Icon = feature.icon
                const colorMap = {
                  orange: 'feature-button-orange',
                  blue: 'feature-button-blue',
                  yellow: 'feature-button-yellow',
                  navy: 'feature-button bg-blue-50 border-[#003D6B]',
                }
                return (
                  <div key={i} className={colorMap[feature.color as keyof typeof colorMap]}>
                    <Icon className="w-5 h-5" />
                    <span className="font-semibold text-[#003D6B]">{feature.text}</span>
                  </div>
                )
              })}
            </motion.div>

            {/* CTA Buttons */}
            <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4 pt-4">
              <button className="btn-canara-primary">
                Get Started Today
              </button>
              <button className="btn-canara-yellow">
                Schedule a Demo
              </button>
            </motion.div>

            {/* Trust Text */}
            <motion.p variants={itemVariants} className="text-sm text-gray-600">
              ✓ Trusted by 250+ banks • ✓ ₹247Cr+ fraud prevented • ✓ 2.4L+ cases analyzed
            </motion.p>
          </motion.div>

          {/* Right: Phone Mockup (45%) */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.3 }}
            className="relative h-96 lg:h-full min-h-96"
          >
            {/* Blue Phone */}
            <div className="absolute right-0 top-0 w-48 h-80 bg-gradient-to-br from-[#00AEEF] to-[#0066B3] rounded-3xl shadow-2xl transform -rotate-12 flex items-center justify-center border-8 border-white">
              <div className="text-center">
                <div className="text-white text-sm font-bold mb-2">Fraud Detection</div>
                <div className="bg-white bg-opacity-20 backdrop-blur rounded-lg p-4 text-white text-xs">
                  <div className="mb-2">99.8% Accuracy</div>
                  <div className="text-green-300 font-bold">✓ Safe</div>
                </div>
              </div>
            </div>

            {/* Yellow Phone */}
            <div className="absolute left-0 bottom-0 w-48 h-80 bg-gradient-to-br from-[#FDB913] to-[#F58220] rounded-3xl shadow-2xl transform rotate-6 flex items-center justify-center border-8 border-white">
              <div className="text-center">
                <div className="text-[#003D6B] text-sm font-bold mb-2">Real-Time</div>
                <div className="bg-white bg-opacity-20 backdrop-blur rounded-lg p-4 text-[#003D6B] text-xs font-bold">
                  <div className="mb-2">&lt;100ms Response</div>
                  <div className="text-green-600">⚡ Lightning Fast</div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Bottom Wave Divider */}
      <svg
        viewBox="0 0 1440 80"
        preserveAspectRatio="none"
        className="w-full h-auto block absolute bottom-0 left-0"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M0,40 Q120,20 240,40 T480,40 T720,40 T960,40 T1200,40 T1440,40 L1440,80 L0,80 Z"
          fill="#F9F9F9"
        />
      </svg>
    </section>
  )
}
