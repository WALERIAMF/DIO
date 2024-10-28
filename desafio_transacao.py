from datetime import date


class Transacao:
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
            return True
        return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao):
        self.transacoes.append(descricao)

    def exibir(self):
        if not self.transacoes:
            return "Sem movimentações."
        return "\n".join(self.transacoes)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao: Transacao):
        if transacao.registrar(conta):
            print("Transação realizada com sucesso!")
        else:
            print("Falha na transação.")

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

class Conta:
    AGENCIA = "0001"

    def __init__(self, numero, cliente: Cliente):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = Conta.AGENCIA
        self.cliente = cliente
        self.historico = Historico()
        cliente.contas.append(self)

    def exibir_saldo(self):
        return self.saldo

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self.historico.adicionar_transacao(f"Saque: R$ {valor:.2f}")
            return True
        return False

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

class ContaCorrente(Conta):
    LIMITE_SAQUES = 3
    LIMITE_SAQUE_VALOR = 500.0

    def __init__(self, numero, cliente: Cliente, limite=LIMITE_SAQUE_VALOR, limite_saques=LIMITE_SAQUES):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_realizados = 0

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > self.limite:
            print("Excede o limite de saque.")
        elif self.saques_realizados >= self.limite_saques:
            print("Número máximo de saques atingido.")
        elif valor > 0:
            self.saldo -= valor
            self.saques_realizados += 1
            self.historico.adicionar_transacao(f"Saque: R$ {valor:.2f}")
            return True
        return False

def main():
    clientes = []
    contas = []

    while True:
        menu = """
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [u] Criar Usuário
        [c] Criar Conta Corrente
        [q] Sair
        => """
        
        opcao = input(menu).lower()

        if opcao == "u":
            cpf = input("CPF (somente números): ")
            if any(cliente.cpf == cpf for cliente in clientes):
                print("CPF já cadastrado!")
                continue
            
            nome = input("Nome completo: ")
            endereco = input("Endereço (logradouro, número, bairro, cidade/sigla estado): ")
            data_nascimento = input("Data de nascimento (aaaa-mm-dd): ")
            cliente = PessoaFisica(nome, cpf, date.fromisoformat(data_nascimento), endereco)
            clientes.append(cliente)
            print("Usuário cadastrado com sucesso!")

        elif opcao == "c":
            cpf = input("Informe o CPF do usuário: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            
            if cliente:
                numero_conta = len(contas) + 1
                conta = ContaCorrente(numero_conta, cliente)
                contas.append(conta)
                print(f"Conta {numero_conta} criada para o usuário {cliente.nome}!")
            else:
                print("Usuário não encontrado. Crie o usuário primeiro.")

        elif opcao == "d":
            numero_conta = int(input("Número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            
            if conta:
                valor = float(input("Valor do depósito: "))
                conta.depositar(valor)

        elif opcao == "s":
            numero_conta = int(input("Número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)

            if conta:
                valor = float(input("Valor do saque: "))
                conta.sacar(valor)

        elif opcao == "e":
            numero_conta = int(input("Número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)

            if conta:
                print("\n=== EXTRATO ===")
                print(conta.historico.exibir())
                print(f"Saldo: R$ {conta.exibir_saldo():.2f}")
                print("================")
            else:
                print("Conta não encontrada.")

        elif opcao == "q":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida!")

main()
