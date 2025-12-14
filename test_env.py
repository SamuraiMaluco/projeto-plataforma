import os

print("--- DIAGNÓSTICO DO AMBIENTE ---")
pasta_atual = os.getcwd()
print(f"1. Pasta onde o Python está rodando: {pasta_atual}")

arquivos = os.listdir(pasta_atual)
print(f"2. Arquivos encontrados nesta pasta: {arquivos}")

if '.env' in arquivos:
    print("3. SUCESSO: O arquivo .env foi encontrado!")
    with open('.env', 'r') as f:
        print(f"4. Conteúdo do .env: {f.read()}")
else:
    print("3. FALHA: O arquivo .env NÃO está nesta lista. Verifique se o nome não é .env.txt")
print("-------------------------------")