'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

export function CtaSection() {
  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 cta-gradient relative overflow-hidden">
      {/* Decorative patterns */}
      <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#000_1px,transparent_1px)] [background-size:20px_20px]"></div>
      
      <div className="max-w-4xl mx-auto text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="space-y-8"
        >
          <h2 className="text-4xl md:text-6xl font-black text-primary-900 tracking-tight">
            Transform Underwriting Today
          </h2>
          <p className="text-xl text-primary-800 max-w-2xl mx-auto">
            Ninety seconds to a decision. Complete forensic evidence. Ready for production.
          </p>
          
          <div className="pt-8">
            <Link href="/login">
              <Button size="lg" className="h-16 px-10 rounded-full bg-primary-900 hover:bg-primary-800 text-white font-bold text-lg shadow-xl hover:scale-105 transition-transform duration-300">
                Access Portal <ArrowRight className="ml-3 w-6 h-6" />
              </Button>
            </Link>
          </div>
          
          <p className="text-sm font-medium text-primary-700/60 pt-8 uppercase tracking-widest">
            Built for Canara Bank SuRaksha Hackathon
          </p>
        </motion.div>
      </div>
    </section>
  )
}
