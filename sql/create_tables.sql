DROP TABLE IF EXISTS enderecos CASCADE;
DROP TABLE IF EXISTS hospitais_pb CASCADE;
DROP TABLE IF EXISTS mantenedoras CASCADE;
DROP TABLE IF EXISTS esferas_administrativas CASCADE;
DROP TABLE IF EXISTS turnos_atendimento CASCADE;


CREATE TABLE esferas_administrativas (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE turnos_atendimento (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE mantenedoras (
    nu_cnpj VARCHAR(20) PRIMARY KEY,
    no_razao_social VARCHAR(255)
);

CREATE TABLE hospitais_pb (
    co_cnes VARCHAR(20) PRIMARY KEY,
    no_fantasia VARCHAR(255),
    nu_telefone VARCHAR(50),
    no_email VARCHAR(150),
    tp_unidade VARCHAR(10),

    -- Chaves Estrangeiras
    mantenedora_cnpj VARCHAR(20) REFERENCES mantenedoras(nu_cnpj),
    esfera_id INTEGER REFERENCES esferas_administrativas(id),
    turno_id INTEGER REFERENCES turnos_atendimento(id)
);

CREATE TABLE enderecos (
    co_cnes VARCHAR(20) PRIMARY KEY, -- Relação 1:1 com hospitais

    no_logradouro VARCHAR(255),
    nu_endereco VARCHAR(50),
    no_bairro VARCHAR(100),
    co_cep VARCHAR(15),

    nu_latitude VARCHAR(20),
    nu_longitude VARCHAR(20),
    co_ibge VARCHAR(10),

    CONSTRAINT fk_endereco_hospital
        FOREIGN KEY (co_cnes) REFERENCES hospitais_pb(co_cnes)
);