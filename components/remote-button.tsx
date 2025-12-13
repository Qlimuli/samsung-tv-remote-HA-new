"use client"

import type React from "react"

import { cn } from "@/lib/utils"

interface RemoteButtonProps {
  onClick: () => void
  children: React.ReactNode
  className?: string
  variant?: "default" | "primary" | "destructive" | "ghost"
  size?: "sm" | "md" | "lg" | "icon"
}

export function RemoteButton({ onClick, children, className, variant = "default", size = "md" }: RemoteButtonProps) {
  const baseStyles = "transition-all duration-150 active:scale-95 font-medium"

  const variantStyles = {
    default: "bg-zinc-800 hover:bg-zinc-700 text-zinc-100 border border-zinc-700",
    primary: "bg-blue-600 hover:bg-blue-500 text-white",
    destructive: "bg-red-600 hover:bg-red-500 text-white",
    ghost: "bg-transparent hover:bg-zinc-800 text-zinc-400 hover:text-zinc-100",
  }

  const sizeStyles = {
    sm: "h-8 px-3 text-xs rounded-lg",
    md: "h-10 px-4 text-sm rounded-xl",
    lg: "h-12 px-6 text-base rounded-xl",
    icon: "h-12 w-12 rounded-xl",
  }

  return (
    <button
      onClick={onClick}
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        "flex items-center justify-center",
        className,
      )}
    >
      {children}
    </button>
  )
}
