import os
import platform
from abc import ABC, abstractmethod
from datetime import datetime

# Função para limpar o terminal dependendo do sistema operacional
def limpar_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Função para pausar o programa até que o usuário pressione Enter
def pausa():
    input("Pressione Enter para voltar ao menu.")
    limpar_terminal()

# Função para exibir o menu principal do banco
def mensagem():
    print(""" 
    =================================
    =========BANCO DO LELÉU==========
    
      QUAL OPERAÇÃO DESEJA REALIZAR?
      
      [1] EXTRATO
      [2] SAQUE
      [3] DEPÓSITO
      [4] NOVA LELEU CONTA
      [5] LISTAR LELEU CONTAS
      [6] NOVO LELEU USUARIO
      [0] SAIR

    =================================
    """)

# Classe representando um cliente genérico do banco
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    # Função para realizar uma transação em uma conta específica
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    # Função para adicionar uma nova conta ao cliente
    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Classe representando um cliente pessoa física, herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe representando uma conta bancária genérica
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    # Método de classe para criar uma nova conta
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    # Propriedades para acessar os atributos privados
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # Função para sacar um valor da conta
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            limpar_terminal()
            print("\nVOCÊ NÃO TEM SALDO SUFICIENTE")
            pausa()
        elif valor > 0:
            self._saldo -= valor
            limpar_terminal()
            print("\nSAQUE FEITO!")
            pausa()
            return True
        else:
            limpar_terminal()
            print("\nVALOR INVÁLIDO!!!")
            pausa()
        return False

    # Função para depositar um valor na conta
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            limpar_terminal()
            print("\nDEPÓSITO FEITO!")
            pausa()
        else:
            limpar_terminal()
            print("\nVALOR INVÁLIDO!")
            pausa()
            return False
        return True

# Classe representando uma conta corrente, herda de Conta
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    # Função para sacar um valor da conta corrente, considerando limite e número de saques
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            limpar_terminal()
            print("\nVALOR DO SAQUE EXCEDE O LIMITE")
            pausa()
        elif excedeu_saques:
            limpar_terminal()
            print("\nNUMERO MAXIMO DE SAQUES EXCEDIDO!!!")
            pausa()
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Classe para manter o histórico de transações de uma conta
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    # Função para adicionar uma transação ao histórico
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

# Classe abstrata representando uma transação
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

# Classe representando uma transação de saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Classe representando uma transação de depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Função para consultar o extrato de uma conta
def consultar_extrato(conta):
    limpar_terminal()
    print("EXTRATO:")
    for transacao in conta.historico.transacoes:
        print(f"{transacao['data']} - {transacao['tipo']}: {transacao['valor']:.2f}")
    print(f"\nSaldo atual: {conta.saldo:.2f}")
    pausa()

# Função para realizar um saque em uma conta
def realizar_saque(conta):
    limpar_terminal()
    while True:
        try:
            valor_saque = float(input("QUAL VALOR DESEJA SACAR? "))
            saque = Saque(valor_saque)
            conta.cliente.realizar_transacao(conta, saque)
            pausa()
            return
        except ValueError:
            limpar_terminal()
            print("ENTRADA INVALIDA!!!")

# Função para realizar um depósito em uma conta
def realizar_deposito(conta):
    limpar_terminal()
    while True:
        try:
            valor_deposito = float(input("QUAL VALOR DESEJA DEPOSITAR EM SUA LELÉU CONTA? "))
            deposito = Deposito(valor_deposito)
            conta.cliente.realizar_transacao(conta, deposito)
            pausa()
            return
        except ValueError:
            limpar_terminal()
            print("ENTRADA INVÁLIDA!!!")

# Função para sair do sistema
def sair():
    limpar_terminal()
    print("TENHA UM LELÉU DIA! :)\n.\n.\n.\n.")

# Função para filtrar um cliente pelo CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função para recuperar a conta de um cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        limpar_terminal()
        print("\nCLIENTE NÃO POSSUI UMA LELEU CONTA!!!")
        pausa()
        return
    return cliente.contas[0]

# Função para realizar um depósito a partir de uma lista de clientes
def depositar(clientes):
    limpar_terminal()
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        limpar_terminal()
        print("\nCLIENTE NÃO ENCONTRADO!!!")
        pausa()
        return

    valor = None
    while valor is None:
        try:
            valor = float(input("QUANTO DESEJA DEPOSITAR EM SUA LELEU CONTA? "))
        except ValueError:
            limpar_terminal()
            print("\nVALOR INVÁLIDO")
            pausa()
            continue

    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        limpar_terminal()
        print("\nCLIENTE NÃO POSSUI UMA LELEU CONTA!!!")
        pausa()
        return

    cliente.realizar_transacao(conta, transacao)

# Função para realizar um saque a partir de uma lista de clientes
def sacar(clientes):
    limpar_terminal()
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        limpar_terminal()
        print("\nCLIENTE NÃO ENCONTRADO!!!")
        pausa()
        return

    valor = None
    while valor is None:
        try:
            valor = float(input("QUANTO DESEJA SACAR DA SUA LELEU CONTA?"))
        except ValueError:
            limpar_terminal()
            print("\nVALOR INVALIDO!!!")
            pausa()

    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        limpar_terminal()
        print("\nCLIENTE NÃO POSSUI UMA LELEU CONTA!!!")
        pausa()
        return

    cliente.realizar_transacao(conta, transacao)

# Função para exibir o extrato de um cliente
def exibir_extrato(clientes):
    limpar_terminal()
    cpf = input("DIGITE O CPF DO CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        limpar_terminal()
        print("\nCLIENTE NÃO ENCONTRADO!!!")
        pausa()
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        limpar_terminal()
        print("\nCLIENTE NÃO POSSUI UMA LELEU CONTA!!!")
        pausa()
        return

    limpar_terminal()
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("ESSA LELEU CONTA NÃO POSSUI HISTORICO DE TRANSAÇÕES.")
    else:
        for transacao in transacoes:
            print(f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}")
    print(f"\nSALDO ATUAL: R$ {conta.saldo:.2f}")
    print("==========================================")
    pausa()

# Função para criar um novo cliente
def criar_cliente(clientes):
    limpar_terminal()
    cpf = input("DIGITE O CPF (SÓ NUMEROS): ")

    if not cpf.isdigit() or len(cpf) != 11:
        limpar_terminal()
        print("\nCPF INVÁLIDO!!!")
        pausa()
        return

    cliente = filtrar_cliente(cpf, clientes)
    if cliente:
        limpar_terminal()
        print("\nJÁ EXISTE UM LELEU CLIENTE COM ESSE CPF!!!")
        pausa()
        return

    nome = input("NOME COMPLETO: ")
    data_nascimento = input("DATA DE NASCIMENTO (dd-mm-aaaa): ")
    endereco = input("ENDEREÇO (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== BEM VINDO AO BANCO LELEU!!! ===")
    pausa()

# Função para criar uma nova conta
def criar_conta(numero_conta, clientes, contas):
    limpar_terminal()
    cpf = input("DIGITE O CPF DO LELEU CLIENTE: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        limpar_terminal()
        print("\nCLIENTE NÃO ENCONTRADO!!!")
        pausa()
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    limpar_terminal()
    print("\n=== LELEU CONTA CRIADA ===")
    pausa()

# Função para listar todas as contas existentes
def listar_contas(contas):
    limpar_terminal()
    for conta in contas:
        print("=" * 40)
        print(f"Agência: {conta.agencia}")
        print(f"Número: {conta.numero}")
        print(f"Títular: {conta.cliente.nome}")
    print("=" * 40)
    pausa()

# Função principal que controla o fluxo do programa
def main():
    clientes = []
    contas = []

    while True:
        mensagem()
        opcao = input("=> ")

        if opcao == "1":
            exibir_extrato(clientes)
        elif opcao == "2":
            sacar(clientes)
        elif opcao == "3":
            depositar(clientes)
        elif opcao == "6":
            criar_cliente(clientes)
        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == "5":
            listar_contas(contas)
        elif opcao == "0":
            sair()
            break
        else:
            limpar_terminal()
            print("\nOPERAÇÃO INVÁLIDA!!!\n")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()