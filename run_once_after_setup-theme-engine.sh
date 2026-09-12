#!/bin/bash

set -e

THEME_ENGINE_DIR="$HOME/.config/theme-engine"

if [ -d "$THEME_ENGINE_DIR" ]; then
    echo "=== Configurando Theme Engine ==="
    if [ -f "$THEME_ENGINE_DIR/requirements.txt" ]; then
        echo "Instalando dependências Python do Theme Engine..."
        pip install --user -r "$THEME_ENGINE_DIR/requirements.txt" || pip3 install --user -r "$THEME_ENGINE_DIR/requirements.txt"
    fi

    if [ -f "$THEME_ENGINE_DIR/apply.py" ]; then
        echo "Aplicando tema padrão (kanagawa)..."
        python3 "$THEME_ENGINE_DIR/apply.py" --theme kanagawa || python "$THEME_ENGINE_DIR/apply.py" --theme kanagawa
    fi
    echo "=== Theme Engine configurado com sucesso ==="
fi
