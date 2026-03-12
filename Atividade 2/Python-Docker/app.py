from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulação de um Banco de Dados NoSQL (Documentos JSON)
db_nosql = [
    {"id": 1, "item": "Servidor Cloud", "status": "ativo"},
    {"id": 2, "item": "Cluster Cassandra", "status": "pendente"}
]

@app.route("/")
def home():
    return "API NoSQL rodando com sucesso no Docker!"

@app.route("/documentos", methods=["GET"])
def listar():
    return jsonify(db_nosql)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)