#!/usr/bin/env bash
# scripts/run-gradio.sh — Inicia a aplicação web Gradio
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"
echo "🌐 Iniciando Gradio em http://localhost:7860 ..."
~/.local/bin/uv run python src/ds_unicamp_applicada_3/app_gradio.py
