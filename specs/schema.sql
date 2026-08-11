-- SQL para criação das tabelas no Supabase (PostgreSQL)
-- Execute no Supabase Dashboard → SQL Editor

-- Tabela de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id    SERIAL PRIMARY KEY,
    nome  TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Tabela de destinos
CREATE TABLE IF NOT EXISTS destinos (
    id    SERIAL PRIMARY KEY,
    nome  TEXT NOT NULL,
    pais  TEXT NOT NULL,
    preco NUMERIC NOT NULL
);

-- Tabela de vendas (relaciona cliente e destino)
CREATE TABLE IF NOT EXISTS vendas (
    id          SERIAL PRIMARY KEY,
    cliente_id  INT NOT NULL REFERENCES clientes(id) ON DELETE CASCADE,
    destino_id  INT NOT NULL REFERENCES destinos(id) ON DELETE CASCADE,
    data_viagem DATE NOT NULL
);
