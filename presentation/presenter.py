#!/usr/bin/env python3
"""
Simple Manim Presentation Player
- Spacebar or 'n': Next frame / Play/Pause
- 'p': Previous
- 'f': Fullscreen toggle
- 'q' or ESC: Quit
"""

import subprocess
import sys
from pathlib import Path

def main():
    video_path = Path(__file__).parent / "media/videos/main/480p15/NumericalMethodsPresentation.mp4"
    
    if not video_path.exists():
        print(f"Error: Video not found at {video_path}")
        sys.exit(1)
    
    # Use mpv with presentation-friendly keybindings
    mpv_cmd = [
        "mpv",
        str(video_path),
        "--fullscreen",
        "--osd-level=2",  # Show OSD for progress/controls
        "--osd-font-size=40",
        "--pause",  # Start paused
    ]
    
    try:
        subprocess.run(mpv_cmd, check=True)
    except FileNotFoundError:
        print("mpv not found. Trying with vlc...")
        vlc_cmd = ["vlc", str(video_path)]
        try:
            subprocess.run(vlc_cmd, check=True)
        except FileNotFoundError:
            print("Neither mpv nor vlc found. Please install one of them:")
            print("  sudo apt install mpv")
            print("  sudo apt install vlc")
            sys.exit(1)

if __name__ == "__main__":
    main()
