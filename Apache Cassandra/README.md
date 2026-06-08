##🔍 Detalhamento Técnico Passo a Passo

1. import sys e import subprocess

•	O que faz: Importa dois módulos nativos do ecossistema Python (não requerem instalação prévia).

•	Por que é usado: * O módulo sys fornece acesso a variáveis e funções que interagem diretamente com o interpretador Python em execução.
o	O módulo subprocess permite que o script crie novos processos no sistema operacional, executando comandos de terminal diretamente de dentro do código de forma protegida.

2. subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

•	O que faz: Executa uma chamada de terminal forçada para o gerenciador de pacotes (pip) instalar a biblioteca requests.

•	A Engenharia por trás do comando:

o	sys.executable: Este é o segredo do comando. Em ambientes de desenvolvimento complexos ou IDEs (como o VSCode ou PyCharm), podem existir múltiplos interpretadores Python ou ambientes virtuais (vnvs) instalados. O sys.executable localiza o caminho exato do executável que está rodando o script naquele milissegundo.

o	"-m", "pip": Executa o pip como um módulo interno desse interpretador específico. Isso evita o erro clássico de instalar uma biblioteca globalmente no Windows, enquanto a IDE tenta ler de um ambiente isolado.

o	"check_call": Garante que o script Python seja interrompido caso a instalação falhe (por falta de internet, por exemplo), impedindo que o programa tente rodar o resto do código sem a biblioteca instalada.

3. import requests

•	O que faz: Importa a biblioteca externa responsável pelo protocolo HTTP.

•	Por que é usado: Como o DataStax Astra DB expõe o banco Apache Cassandra através de uma camada de API baseada em nuvem, a comunicação não é feita por conexões binárias tradicionais. O requests é o motor que nos permite disparar métodos HTTP como GET (buscar dados) e POST (inserir dados) em direção ao cluster NoSQL.

4. import json

•	O que faz: Importa o manipulador nativo de objetos JSON do Python.

•	Por que é usado: A linguagem de comunicação das APIs modernas do Astra DB é o JSON (JavaScript Object Notation). Este módulo é utilizado para converter dicionários nativos do Python em strings JSON formatadas para envio, bem como decodificar as respostas textuais estruturadas que retornam dos nós do Cassandra.

 Nota de Arquitetura para o Relatório

•	A inclusão deste bloco implementa o conceito de Idempotência no Setup da Aplicação. Não importa se a biblioteca requests já existe ou não na máquina do usuário: o script se autoajusta no interpretador correto antes de iniciar a camada de persistência de dados.

##💻 Documentação do Bloco: Script de Consulta Dinâmica e Interativa

Este script é responsável por criar uma interface interativa via terminal que permite ao operador buscar, de forma cirúrgica e performática, as leituras de qualquer sensor cadastrado no Apache Cassandra em uma data específica.

1. Bloco de Tratamento Resiliente de Dependências

try:
    import requests
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests
import json

•	O que faz: Tenta carregar a biblioteca requests. Se ela não estiver instalada no interpretador atual, captura a exceção (ModuleNotFoundError) e força a instalação em tempo de execução via terminal em segundo plano.

•	Importância: Garante que o script seja executado com sucesso em qualquer máquina, sem exigir que o usuário precise instalar dependências manualmente antes de testar o projeto.

2. Bloco de Configurações de Conexão e Definição de Metadados (API REST v2)

ASTRA_TOKEN = "AstraCS:..." 
BASE_URL = "https://68a5bf7f-bbf0-407b-ab3e-0a8aa6c11a2a-us-east-2.apps.astra.datastax.com"
KEYSPACE = "default_keyspace"
TABLE = "leituras_sensor"
endpoint_url = f"{BASE_URL}/api/rest/v2/keyspaces/{KEYSPACE}/{TABLE}"
headers = {
    "X-Cassandra-Token": ASTRA_TOKEN,
    "Content-Type": "application/json"
}

•	ASTRA_TOKEN: Chave de segurança gerada na organização da DataStax com a atribuição de Database Administrator. É o passaporte do código para passar pelo firewall do banco.

•	BASE_URL, KEYSPACE e TABLE: Definem as coordenadas geográficas lógicas do cluster. O Cassandra agrupa suas tabelas em Keyspaces (equivalente aos schemas do mundo SQL).

•	endpoint_url: Monta a URL exata baseada na arquitetura REST da API Stargate do Astra. Cada tabela se transforma em um recurso acessível via rota HTTP.

•	headers: O dicionário de cabeçalhos injeta o Token de autenticação no campo proprietário X-Cassandra-Token e especifica que a aplicação trafegará dados puramente no formato JSON.

3. Bloco de Captura de Dados Dinâmicos (Interface de Usuário)

print("=" * 50)
print("🔍 SISTEMA DE CONSULTA DE TELEMETRIA NOSQL")
print("=" * 50)
sensor_escolhido = input("Digite o ID do Sensor (ex: sensor-001, sensor-003): ").strip()
data_escolhida = input("Digite a Data da Leitura (padrão AAAA-MM-DD, ex: 2026-05-22): ").strip()

•	O que faz: Imprime um menu visual limpo e suspende a execução do programa para capturar os inputs do usuário via teclado. O método .strip() é aplicado ao final para remover automaticamente quaisquer espaços em branco que o usuário digite acidentalmente no início ou no fim dos textos.

4. Bloco de Construção da Query NoSQL (Parâmetros Dinâmicos)

query_params = {
    "where": json.dumps({
        "sensor_id": {"$eq": sensor_escolhido},
        "data_leitura": {"$eq": data_escolhida}
    }),
    "page-size": 10
}

•	O que faz: Cria os parâmetros de URL que guiarão a filtragem do banco.

•	A Engenharia por trás: * A API REST do Astra DB exige que o filtro de busca (where) seja passado como uma string contendo um JSON válido de operadores. Por isso, usamos o json.dumps() para transformar o dicionário Python em uma string JSON estruturada.

o	O operador {"$eq": ...} simula o comportamento do operador de igualdade (=) do SQL tradicional.

o	Chave Primária Obrigatória: Note que o script exige o sensor_id e a data_leitura. No Cassandra, estes dois campos formam a Chave de Partição. Sem passar ambos, a API negará a busca por motivos de performance, pois o Cassandra proíbe varreduras completas (Full Table Scans) em tabelas distribuídas em produção.

o	page-size: 10: Limita o retorno da API a no máximo 10 registros por página, protegendo a memória RAM da aplicação.

5. Bloco de Consumo HTTP e Tratamento de Respostas

try:
    response = requests.get(endpoint_url, headers=headers, params=query_params)

•	O que faz: Dispara um pedido HTTP do tipo GET contendo os cabeçalhos de segurança e os parâmetros de filtragem anexados na URL direcionada para a AWS (região us-east-2).

    if response.status_code == 200:
        dados = response.json()
        registros = dados.get("data", [])
        if registros:
            print(f"✅ Sucesso! Foram encontradas {dados.get('count')} leituras.")
            print("\n--- RESULTADO DA FILTRAGEM ---")
            for reg in registros:
                print(f"Horário: {reg.get('horario')} | "
                      f"Temp: {reg.get('temperatura')}°C | "
                      f"Umidade: {reg.get('umidade')}% | "
                      f"Status: {reg.get('status')}")

•	Tratamento do Código 200: Se o servidor responder com status 200 (Sucesso absoluto), o script converte a string bruta do JSON retornado em um dicionário Python utilizável via response.json(). Ele varre a lista contida dentro do nó "data" e formata as colunas de telemetria de forma legível na tela.

        else:
            print("⚠️ Nenhuns dados encontrados para este Sensor nesta Data específica.")

•	Tratamento de Lista Vazia: Caso a conexão seja perfeita, mas o sensor digitado não possua leituras na data informada, o sistema alerta o usuário em vez de quebrar ou exibir uma tela em branco.

    elif response.status_code == 401:
        print("❌ Erro de Autenticação: O Token fornecido foi rejeitado.")
    else:
        print(f"❌ Erro na API (Código HTTP {response.status_code}): {response.text}")
except Exception as e:
    print(f"❌ Erro crítico de comunicação: {e}")

•	Tratamento de Erros de Infraestrutura: O script mapeia os erros de escopo. Se retornar 401, o desenvolvedor sabe imediatamente que o problema está no token. Qualquer outro erro (como o 400 se o Keyspace sumir) ou falhas de falta de internet (except Exception) são capturados e impressos de forma amigável, impedindo o travamento abrupto do software.

##💻 Documentação do Bloco: Script de Inserção Dinâmica e Lançamento de Dados

Este script implementa uma interface interativa via terminal responsável por simular o comportamento de um dispositivo IoT ou de um operador de data center, coletando métricas em tempo real e realizando a persistência imediata (ingestão) no ecossistema distribuído do Apache Cassandra.

1. Bloco de Importação e Gerenciamento de Data/Hora

from datetime import datetime

•	O que faz: Importa a classe datetime do módulo nativo do Python.

•	Por que é usado: O Apache Cassandra exige uma formatação cronológica estrita para colunas do tipo timestamp e date. Essa biblioteca é o componente que gera as strings temporais padronizadas automaticamente a partir do relógio interno do sistema operacional.

2. Bloco de Entrada e Validação Dinâmica de Tipos (Sanitização)

sensor_id = input("Introduza o ID do Sensor (ex: sensor-004): ").strip()
try:
    temperatura = float(input("Introduza a Temperatura (°C - ex: 26.8): "))
    umidade = float(input("Introduza a Humidade (% - ex: 55.4): "))
except ValueError:
    print("❌ Erro: Temperatura e Humidade devem ser valores numéricos (use ponto em vez de vírgula).")
    sys.exit()
status = input("Introduza o Status (OK, ALERTA, CRÍTICO): ").strip().upper()

•	O que faz: Solicita as métricas do sensor e as sanitiza antes de trafegar pela rede.

•	A Engenharia por trás:

o	float(): Força a conversão das strings digitadas para números de ponto flutuante. Bancos relacionais ou NoSQL tipados rejeitam strings textuais em colunas numéricas.

o	try / except ValueError: Captura falhas de digitação (ex: digitar uma vírgula ou uma letra no lugar do ponto decimal). Se ocorrer o erro, o programa aborta com sys.exit() de forma graciosa, poupando processamento e evitando o envio de dados corrompidos para a API.

o	.upper(): Padroniza a string de status em letras maiúsculas, mantendo a consistência conceitual dos metadados gravados no Cassandra.

3. Bloco de Geração Automática do Padrão Temporal ISO 8601

data_atual = datetime.utcnow().strftime("%Y-%m-%d")
horario_atual = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

•	O que faz: Captura o tempo no padrão UTC (Tempo Universal Coordenado) e o formata como texto legível para o banco.

•	A Engenharia por trás: * O método utcnow() é uma excelente prática na arquitetura de sistemas distribuídos. Em vez de usar a hora local da máquina do usuário, ele adota o fuso horário global (Zero absoluto de Greenwich / Zulu Time), o que evita conflitos cronológicos caso múltiplos servidores ao redor do mundo gravem dados simultaneamente.

o	O formato "%Y-%m-%dT%H:%M:%SZ" injeta a letra T (separador de tempo) e a letra Z (marcador de fuso UTC), atendendo perfeitamente ao formato ISO 8601 exigido internamente pelo gateway Stargate do Astra DB para deserializar colunas do tipo timestamp.

4. Bloco de Estruturação do Payload JSON

novo_registro = {
    "sensor_id": sensor_id,
    "data_leitura": data_atual,
    "horario": horario_atual,
    "temperatura": temperatura,
    "umidade": umidade,
    "status": status
}

•	O que faz: Consolida todas as variáveis capturadas e validadas em uma estrutura de dicionário Python de documento único, mapeando chaves cujos nomes correspondem exatamente aos nomes das colunas mapeadas na tabela do Cassandra.

5. Bloco de Persistência via Protocolo HTTP POST e Confirmação de Escrita

try:
    response = requests.post(endpoint_url, headers=headers, json=novo_registro)

•	O que faz: Dispara um método de escrita POST em direção à URL da tabela. Os dados do dicionário são injetados diretamente no corpo da requisição (body) serializados como JSON.

    if response.status_code in [200, 201]:
        print("\n✅ SUCESSO! Os dados foram lançados e replicados no Cassandra!")

•	A Engenharia por trás: A API REST do Astra DB responde com os códigos de status HTTP 201 (Created) ou 200 (OK) assim que o cluster recebe o payload. Diferente do mundo SQL clássico, o Cassandra não valida a existência prévia de chaves estrangeiras ou relacionamentos complexos, executando a operação de escrita de forma assíncrona ultra rápida na memória RAM (Memtable) do nó coordenador.

    else:
        print(f"\n❌ Falha no Lançamento (Código HTTP {response.status_code})")
        print(f"Mensagem do Astra: {response.text}")

•	Tratamento de Exceções de Negócio: Se houver erros como formato de data quebrado (HTTP 400), credencial de token inválida (HTTP 401) ou Keyspace incorreto, o script captura e expõe a mensagem oficial devolvida pelo servidor, acelerando o processo de auditoria e manutenção de código do desenvolvedor.

