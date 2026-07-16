'use client'

import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface SectionTitleProps {
  title: string
  subtitle?: string
  className?: string
  titleClassName?: string
  subtitleClassName?: string
  highlight?: string // word(s) in title to color with primary gradient
  align?: 'center' | 'left'
}

export function SectionTitle({
  title,
  subtitle,
  className,
  titleClassName,
  subtitleClassName,
  highlight,
  align = 'center',
}: SectionTitleProps) {
  const words = title.split(' ')

  const container = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.08, delayChildren: 0.1 },
    },
  }

  const wordVariant = {
    hidden: { opacity: 0, y: 24, filter: 'blur(6px)' },
    visible: {
      opacity: 1,
      y: 0,
      filter: 'blur(0px)',
      transition: { duration: 0.5 },
    },
  }

  const subtitleVariant = {
    hidden: { opacity: 0, y: 16 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, delay: words.length * 0.08 + 0.2 },
    },
  }

  return (
    <motion.div
      className={cn(align === 'center' ? 'text-center' : 'text-left', 'mb-16', className)}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: '-80px' }}
    >
      <motion.h2
        className={cn(
          'text-4xl md:text-5xl font-bold tracking-tight text-primary-900',
          titleClassName
        )}
        variants={container}
        // Needed so the h2 itself participates in the stagger
        style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35em', justifyContent: align === 'center' ? 'center' : 'flex-start' }}
      >
        {words.map((word, i) => {
          const isHighlighted = highlight && highlight.toLowerCase().includes(word.toLowerCase())
          return (
            <motion.span
              key={i}
              variants={wordVariant}
              className={isHighlighted ? 'bg-gradient-to-r from-primary-600 to-blue-500 bg-clip-text text-transparent' : ''}
            >
              {word}
            </motion.span>
          )
        })}
      </motion.h2>

      {subtitle && (
        <motion.p
          className={cn(
            'mt-5 text-lg text-slate-600 max-w-3xl leading-relaxed',
            align === 'center' ? 'mx-auto' : '',
            subtitleClassName
          )}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: '-80px' }}
          variants={subtitleVariant}
        >
          {subtitle}
        </motion.p>
      )}
    </motion.div>
  )
}
