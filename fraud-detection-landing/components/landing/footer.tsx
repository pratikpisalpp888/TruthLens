'use client'

import { motion } from 'framer-motion'

export function Footer() {
  const currentYear = new Date().getFullYear()

  const footerLinks = {
    Product: ['Features', 'Security', 'Pricing', 'Documentation'],
    Company: ['About', 'Careers', 'Contact', 'Blog'],
    Legal: ['Privacy Policy', 'Terms of Service', 'Compliance', 'Certifications'],
  }

  return (
    <footer className="relative border-t border-[#FDB913]/20 bg-gradient-to-b from-[#003D6B] to-[#001F3F] text-white">
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-12 mb-12">
          {/* Brand */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="space-y-3"
          >
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-lg bg-[#00AEEF] flex items-center justify-center">
                <span className="text-[#003D6B] font-bold text-base">T</span>
              </div>
              <div>
                <div className="font-bold text-white text-sm">TruthLens</div>
                <div className="text-xs text-[#FDB913] font-bold">Fraud Detection</div>
              </div>
            </div>
            <p className="text-sm text-gray-300">Intelligent loan fraud detection with 7 intelligence layers, offline-first architecture, and enterprise-grade security.</p>
          </motion.div>

          {/* Links */}
          {Object.entries(footerLinks).map((category, i) => (
            <motion.div
              key={category[0]}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="space-y-4"
            >
              <h3 className="font-bold text-white text-sm">{category[0]}</h3>
              <ul className="space-y-2">
                {(category[1] as string[]).map((link) => (
                  <li key={link}>
                    <a href="#" className="text-sm text-gray-300 hover:text-[#FDB913] transition-colors">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}

          {/* CTA */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.3 }}
            className="space-y-4"
          >
            <h3 className="font-bold text-white text-sm">Get Started</h3>
            <motion.button
              whileHover={{ backgroundColor: '#FFD700' }}
              whileTap={{ scale: 0.98 }}
              className="w-full px-4 py-2.5 rounded-full font-bold text-sm text-[#003D6B] bg-[#FDB913] hover:bg-yellow-300 transition-colors"
            >
              Request Demo
            </motion.button>
            <p className="text-xs text-gray-500">Get started in minutes. No credit card required.</p>
          </motion.div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-600 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-xs text-gray-400">
              © {currentYear} TruthLens. All rights reserved. | DPDP Compliant | ISO 27001 Certified | Built for Banking Intelligence
            </p>
            <div className="flex gap-6">
              <a href="#" className="text-xs text-gray-400 hover:text-[#FDB913] transition-colors">
                Privacy
              </a>
              <a href="#" className="text-xs text-gray-400 hover:text-[#FDB913] transition-colors">
                Terms
              </a>
              <a href="#" className="text-xs text-gray-400 hover:text-[#FDB913] transition-colors">
                Compliance
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}
