#!/usr/bin/env bash
# scripts/run-tkinter.sh — Inicia a aplicação desktop Tkinter
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"
echo "🖥️  Iniciando Painel Administrativo (Tkinter)..."
~/.local/bin/uv run python src/ds_unicamp_applicada_3/app_tkinter.py
