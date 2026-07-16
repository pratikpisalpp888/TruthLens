'use client'

import { motion } from 'framer-motion'
import { Phone, Mail } from 'lucide-react'

export function Header() {
  return (
    <>
      {/* Utility Header */}
      <motion.header
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full bg-[#00AEEF] text-white px-4 sm:px-6 lg:px-8 py-3"
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between text-sm">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg">TruthLens</span>
              <span className="text-xs opacity-90">Fraud Detection Intelligence</span>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            <a href="tel:1800103000" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
              <Phone className="w-4 h-4" />
              <span className="hidden sm:inline">1800 103 000</span>
            </a>
            <button className="bg-white text-[#00AEEF] px-3 py-1 rounded-full text-xs font-bold hover:bg-opacity-90 transition-all">
              EN | हिंदी
            </button>
          </div>
        </div>
      </motion.header>

      {/* Yellow Band with Wavy Divider */}
      <div className="w-full bg-[#FDB913]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center text-sm font-bold text-[#003D6B]">
          <span>Detect Fraud in 90 Seconds</span>
          <span className="mx-4">|</span>
          <span>100% Offline, 7 Intelligence Layers, Enterprise-Grade Security</span>
        </div>

        {/* Wavy Divider */}
        <svg
          viewBox="0 0 1440 80"
          preserveAspectRatio="none"
          className="w-full h-auto block -mb-px"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#FDB913" />
              <stop offset="100%" stopColor="#FDB913" />
            </linearGradient>
          </defs>
          <path
            d="M0,40 Q120,20 240,40 T480,40 T720,40 T960,40 T1200,40 T1440,40 L1440,80 L0,80 Z"
            fill="white"
          />
        </svg>
      </div>

      {/* Navigation Bar */}
      <motion.nav
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1, duration: 0.5 }}
        className="sticky top-0 z-40 w-full bg-white shadow-sm"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <motion.div whileHover={{ scale: 1.05 }} className="flex items-center gap-2">
              <div className="w-10 h-10 bg-[#00AEEF] rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">₹</span>
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-[#003D6B] text-sm">CANARA</span>
                <span className="text-xs text-[#00AEEF] font-bold">FraudShield</span>
              </div>
            </motion.div>

            {/* Nav Items */}
            <div className="hidden md:flex items-center gap-8">
              {['FEATURES', 'SECURITY', 'COMPLIANCE', 'PRICING'].map((item, i) => (
                <motion.a
                  key={item}
                  href="#"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2 + i * 0.05 }}
                  className="text-sm font-bold text-[#003D6B] uppercase hover:text-[#F58220] transition-colors relative group"
                >
                  {item}
                  <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#F58220] group-hover:w-full transition-all duration-300" />
                </motion.a>
              ))}
            </div>

            {/* CTA Button */}
            <motion.button
              whileHover={{ backgroundColor: '#0099DD' }}
              whileTap={{ scale: 0.98 }}
              className="px-6 py-2.5 rounded-full font-bold text-sm text-white bg-[#0066B3] hover:bg-blue-700 transition-colors shadow-md"
            >
              Request Demo
            </motion.button>
          </div>

          {/* Curved Bottom */}
          <svg
            viewBox="0 0 1440 40"
            preserveAspectRatio="none"
            className="absolute left-0 right-0 -bottom-1 w-full h-auto"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M0,0 Q360,40 720,40 T1440,40 L1440,0 Z"
              fill="white"
            />
          </svg>
        </div>
      </motion.nav>
    </>
  )
}
