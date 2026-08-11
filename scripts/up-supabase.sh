#!/usr/bin/env bash
# scripts/up-supabase.sh
#
# Cria as tabelas no Supabase (PostgreSQL) a partir de specs/schema.sql.
# Requer: psql instalado (brew install libpq).
#
# Variáveis lidas do .env da raiz do projeto:
#   SUPABASE_URL   → ex: https://<project-ref>.supabase.co
#   SUPABASE_PWD   → senha do banco (Settings → Database → Database password)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$ROOT_DIR/.env"
SCHEMA_FILE="$ROOT_DIR/specs/schema.sql"

# ── Lê .env linha a linha (evita problemas com caracteres especiais via xargs) ──
if [[ ! -f "$ENV_FILE" ]]; then
  echo "⚠️  Arquivo .env não encontrado em $ENV_FILE"
  echo "   Copie .env.example para .env e preencha as credenciais."
  exit 1
fi

_read_env() {
  local key="$1"
  grep -E "^${key}=" "$ENV_FILE" | head -1 | cut -d'=' -f2- | sed 's/^"//;s/"$//'
}

SUPABASE_URL="$(_read_env SUPABASE_URL)"
SUPABASE_PWD="$(_read_env SUPABASE_PWD)"

# ── Valida variáveis obrigatórias ────────────────────────────────
MISSING=()
[[ -z "$SUPABASE_URL" ]] && MISSING+=("SUPABASE_URL")
[[ -z "$SUPABASE_PWD" ]] && MISSING+=("SUPABASE_PWD")

if [[ ${#MISSING[@]} -gt 0 ]]; then
  echo ""
  echo "🚨 ATENÇÃO: As seguintes variáveis não estão definidas no .env:"
  for VAR in "${MISSING[@]}"; do
    echo "   ❌  $VAR=<sua-credencial-aqui>"
  done
  echo ""
  echo "   Edite o arquivo .env antes de continuar."
  echo "   Consulte .env.example para ver o template completo."
  exit 1
fi

# ── Deriva parâmetros de conexão ─────────────────────────────────
# SUPABASE_URL = https://<ref>.supabase.co  →  ref = <ref>
PROJECT_REF="$(echo "$SUPABASE_URL" | sed 's|https://||' | cut -d'.' -f1)"
DB_HOST="db.${PROJECT_REF}.supabase.co"
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres

# ── Executa o schema ─────────────────────────────────────────────
echo ""
echo "🔌 Conectando: ${DB_USER}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
echo "📄 Executando: $SCHEMA_FILE"
echo ""

PGPASSWORD="$SUPABASE_PWD" psql \
  --host="$DB_HOST" \
  --port="$DB_PORT" \
  --dbname="$DB_NAME" \
  --username="$DB_USER" \
  --file="$SCHEMA_FILE" \
  --echo-all

echo ""
echo "✅ Schema aplicado com sucesso."
