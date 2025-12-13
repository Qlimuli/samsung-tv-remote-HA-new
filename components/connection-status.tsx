"use client"

interface ConnectionStatusProps {
  isConnected: boolean
  lastCommand: string | null
}

export function ConnectionStatus({ isConnected, lastCommand }: ConnectionStatusProps) {
  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${isConnected ? "bg-green-500" : "bg-zinc-600"}`} />
      <span className="text-zinc-500 text-xs">
        {lastCommand ? `Letzter Befehl: ${lastCommand}` : "Nicht verbunden"}
      </span>
    </div>
  )
}
