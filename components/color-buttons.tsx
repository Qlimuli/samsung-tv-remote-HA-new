"use client"

interface ColorButtonsProps {
  onCommand: (command: string) => void
}

export function ColorButtons({ onCommand }: ColorButtonsProps) {
  const colors = [
    { key: "RED", color: "bg-red-600 hover:bg-red-500" },
    { key: "GREEN", color: "bg-green-600 hover:bg-green-500" },
    { key: "YELLOW", color: "bg-yellow-500 hover:bg-yellow-400" },
    { key: "BLUE", color: "bg-blue-600 hover:bg-blue-500" },
  ]

  return (
    <div className="mb-6">
      <div className="flex items-center justify-center gap-2">
        {colors.map(({ key, color }) => (
          <button
            key={key}
            onClick={() => onCommand(key)}
            className={`w-14 h-6 rounded-full ${color} transition-colors active:scale-95`}
          />
        ))}
      </div>
    </div>
  )
}
