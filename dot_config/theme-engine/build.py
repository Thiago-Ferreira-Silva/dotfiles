import os
import sys
import argparse
from jinja2 import Environment, FileSystemLoader
from theme_model import ThemeModel

# Ensure working directory is the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def build_theme(theme_path: str, wallpaper_path: str = "", templates_dir: str = "templates", cache_dir: str = "cache"):
    """Renders all templates using the given theme and writes outputs to cache directory."""
    if not os.path.exists(theme_path):
        print(f"Error: Theme file does not exist: {theme_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading theme from: {theme_path}")
    theme_model = ThemeModel.from_json_file(theme_path, wallpaper_path=wallpaper_path)
    context = theme_model.to_dict()

    if not os.path.exists(templates_dir):
        print(f"Error: Templates directory not found: {templates_dir}", file=sys.stderr)
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True)

    print(f"Rendering templates from '{templates_dir}' to '{cache_dir}'...")

    rendered_files = []
    # Walk through template directory and render each .j2 or template file
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            rel_dir = os.path.relpath(root, templates_dir)
            template_path = os.path.join(rel_dir, file) if rel_dir != "." else file
            
            # Determine target output filename (strip .j2 extension if present)
            out_filename = file[:-3] if file.endswith(".j2") else file
            out_dir = os.path.join(cache_dir, rel_dir) if rel_dir != "." else cache_dir
            os.makedirs(out_dir, exist_ok=True)
            
            out_filepath = os.path.join(out_dir, out_filename)
            
            # Render template
            template = env.get_template(template_path.replace("\\", "/"))
            rendered_content = template.render(**context)
            
            with open(out_filepath, "w", encoding="utf-8") as out_f:
                out_f.write(rendered_content)
                
            rendered_files.append(out_filepath)
            print(f"  [OK] Generated: {out_filepath}")

    print(f"Build complete. Total files generated: {len(rendered_files)}")
    return rendered_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Theme Engine Builder")
    parser.add_argument("--theme", "-t", required=True, help="Path to colors.json file or theme name")
    parser.add_argument("--wallpaper", "-w", default="", help="Path to wallpaper image")
    parser.add_argument("--templates", default="templates", help="Templates directory")
    parser.add_argument("--cache", default="cache", help="Output cache directory")
    
    args = parser.parse_args()
    
    theme_json = args.theme
    if not theme_json.endswith(".json"):
        theme_json = os.path.join("themes", args.theme, "colors.json")
        
    build_theme(theme_json, wallpaper_path=args.wallpaper, templates_dir=args.templates, cache_dir=args.cache)
