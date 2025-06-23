import datetime

saldo = 0.0
limite_saque = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES_DIARIOS = 3

def menu():
    print("\n--- MENU ---")
    print("1 - Depositar")
    print("2 - Sacar")
    print("3 - Extrato")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def depositar(valor):
    global saldo, extrato
    if valor > 0:
        saldo += valor
        extrato += f"[{data_atual()}] Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso.")
    else:
        print("Valor inválido para depósito.")

def sacar(valor):
    global saldo, extrato, numero_saques
    if numero_saques >= LIMITE_SAQUES_DIARIOS:
        print("Limite diário de saques atingido.")
    elif valor > limite_saque:
        print("Valor excede o limite por saque.")
    elif valor > saldo:
        print("Saldo insuficiente.")
    elif valor <= 0:
        print("Valor inválido para saque.")
    else:
        saldo -= valor
        extrato += f"[{data_atual()}] Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso.")

def mostrar_extrato():
    print("\n--- EXTRATO ---")
    print(extrato if extrato else "Nenhuma movimentação.")
    print(f"Saldo atual: R$ {saldo:.2f}")

def data_atual():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

while True:
    opcao = menu()
    if opcao == "1":
        try:
            valor = float(input("Informe o valor do depósito: "))
            depositar(valor)
        except ValueError:
            print("Entrada inválida.")
    elif opcao == "2":
        try:
            valor = float(input("Informe o valor do saque: "))
            sacar(valor)
        except ValueError:
            print("Entrada inválida.")
    elif opcao == "3":
        mostrar_extrato()
    elif opcao == "0":
        print("Saindo do sistema. Até mais!")
        break
    else:
        print("Opção inválida.")
