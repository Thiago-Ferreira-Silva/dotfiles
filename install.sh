#!/bin/sh

set -e

# Script de Bootstrap para inicialização do Chezmoi e dotfiles

echo "=== Inicializando Dotfiles com Chezmoi ==="

# Verifica se o chezmoi está instalado, caso contrário instala
if ! command -v chezmoi >/dev/null 2>&1; then
    echo "Instalando chezmoi..."
    sh -c "$(curl -fsLS get.chezmoi.io)"
    export PATH="$HOME/.local/bin:$PATH"
fi

# Diretório do repositório de dotfiles (ou usa o repositório remoto)
REPO_URL="https://github.com/seu-usuario/dotfiles.git" # Ajustar conforme necessário

if [ -d "$HOME/.local/share/chezmoi" ]; then
    echo "Repositório chezmoi já existe localmente."
    chezmoi init --apply
else
    echo "Inicializando chezmoi a partir do repositório..."
    chezmoi init --apply "$REPO_URL"
fi

echo "=== Dotfiles aplicados com sucesso! ==="
