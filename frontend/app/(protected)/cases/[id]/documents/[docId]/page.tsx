import dynamic from 'next/dynamic'
import { ShieldAlert } from 'lucide-react'

// Dynamically import the viewer to completely bypass Next.js SSR evaluation
// This solves the 'Object.defineProperty called on non-object' error from pdfjs
const DocumentViewerClient = dynamic(
  () => import('./viewer-client'),
  { 
    ssr: false,
    loading: () => (
      <div className="h-[calc(100vh-64px)] flex flex-col items-center justify-center bg-[#0d1018] -mx-6 -my-8 absolute inset-0 top-16 z-40">
        <div className="w-10 h-10 border-4 border-slate-700 border-t-indigo-500 rounded-full animate-spin mb-4" />
        <p className="text-slate-400 font-medium text-sm">Initializing Document Viewer...</p>
      </div>
    )
  }
)

export default function DocumentViewerPage({ params }: { params: { id: string, docId: string } }) {
  return <DocumentViewerClient params={params} />
}
