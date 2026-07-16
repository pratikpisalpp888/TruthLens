'use client'

import { Search, X } from 'lucide-react'
import { useState, useEffect } from 'react'

interface SearchBarProps {
  placeholder?: string
  onSearch: (value: string) => void
}

export function SearchBar({ placeholder = "Search...", onSearch }: SearchBarProps) {
  const [value, setValue] = useState('')

  useEffect(() => {
    const handler = setTimeout(() => {
      onSearch(value)
    }, 300)
    return () => clearTimeout(handler)
  }, [value, onSearch])

  return (
    <div className="relative w-full max-w-md flex items-center">
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <Search className={`w-4 h-4 text-slate-400 ${value ? 'text-primary animate-pulse' : ''}`} />
      </div>
      <input
        type="text"
        className="block w-full pl-10 pr-10 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all"
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      {value && (
        <button 
          onClick={() => setValue('')} 
          className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
        >
          <X className="w-4 h-4" />
        </button>
      )}
      {!value && (
        <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
          <kbd className="hidden sm:inline-block px-1.5 py-0.5 text-[10px] font-mono text-slate-400 bg-slate-100 border border-slate-200 rounded">⌘K</kbd>
        </div>
      )}
    </div>
  )
}
