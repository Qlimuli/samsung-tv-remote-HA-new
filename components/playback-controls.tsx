"use client"

import { RemoteButton } from "@/components/remote-button"
import { Play, Pause, Square, Rewind, FastForward } from "lucide-react"

interface PlaybackControlsProps {
  onCommand: (command: string) => void
}

export function PlaybackControls({ onCommand }: PlaybackControlsProps) {
  return (
    <div className="mb-6">
      <span className="text-zinc-500 text-xs mb-2 uppercase tracking-wider block text-center">Playback</span>
      <div className="flex items-center justify-center gap-2">
        <RemoteButton onClick={() => onCommand("REWIND")} size="icon" variant="ghost">
          <Rewind className="w-5 h-5" />
        </RemoteButton>

        <RemoteButton onClick={() => onCommand("PLAY")} size="icon" variant="primary">
          <Play className="w-5 h-5" />
        </RemoteButton>

        <RemoteButton onClick={() => onCommand("PAUSE")} size="icon">
          <Pause className="w-5 h-5" />
        </RemoteButton>

        <RemoteButton onClick={() => onCommand("STOP")} size="icon" variant="ghost">
          <Square className="w-4 h-4" />
        </RemoteButton>

        <RemoteButton onClick={() => onCommand("FF")} size="icon" variant="ghost">
          <FastForward className="w-5 h-5" />
        </RemoteButton>
      </div>
    </div>
  )
}
