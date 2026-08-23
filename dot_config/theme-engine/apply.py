import os
import sys
import argparse
import subprocess
import shutil
from build import build_theme

# Ensure working directory is the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def reload_applications():
    """Triggers reload commands for active desktop environment applications."""
    print("Reloading desktop environment applications...")
    
    # Hyprland
    if shutil.which("hyprctl"):
        try:
            res = subprocess.run(["hyprctl", "reload"], capture_output=True, text=True)
            print(f"  [OK] Hyprland reloaded ({res.returncode})")
        except Exception as e:
            print(f"  [X] Hyprland reload error: {e}")
    else:
        print("  - Hyprland (hyprctl) not found, skipping reload.")

    # Waybar
    if shutil.which("waybar"):
        try:
            subprocess.run(["pkill", "-USR2", "waybar"], capture_output=True)
            print("  [OK] Waybar reloaded (SIGUSR2)")
        except Exception as e:
            print(f"  [X] Waybar reload error: {e}")
    else:
        print("  - Waybar not running/found, skipping reload.")

    # SwayNC
    if shutil.which("swaync-client"):
        try:
            subprocess.run(["swaync-client", "-R"], capture_output=True)
            subprocess.run(["swaync-client", "-rs"], capture_output=True)
            print("  [OK] SwayNC reloaded config and style")
        except Exception as e:
            print(f"  [X] SwayNC reload error: {e}")
    else:
        print("  - SwayNC (swaync-client) not found, skipping reload.")

def set_wallpaper(wallpaper_path: str):
    """Applies wallpaper using awww if available."""
    if not wallpaper_path or not os.path.exists(wallpaper_path):
        print(f"  - No valid wallpaper provided or file does not exist: {wallpaper_path}")
        return

    print(f"Setting wallpaper: {wallpaper_path}")
    if shutil.which("awww"):
        try:
            res = subprocess.run(["awww", "img", wallpaper_path], capture_output=True, text=True)
            print(f"  [OK] Wallpaper updated via awww ({res.returncode})")
        except Exception as e:
            print(f"  [X] awww error: {e}")
    elif shutil.which("swww"):
        try:
            res = subprocess.run(["swww", "img", wallpaper_path], capture_output=True, text=True)
            print(f"  [OK] Wallpaper updated via swww ({res.returncode})")
        except Exception as e:
            print(f"  [X] swww error: {e}")
    else:
        print("  - Wallpaper daemon (awww / swww) not found in PATH.")

def apply_theme(theme_name: str, wallpaper_path: str = ""):
    """Complete workflow: identify theme -> build cache -> set wallpaper -> reload apps."""
    theme_dir = os.path.join("themes", theme_name)
    colors_json = os.path.join(theme_dir, "colors.json")

    if not os.path.exists(colors_json):
        # Fallback to direct json file if provided
        if os.path.exists(theme_name):
            colors_json = theme_name
        else:
            print(f"Error: Could not find theme '{theme_name}' at {colors_json}", file=sys.stderr)
            sys.exit(1)

    # Resolve default wallpaper if not provided
    if not wallpaper_path:
        wallpapers_folder = os.path.join(theme_dir, "wallpapers")
        if os.path.exists(wallpapers_folder):
            walls = [os.path.join(wallpapers_folder, f) for f in os.listdir(wallpapers_folder)
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            if walls:
                wallpaper_path = walls[0]

    print(f"=== Applying Theme: {theme_name} ===")
    build_theme(colors_json, wallpaper_path=wallpaper_path)
    set_wallpaper(wallpaper_path)
    reload_applications()
    print(f"=== Theme '{theme_name}' applied successfully! ===")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Theme Engine Applier")
    parser.add_argument("--theme", "-t", required=True, help="Theme name (e.g. kanagawa, nord, catppuccin, gruvbox)")
    parser.add_argument("--wallpaper", "-w", default="", help="Path to wallpaper image")
    
    args = parser.parse_args()
    apply_theme(args.theme, args.wallpaper)
