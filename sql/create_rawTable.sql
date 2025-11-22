CREATE TABLE IF NOT EXISTS stg_hospitais_raw (
    co_cnes VARCHAR(20),
    no_fantasia VARCHAR(255),
    nu_cnpj_mantenedora VARCHAR(50),
    no_razao_social VARCHAR(255),
    co_ibge VARCHAR(20),
    no_logradouro VARCHAR(255),
    nu_endereco VARCHAR(50),
    no_bairro VARCHAR(100),
    co_cep VARCHAR(20),
    nu_telefone VARCHAR(50),
    tp_unidade VARCHAR(50),
    ds_esfera_administrativa VARCHAR(100),
    ds_turno_atendimento VARCHAR(100),
    nu_latitude VARCHAR(20),
    nu_longitude VARCHAR(20),
    no_email VARCHAR(150)
);