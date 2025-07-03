import sqlite3

# Criação do banco e tabela
conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    data TEXT NOT NULL
)
''')
conexao.commit()
conexao.close()


def adicionar_transacao(tipo):
    descricao = input("Descrição: ")
    valor = float(input("Valor: "))
    data = input("Data (YYYY-MM-DD): ")

    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO transacoes (tipo, descricao, valor, data)
        VALUES (?, ?, ?, ?)
    ''', (tipo, descricao, valor, data))
    conexao.commit()
    conexao.close()
    print(f"{tipo.capitalize()} adicionada com sucesso!\n")


def listar_transacoes():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM transacoes ORDER BY data")
    transacoes = cursor.fetchall()

    if len(transacoes) == 0:
        print("Nenhuma transação encontrada.")
    else:
        print("\n--- Transações ---")
        for t in transacoes:
            print(f"[{t[0]}] {t[3]:.2f} - {t[1].capitalize()} - {t[2]} ({t[4]})")

    conexao.close()


def mostrar_saldo():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo='receita'")
    total_receitas = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo='despesa'")
    total_despesas = cursor.fetchone()[0] or 0

    saldo = total_receitas - total_despesas
    print(f"\n💰 Saldo atual: R$ {saldo:.2f}")
    conexao.close()


# 🧭 MENU PRINCIPAL
while True:
    print("\n--- MENU FINANCEIRO ---")
    print("1. Adicionar receita")
    print("2. Adicionar despesa")
    print("3. Listar transações")
    print("4. Mostrar saldo atual")
    print("0. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        adicionar_transacao("receita")
    elif opcao == "2":
        adicionar_transacao("despesa")
    elif opcao == "3":
        listar_transacoes()
    elif opcao == "4":
        mostrar_saldo()
    elif opcao == "0":
        print("Saindo...")
        break
    else:
        print("Opção inválida. Tente novamente.")
