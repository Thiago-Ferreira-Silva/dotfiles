#!/bin/bash

set -e

THEME_ENGINE_DIR="$HOME/.config/theme-engine"

if [ -d "$THEME_ENGINE_DIR" ]; then
    echo "=== Configurando Theme Engine ==="
    
    # Criar ambiente virtual Python para evitar restrições de pacotes externos do Arch Linux
    if [ ! -d "$THEME_ENGINE_DIR/venv" ]; then
        echo "Criando ambiente virtual Python para o Theme Engine..."
        python3 -m venv --system-site-packages "$THEME_ENGINE_DIR/venv"
    fi

    # Ativar venv e instalar dependências se necessário
    if [ -f "$THEME_ENGINE_DIR/requirements.txt" ]; then
        echo "Instalando/verificando dependências Python..."
        "$THEME_ENGINE_DIR/venv/bin/pip" install --upgrade pip --quiet || true
        "$THEME_ENGINE_DIR/venv/bin/pip" install -r "$THEME_ENGINE_DIR/requirements.txt"
    fi

    if [ -f "$THEME_ENGINE_DIR/apply.py" ]; then
        echo "Aplicando tema padrão (kanagawa)..."
        "$THEME_ENGINE_DIR/venv/bin/python" "$THEME_ENGINE_DIR/apply.py" --theme kanagawa || python3 "$THEME_ENGINE_DIR/apply.py" --theme kanagawa
    fi
    echo "=== Theme Engine configurado com sucesso ==="
fi
