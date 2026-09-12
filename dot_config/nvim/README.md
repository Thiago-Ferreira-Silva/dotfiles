# 🚀 Manual do Neovim (Kickstart Configuration)

Bem-vindo ao manual completo de utilização e configuração do Neovim. Esta configuração é uma versão moderna, modularizada e performática do **Kickstart.nvim**, desenvolvida em Lua e utilizando o gerenciador de pacotes nativo do Neovim (`vim.pack`).

---

## 📋 Sumário
1. [Descrição da Configuração](#1-descrição-da-configuração)
2. [Requisitos do Sistema](#2-requisitos-do-sistema)
3. [Instalação](#3-instalação)
4. [Descrição de Todos os Plugins Utilizados](#4-descrição-de-todos-os-plugins-utilizados)
5. [Comandos Básicos do Neovim e dos Plugins](#5-comandos-básicos-do-neovim-e-dos-plugins)
6. [Listagem Completa de Atalhos (Keymaps)](#6-listagem-completa-de-atalhos-keymaps)

---

## 1. Descrição da Configuração

A configuração segue uma arquitetura modularizada para facilitar a manutenção, legibilidade e personalização:

```
~/.config/nvim/
├── init.lua                   # Ponto de entrada principal
├── nvim-pack-lock.json        # Trava de versões dos plugins
├── lua/
│   ├── config/                # Configurações do núcleo do Neovim
│   │   ├── options.lua        # Opções nativas (linhas, recuo, clipboard, etc.)
│   │   ├── keymaps.lua        # Mapeamentos de teclas básicos e janelas
│   │   ├── autocmds.lua       # Autocomandos e hooks de compilação do vim.pack
│   │   └── health.lua         # Verificações de integridade
│   └── plugins/               # Módulos e especificações dos plugins
│       ├── ui.lua             # Temas, statusline, ícones, which-key, mini.*
│       ├── telescope.lua      # Busca fuzzy, navegação de arquivos e buffers
│       ├── lsp.lua            # Servidores LSP, Mason e fidget
│       ├── conform.lua        # Formatação de código assíncrona
│       ├── completion.lua     # Autocompletar (blink.cmp) e Snippets (LuaSnip)
│       ├── treesitter.lua     # Parser sintático e destaques de código
│       ├── debug.lua          # Depuração (DAP, DAP UI)
│       ├── neo-tree.lua       # Navegador de arquivos em árvore
│       ├── gitsigns.lua       # Integração com Git
│       ├── indent_line.lua    # Linhas de guia de indentação
│       ├── lint.lua           # Linters de código
│       └── autopairs.lua      # Fechamento automático de pares
```

### Principais recursos inclusos:
- **Gerenciador de Plugins Nativo (`vim.pack`)**: Gerenciamento direto sem dependência de gerenciadores externos como `lazy.nvim` ou `packer.nvim`.
- **Suporte LSP Avançado**: Configurado com `nvim-lspconfig`, `mason.nvim` e instalações automáticas de LSPs.
- **Autocompletar Ultrarrápido**: Alimentado por `blink.cmp` e `LuaSnip` com trechos prontos do `friendly-snippets`.
- **Análise Sintática Inteligente**: Com `nvim-treesitter` para destaque colorido e dobras precisas.
- **Formatação e Linting**: Suporte a autoformatação com `conform.nvim` e diagnóstico com `nvim-lint`.
- **Ambiente de Depuração (DAP)**: Configuração de depurador pronta para uso (suporte nativo a Go e extensível a outras linguagens).

---

## 2. Requisitos do Sistema

Para obter o funcionamento ideal de todas as funcionalidades e plugins, certifique-se de possuir instalado em seu ambiente:

| Requisito | Versão Recomendada | Finalidade |
| :--- | :--- | :--- |
| **Neovim** | `>= 0.10.0` (Recomendado `0.12+`) | Suporte ao `vim.pack` e APIs Lua modernas |
| **Git** | Qualquer versão recente | Clonagem e atualização automática de plugins |
| **Compilador C / `make`** | `gcc`, `clang` ou `make` | Compilação do `telescope-fzf-native` e `jsregexp` |
| **Ripgrep** | `rg` | Execução ultra-rápida do `live_grep` no Telescope |
| **fd** | `fd` | Busca otimizada de arquivos no sistema |
| **Nerd Font** | Qualquer uma (ex: JetBrainsMono, FiraCode) | Exibição correta de ícones no editor e na statusline |
| **Node.js & npm** | `>= 18.x` (Opcional) | Suporte a LSPs baseados em Node (TypeScript, Pyright, HTML, CSS, etc.) |
| **Python 3** | `>= 3.9` (Opcional) | Suporte a linters e formatadores em Python (`black`, `isort`) |

---

## 3. Instalação

Siga os passos abaixo para instalar e executar esta configuração:

### 1. Fazer Backup da Configuração Atual (Se houver)
```bash
mv ~/.config/nvim ~/.config/nvim.backup
mv ~/.local/share/nvim ~/.local/share/nvim.backup
```

### 2. Clonar o Repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO> ~/.config/nvim
```

### 3. Abrir o Neovim
```bash
nvim
```
Ao iniciar pela primeira vez, o Neovim baixará automaticamente os plugins configurados via `vim.pack` e executará as etapas de compilação pós-instalação (como a compilação do FZF native).

### 4. Verificar a Integridade
Dentro do Neovim, execute o comando de diagnóstico para garantir que todas as ferramentas estão funcionais:
```vim
:checkhealth
```

---

## 4. Descrição de Todos os Plugins Utilizados

### 🎨 Interface, Tema e UX
- **`folke/tokyonight.nvim`**: Tema visual moderno. O esquema ativado por padrão é o `tokyonight-night`.
- **`folke/which-key.nvim`**: Exibe uma janela pop-up interativa mostrando os atalhos disponíveis ao pressionar teclas líderes (`<leader>`).
- **`folke/todo-comments.nvim`**: Destaca palavras-chave em comentários como `TODO`, `FIX`, `NOTE`, `WARN`, `HACK`.
- **`nvim-mini/mini.nvim`**: Coleção modular de utilitários leves:
  - `mini.icons`: Gerenciador de ícones para componentes da interface.
  - `mini.ai`: Objetos de texto aprimorados para seleção/edição (`a`/`i`) ao redor ou dentro de parênteses, aspas, etc.
  - `mini.surround`: Adiciona, deleta ou substitui elementos envolventes (aspas, colchetes, parênteses).
  - `mini.statusline`: Barra de status limpa e leve na parte inferior da tela.
- **`NMAC427/guess-indent.nvim`**: Detecta e ajusta automaticamente a indentação do arquivo aberto (tabs vs. espaços e tamanho).
- **`lukas-reineke/indent-blankline.nvim`**: Desenha guias visuais verticais de indentação no código, incluindo linhas em branco.

### 🔍 Busca e Navegação
- **`nvim-telescope/telescope.nvim`**: Mecanismo principal de busca fuzzy para arquivos, textos, símbolos LSP, comandos e ajuda.
- **`nvim-lua/plenary.nvim`**: Biblioteca de funções em Lua requerida por múltiplos plugins (Telescope, Neo-tree, Gitsigns).
- **`nvim-telescope/telescope-ui-select.nvim`**: Converte os menus de seleção do Neovim para a interface do Telescope.
- **`nvim-telescope/telescope-fzf-native.nvim`**: Extensão escrita em C para aceleração da busca fuzzy no Telescope.
- **`nvim-neo-tree/neo-tree.nvim`** *(com `MunifTanjim/nui.nvim`)*: Árvore lateral de arquivos para navegação e manipulação do diretório.

### 🌳 Sintaxe e Parsing
- **`nvim-treesitter/nvim-treesitter`**: Gerador de árvore sintática (AST) que proporciona realce de sintaxe avançado, indentação precisa e suporte a dobras de código.

### 🧠 LSP & Gerenciamento de Ferramentas
- **`neovim/nvim-lspconfig`**: Configurações padrão para servidores de linguagem (LSP).
- **`mason-org/mason.nvim`**: Gerenciador de pacotes dentro do Neovim para instalar LSPs, formatadores e linters.
- **`mason-org/mason-lspconfig.nvim`**: Conecta o Mason ao `nvim-lspconfig`.
- **`WhoIsSethDaniel/mason-tool-installer.nvim`**: Garante a instalação automática dos servidores configurados (`gopls`, `pyright`, `stylua`, `bash-language-server`, `typescript-language-server`, etc.).
- **`j-hui/fidget.nvim`**: Notificações discretas com o progresso das operações do LSP no canto inferior da tela.

### ⚡ Autocompletar e Snippets
- **`saghen/blink.cmp`**: Engine de autocompletar rápida com suporte a LSP, caminhos e snippets.
- **`L3MON4D3/LuaSnip`**: Mecanismo de expansão e manipulação de trechos de código (snippets).
- **`rafamadriz/friendly-snippets`**: Biblioteca com centenas de snippets pré-definidos para diversas linguagens.

### 🛠️ Formatação e Linting
- **`stevearc/conform.nvim`**: Formatador de código com suporte a execução assíncrona ao salvar e integração com ferramentas como `stylua`, `black`, `isort` ou LSP fallback.
- **`mfussenegger/nvim-lint`**: Executa linters assincronamente (ex: `markdownlint`).

### 🐙 Integração com Git
- **`lewis6991/gitsigns.nvim`**: Exibe sinais visuais no gutter para linhas modificadas/adicionadas/removidas, além de permitir navegação por hunks, staging, reset e blame.

### ✍️ Edição
- **`windwp/nvim-autopairs`**: Fecha automaticamente parênteses, colchetes, chaves e aspas ao digitar.

### 🐛 Depuração (DAP)
- **`mfussenegger/nvim-dap`**: Cliente do protocolo de depuração (Debug Adapter Protocol).
- **`rcarriga/nvim-dap-ui`** & **`nvim-neotest/nvim-nio`**: Interface visual gráfica para inspeção de variáveis, pilha de chamadas e pontos de interrupção.
- **`jay-babu/mason-nvim-dap.nvim`**: Conecta o Mason para gerenciamento automático de depuradores.
- **`leoluz/nvim-dap-go`**: Configurações e facilidades de depuração para código em linguagem Go via Delve.

---

## 5. Comandos Básicos do Neovim e dos Plugins

### 📄 Comandos Gerais do Neovim
- `:w` — Salva as alterações do arquivo atual.
- `:q` — Fecha o buffer/janela atual.
- `:qa` — Fecha todas as janelas do Neovim.
- `:vsplit` ou `:split` — Divide a janela verticalmente ou horizontalmente.
- `:checkhealth` — Executa uma verificação completa de saúde da configuração e dependências.
- `:Tutor` — Inicia o tutorial nativo do Neovim para aprendizado de movimentações e edições básicas.

### 📦 Comandos do Gerenciador de Plugins (`vim.pack`)
- `:lua vim.pack.update()` — Baixa e atualiza todos os plugins listados.
- `:lua vim.pack.update(nil, { offline = true })` — Inspeciona o estado atual dos plugins instalados sem realizar downloads.

### 🧩 Comandos Úteis dos Plugins
- **Mason**:
  - `:Mason` — Abre o painel do Mason para gerenciar e instalar servidores LSP, linters e formatadores.
- **Treesitter**:
  - `:TSUpdate` — Atualiza os parsers de sintaxe do Treesitter.
- **Neo-tree**:
  - `:Neotree reveal` — Abre a árvore de arquivos e foca no arquivo atual.
  - `:Neotree close` — Fecha a janela do Neo-tree.
- **Telescope**:
  - `:Telescope <picker>` — Executa um buscador específico (ex: `:Telescope find_files`, `:Telescope live_grep`, `:Telescope colorscheme`).

---

## 6. Listagem Completa de Atalhos (Keymaps)

> **Nota:** A tecla **Leader** desta configuração está definida como o `<Espaço>` (`<Space>`).

### 🖥️ Navegação e Ações Gerais
| Modo | Atalho | Ação / Descrição |
| :---: | :--- | :--- |
| **N** | `<Esc>` | Limpa o destaque das buscas ativas (`nohlsearch`) |
| **T** | `<Esc><Esc>` | Sai do modo terminal embutido (`<C-\><C-n>`) |
| **N** | `<C-h>` | Mover o foco para a janela da **esquerda** |
| **N** | `<C-l>` | Mover o foco para a janela da **direita** |
| **N** | `<C-j>` | Mover o foco para a janela **abaixo** |
| **N** | `<C-k>` | Mover o foco para a janela **acima** |
| **N** | `<leader>q` | Abrir a lista Quickfix de diagnósticos (`loclist`) |
| **N** | `\` | Revelar o arquivo atual na árvore do Neo-tree |

---

### 🔍 Busca e Navegação (Telescope)
| Modo | Atalho | Ação / Descrição |
| :---: | :--- | :--- |
| **N** | `<leader>sf` | **[S]earch [F]iles**: Buscar arquivos no projeto |
| **N** | `<leader>sg` | **[S]earch by [G]rep**: Buscar texto em todo o projeto via Grep |
| **N, V** | `<leader>sw` | **[S]earch current [W]ord**: Buscar a palavra sob o cursor |
| **N** | `<leader><space>` | Buscar e alternar entre **buffers abertos** |
| **N** | `<leader>/` | Busca Fuzzy dentro do **buffer atual** |
| **N** | `<leader>s/` | **[S]earch [/]**: Live Grep pesquisando apenas nos arquivos abertos |
| **N** | `<leader>sd` | **[S]earch [D]iagnostics**: Listar mensagens de erros/avisos |
| **N** | `<leader>sh` | **[S]earch [H]elp**: Buscar na documentação de ajuda do Neovim |
| **N** | `<leader>sk` | **[S]earch [K]eymaps**: Buscar atalhos de teclado cadastrados |
| **N** | `<leader>ss` | **[S]earch [S]elect**: Listar todos os pickers disponíveis no Telescope |
| **N** | `<leader>sr` | **[S]earch [R]esume**: Retomar a janela da última busca feita no Telescope |
| **N** | `<leader>s.` | **[S]earch Recent Files**: Buscar em arquivos abertos recentemente |
| **N** | `<leader>sc` | **[S]earch [C]ommands**: Buscar comandos do Neovim |
| **N** | `<leader>sn` | **[S]earch [N]eovim files**: Buscar arquivos da configuração do Neovim |

---

### 🧠 Linguagem e Inteligência de Código (LSP)
*(Ativados automaticamente quando um servidor LSP conecta ao arquivo)*

| Modo | Atalho | Ação / Descrição |
| :---: | :--- | :--- |
| **N** | `K` | Exibir documentação / informações do tipo sob o cursor (**Hover**) |
| **N** | `gd` | **[G]oto [D]efinition**: Ir para a definição do símbolo |
| **N** | `gD` | **[G]oto [D]eclaration**: Ir para a declaração |
| **N** | `gr` | **[G]oto [R]eferences**: Listar referências do símbolo |
| **N** | `gi` | **[G]oto [I]mplementation**: Ir para a implementação |
| **N** | `grt` | **[G]oto [T]ype Definition**: Ir para a definição do tipo |
| **N** | `gO` | Exibir estrutura de símbolos do documento atual (**Document Symbols**) |
| **N** | `gW` | Exibir símbolos de todo o projeto (**Workspace Symbols**) |
| **N** | `<leader>rn` | **[R]e[n]ame**: Renomear o símbolo sob o cursor em todo o projeto |
| **N, X** | `<leader>ca` | **[C]ode [A]ction**: Executar Ação de Código sugerida pelo LSP |
| **N** | `<leader>th` | **[T]oggle Inlay [H]ints**: Alternar exibição de dicas embutidas no código |

---

### 🎨 Formatação de Código
| Modo | Atalho | Ação / Descrição |
| :---: | :--- | :--- |
| **N, V** | `<leader>f` | **[F]ormat**: Formatar o arquivo ou trecho selecionado via Conform |

---

### 🐙 Integração com Git (Gitsigns)
| Modo | Atalho | Ação / Descrição |
| :---: | :--- | :--- |
| **N** | `]c` | Ir para a **próxima** alteração de Git (Next Hunk) |
| **N** | `[c` | Ir para a alteração de Git **anterior** (Previous Hunk) |
| **N, V** | `<leader>hs` | Git **[s]tage hunk**: Adicionar o hunk selecionado/atual ao staging |
| **N, V** | `<leader>hr` | Git **[r]eset hunk**: Reverter as alterações do hunk |
| **N** | `<leader>hS` | Git **[S]tage buffer**: Adicionar todas as alterações do buffer ao staging |
| **N** | `<leader>hR` | Git **[R]eset buffer**: Reverter todas as alterações do buffer |
| **N** | `<leader>hp` | Git **[p]review hunk**: Abrir janela flutuante com a prévia da alteração |
| **N** | `<leader>hi` | Git preview hunk **[i]nline**: Exibir prévia da alteração na própria linha |
| **N** | `<leader>hb` | Git **[b]lame line**: Exibir detalhes do commit e autor da linha atual |
| **N** | `<leader>hd` | Git **[d]iff index**: Exibir diff comparando com o índice do Git |
| **N** | `<leader>hD` | Git **[D]iff commit**: Exibir diff comparando com o último commit (`@`) |
| **N** | `<leader>hq` | Git hunk **[q]uickfix**: Abrir lista quickfix com alterações do arquivo atual |
| **N** | `<leader>hQ` | Git hunk **[Q]uickfix**: Abrir lista quickfix com alterações de todo o repositório |
| **N** | `<leader>tb` | **[T]oggle [b]lame**: Alternar exibição permanente de blame no final da linha |
| **N** | `<leader>tw` | **[T]oggle [w]ord diff**: Alternar destaque de diferenças palavra por palavra |
| **O, X** | `ih` | Objeto de texto para selecionar o hunk do Git |

---

### 🐛 Depuração (DAP - Debug Adapter Protocol)
| Modo | Atalho | Ação / Descrição |
| :---: | :--- | :--- |
| **N** | `<F5>` | Iniciar ou continuar execução da depuração |
| **N** | `<F1>` | Entrar na função (**Step Into**) |
| **N** | `<F2>` | Passar sobre a instrução (**Step Over**) |
| **N** | `<F3>` | Sair da função (**Step Out**) |
| **N** | `<F7>` | Alternar a exibição da interface do depurador (DAP UI) |
| **N** | `<leader>b` | Alternar ponto de interrupção (**Toggle Breakpoint**) |
| **N** | `<leader>B` | Definir ponto de interrupção **condicional** |

---

### ⚡ Autocompletar e Snippets (Blink.cmp)
*(Disponíveis durante o Modo de Inserção)*

| Atalho | Ação / Descrição |
| :--- | :--- |
| `<C-y>` | **Aceitar sugestão**: Insere a sugestão, executa auto-importação e expande o snippet |
| `<Tab>` / `<S-Tab>` | **Navegar pelo snippet**: Mover para a direita/esquerda nos campos do snippet |
| `<C-space>` | **Abrir menu**: Abre o menu de sugestões ou a documentação estendida |
| `<C-n>` / `<Down>` | Selecionar a **próxima** sugestão |
| `<C-p>` / `<Up>` | Selecionar a sugestão **anterior** |
| `<C-e>` | **Ocultar** o menu de autocompletar |
| `<C-k>` | Alternar exibição da caixa de **ajuda de assinatura** da função |

---

### ✏️ Edição, Manipulação de Texto e Envolvimento (mini.ai & mini.surround)

#### Objetos de Texto Avançados (`mini.ai`)
| Atalho | Exemplo | Descrição |
| :--- | :--- | :--- |
| `va)` | Modo Visual | Seleciona visualmente ao redor do parênteses |
| `ciiq` | Modo Normal | Altera o conteúdo dentro das próximas aspas (`next quote`) |

#### Caracteres Envolventes (`mini.surround`)
| Comando | Ação | Exemplo |
| :--- | :--- | :--- |
| `saiw)` | **Adicionar** envolvimento | Adiciona parênteses ao redor da palavra atual |
| `sd'` | **Deletar** envolvimento | Remove as aspas simples que envolvem o trecho |
| `sr)'` | **Substituir** envolvimento | Substitui parênteses envolventes por aspas simples |

---

*Manual gerado para a configuração do Neovim baseada em Kickstart.nvim.*
