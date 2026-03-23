import json
import random

nomes = ["Ana", "Bruno", "Carla", "Diego", "Elena", "Fabio", "Gisele", "Hugo", "Iara", "João", "Karina", "Lucas", "Marina", "Nuno", "Olivia", "Paulo", "Raquel", "Samuel", "Tatiana", "Vitor"]
sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira", "Costa", "Ferreira", "Rodrigues", "Almeida", "Nascimento"]
cargos = ["Desenvolvedor", "Analista", "Gerente", "Coordenador", "Designer", "Estagiário"]
setores = ["TI", "RH", "Financeiro", "Marketing", "Operações", "Vendas"]

dados = []

for i in range(1, 101):
    nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
    email = f"{nome_completo.lower().replace(' ', '.')}@empresa.com"
    
    documento = {
        "nome": nome_completo,
        "idade": random.randint(20, 60),
        "email": email,
        "cargo": random.choice(cargos),
        "salario": round(random.uniform(3000, 15000), 2),
        "setor": random.choice(setores)
    }
    dados.append(documento)

# Guarda o ficheiro para importar no MongoDB
with open('funcionarios.json', 'w', encoding='utf-8') as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)

print("Ficheiro 'funcionarios.json' criado com 100 documentos!")