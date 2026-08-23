# Sistema de Temas para Hyprland (Theme Engine)

Um sistema completo, dinâmico e centralizado de gerenciamento de temas para a suíte Hyprland.

## 🚀 Recursos
- **Uma única fonte de verdade**: Paleta definida via `colors.json`.
- **Geração por Templates**: Jinja2 compila as configurações para todas as aplicações desktop.
- **Modelagem de Cores**: Converte e calcula automaticamente variações de HEX, RGB, RGBA e tons derivados (claros/escuros).
- **Troca Instantânea**: Aplica wallpapers via `awww` (ou `swww`) e recarrega os daemons ativos (`hyprctl`, `waybar`, `swaync`).
- **Suporte Futuro a Temas Dinâmicos**: Integração direta com Matugen / Wallust gerando `colors.json`.

---

## 📂 Estrutura de Diretórios

```
~/.config/theme-engine/
├── apply.py               # CLI principal para trocar temas
├── build.py               # Gerador de cache via Jinja2
├── theme_model.py         # Modelo Python com cálculo de cores
├── config.toml            # Configuração global e rotas de reload
├── requirements.txt
│
├── themes/                # Diretório de temas pré-definidos
│   ├── kanagawa/
│   │   ├── colors.json
│   │   ├── metadata.toml
│   │   └── wallpapers/
│   ├── nord/
│   ├── catppuccin/
│   └── gruvbox/
│
├── templates/             # Templates Jinja2 (.j2)
│   ├── hypr/colors.lua.j2
│   ├── waybar/style.css.j2
│   ├── foot/foot.ini.j2
│   ├── rofi/theme.rasi.j2
│   ├── swaync/style.css.j2
│   ├── hyprlock/hyprlock.conf.j2
│   └── wlogout/style.css.j2
│
└── cache/                 # Arquivos compilados gerados automaticamente
    ├── hypr/colors.lua
    ├── waybar/style.css
    ├── foot/foot.ini
    ├── rofi/theme.rasi
    ├── swaync/style.css
    ├── hyprlock/hyprlock.conf
    └── wlogout/style.css
```

---

## 🛠️ Configuração nos Programas

Para utilizar o Theme Engine, edite as configurações dos seus aplicativos para incluir os arquivos gerados em `cache/`:

| Aplicação | Arquivo Principal | Diretiva de Inclusão |
| :--- | :--- | :--- |
| **Hyprland** (0.55+ Lua) | `~/.config/hypr/hyprland.lua` | `dofile(os.getenv("HOME") .. "/.config/theme-engine/cache/hypr/colors.lua")` |
| **Waybar** | `~/.config/waybar/style.css` | `@import "../../theme-engine/cache/waybar/style.css";` |
| **Foot** | `~/.config/foot/foot.ini` | `include=~/.config/theme-engine/cache/foot/foot.ini` |
| **Rofi** | `~/.config/rofi/config.rasi` | `@theme "~/.config/theme-engine/cache/rofi/theme.rasi"` |
| **SwayNC** | `~/.config/swaync/config.json` | Usar caminho para `cache/swaync/style.css` |
| **Hyprlock** | `~/.config/hypr/hyprlock.conf` | `source = ~/.config/theme-engine/cache/hyprlock/hyprlock.conf` |
| **Wlogout** | `~/.config/wlogout/style.css` | `@import "../theme-engine/cache/wlogout/style.css";` |

---

## 💻 Instalação e Uso

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Aplicar um Tema
```bash
# Aplicar o tema Kanagawa
python apply.py --theme kanagawa

# Aplicar o tema Nord especificando um wallpaper personalizado
python apply.py --theme nord --wallpaper ~/Pictures/wallpapers/nord.jpg
```

---

## 🔄 Fluxo para Temas Dinâmicos (Matugen / Wallust)

Como toda a infraestrutura consome exclusivamente o `colors.json`, você pode utilizar geradores de paletas a partir de imagens para sobrescrever ou criar um `colors.json` temporário:

```
Wallpaper -> Matugen / Wallust -> colors.json -> Theme Model -> Templates -> Arquivos Gerados em cache/
```
