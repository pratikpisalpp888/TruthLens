'use client'

import { motion } from 'framer-motion'
import { CheckCircle2, AlertCircle, TrendingUp } from 'lucide-react'

export function HeroVisualization() {
  const containerVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: {
        duration: 0.8,
        ease: 'easeOut',
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: 0.1 * i,
        duration: 0.6,
      },
    }),
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: '-100px' }}
      className="relative"
    >
      {/* Dashboard card */}
      <div className="relative rounded-xl overflow-hidden shadow-xl bg-white border border-border">
        {/* Header */}
        <div className="bg-secondary border-b border-border px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-2.5 h-2.5 rounded-full bg-primary" />
            <span className="text-sm font-medium text-foreground">Fraud Detection Dashboard</span>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-md bg-primary/10 text-primary font-semibold">Live</span>
        </div>

        {/* Content */}
        <div className="p-8 bg-white min-h-96 space-y-8">
          {/* Stat cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { icon: CheckCircle2, label: 'Detection Rate', value: '99.8%', color: 'from-primary' },
              { icon: TrendingUp, label: 'Loans Analyzed', value: '2.5M+', color: 'from-accent' },
              { icon: AlertCircle, label: 'Threats Detected', value: '₹847M', color: 'from-primary/70' },
            ].map((stat, i) => {
              const Icon = stat.icon
              return (
                <motion.div
                  key={i}
                  custom={i}
                  variants={itemVariants}
                  initial="hidden"
                  whileInView="visible"
                  viewport={{ once: true }}
                  className="rounded-lg bg-secondary p-5 border border-border"
                >
                  <div className="flex items-start gap-3 mb-3">
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${stat.color} to-transparent flex items-center justify-center text-primary`}>
                      <Icon className="w-5 h-5" />
                    </div>
                  </div>
                  <p className="text-xs font-medium text-foreground/60 mb-1">{stat.label}</p>
                  <p className="text-2xl font-bold text-foreground">{stat.value}</p>
                </motion.div>
              )
            })}
          </div>

          {/* Chart area */}
          <motion.div
            custom={3}
            variants={itemVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="rounded-lg bg-secondary p-6 border border-border"
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold text-foreground text-sm">Detection Timeline</h3>
              <div className="flex gap-2">
                <div className="w-2 h-2 rounded-full bg-primary" />
                <div className="w-2 h-2 rounded-full bg-foreground/20" />
              </div>
            </div>
            <div className="h-24 flex items-end gap-1.5 justify-between">
              {[...Array(20)].map((_, i) => (
                <motion.div
                  key={i}
                  animate={{ height: `${Math.sin(i * 0.5) * 30 + 50}%` }}
                  transition={{
                    duration: 3,
                    delay: i * 0.05,
                    repeat: Infinity,
                    repeatType: 'reverse',
                  }}
                  className="flex-1 rounded-sm bg-primary/60 hover:bg-primary transition-colors"
                />
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  )
}
