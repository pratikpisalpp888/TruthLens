'use client'

import { motion } from 'framer-motion'
import { Database, Search, Cpu, Network } from 'lucide-react'

export function TechnologySection() {
  const stack = [
    {
      icon: Database,
      title: 'Bank-Grade Database',
      desc: 'CockroachDB provides distributed SQL with ACID compliance for financial data integrity.',
    },
    {
      icon: Search,
      title: 'Advanced Vector Search',
      desc: 'Qdrant delivers production-grade vector search powering RAG and fraud pattern matching.',
    },
    {
      icon: Cpu,
      title: 'Local LLM Inference',
      desc: 'Ollama runs Phi-3 and Llama models locally with zero external dependencies.',
    },
    {
      icon: Network,
      title: 'Agent Orchestration',
      desc: 'LangGraph coordinates multi-agent workflows with state management and parallel execution.',
    },
  ]

  return (
    <section className="py-24 px-4 sm:px-6 lg:px-8 bg-white border-t border-border">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mb-16"
        >
          <h2 className="text-3xl md:text-5xl font-bold text-primary-900 mb-4 tracking-tight">
            Production Architecture <br/> from Day One
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl">
            Built with the stack designed for bank deployment.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stack.map((item, i) => {
            const Icon = item.icon
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1, duration: 0.5 }}
                className="space-y-4"
              >
                <div className="w-12 h-12 rounded-lg bg-slate-100 flex items-center justify-center">
                  <Icon className="w-6 h-6 text-primary-700" />
                </div>
                <h3 className="text-xl font-bold text-primary-900">{item.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{item.desc}</p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
