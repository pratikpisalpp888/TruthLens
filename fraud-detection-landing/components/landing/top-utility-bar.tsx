'use client'

import { motion } from 'framer-motion'

export function TopUtilityBar() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="w-full bg-primary text-white px-4 py-3 text-center text-sm font-medium"
    >
      <span>
        Trusted by India's Leading Banks • RBI & NPCI Compliant • Real-Time Fraud Prevention
      </span>
    </motion.div>
  )
}
