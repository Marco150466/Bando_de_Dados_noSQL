Arthur Machado Santos;
Guilherme Nogueira Medeiros; 
Marco Antônio Soares de Brito

# Relatório de Migração e Integridade: MongoDB para PostgreSQL

## Resumo do Processo
Este projeto consistiu na migração de 101MB de dados cinematográficos do modelo NoSQL (MongoDB) para o modelo Relacional (PostgreSQL), garantindo a consistência dos dados.

## Etapas Técnicas Realizadas

### 1. Saneamento de Dados (Cleaning)
Devido à natureza flexível do NoSQL, os dados migrados continham duplicatas. Utilizamos a técnica `DISTINCT ON` para recriar as tabelas de forma otimizada, eliminando redundâncias sem travar o motor do banco de dados.

### 2. Normalização e Integridade Referencial
- **Primary Keys (PK):** Definimos `id_pessoa` e `id_producao` como chaves primárias únicas.
- **Foreign Keys (FK):** Estabelecemos vínculos físicos na tabela associativa `equipe_final`. 
- **Resultado Visual:** O diagrama ER agora apresenta conectores sólidos ("bolinhas pretas"), garantindo que nenhum ator ou papel exista sem um filme correspondente.

## Comparativo de Performance (Validação)
Enquanto o MongoDB oferece leituras rápidas de documentos únicos, o PostgreSQL garante a **Integridade Referencial**. O custo de performance dos `JOINs` é compensado pela segurança de que não existem dados órfãos ou inconsistentes na base de dados.

## Como Executar
Os scripts SQL fornecidos realizam a limpeza automática, a criação das constraints e a consulta final de validação que une as três tabelas principais.
