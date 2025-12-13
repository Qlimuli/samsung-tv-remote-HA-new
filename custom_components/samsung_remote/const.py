"""Constants for Samsung TV Remote integration."""
from typing import Final

DOMAIN: Final = "samsung_remote"

# Configuration keys
CONF_DEVICE_ID: Final = "device_id"
CONF_DEVICE_NAME: Final = "device_name"
CONF_SMARTTHINGS_ENTRY_ID: Final = "smartthings_entry_id"

# SmartThings API
SMARTTHINGS_API_BASE: Final = "https://api.smartthings.com/v1"

# Supported commands for SmartThings API
SMARTTHINGS_COMMANDS: Final = {
    # Navigation
    "UP": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["UP"]},
    "DOWN": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["DOWN"]},
    "LEFT": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["LEFT"]},
    "RIGHT": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["RIGHT"]},
    "OK": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["OK"]},
    "ENTER": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["OK"]},
    "BACK": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["BACK"]},
    "HOME": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["HOME"]},
    "MENU": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["MENU"]},
    "EXIT": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["EXIT"]},
    
    # Volume
    "MUTE": {"component": "main", "capability": "audioMute", "command": "mute", "args": []},
    "UNMUTE": {"component": "main", "capability": "audioMute", "command": "unmute", "args": []},
    "VOLUME_UP": {"component": "main", "capability": "audioVolume", "command": "volumeUp", "args": []},
    "VOLUME_DOWN": {"component": "main", "capability": "audioVolume", "command": "volumeDown", "args": []},
    
    # Playback
    "PLAY": {"component": "main", "capability": "mediaPlayback", "command": "play", "args": []},
    "PAUSE": {"component": "main", "capability": "mediaPlayback", "command": "pause", "args": []},
    "STOP": {"component": "main", "capability": "mediaPlayback", "command": "stop", "args": []},
    "REWIND": {"component": "main", "capability": "mediaPlayback", "command": "rewind", "args": []},
    "FF": {"component": "main", "capability": "mediaPlayback", "command": "fastForward", "args": []},
    "FAST_FORWARD": {"component": "main", "capability": "mediaPlayback", "command": "fastForward", "args": []},
    
    # Power
    "POWER": {"component": "main", "capability": "switch", "command": "off", "args": []},
    "POWER_ON": {"component": "main", "capability": "switch", "command": "on", "args": []},
    "POWER_OFF": {"component": "main", "capability": "switch", "command": "off", "args": []},
    
    # Source
    "SOURCE": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["SOURCE"]},
    "HDMI": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["HDMI"]},
    "HDMI1": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["HDMI1"]},
    "HDMI2": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["HDMI2"]},
    "HDMI3": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["HDMI3"]},
    "HDMI4": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["HDMI4"]},
    
    # Channel
    "CHANNEL_UP": {"component": "main", "capability": "tvChannel", "command": "channelUp", "args": []},
    "CHANNEL_DOWN": {"component": "main", "capability": "tvChannel", "command": "channelDown", "args": []},
    "PRECH": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["PRECH"]},
    "CH_LIST": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["CH_LIST"]},
    
    # Numbers
    "0": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["0"]},
    "1": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["1"]},
    "2": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["2"]},
    "3": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["3"]},
    "4": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["4"]},
    "5": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["5"]},
    "6": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["6"]},
    "7": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["7"]},
    "8": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["8"]},
    "9": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["9"]},
    
    # Color buttons
    "RED": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["RED"]},
    "GREEN": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["GREEN"]},
    "YELLOW": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["YELLOW"]},
    "BLUE": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["BLUE"]},
    
    # Special
    "GUIDE": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["GUIDE"]},
    "INFO": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["INFO"]},
    "TOOLS": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["TOOLS"]},
    "SETTINGS": {"component": "main", "capability": "samsungvd.remoteControl", "command": "send", "args": ["MENU"]},
}

# Activity list for remote entity
ACTIVITIES: Final = ["watching_tv", "streaming", "gaming"]

# Default scan interval in seconds
DEFAULT_SCAN_INTERVAL: Final = 30
