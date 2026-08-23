#!/usr/bin/env bash

cd "$(dirname "$0")"

THEME_DIR="./themes"
VENV_PYTHON="./venv/bin/python"
APPLY_SCRIPT="./apply.py"

# Lista os subdiretórios em themes/ (nomes dos temas)
themes=$(ls -1 "$THEME_DIR")

# Exibe o menu dmenu do Rofi
selected_theme=$(echo -e "$themes" | rofi -dmenu -p "🎨 Selecionar Tema")

# Se um tema foi selecionado, aplica-o
if [ -n "$selected_theme" ]; then
    "$VENV_PYTHON" "$APPLY_SCRIPT" --theme "$selected_theme"
    notify-send "Theme Engine" "Tema '$selected_theme' aplicado com sucesso!"
fi
