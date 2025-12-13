"use client"

import { useState, useCallback } from "react"
import { Card } from "@/components/ui/card"
import { PowerSection } from "@/components/power-section"
import { NavigationPad } from "@/components/navigation-pad"
import { VolumeChannelControls } from "@/components/volume-channel-controls"
import { PlaybackControls } from "@/components/playback-controls"
import { NumberPad } from "@/components/number-pad"
import { ColorButtons } from "@/components/color-buttons"
import { SourceSelector } from "@/components/source-selector"
import { ConnectionStatus } from "@/components/connection-status"
import { SettingsDialog } from "@/components/settings-dialog"

export function SamsungRemote() {
  const [haUrl, setHaUrl] = useState("")
  const [token, setToken] = useState("")
  const [entityId, setEntityId] = useState("remote.samsung_tv")
  const [isConnected, setIsConnected] = useState(false)
  const [lastCommand, setLastCommand] = useState<string | null>(null)

  const sendCommand = useCallback(
    async (command: string) => {
      if (!haUrl || !token || !entityId) {
        console.log("Not configured:", { haUrl, token, entityId })
        return
      }

      setLastCommand(command)

      try {
        const response = await fetch(`${haUrl}/api/services/remote/send_command`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            entity_id: entityId,
            command: command,
          }),
        })

        if (response.ok) {
          setIsConnected(true)
        } else {
          console.error("Command failed:", response.status)
          setIsConnected(false)
        }
      } catch (error) {
        console.error("Error sending command:", error)
        setIsConnected(false)
      }
    },
    [haUrl, token, entityId],
  )

  const handleSettingsSave = (url: string, accessToken: string, entity: string) => {
    setHaUrl(url)
    setToken(accessToken)
    setEntityId(entity)

    // Save to localStorage
    if (typeof window !== "undefined") {
      localStorage.setItem(
        "samsung_remote_config",
        JSON.stringify({
          haUrl: url,
          token: accessToken,
          entityId: entity,
        }),
      )
    }
  }

  // Load settings on mount
  useState(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("samsung_remote_config")
      if (saved) {
        const config = JSON.parse(saved)
        setHaUrl(config.haUrl || "")
        setToken(config.token || "")
        setEntityId(config.entityId || "remote.samsung_tv")
      }
    }
  })

  return (
    <Card className="w-full max-w-sm bg-gradient-to-b from-zinc-900 to-zinc-950 border-zinc-800 rounded-3xl p-6 shadow-2xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          </div>
          <div>
            <h1 className="text-white font-semibold text-lg">Samsung TV</h1>
            <ConnectionStatus isConnected={isConnected} lastCommand={lastCommand} />
          </div>
        </div>
        <SettingsDialog onSave={handleSettingsSave} currentUrl={haUrl} currentToken={token} currentEntity={entityId} />
      </div>

      {/* Power & Source */}
      <PowerSection onCommand={sendCommand} />

      {/* Navigation */}
      <NavigationPad onCommand={sendCommand} />

      {/* Volume & Channel */}
      <VolumeChannelControls onCommand={sendCommand} />

      {/* Playback */}
      <PlaybackControls onCommand={sendCommand} />

      {/* Number Pad */}
      <NumberPad onCommand={sendCommand} />

      {/* Color Buttons */}
      <ColorButtons onCommand={sendCommand} />

      {/* Source Selector */}
      <SourceSelector onCommand={sendCommand} />
    </Card>
  )
}
