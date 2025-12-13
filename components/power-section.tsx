"use client"

import { RemoteButton } from "@/components/remote-button"
import { Power, Home, Menu, ArrowLeft } from "lucide-react"

interface PowerSectionProps {
  onCommand: (command: string) => void
}

export function PowerSection({ onCommand }: PowerSectionProps) {
  return (
    <div className="grid grid-cols-4 gap-3 mb-6">
      <RemoteButton onClick={() => onCommand("POWER")} variant="destructive" size="icon">
        <Power className="w-5 h-5" />
      </RemoteButton>

      <RemoteButton onClick={() => onCommand("HOME")} size="icon">
        <Home className="w-5 h-5" />
      </RemoteButton>

      <RemoteButton onClick={() => onCommand("MENU")} size="icon">
        <Menu className="w-5 h-5" />
      </RemoteButton>

      <RemoteButton onClick={() => onCommand("BACK")} size="icon">
        <ArrowLeft className="w-5 h-5" />
      </RemoteButton>
    </div>
  )
}
