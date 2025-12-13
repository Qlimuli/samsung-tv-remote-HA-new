"use client"

interface NumberPadProps {
  onCommand: (command: string) => void
}

export function NumberPad({ onCommand }: NumberPadProps) {
  const numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "PRECH", "0", "GUIDE"]

  return (
    <div className="mb-6">
      <span className="text-zinc-500 text-xs mb-2 uppercase tracking-wider block text-center">Numbers</span>
      <div className="grid grid-cols-3 gap-2">
        {numbers.map((num) => (
          <button
            key={num}
            onClick={() => onCommand(num)}
            className="h-10 rounded-xl bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 text-zinc-100 text-sm font-medium transition-colors active:scale-95"
          >
            {num === "PRECH" ? "PRE" : num === "GUIDE" ? "EPG" : num}
          </button>
        ))}
      </div>
    </div>
  )
}
