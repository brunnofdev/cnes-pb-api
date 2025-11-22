CREATE TABLE IF NOT EXISTS esferas_administrativas (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100) UNIQUE NOT NULL
);

-- 2. Tabela de Turnos de Atendimento (Lookup / Domínio)
CREATE TABLE IF NOT EXISTS turnos_atendimento (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(255) UNIQUE NOT NULL
);

-- 3. Tabela de Mantenedoras (Empresas/Prefeituras)
CREATE TABLE IF NOT EXISTS mantenedoras (
    nu_cnpj VARCHAR(20) PRIMARY KEY,
    no_razao_social VARCHAR(255)
);

-- 4. Tabela de Endereços
CREATE TABLE IF NOT EXISTS enderecos (
    id SERIAL PRIMARY KEY,
    co_ibge VARCHAR(10),
    co_cep VARCHAR(15),
    no_bairro VARCHAR(100),
    no_logradouro VARCHAR(255),
    nu_endereco VARCHAR(50)
);

-- 5. Tabela Principal (Hospitais)
CREATE TABLE IF NOT EXISTS hospitais_pb (
    co_cnes VARCHAR(20) PRIMARY KEY,
    no_fantasia VARCHAR(255),
    nu_telefone VARCHAR(50),
    tp_unidade VARCHAR(10),

    -- Chaves Estrangeiras (Foreign Keys)
    mantenedora_cnpj VARCHAR(20) REFERENCES mantenedoras(nu_cnpj),
    endereco_id INTEGER REFERENCES enderecos(id),
    esfera_id INTEGER REFERENCES esferas_administrativas(id),
    turno_id INTEGER REFERENCES turnos_atendimento(id)
);