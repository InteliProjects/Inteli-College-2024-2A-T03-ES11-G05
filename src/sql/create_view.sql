CREATE VIEW IF NOT EXISTS sku_costs AS
SELECT
    JSONExtractInt(dado_linha, 'cod_prod') AS cod_prod,
    toDateTime(JSONExtractString(dado_linha, 'data_inicio')) AS data_inicio_datetime,
    toDateTime(JSONExtractString(dado_linha, 'data_fim')) AS data_fim_datetime,
    JSONExtractFloat(dado_linha, 'custo') AS custo,
    toDateTime(
        JSONExtractInt(dado_linha, 'data_ingestao') / 1000
    ) AS data_ingestao_datetime
FROM working_data
WHERE tag = 'sku_cost';