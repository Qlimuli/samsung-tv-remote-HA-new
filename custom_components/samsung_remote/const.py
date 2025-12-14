"""Constants for Samsung TV Remote integration."""
from typing import Final

DOMAIN: Final = "samsung_remote"

# Configuration keys
CONF_DEVICE_ID: Final = "device_id"
CONF_DEVICE_NAME: Final = "device_name"
CONF_SMARTTHINGS_ENTRY_ID: Final = "smartthings_entry_id"

# SmartThings API
SMARTTHINGS_API_BASE: Final = "https://api.smartthings.com/v1"


# Navigation Button Commands
NAVIGATION_COMMANDS: Final = {
    "UP": {"icon": "mdi:chevron-up", "name": "Up"},
    "DOWN": {"icon": "mdi:chevron-down", "name": "Down"},
    "LEFT": {"icon": "mdi:chevron-left", "name": "Left"},
    "RIGHT": {"icon": "mdi:chevron-right", "name": "Right"},
    "OK": {"icon": "mdi:checkbox-marked-circle", "name": "OK"},
    "ENTER": {"icon": "mdi:keyboard-return", "name": "Enter"},
    "BACK": {"icon": "mdi:arrow-left", "name": "Back"},
    "HOME": {"icon": "mdi:home", "name": "Home"},
    "MENU": {"icon": "mdi:menu", "name": "Menu"},
    "EXIT": {"icon": "mdi:exit-to-app", "name": "Exit"},
}

# Playback Button Commands
PLAYBACK_COMMANDS: Final = {
    "PLAY": {"icon": "mdi:play", "name": "Play"},
    "PAUSE": {"icon": "mdi:pause", "name": "Pause"},
    "STOP": {"icon": "mdi:stop", "name": "Stop"},
    "REWIND": {"icon": "mdi:rewind", "name": "Rewind"},
    "FF": {"icon": "mdi:fast-forward", "name": "Fast Forward"},
    "FAST_FORWARD": {"icon": "mdi:fast-forward", "name": "Fast Forward"},
}

# Channel Button Commands
CHANNEL_COMMANDS: Final = {
    "CHANNEL_UP": {"icon": "mdi:chevron-up-box", "name": "Channel Up"},
    "CHANNEL_DOWN": {"icon": "mdi:chevron-down-box", "name": "Channel Down"},
    "PRECH": {"icon": "mdi:history", "name": "Previous Channel"},
    "CH_LIST": {"icon": "mdi:format-list-numbered", "name": "Channel List"},
}

# Number Pad Commands
NUMBER_COMMANDS: Final = {
    "0": {"icon": "mdi:numeric-0-box", "name": "0"},
    "1": {"icon": "mdi:numeric-1-box", "name": "1"},
    "2": {"icon": "mdi:numeric-2-box", "name": "2"},
    "3": {"icon": "mdi:numeric-3-box", "name": "3"},
    "4": {"icon": "mdi:numeric-4-box", "name": "4"},
    "5": {"icon": "mdi:numeric-5-box", "name": "5"},
    "6": {"icon": "mdi:numeric-6-box", "name": "6"},
    "7": {"icon": "mdi:numeric-7-box", "name": "7"},
    "8": {"icon": "mdi:numeric-8-box", "name": "8"},
    "9": {"icon": "mdi:numeric-9-box", "name": "9"},
}

# Color Button Commands
COLOR_COMMANDS: Final = {
    "RED": {"icon": "mdi:alpha-r-box", "name": "Red"},
    "GREEN": {"icon": "mdi:alpha-g-box", "name": "Green"},
    "YELLOW": {"icon": "mdi:alpha-y-box", "name": "Yellow"},
    "BLUE": {"icon": "mdi:alpha-b-box", "name": "Blue"},
}

# Special Button Commands
SPECIAL_COMMANDS: Final = {
    "GUIDE": {"icon": "mdi:television-guide", "name": "Guide"},
    "INFO": {"icon": "mdi:information", "name": "Info"},
    "TOOLS": {"icon": "mdi:tools", "name": "Tools"},
    "SETTINGS": {"icon": "mdi:cog", "name": "Settings"},
    "SOURCE": {"icon": "mdi:import", "name": "Source"},
}

# Volume Commands (for buttons, switch handles mute)
VOLUME_COMMANDS: Final = {
    "VOLUME_UP": {"icon": "mdi:volume-plus", "name": "Volume Up"},
    "VOLUME_DOWN": {"icon": "mdi:volume-minus", "name": "Volume Down"},
}

# HDMI Source Options
HDMI_SOURCES: Final = ["HDMI", "HDMI1", "HDMI2", "HDMI3", "HDMI4"]

# All button commands combined
ALL_BUTTON_COMMANDS: Final = {
    **NAVIGATION_COMMANDS,
    **PLAYBACK_COMMANDS,
    **CHANNEL_COMMANDS,
    **NUMBER_COMMANDS,
    **COLOR_COMMANDS,
    **SPECIAL_COMMANDS,
    **VOLUME_COMMANDS,
}

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
    "SET_VOLUME": {"component": "main", "capability": "audioVolume", "command": "setVolume", "args": []},
    
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
    "SET_CHANNEL": {"component": "main", "capability": "tvChannel", "command": "setTvChannel", "args": []},
    
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
