import cx_Oracle
import pandas as pd
import joblib

# =============================
# CONFIGURAÇÃO DE CONEXÃO ORACLE
# =============================
username = "RM562317"
password = "100598"
dsn = "oracle.fiap.com.br/orcl"

# =============================
# CLASSIFICADOR DE STATUS
# =============================
def classificar_status(temp):
    return "ALERTA DE CALOR" if temp >= 37 else "NORMAL"

# =============================
# CONECTAR AO BANCO
# =============================
try:
    connection = cx_Oracle.connect(username, password, dsn)
    cursor = connection.cursor()
    print("[✓] Conectado ao banco Oracle.")
except cx_Oracle.DatabaseError as e:
    print("Erro ao conectar ao banco:", e)
    exit()

# =============================
# MENU COMPLETO
# =============================
def ler_tudo():
    cursor.execute("SELECT * FROM monitoramento_calor ORDER BY id")
    registros = cursor.fetchall()
    print("\n=== MONITORAMENTO DE CALOR ===")
    for r in registros:
        print(f"id: {r[0]} | Temp: {r[1]:.2f} °C | Umid: {r[2]:.1f}% | Pressão: {r[3]:.1f} mB | Status: {r[4]}")
    print("--------------------------------")

def criar_registro():
    try:
        temperatura = float(input("Temperatura (°C): "))
        umidade = float(input("Umidade (%): "))
        pressao = float(input("Pressão (mB): "))

        if temperatura < -10 or temperatura > 60:
            print("Temperatura fora do intervalo aceitável.")
            return
        if umidade < 0 or umidade > 100:
            print("Umidade inválida.")
            return
        if pressao < 850 or pressao > 1050:
            print("Pressão fora do intervalo esperado.")
            return

        status = classificar_status(temperatura)
        cursor.execute("""
            INSERT INTO monitoramento_calor (temperatura, umidade, pressao, status)
            VALUES (:1, :2, :3, :4)
        """, (temperatura, umidade, pressao, status))
        connection.commit()
        print("[✓] Registro inserido.")
    except ValueError:
        print("Erro: entrada inválida.")

def atualizar():
    ler_tudo()
    try:
        id_registro = int(input("ID do registro a atualizar: "))
        temperatura = float(input("Nova temperatura (°C): "))
        umidade = float(input("Nova umidade (%): "))
        pressao = float(input("Nova pressão (mB): "))
        status = classificar_status(temperatura)

        cursor.execute("""
            UPDATE monitoramento_calor
            SET temperatura = :1, umidade = :2, pressao = :3, status = :4
            WHERE id = :5
        """, (temperatura, umidade, pressao, status, id_registro))
        connection.commit()
        print("[✓] Registro atualizado.")
    except ValueError:
        print("Erro na entrada.")

def deletar():
    ler_tudo()
    try:
        id_registro = int(input("ID do registro a excluir: "))
        cursor.execute("DELETE FROM monitoramento_calor WHERE id = :1", (id_registro,))
        connection.commit()
        print("[✓] Registro removido.")
    except ValueError:
        print("ID inválido.")

# =============================
# PREVER TEMPERATURA DE AMANHÃ (ML)
# =============================
def prever_temperatura_amanha():
    try:
        umidade = float(input("Umidade (%): "))
        pressao = float(input("Pressão (mB): "))
        temp_atual = float(input("Temperatura atual (°C): "))

        if pressao < 860 or pressao > 900:
            print("[!] Pressão fora do intervalo aceitável (860 a 900 mB).")
            return

        modelo = joblib.load("modelo_previsao_treinado_3variaveis.pkl")
        entrada = pd.DataFrame([[temp_atual, umidade, pressao]], columns=["temp_atual", "umidade", "pressao"])

        previsao = modelo.predict(entrada)[0]
        status = classificar_status(previsao)

        print("\n=== PREVISÃO COM ML ===")
        print(f"Temperatura prevista para amanhã: {previsao:.2f} °C → {status}")
        print("\n(Dados usados para previsão NÃO foram gravados no banco de dados.)")

    except Exception as e:
        print("Erro na previsão:", e)

# =============================
# MENU
# =============================
def menu():
    while True:
        print("\n===== MONITORAMENTO DE CALOR =====")
        print("1 - Ver registros")
        print("2 - Inserir novo registro")
        print("3 - Atualizar registro")
        print("4 - Deletar registro")
        print("5 - Prever temperatura de amanhã (ML)")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            ler_tudo()
        elif opcao == "2":
            criar_registro()
        elif opcao == "3":
            atualizar()
        elif opcao == "4":
            deletar()
        elif opcao == "5":
            prever_temperatura_amanha()
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

    cursor.close()
    connection.close()
    print("[✓] Conexão encerrada.")

# =============================
# EXECUTAR O PROGRAMA
# =============================
if __name__ == "__main__":
    menu()
