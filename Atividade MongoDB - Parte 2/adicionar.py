# Importação das bibliotecas necessárias
import random

import requests # Para fazer requisições HTTP e obter dados de uma API
import pymongo # Para interagir com o banco de dados MongoDB
# Conectar ao MongoDB
# Criamos um cliente para acessar o servidor MongoDB local na porta padrão (27017)
client = pymongo.MongoClient("mongodb://localhost:27017/")
# Selecionamos o banco de dados chamado &quot;startup&quot;
db = client["Empresa_RH"]
# Escolhemos a coleção (equivalente a uma tabela em bancos relacionais) chamada "funcionarios"
collection = db["funcionarios"]
# URL da API que fornece dados de usuários aleatórios
# O parâmetro &quot;results=10&quot; indica que queremos obter 10 usuários
# O parâmetro &quot;nat=br&quot; faz com que os usuários sejam de nacionalidade brasileira
url = "https://randomuser.me/api/?results=10&amp;nat=br"
# Fazemos uma requisição GET para a API e obtemos os dados no formato JSON
response = requests.get(url).json()
# Criamos uma lista para armazenar os funcionários processados antes de inseri-los no MongoDB
funcionarios = []
# Percorremos cada usuário retornado pela API
for user in response["results"]:
# Extraímos os dados necessários e organizamos em um dicionário
    funcionarios.append({
    "nome": f"{user['name']['first']} {user['name']['last']}", # Nome completo do funcionário
    "idade": user['dob']['age'], # Idade do funcionário
    "email": user['email'], # Email do funcionário
    "cargo": "Desenvolvedor", # Cargo fixo para todos os funcionários
    "salario": round(random.uniform(3000, 15000), 2), # Salário aleatório entre 3000 e 15000
    "setor": "TI" # Setor fixo para todos os funcionários
})
# Inserimos a lista de funcionários no MongoDB usando insert_many
collection.insert_many(funcionarios)
# Mensagem indicando que os dados foram inseridos com sucesso no banco de dados
print("Funcionários inseridos no MongoDB com sucesso!")
      


