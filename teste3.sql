-- 3.3 Estruturação das Tabelas

-- Criar tabela para armazenar dados das operadoras de saúde
CREATE TABLE operadoras_saude (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data INT,
    REG_ANS INT,
    CD_CONTA_CONTABIL INT,
    DESCRICAO VARCHAR(255),
    VL_SALDO_INICIAL DECIMAL(18,2),
    VL_SALDO_FINAL VARCHAR(255),
    ano INT,
    trimestre INT,
    operadora VARCHAR(255),
    categoria VARCHAR(255),
    despesa_evento_sinistros DECIMAL(18,2),
    arquivo_origem VARCHAR(255)
);

-- 3.4 Importação de Dados CSV
-- Comando para importação (adapte o caminho do arquivo)
-- No MySQL Workbench, use:
-- Server > Data Import 
-- Ou use o seguinte comando (ajuste conforme necessário):
LOAD DATA LOCAL INFILE 'C:/caminho/para/seu/arquivo.csv'
INTO TABLE operadoras_saude
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    data,
    REG_ANS,
    CD_CONTA_CONTABIL,
    DESCRICAO,
    VL_SALDO_INICIAL,
    VL_SALDO_FINAL,
    ano,
    trimestre,
    operadora,
    categoria,
    despesa_evento_sinistros,
    arquivo_origem
)
SET arquivo_origem = 'nome_do_arquivo.csv';

-- 3.5 Queries Analíticas

-- 10 operadoras com maiores despesas no último trimestre
WITH UltimoTrimestre AS (
    SELECT 
        MAX(ano * 4 + trimestre) AS max_periodo
    FROM operadoras_saude
)
SELECT 
    operadora,
    ROUND(SUM(despesa_evento_sinistros), 2) AS total_despesas,
    COUNT(DISTINCT arquivo_origem) AS arquivos_fonte
FROM operadoras_saude
WHERE 
    ano * 4 + trimestre = (SELECT max_periodo FROM UltimoTrimestre)
    AND categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY operadora
ORDER BY total_despesas DESC
LIMIT 10;

-- 10 operadoras com maiores despesas no último ano
WITH UltimoAno AS (
    SELECT 
        MAX(ano) AS max_ano
    FROM operadoras_saude
)
SELECT 
    operadora,
    ROUND(SUM(despesa_evento_sinistros), 2) AS total_despesas,
    COUNT(DISTINCT arquivo_origem) AS arquivos_fonte
FROM operadoras_saude
WHERE 
    ano = (SELECT max_ano FROM UltimoAno)
    AND categoria = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'
GROUP BY operadora
ORDER BY total_despesas DESC
LIMIT 10;