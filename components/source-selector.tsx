"use client"

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface SourceSelectorProps {
  onCommand: (command: string) => void
}

export function SourceSelector({ onCommand }: SourceSelectorProps) {
  const sources = [
    { value: "SOURCE", label: "Quelle wählen" },
    { value: "HDMI1", label: "HDMI 1" },
    { value: "HDMI2", label: "HDMI 2" },
    { value: "HDMI3", label: "HDMI 3" },
    { value: "HDMI4", label: "HDMI 4" },
  ]

  return (
    <div>
      <Select onValueChange={(value) => onCommand(value)}>
        <SelectTrigger className="w-full bg-zinc-800 border-zinc-700 text-zinc-100">
          <SelectValue placeholder="Eingangsquelle" />
        </SelectTrigger>
        <SelectContent className="bg-zinc-800 border-zinc-700">
          {sources.map((source) => (
            <SelectItem
              key={source.value}
              value={source.value}
              className="text-zinc-100 focus:bg-zinc-700 focus:text-zinc-100"
            >
              {source.label}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  )
}
