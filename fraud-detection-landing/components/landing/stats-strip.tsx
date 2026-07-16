'use client'

import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'

interface Stat {
  label: string
  value: string | number
  suffix?: string
  color: 'blue' | 'orange' | 'yellow' | 'navy'
}

function CountUpNumber({ target, suffix = '' }: { target: number; suffix?: string }) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    let start = 0
    const end = target
    const duration = 2000
    const increment = end / (duration / 16)

    const timer = setInterval(() => {
      start += increment
      if (start >= end) {
        setCount(end)
        clearInterval(timer)
      } else {
        setCount(Math.floor(start))
      }
    }, 16)

    return () => clearInterval(timer)
  }, [target])

  return (
    <span>
      {count}
      {suffix}
    </span>
  )
}

export function StatsStrip() {
  const stats: Stat[] = [
    { label: 'Fraud Cases Prevented', value: 247, suffix: 'Cr+', color: 'blue' },
    { label: 'Average Response Time', value: 87, suffix: 'ms', color: 'orange' },
    { label: 'Detection Accuracy', value: 94.7, suffix: '%', color: 'yellow' },
    { label: 'Cases Analyzed', value: 2.4, suffix: 'L+', color: 'navy' },
  ]

  const colorMap = {
    blue: 'stat-card-blue',
    orange: 'stat-card-orange',
    yellow: 'stat-card-yellow',
    navy: 'stat-card-navy',
  }

  return (
    <section className="relative w-full bg-gradient-to-b from-white via-[#FDB913]/5 to-[#F58220]/5 py-20 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl lg:text-5xl font-bold text-[#003D6B] mb-4">
            <span className="text-[#F58220]">Proven</span> Results
          </h2>
          <p className="text-lg text-gray-700">Protecting India's lending ecosystem with measurable impact</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-100px' }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              className={colorMap[stat.color]}
            >
              <motion.div
                className="text-4xl font-bold text-[#003D6B] mb-2"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true, margin: '-100px' }}
                transition={{ duration: 0.6, delay: i * 0.1 + 0.2 }}
              >
                <CountUpNumber target={typeof stat.value === 'number' ? stat.value : 0} suffix={stat.suffix} />
              </motion.div>
              <p className="text-sm font-semibold text-gray-700">{stat.label}</p>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Wave Divider */}
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
