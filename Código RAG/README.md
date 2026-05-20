# Projeto RAG Avançado com Qdrant Local + Maritaca AI

Este projeto implementa uma arquitetura de **RAG Avançado (Retrieval-Augmented Generation)** utilizando uma base de dados de filmes (IMDb Top 1000). A evolução em relação ao modelo tradicional (*Naive*) visa mitigar falhas comuns de contexto através de técnicas sofisticadas de manipulação de consultas e filtragem profunda de resultados.

## 🚀 Tecnologias Utilizadas

- **Base de Dados:** Catálogo `imdb_top_1000.csv`
- **Banco de Dados Não Relacional Vetorial:** Qdrant (rodando localmente via Docker)
- **Modelo de Embeddings (Bi-Encoder):** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensões)
- **Modelo de Re-ranqueamento (Cross-Encoder):** `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **Provedor de LLM:** Maritaca AI (Modelo: `sabiazinho-4`)

---

## 🏗️ Arquitetura do RAG Avançado Implementada

Diferente do RAG tradicional que faz uma busca linear e direta, este projeto implementa três camadas inteligentes de processamento:
| [ Pergunta do Usuário ]                                                            |
|------------------------------------------------------------------------------------|
| │                                                                                  |
| ▼                                                                                  |
| ┌─────────────────────────────────┐                                                |
| │ 1. PRÉ-RECUPERAÇÃO (Pre-Rank)   │ ➔ Query Expansion via Maritaca AI              |
| └──────────┬──────────────────────┘                                                |
| │ (Vetorização do termo expandido)                                                 |
| ▼                                                                                  |
| ┌─────────────────────────────────┐                                                |
| │ 2. RECUPERAÇÃO VETORIAL         │ ➔ Busca no Qdrant (Recupera TOP 10 candidatos) |
| └──────────┬──────────────────────┘                                                |
| │                                                                                  |
| ▼                                                                                  |
| ┌─────────────────────────────────┐                                                |
| │ 3. PÓS-RECUPERAÇÃO (Post-Rank)  │ ➔ Re-ranqueamento profundo com Cross-Encoder   |
| └──────────┬──────────────────────┘                                                |
| │ (Filtra apenas o TOP 3 definitivo)                                               |
| ▼                                                                                  |
| ┌─────────────────────────────────┐                                                |
| │ 4. COMPRESSÃO DE CONTEXTO       │ ➔ Ingestão de contexto limpo no prompt da LLM  |
| └──────────┬──────────────────────┘                                                |
| │                                                                                  |
| ▼                                                                                  |
| [ Resposta Final Otimizada ]                                                       |

### 1. Pré-recuperação (Pre-Retrieval)
- **Técnica:** *Query Expansion* (Expansão de Consulta).
- **Funcionamento:** A intenção de busca do usuário é interceptada antes de chegar ao banco. A LLM Maritaca atua como uma especialista de cinema para expandir o termo original, adicionando sinônimos, gêneros implícitos e conceitos correlacionados. Isso enriquece drasticamente o vetor de busca e evita que o banco ignore sinônimos semânticos importantes.

### 2. Pós-recuperação & Re-ranqueamento (Post-Retrieval & Re-ranking)
- **Técnica:** *Cross-Encoder Scoring* & *Context Compression*.
- **Funcionamento:** 1. O Qdrant realiza uma busca rápida (utilizando a lógica de *Bi-Encoder*) e extrai os 10 filmes mais próximos.
  2. Entra em ação o modelo **Cross-Encoder**, que analisa o par `(Pergunta Original, Payload do Filme)` de forma combinada e simultânea. Ele recalcula uma nota fina de relevância contextual.
  3. O sistema reordena a lista com base nessa nova nota. Filmes altamente relevantes que o Qdrant havia posicionado abaixo são trazidos para o topo (ex: *Solaris* assumindo o 1º lugar).
  4. Realiza-se a **Compressão de Contexto**, selecionando cirurgicamente apenas o TOP 3 definitivo, economizando tokens e blindando a LLM contra alucinações.

---

## 🔧 Configuração e Instalação

### 1. Instalar as Dependências
Abra o seu terminal dentro da pasta do projeto (certifique-se de que o seu ambiente virtual `venv` está ativo) e execute:
```bash
pip install -r requirements.txt

