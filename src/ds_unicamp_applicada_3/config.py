"""Carregamento de variáveis de ambiente via python-dotenv."""

import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

# Localiza o .env subindo a árvore de diretórios a partir deste arquivo
_env_path = find_dotenv(usecwd=True) or str(Path(__file__).resolve().parents[3] / ".env")
load_dotenv(dotenv_path=_env_path, override=False)


def _require(name: str) -> str:
    """Retorna o valor da variável de ambiente ou lança ValueError."""
    value = os.getenv(name)
    if not value:
        raise ValueError(
            f"Variável de ambiente obrigatória não definida: {name!r}. "
            "Verifique o arquivo .env na raiz do projeto."
        )
    return value


SUPABASE_URL: str = _require("SUPABASE_URL")
SUPABASE_KEY: str = _require("SUPABASE_PUBLISHABLE_KEY")
MONGODB_URI: str = _require("MONGODB_URI")
MONGODB_DB_NAME: str = "agencia_viagens"
