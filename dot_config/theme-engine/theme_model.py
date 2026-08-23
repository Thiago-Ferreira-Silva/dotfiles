import json
import os
import colorsys

class Color:
    """Helper class to represent a single color with multiple formatted outputs."""
    def __init__(self, hex_code: str):
        hex_clean = hex_code.strip().lstrip("#")
        if len(hex_clean) == 3:
            hex_clean = "".join([c * 2 for c in hex_clean])
        self.hex = f"#{hex_clean.lower()}"
        self.nohash = hex_clean.lower()
        
        # Convert hex to RGB (0-255)
        self.r = int(self.nohash[0:2], 16)
        self.g = int(self.nohash[2:4], 16)
        self.b = int(self.nohash[4:6], 16)
        
        self.rgb = f"{self.r}, {self.g}, {self.b}"
        self.rgb_space = f"{self.r} {self.g} {self.b}"
        
    def rgba(self, alpha: float) -> str:
        """Returns rgba string like 'rgba(255, 255, 255, 0.8)'."""
        return f"rgba({self.r}, {self.g}, {self.b}, {alpha:.2f})"

    def lighten(self, amount: float = 0.15) -> "Color":
        """Lighten color by increasing lightness in HLS space."""
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        new_l = min(1.0, l + amount)
        nr, ng, nb = colorsys.hls_to_rgb(h, new_l, s)
        return Color(f"{int(nr*255):02x}{int(ng*255):02x}{int(nb*255):02x}")

    def darken(self, amount: float = 0.15) -> "Color":
        """Darken color by decreasing lightness in HLS space."""
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        new_l = max(0.0, l - amount)
        nr, ng, nb = colorsys.hls_to_rgb(h, new_l, s)
        return Color(f"{int(nr*255):02x}{int(ng*255):02x}{int(nb*255):02x}")

    def __str__(self):
        return self.hex

    def __repr__(self):
        return f"Color('{self.hex}')"


class ThemeModel:
    """Loads colors.json and metadata, producing a rich object for Jinja2 templates."""
    COLOR_KEYS = [
        "background", "surface", "foreground", "primary", "secondary",
        "red", "green", "yellow", "blue", "magenta", "cyan", "border",
        "muted", "warning"
    ]

    def __init__(self, theme_data: dict, wallpaper_path: str = ""):
        self.raw = theme_data
        self.name = theme_data.get("name", "Custom")
        self.radius = theme_data.get("radius", 12)
        self.opacity = theme_data.get("opacity", {
            "bar": 0.90,
            "notifications": 0.95,
            "lockscreen": 0.80
        })
        self.wallpaper = wallpaper_path

        # Parse primary color fields into Color objects & derived properties
        self.colors = {}
        for key in self.COLOR_KEYS:
            val = theme_data.get(key, "#000000")
            color_obj = Color(val)
            self.colors[key] = color_obj
            setattr(self, key, color_obj.hex)
            setattr(self, f"{key}_hex", color_obj.hex)
            setattr(self, f"{key}_nohash", color_obj.nohash)
            setattr(self, f"{key}_rgb", color_obj.rgb)
            setattr(self, f"{key}_rgb_space", color_obj.rgb_space)
            setattr(self, f"{key}_light", color_obj.lighten().hex)
            setattr(self, f"{key}_dark", color_obj.darken().hex)
            setattr(self, f"{key}_light_nohash", color_obj.lighten().nohash)
            setattr(self, f"{key}_dark_nohash", color_obj.darken().nohash)

    @classmethod
    def from_json_file(cls, json_path: str, wallpaper_path: str = "") -> "ThemeModel":
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Theme file not found: {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data, wallpaper_path=wallpaper_path)

    def to_dict(self) -> dict:
        """Exposes all attributes in a flat dictionary for Jinja2 template rendering."""
        d = {
            "name": self.name,
            "radius": self.radius,
            "opacity": self.opacity,
            "wallpaper": self.wallpaper,
        }

        # Add all derived color attributes
        for key in self.COLOR_KEYS:
            color_obj = self.colors[key]
            d[key] = color_obj.hex
            d[f"{key}_hex"] = color_obj.hex
            d[f"{key}_nohash"] = color_obj.nohash
            d[f"{key}_rgb"] = color_obj.rgb
            d[f"{key}_rgb_space"] = color_obj.rgb_space
            d[f"{key}_light"] = color_obj.lighten().hex
            d[f"{key}_dark"] = color_obj.darken().hex
            d[f"{key}_light_nohash"] = color_obj.lighten().nohash
            d[f"{key}_dark_nohash"] = color_obj.darken().nohash
            d[f"{key}_obj"] = color_obj

        return d
