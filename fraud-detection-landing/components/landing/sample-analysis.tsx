'use client'

import { motion } from 'framer-motion'
import { AlertTriangle, CheckCircle } from 'lucide-react'

export function SampleAnalysis() {
  const findings = [
    { issue: 'Signature Mismatch', severity: 'high', layer: 'Document Forensics' },
    { issue: 'Income Inflation Detected', severity: 'high', layer: 'ITR Verification' },
    { issue: 'Document Date Inconsistency', severity: 'medium', layer: 'Cross-Document' },
    { issue: 'PAN Already Linked to 3 Applications', severity: 'high', layer: 'Fraud DNA' },
    { issue: 'Address Changed 5 Times in 6 Months', severity: 'medium', layer: 'Risk Intelligence' },
    { issue: 'Image Quality Degradation Detected', severity: 'medium', layer: 'Forensics' },
    { issue: 'Credit Score Mismatch', severity: 'low', layer: 'Risk Intelligence' },
    { issue: 'Document Expiry Not Verified', severity: 'low', layer: 'Compliance' },
  ]

  return (
    <section className="relative w-full bg-gradient-to-b from-[#FFF8E7] to-white py-20 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl lg:text-5xl font-bold text-[#003D6B] mb-4">
            Sample <span className="text-[#F58220]">Analysis Result</span>
          </h2>
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Real-world example of TruthLens detecting sophisticated fraud scheme
          </p>
        </motion.div>

        {/* Analysis Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="bg-white rounded-xl shadow-2xl overflow-hidden border border-gray-200"
        >
          {/* Header */}
          <div className="bg-gradient-to-r from-[#003D6B] to-[#00AEEF] p-8 text-white">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-2xl font-bold mb-2">Loan Application #LA-2025-08742</h3>
                <p className="text-blue-100">₹45,00,000 Unsecured Personal Loan | Processing Time: 87 seconds</p>
              </div>
              <div className="text-right">
                <div className="text-5xl font-bold text-[#FDB913]">18</div>
                <p className="text-sm text-blue-100 mt-1">Trust Score / 100</p>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-8">
            {/* Status Badge */}
            <motion.div
              initial={{ scale: 0 }}
              whileInView={{ scale: 1 }}
              viewport={{ once: true }}
              className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-4"
            >
              <AlertTriangle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-red-900 mb-1">HIGH FRAUD RISK - RECOMMENDATION: REJECT</h4>
                <p className="text-sm text-red-800">Multiple critical fraud indicators detected across document forensics, income verification, and pattern matching</p>
              </div>
            </motion.div>

            {/* Findings Grid */}
            <div className="mb-8">
              <h4 className="font-bold text-[#003D6B] text-lg mb-4">Detailed Findings (8 Issues Detected)</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {findings.map((finding, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.05 }}
                    className={`p-4 rounded-lg border-l-4 ${
                      finding.severity === 'high'
                        ? 'bg-red-50 border-red-500'
                        : finding.severity === 'medium'
                          ? 'bg-yellow-50 border-yellow-500'
                          : 'bg-blue-50 border-blue-500'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <p className="font-semibold text-gray-900">{finding.issue}</p>
                        <p className="text-xs text-gray-600 mt-1">{finding.layer}</p>
                      </div>
                      <span
                        className={`text-xs font-bold px-2 py-1 rounded whitespace-nowrap ${
                          finding.severity === 'high'
                            ? 'bg-red-200 text-red-900'
                            : finding.severity === 'medium'
                              ? 'bg-yellow-200 text-yellow-900'
                              : 'bg-blue-200 text-blue-900'
                        }`}
                      >
                        {finding.severity.toUpperCase()}
                      </span>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Layer Breakdown */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <h4 className="font-bold text-[#003D6B] mb-4">Intelligence Layer Analysis</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">Document Forensics</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-gray-200 rounded-full">
                      <div className="w-4/5 h-full bg-red-500 rounded-full" />
                    </div>
                    <span className="text-xs font-bold text-red-600">80% Risk</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">ITR Verification</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-gray-200 rounded-full">
                      <div className="w-3/5 h-full bg-red-500 rounded-full" />
                    </div>
                    <span className="text-xs font-bold text-red-600">75% Risk</span>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">Fraud DNA Matching</span>
                  <div className="flex items-center gap-2">
                    <div className="w-32 h-2 bg-gray-200 rounded-full">
                      <div className="w-5/6 h-full bg-red-500 rounded-full" />
                    </div>
                    <span className="text-xs font-bold text-red-600">82% Risk</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Key Insight */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          transition={{ delay: 0.6 }}
          className="mt-12 text-center text-gray-700"
        >
          <p className="text-lg max-w-2xl mx-auto">
            This loan would have been <span className="font-bold text-red-600">approved using traditional manual review</span> due to surface-level document compliance, but TruthLens identified sophisticated fraud indicators across 8 different dimensions in just 87 seconds.
          </p>
        </motion.div>
      </div>
    </section>
  )
}
