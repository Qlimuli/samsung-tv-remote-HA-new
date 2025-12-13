"use client"
import { VolumeX, Plus, Minus } from "lucide-react"

interface VolumeChannelControlsProps {
  onCommand: (command: string) => void
}

export function VolumeChannelControls({ onCommand }: VolumeChannelControlsProps) {
  return (
    <div className="grid grid-cols-2 gap-6 mb-6">
      {/* Volume Controls */}
      <div className="flex flex-col items-center">
        <span className="text-zinc-500 text-xs mb-2 uppercase tracking-wider">Volume</span>
        <div className="flex flex-col gap-1 bg-zinc-800 rounded-2xl p-1 border border-zinc-700">
          <button
            onClick={() => onCommand("VOLUME_UP")}
            className="w-16 h-12 rounded-xl bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
          >
            <Plus className="w-5 h-5 text-zinc-100" />
          </button>
          <button
            onClick={() => onCommand("MUTE")}
            className="w-16 h-10 rounded-xl bg-zinc-800 hover:bg-zinc-700 flex items-center justify-center transition-colors active:scale-95"
          >
            <VolumeX className="w-4 h-4 text-zinc-400" />
          </button>
          <button
            onClick={() => onCommand("VOLUME_DOWN")}
            className="w-16 h-12 rounded-xl bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
          >
            <Minus className="w-5 h-5 text-zinc-100" />
          </button>
        </div>
      </div>

      {/* Channel Controls */}
      <div className="flex flex-col items-center">
        <span className="text-zinc-500 text-xs mb-2 uppercase tracking-wider">Channel</span>
        <div className="flex flex-col gap-1 bg-zinc-800 rounded-2xl p-1 border border-zinc-700">
          <button
            onClick={() => onCommand("CHANNEL_UP")}
            className="w-16 h-12 rounded-xl bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
          >
            <Plus className="w-5 h-5 text-zinc-100" />
          </button>
          <button
            onClick={() => onCommand("CH_LIST")}
            className="w-16 h-10 rounded-xl bg-zinc-800 hover:bg-zinc-700 flex items-center justify-center transition-colors active:scale-95"
          >
            <span className="text-xs text-zinc-400">LIST</span>
          </button>
          <button
            onClick={() => onCommand("CHANNEL_DOWN")}
            className="w-16 h-12 rounded-xl bg-zinc-700 hover:bg-zinc-600 flex items-center justify-center transition-colors active:scale-95"
          >
            <Minus className="w-5 h-5 text-zinc-100" />
          </button>
        </div>
      </div>
    </div>
  )
}
