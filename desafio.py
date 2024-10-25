menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar Usuário
[c] Criar Conta Corrente
[q] Sair

=> """

usuarios = []
contas = []
AGENCIA = "0001"
LIMITE_SAQUES = 3
limite_saque_valor = 500

def criar_usuario():
    cpf = input("CPF (somente números): ")
    if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("CPF já cadastrado!")
        return

    nome = input("Nome completo: ")
    endereco = input("Endereço (logradouro, número, bairro, cidade/sigla estado): ")
    usuarios.append({"cpf": cpf, "nome": nome, "endereco": endereco})
    print("Usuário cadastrado com sucesso!")

def criar_conta_corrente():
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)
    
    if usuario:
        numero_conta = len(contas) + 1
        contas.append({"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "", "saques": 0})
        print(f"Conta {numero_conta} criada para o usuário {usuario['nome']}!")
    else:
        print("Usuário não encontrado. Crie o usuário primeiro.")

def realizar_deposito():
    numero_conta = int(input("Número da conta: "))
    conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)
    
    if conta:
        valor = float(input("Valor do depósito: "))
        if valor > 0:
            conta["saldo"] += valor
            conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido!")
    else:
        print("Conta não encontrada.")

def realizar_saque():
    numero_conta = int(input("Número da conta: "))
    conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

    if conta:
        valor = float(input("Valor do saque: "))
        if valor > conta["saldo"]:
            print("Saldo insuficiente.")
        elif valor > limite_saque_valor:
            print("Excede o limite de saque.")
        elif conta["saques"] >= LIMITE_SAQUES:
            print("Número máximo de saques atingido.")
        elif valor > 0:
            conta["saldo"] -= valor
            conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
            conta["saques"] += 1
            print("Saque realizado!")
        else:
            print("Valor inválido!")
    else:
        print("Conta não encontrada.")

def exibir_extrato():
    numero_conta = int(input("Número da conta: "))
    conta = next((conta for conta in contas if conta["numero_conta"] == numero_conta), None)

    if conta:
        print("\n=== EXTRATO ===")
        print("Sem movimentações." if not conta["extrato"] else conta["extrato"])
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("================")
    else:
        print("Conta não encontrada.")

while True:
    opcao = input(menu)

    if opcao == "d":
        realizar_deposito()
    elif opcao == "s":
        realizar_saque()
    elif opcao == "e":
        exibir_extrato()
    elif opcao == "u":
        criar_usuario()
    elif opcao == "c":
        criar_conta_corrente()
    elif opcao == "q":
        break
    else:
        print("Opção inválida!")
