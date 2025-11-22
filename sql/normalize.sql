-- 1. Popula Tabelas Auxiliares (DISTINCT para não duplicar)
INSERT INTO esferas_administrativas (descricao)
SELECT DISTINCT ds_esfera_administrativa FROM stg_hospitais_raw 
WHERE ds_esfera_administrativa IS NOT NULL
ON CONFLICT (descricao) DO NOTHING;

INSERT INTO turnos_atendimento (descricao)
SELECT DISTINCT ds_turno_atendimento FROM stg_hospitais_raw 
WHERE ds_turno_atendimento IS NOT NULL
ON CONFLICT (descricao) DO NOTHING;

INSERT INTO mantenedoras (nu_cnpj, no_razao_social)
SELECT DISTINCT nu_cnpj_mantenedora, no_razao_social FROM stg_hospitais_raw 
WHERE nu_cnpj_mantenedora IS NOT NULL
ON CONFLICT (nu_cnpj) DO NOTHING;

-- 2. Popula Tabela Principal (Fazendo JOIN para pegar os IDs)
INSERT INTO hospitais_pb (
    co_cnes, no_fantasia, co_ibge, nu_telefone, tp_unidade, 
    nu_latitude, nu_longitude, no_email,
    mantenedora_cnpj, esfera_id, turno_id
)
SELECT 
    stg.co_cnes, stg.no_fantasia, stg.co_ibge, stg.nu_telefone, stg.tp_unidade,
    stg.nu_latitude, stg.nu_longitude, stg.no_email,
    stg.nu_cnpj_mantenedora,
    esf.id,  -- Pega o ID numérico da esfera
    trn.id   -- Pega o ID numérico do turno
FROM stg_hospitais_raw stg
LEFT JOIN esferas_administrativas esf ON stg.ds_esfera_administrativa = esf.descricao
LEFT JOIN turnos_atendimento trn ON stg.ds_turno_atendimento = trn.descricao
ON CONFLICT (co_cnes) DO NOTHING;

-- 3. Popula Endereços
INSERT INTO enderecos (co_cnes, no_logradouro, nu_endereco, no_bairro, co_cep)
SELECT co_cnes, no_logradouro, nu_endereco, no_bairro, co_cep
FROM stg_hospitais_raw
ON CONFLICT (co_cnes) DO NOTHING;