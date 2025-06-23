import datetime
import textwrap

def data_atual():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def menu():
    menu_texto = """\n
    ================ MENU ================
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Usuários/Contas
    [0] Sair
    => """
    return input(textwrap.dedent(menu_texto))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append(f"[{data_atual()}] Depósito:\tR$ {valor:.2f}")
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nOperação falhou! O valor informado é inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Saldo insuficiente.")
    elif excedeu_limite:
        print("\nOperação falhou! Valor excede o limite.")
    elif excedeu_saques:
        print("\nOperação falhou! Limite de saques diários excedido.")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"[{data_atual()}] Saque:\t\tR$ {valor:.2f}")
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\nOperação falhou! Valor inválido.")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    if extrato:
        for linha in extrato:
            print(linha)
    else:
        print("Nenhuma movimentação realizada.")
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\nJá existe um usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\nUsuário criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [u for u in usuarios if u["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario
        }

    print("\nUsuário não encontrado! Criação de conta cancelada.")

def listar_contas(contas):
    print("\n========= LISTA DE CONTAS =========")
    for conta in contas:
        linha = f"""
            Agência:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 40)
        print(textwrap.dedent(linha))

def gerenciar_usuarios_e_contas(usuarios, contas, agencia):
    submenu = """\n
    ======== SUBMENU USUÁRIO/CONTA ========
    [1] Novo usuário
    [2] Nova conta
    [3] Listar contas
    [0] Voltar
    => """
    while True:
        opcao = input(textwrap.dedent(submenu))

        if opcao == "1":
            criar_usuario(usuarios)
        elif opcao == "2":
            numero_conta = len(contas) + 1
            conta = criar_conta(agencia, numero_conta, usuarios)
            if conta:
                contas.append(conta)
        elif opcao == "3":
            listar_contas(contas)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3
    LIMITE_VALOR_SAQUE = 500.00

    saldo = 0.0
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            try:
                valor = float(input("Informe o valor para depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except ValueError:
                print("\nEntrada inválida!")

        elif opcao == "2":
            try:
                valor = float(input("Informe o valor para saque: "))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=LIMITE_VALOR_SAQUE,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES
                )
            except ValueError:
                print("\nEntrada inválida!")

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            gerenciar_usuarios_e_contas(usuarios, contas, AGENCIA)

        elif opcao == "0":
            print("\nSaindo do sistema... Até logo!")
            break

        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
