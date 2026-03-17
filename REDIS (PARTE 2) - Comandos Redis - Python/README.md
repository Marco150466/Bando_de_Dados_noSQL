
# Atividade: Persistência de Dados e Performance com Redis (NoSQL)

Este projeto demonstra a integração entre **Python** e o banco de dados não relacional **Redis**, focando em quatro pilares fundamentais de sistemas de alto desempenho.

## 🚀 Funcionalidades Demonstradas

O código desenvolvido realiza testes automatizados para validar as seguintes características do Redis:

* 
**Alto Desempenho:** Medição do tempo de resposta para operações simples de escrita (`SET`) e leitura (`GET`).


* 
**Escalabilidade:** Simulação de carga com o armazenamento massivo de chaves para observar o comportamento do banco sob estresse.


* **Flexibilidade de Dados:** Demonstração de que o Redis suporta múltiplos tipos de estruturas, incluindo:
* 
**Strings:** Textos simples.


* 
**Lists:** Coleções ordenadas de itens.


* 
**Hashes:** Estruturas de mapeamento objeto-valor.


* 
**Dados Binários (Base64):** Armazenamento de arquivos ou imagens convertidos em texto.




* 
**Baixa Latência:** Uso do Redis como camada de cache para acesso ultrarrápido a configurações e dados recorrentes.



## 🛠️ Tecnologias Utilizadas

* 
**Python 3.11+**.


* 
**Redis Server** (Rodando localmente na porta 6379).


* 
**Bibliotecas Python:** `redis`, `time`, `base64`.



## 📋 Como Executar

1. Certifique-se de que o servidor Redis está ativo (`redis-server.exe`).
2. Execute o script principal:
```bash
python teste_redis.py

```


3. Verifique os logs no terminal confirmando o sucesso das operações e os tempos de execução.



