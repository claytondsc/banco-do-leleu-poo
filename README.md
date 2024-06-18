# Banco Leleu

Este é um sistema de simulação de operações bancárias desenvolvido em Python utilizando a Programação Orientada a Objetos (POO). O sistema permite criar clientes e contas correntes, realizar transações como depósitos e saques, e consultar extratos. A POO foi empregada para organizar o código em classes, tornando-o modular, reutilizável e fácil de manter.

## Funcionalidades

- **Criar Cliente**: Registra novos clientes no sistema.
- **Criar Conta Corrente**: Cria novas contas correntes para clientes existentes.
- **Realizar Depósito**: Permite aos clientes depositar dinheiro em suas contas.
- **Realizar Saque**: Permite aos clientes sacar dinheiro de suas contas, respeitando limites e número máximo de saques.
- **Consultar Extrato**: Exibe o histórico de transações e o saldo atual da conta.
- **Listar Contas**: Exibe todas as contas criadas no banco.

## Estrutura do Código

### Funções Principais

- **`limpar_terminal()`**: Limpa o terminal, dependendo do sistema operacional.
- **`pausa()`**: Pausa o programa até que o usuário pressione Enter.
- **`mensagem()`**: Exibe o menu principal do banco.

### Classes

- **`Cliente`**: Representa um cliente genérico do banco.
- **`PessoaFisica`**: Herda de `Cliente`, representa um cliente pessoa física.
- **`Conta`**: Representa uma conta bancária genérica.
- **`ContaCorrente`**: Herda de `Conta`, representa uma conta corrente.
- **`Historico`**: Mantém o histórico de transações de uma conta.
- **`Transacao`**: Classe abstrata para representar transações.
  - **`Saque`**: Herda de `Transacao`, representa uma transação de saque.
  - **`Deposito`**: Herda de `Transacao`, representa uma transação de depósito.

### Funções de Operação

- **`consultar_extrato(conta)`**: Consulta o extrato de uma conta.
- **`realizar_saque(conta)`**: Realiza um saque em uma conta.
- **`realizar_deposito(conta)`**: Realiza um depósito em uma conta.
- **`sair()`**: Sai do sistema.
- **`filtrar_cliente(cpf, clientes)`**: Filtra um cliente pelo CPF.
- **`recuperar_conta_cliente(cliente)`**: Recupera a conta de um cliente.
- **`depositar(clientes)`**: Realiza um depósito a partir de uma lista de clientes.
- **`sacar(clientes)`**: Realiza um saque a partir de uma lista de clientes.
- **`exibir_extrato(clientes)`**: Exibe o extrato de um cliente.
- **`criar_cliente(clientes)`**: Cria um novo cliente.
- **`criar_conta(numero_conta, clientes, contas)`**: Cria uma nova conta.
- **`listar_contas(contas)`**: Lista todas as contas existentes.

## Como Executar

1. Certifique-se de ter o Python instalado em seu sistema.
2. Clone este repositório ou baixe os arquivos.
3. Navegue até o diretório do projeto.
4. Execute o script principal:

   ```bash
   python banco-do-leleu-poo.py

## Requisitos

- Python 3.x

## Autor

- Desenvolvido por [Clayton Dias](https://github.com/claytondsc)
