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
    co_cnes, no_fantasia, nu_telefone, no_email, tp_unidade, 
    mantenedora_cnpj, esfera_id, turno_id
)
SELECT 
    stg.co_cnes, 
    stg.no_fantasia, 
    stg.nu_telefone, 
    stg.no_email, 
    stg.tp_unidade,
    stg.nu_cnpj_mantenedora,
    esf.id, -- Pega o ID gerado para a esfera
    trn.id  -- Pega o ID gerado para o turno
FROM stg_hospitais_raw stg
LEFT JOIN esferas_administrativas esf ON stg.ds_esfera_administrativa = esf.descricao
LEFT JOIN turnos_atendimento trn ON stg.ds_turno_atendimento = trn.descricao
ON CONFLICT (co_cnes) DO NOTHING;

-- 3. Popula Endereços (Com Latitude, Longitude e o Código IBGE direto)
INSERT INTO enderecos (
    co_cnes, 
    no_logradouro, nu_endereco, no_bairro, co_cep,
    nu_latitude, nu_longitude, co_ibge
)
SELECT 
    stg.co_cnes, 
    stg.no_logradouro, stg.nu_endereco, stg.no_bairro, stg.co_cep,
    stg.nu_latitude, stg.nu_longitude, stg.co_ibge
FROM stg_hospitais_raw stg
INNER JOIN hospitais_pb h ON stg.co_cnes = h.co_cnes
ON CONFLICT (co_cnes) DO NOTHING;