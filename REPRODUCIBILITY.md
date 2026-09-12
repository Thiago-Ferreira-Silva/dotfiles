# 🖥️ Manual de Reproduzibilidade e Manutenção do Sistema

Este documento descreve detalhadamente como o sistema é reproduzido a partir deste repositório de dotfiles utilizando **Chezmoi**, além de fornecer manuais práticos para manutenção e futuras alterações.

---

## 🚀 1. Guia de Instalação (Restauração em Nova Máquina)

Para clonar e aplicar todo o ambiente de dotfiles e dependências em uma instalação limpa (ex: Arch Linux):

1. **Instale o sistema operacional base** com suporte a rede e terminal.
2. **Execute o script de bootstrap one-liner**:
   ```bash
   sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply <seu-usuario-github>
   ```
   *(Ou se já clonou o repositório localmente, execute `./install.sh`)*
3. **Preencha os prompts interativos** do Chezmoi (Nome, E-mail, etc.).
4. O script executará automaticamente:
   - A instalação de pacotes nativos (`pacman`) e AUR (`yay`/`paru` com auto-bootstrap se necessário).
   - A configuração de recursos de sistema fora do `$HOME`:
     - Altera o shell padrão para `/bin/zsh`.
     - Habilita serviços essenciais no Systemd (`NetworkManager`, `bluetooth`, `greetd`).
     - Configura o gerenciador de login (`/etc/greetd/config.toml` para iniciar o Hyprland via `tuigreet`).
   - A aplicação de todos os arquivos de configuração (Hyprland, Waybar, Neovim, Zsh, Qt5ct, Qt6ct, etc.).
   - A instalação de dependências Python e compilação inicial do **Theme Engine**.
5. Reinicie o computador para carregar o greeter e iniciar a sessão gráfica com todas as configurações.

---

## ⚙️ 2. Gerenciamento de Recursos de Sistema (Fora do `/home`)

Como o Chezmoi gerencia nativamente apenas o diretório do usuário (`$HOME`), as configurações de sistema que residem em `/etc/` são tratadas automaticamente pelo script de pré-instalação (`run_once_before_install-packages.sh.tmpl`):
- **Greeter (`greetd`):** O arquivo `/etc/greetd/config.toml` é gerado automaticamente apontando para o `tuigreet` com inicialização do Hyprland.
- **Shell Padrão:** O comando `chsh -s /bin/zsh` configura o Zsh como shell do usuário.
- **Serviços:** NetworkManager, Bluetooth e Greetd são habilitados via `systemctl enable`.

---

## 📦 3. Manual de Adição de Novos Pacotes

Para garantir que novos programas instalados no sistema passem a fazer parte da lista reproduzível:

1. Abra o arquivo de manifesto de pacotes:
   `~/.local/share/chezmoi/.chezmoidata/packages.toml`
2. Adicione o nome do pacote na lista correspondente:
   - `native`: Para pacotes dos repositórios oficiais do Arch Linux.
   - `aur`: Para pacotes do AUR.
   - `flatpak`: Para aplicações Flatpak.
3. Commit e envie as alterações para o repositório git:
   ```bash
   git add .chezmoidata/packages.toml
   git commit -m "feat: adiciona novo pacote <nome>"
   git push
   ```

---

## 🎨 4. Manual de Criação e Edição de Temas (Theme Engine)

O sistema de temas centralizado gerencia a estética do Hyprland, Waybar, Rofi, Foot, SwayNC, Hyprlock e Wlogout.

### Como criar um novo tema:
1. Crie um diretório para o novo tema em:
   `~/.config/theme-engine/themes/<nome-do-tema>/`
2. Adicione os seguintes arquivos obrigatórios:
   - `metadata.toml`: Metadados do tema (nome, autor, versão).
   - `colors.json`: Paleta de cores em formato JSON (contendo variáveis de cores HEX/RGB).
3. Teste a compilação localmente:
   ```bash
   python3 ~/.config/theme-engine/build.py --theme <nome-do-tema>
   python3 ~/.config/theme-engine/apply.py --theme <nome-do-tema>
   ```
4. Adicione os arquivos ao chezmoi (`chezmoi add`) para versionamento.

---

## 🔒 5. Manual de Gerenciamento de Segredos (Secrets)

Caso precise gerenciar chaves de API, tokens de acesso ou configurações privadas:

1. Criptografe o arquivo utilizando o suporte nativo do Chezmoi com `age`:
   ```bash
   chezmoi add --encrypt ~/.config/seu-arquivo-secreto
   ```
2. O Chezmoi armazenará a versão criptografada no repositório com o prefixo `.chezmoicrypt` ou gerenciará a chave privada localmente de forma segura.

---

## 🔄 6. Fluxo de Trabalho Contínuo (Desenvolvimento e Alterações)

Sempre que modificar qualquer configuração diretamente no sistema:
1. Atualize o rastreamento no chezmoi:
   ```bash
   chezmoi add ~/.config/seu-programa/config.conf
   ```
2. Verifique as diferenças pendentes:
   ```bash
   chezmoi diff
   ```
3. Commit e push para o repositório remoto:
   ```bash
   chezmoi cd
   git add .
   git commit -m "chore: atualiza configuração do <programa>"
   git push
   ```
