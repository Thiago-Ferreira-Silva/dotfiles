import os
import unittest
from theme_model import ThemeModel, Color
from build import build_theme

class TestThemeEngine(unittest.TestCase):
    def test_color_conversions(self):
        c = Color("#1f1f28")
        self.assertEqual(c.hex, "#1f1f28")
        self.assertEqual(c.nohash, "1f1f28")
        self.assertEqual(c.r, 31)
        self.assertEqual(c.g, 31)
        self.assertEqual(c.b, 40)
        self.assertEqual(c.rgb, "31, 31, 40")
        self.assertEqual(c.rgb_space, "31 31 40")
        self.assertEqual(c.rgba(0.9), "rgba(31, 31, 40, 0.90)")

    def test_theme_model(self):
        kanagawa_json = os.path.join("themes", "kanagawa", "colors.json")
        model = ThemeModel.from_json_file(kanagawa_json, wallpaper_path="/tmp/wall.jpg")
        ctx = model.to_dict()
        
        self.assertEqual(ctx["name"], "Kanagawa")
        self.assertEqual(ctx["background"], "#1f1f28")
        self.assertEqual(ctx["background_nohash"], "1f1f28")
        self.assertEqual(ctx["background_rgb"], "31, 31, 40")
        self.assertEqual(ctx["radius"], 14)
        self.assertEqual(ctx["wallpaper"], "/tmp/wall.jpg")

    def test_build_all_themes(self):
        themes = ["kanagawa", "nord", "catppuccin", "gruvbox"]
        for t in themes:
            colors_json = os.path.join("themes", t, "colors.json")
            cache_out = os.path.join("cache_test", t)
            generated = build_theme(colors_json, templates_dir="templates", cache_dir=cache_out)
            
            # Check expected files
            self.assertTrue(os.path.exists(os.path.join(cache_out, "hypr", "colors.lua")))
            self.assertTrue(os.path.exists(os.path.join(cache_out, "waybar", "style.css")))
            self.assertTrue(os.path.exists(os.path.join(cache_out, "foot", "foot.ini")))
            self.assertTrue(os.path.exists(os.path.join(cache_out, "rofi", "theme.rasi")))
            self.assertTrue(os.path.exists(os.path.join(cache_out, "swaync", "style.css")))
            self.assertTrue(os.path.exists(os.path.join(cache_out, "hyprlock", "hyprlock.conf")))
            self.assertTrue(os.path.exists(os.path.join(cache_out, "wlogout", "style.css")))

if __name__ == "__main__":
    unittest.main()
