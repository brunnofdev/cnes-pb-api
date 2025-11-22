-- Tabelas Auxiliares 
CREATE TABLE IF NOT EXISTS esferas_administrativas (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS turnos_atendimento (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS mantenedoras (
    nu_cnpj VARCHAR(20) PRIMARY KEY,
    no_razao_social VARCHAR(255)
);

-- 3. Tabela Principal ("QUEM" é o hospital)
CREATE TABLE IF NOT EXISTS hospitais_pb (
    co_cnes VARCHAR(20) PRIMARY KEY,
    no_fantasia VARCHAR(255),
    nu_telefone VARCHAR(50),
    no_email VARCHAR(150),
    tp_unidade VARCHAR(10),

    -- Vínculos Institucionais
    mantenedora_cnpj VARCHAR(20) REFERENCES mantenedoras(nu_cnpj),
    esfera_id INTEGER REFERENCES esferas_administrativas(id),
    turno_id INTEGER REFERENCES turnos_atendimento(id)
);

-- 4. Tabela de Endereços ("ONDE" fica)
CREATE TABLE IF NOT EXISTS enderecos (
    co_cnes VARCHAR(20) PRIMARY KEY, -- Vínculo 1-para-1 com Hospital
    
    -- Dados de Logradouro
    no_logradouro VARCHAR(255),
    nu_endereco VARCHAR(50),
    no_bairro VARCHAR(100),
    co_cep VARCHAR(15),
    
    -- Dados Geográficos
    nu_latitude VARCHAR(20),
    nu_longitude VARCHAR(20),
    
    -- Cidade (futuramente adicionar FK para tabela de cidades)
    co_ibge VARCHAR(10), 

    -- Relacionamento com Hospital
    CONSTRAINT fk_endereco_hospital 
        FOREIGN KEY (co_cnes) REFERENCES hospitais_pb(co_cnes)
);