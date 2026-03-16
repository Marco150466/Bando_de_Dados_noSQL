import redis  
import time   
import base64  

# Conexão com o Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# ALTO DESEMPENHO
print("=== Testando Alto Desempenho ===")
start_time = time.time()  
redis_client.set("chave_teste", "valor_teste")
retrieved_value = redis_client.get("chave_teste")
end_time = time.time()  
print(f"Valor armazenado: {retrieved_value}")  
print(f"Tempo de execução: {end_time - start_time:.6f} segundos\n")

# ESCALABILIDADE
print("=== Testando Escalabilidade ===")
# Reduzi para 1000 para ser mais rápido no seu teste local
for i in range(1000):  
    redis_client.set(f"chave_{i}", f"valor_{i}")
print(f"Exemplo de valor armazenado: {redis_client.get('chave_500')}\n")

# FLEXIBILIDADE
print("=== Testando Flexibilidade ===")
# 1. String
redis_client.set("string_exemplo", "Hello Redis!")
print(f"String armazenada: {redis_client.get('string_exemplo')}")

# 2. Lista
# Limpa a lista antes de adicionar para não acumular itens de execuções anteriores
redis_client.delete("lista_exemplo") 
redis_client.rpush("lista_exemplo", "item1", "item2", "item3")
print(f"Lista armazenada: {redis_client.lrange('lista_exemplo', 0, -1)}")

# 3. Hash
redis_client.hset("hash_exemplo", "campo1", "valor1")
redis_client.hset("hash_exemplo", "campo2", "valor2")
print(f"Hash armazenado: {redis_client.hgetall('hash_exemplo')}")

# 4. Dados Binários (Base64)
image_data = base64.b64encode(b"imagem_em_binario_simulada").decode("utf-8")
redis_client.set("imagem_binario", image_data)
print(f"Imagem (binário): {redis_client.get('imagem_binario')[:20]}... [Cortado]\n")

# BAIXA LATÊNCIA
print("=== Testando Baixa Latência ===")
redis_client.set("configuracao_cache", "config_inicial")
for _ in range(5):
    start = time.time()
    cache_value = redis_client.get("configuracao_cache")
    print(f"Cache acessado: {cache_value} | Tempo: {time.time() - start:.6f} segundos")

print("\nTeste concluído com sucesso!")