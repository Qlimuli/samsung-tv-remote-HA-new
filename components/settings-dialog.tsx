"use client"

import { useState } from "react"
import { Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface SettingsDialogProps {
  onSave: (url: string, token: string, entityId: string) => void
  currentUrl: string
  currentToken: string
  currentEntity: string
}

export function SettingsDialog({ onSave, currentUrl, currentToken, currentEntity }: SettingsDialogProps) {
  const [url, setUrl] = useState(currentUrl)
  const [token, setToken] = useState(currentToken)
  const [entityId, setEntityId] = useState(currentEntity || "remote.samsung_tv")
  const [open, setOpen] = useState(false)

  const handleSave = () => {
    onSave(url, token, entityId)
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <button className="w-10 h-10 rounded-full bg-zinc-800 hover:bg-zinc-700 flex items-center justify-center transition-colors">
          <Settings className="w-5 h-5 text-zinc-400" />
        </button>
      </DialogTrigger>
      <DialogContent className="bg-zinc-900 border-zinc-800 text-zinc-100">
        <DialogHeader>
          <DialogTitle>Home Assistant Verbindung</DialogTitle>
          <DialogDescription className="text-zinc-400">
            Geben Sie Ihre Home Assistant Zugangsdaten ein.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid gap-2">
            <Label htmlFor="url" className="text-zinc-300">
              Home Assistant URL
            </Label>
            <Input
              id="url"
              placeholder="http://homeassistant.local:8123"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="bg-zinc-800 border-zinc-700 text-zinc-100"
            />
          </div>
          <div className="grid gap-2">
            <Label htmlFor="token" className="text-zinc-300">
              Long-Lived Access Token
            </Label>
            <Input
              id="token"
              type="password"
              placeholder="eyJ0eXAiOi..."
              value={token}
              onChange={(e) => setToken(e.target.value)}
              className="bg-zinc-800 border-zinc-700 text-zinc-100"
            />
            <p className="text-xs text-zinc-500">Erstellen Sie einen Token unter: Profil → Long-Lived Access Tokens</p>
          </div>
          <div className="grid gap-2">
            <Label htmlFor="entity" className="text-zinc-300">
              Remote Entity ID
            </Label>
            <Input
              id="entity"
              placeholder="remote.samsung_tv"
              value={entityId}
              onChange={(e) => setEntityId(e.target.value)}
              className="bg-zinc-800 border-zinc-700 text-zinc-100"
            />
          </div>
        </div>
        <DialogFooter>
          <Button onClick={handleSave} className="bg-blue-600 hover:bg-blue-500 text-white">
            Speichern
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
