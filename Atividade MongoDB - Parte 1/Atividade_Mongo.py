from pymongo import MongoClient
import pandas as pd

# 1. Conexão Local
uri = "mongodb://localhost:27017"
client = MongoClient(uri)

# 2. AJUSTE TÉCNICO: Onde os dados realmente estão
db = client['local']   # Banco encontrado na varredura
colecao = db['Vendas'] # Nome exato com 'V' maiúsculo

try:
    # 3. Recuperação e Exibição
    cursor = colecao.find({"Item_Type": "Soft Drinks"}).limit(5)
    df = pd.DataFrame(list(cursor))
    
    if df.empty:
        print("Erro inesperado: a coleção foi encontrada mas o DataFrame está vazio.")
    else:
        # Removemos o _id para limpar a tabela
        if '_id' in df.columns:
            df = df.drop(columns=['_id'])
            
        # Configura o Pandas para não esconder colunas e ajustar a largura
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        pd.set_option('display.colheader_justify', 'center')

        print("\n" + "="*110)
        print("RELATÓRIO DE VENDAS - BIG MART SALES".center(110))
        print("="*110)
        
        # Exibe o DataFrame formatado
        print(df.to_string(index=False))
        
        print("="*110)
        print(f"Total de registros na base: {total_documentos} | Amostra: 5 registros".center(110))

except Exception as e:
    print(f"Erro ao processar: {e}")

finally:
    client.close()