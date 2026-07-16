'use client'

import { motion, useInView, useMotionValue, useSpring, useTransform } from 'framer-motion'
import { Timer, Layers, Bot, WifiOff } from 'lucide-react'
import { useEffect, useRef } from 'react'

function AnimatedNumber({ value, suffix = '' }: { value: number; suffix?: string }) {
  const ref = useRef<HTMLSpanElement>(null)
  const inView = useInView(ref, { once: true })
  const motionVal = useMotionValue(0)
  const spring = useSpring(motionVal, { duration: 2000, bounce: 0 })
  const display = useTransform(spring, (v) => `${Math.round(v)}${suffix}`)

  useEffect(() => {
    if (inView) motionVal.set(value)
  }, [inView, value, motionVal])

  return <motion.span ref={ref}>{display}</motion.span>
}

const metrics = [
  {
    numericValue: 90,
    suffix: 's',
    label: 'Average analysis time',
    icon: Timer,
    color: 'text-blue-600',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-100',
    glowColor: 'rgba(59,130,246,0.15)',
  },
  {
    numericValue: 7,
    suffix: '',
    label: 'Intelligence layers',
    icon: Layers,
    color: 'text-amber-500',
    bgColor: 'bg-amber-50',
    borderColor: 'border-amber-100',
    glowColor: 'rgba(245,158,11,0.15)',
  },
  {
    numericValue: 5,
    suffix: '',
    label: 'Autonomous AI agents',
    icon: Bot,
    color: 'text-violet-600',
    bgColor: 'bg-violet-50',
    borderColor: 'border-violet-100',
    glowColor: 'rgba(139,92,246,0.15)',
  },
  {
    numericValue: 100,
    suffix: '%',
    label: 'Offline capable',
    icon: WifiOff,
    color: 'text-emerald-500',
    bgColor: 'bg-emerald-50',
    borderColor: 'border-emerald-100',
    glowColor: 'rgba(16,185,129,0.15)',
  },
]

export function MetricsBar() {
  return (
    <section className="relative py-16 bg-white overflow-hidden">
      {/* Subtle top border line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
          {metrics.map((metric, i) => {
            const Icon = metric.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30, scale: 0.95 }}
                whileInView={{ opacity: 1, y: 0, scale: 1 }}
                viewport={{ once: true, margin: '-50px' }}
                transition={{ delay: i * 0.12, duration: 0.6, ease: 'easeOut' }}
                whileHover={{ y: -4, scale: 1.03 }}
                className={`
                  relative flex flex-col items-center text-center
                  rounded-2xl p-6 border ${metric.borderColor}
                  bg-white shadow-sm hover:shadow-md transition-shadow duration-300
                  overflow-hidden cursor-default
                `}
              >
                {/* Glow blob behind */}
                <div
                  className="absolute inset-0 pointer-events-none rounded-2xl"
                  style={{
                    background: `radial-gradient(circle at 50% 0%, ${metric.glowColor} 0%, transparent 70%)`,
                  }}
                />

                {/* Icon */}
                <div className={`relative z-10 p-3 rounded-xl ${metric.bgColor} mb-4`}>
                  <Icon className={`w-6 h-6 ${metric.color}`} strokeWidth={1.8} />
                </div>

                {/* Animated number */}
                <h3 className={`relative z-10 text-4xl md:text-5xl font-black tracking-tight mb-1 ${metric.color}`}>
                  <AnimatedNumber value={metric.numericValue} suffix={metric.suffix} />
                </h3>

                {/* Label */}
                <p className="relative z-10 text-xs md:text-sm font-medium text-slate-500 leading-snug">
                  {metric.label}
                </p>

                {/* Bottom accent line */}
                <motion.div
                  initial={{ scaleX: 0 }}
                  whileInView={{ scaleX: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.12 + 0.4, duration: 0.6 }}
                  className={`absolute bottom-0 left-1/4 right-1/4 h-0.5 rounded-full ${metric.bgColor}`}
                  style={{ transformOrigin: 'center' }}
                />
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Subtle bottom border line */}
      <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />
    </section>
  )
}
