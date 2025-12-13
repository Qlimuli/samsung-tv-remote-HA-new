"use client"
import { ChevronUp, ChevronDown, ChevronLeft, ChevronRight } from "lucide-react"

interface NavigationPadProps {
  onCommand: (command: string) => void
}

export function NavigationPad({ onCommand }: NavigationPadProps) {
  return (
    <div className="mb-6">
      <div className="relative w-48 h-48 mx-auto">
        {/* Outer ring */}
        <div className="absolute inset-0 rounded-full bg-zinc-800 border-2 border-zinc-700" />

        {/* Direction buttons */}
        <button
          onClick={() => onCommand("UP")}
          className="absolute top-2 left-1/2 -translate-x-1/2 w-14 h-14 rounded-full bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
        >
          <ChevronUp className="w-6 h-6 text-zinc-100" />
        </button>

        <button
          onClick={() => onCommand("DOWN")}
          className="absolute bottom-2 left-1/2 -translate-x-1/2 w-14 h-14 rounded-full bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
        >
          <ChevronDown className="w-6 h-6 text-zinc-100" />
        </button>

        <button
          onClick={() => onCommand("LEFT")}
          className="absolute left-2 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
        >
          <ChevronLeft className="w-6 h-6 text-zinc-100" />
        </button>

        <button
          onClick={() => onCommand("RIGHT")}
          className="absolute right-2 top-1/2 -translate-y-1/2 w-14 h-14 rounded-full bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
        >
          <ChevronRight className="w-6 h-6 text-zinc-100" />
        </button>

        {/* Center OK button */}
        <button
          onClick={() => onCommand("OK")}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 rounded-full bg-blue-600 hover:bg-blue-500 flex items-center justify-center transition-colors active:scale-95 shadow-lg"
        >
          <span className="text-white font-bold text-sm">OK</span>
        </button>
      </div>
    </div>
  )
}
