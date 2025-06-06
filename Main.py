import csv
from datetime import datetime
from collections import defaultdict

ARQUIVO_REGISTRO = "registro_ponto.csv"

def registrar_ponto():
    nome = input("Digite o nome do funcionário: ").strip()
    
    print("\nEscolha o tipo de registro:")
    print("1. Primeira Entrada")
    print("2. Primeira Saída")
    print("3. Segunda Entrada")
    print("4. Segunda Saída")
    
    opcao = input("Opção: ")
    tipos = {
        "1": "Primeira Entrada",
        "2": "Primeira Saída",
        "3": "Segunda Entrada",
        "4": "Segunda Saída"
    }

    if opcao not in tipos:
        print("Opção inválida.")
        return
    
    tipo = tipos[opcao]
    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")
    
    registros_dia = []
    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                nome_reg, data_reg, hora_reg, tipo_reg = linha
                if nome_reg == nome and data_reg == data:
                    registros_dia.append(tipo_reg)
    except FileNotFoundError:
        pass

    if tipo == "Primeira Saída" and "Primeira Entrada" not in registros_dia:
        print("Erro: não é possível registrar Primeira Saída sem Primeira Entrada.")
        return
    if tipo == "Segunda Entrada" and "Primeira Saída" not in registros_dia:
        print("Erro: não é possível registrar Segunda Entrada sem Primeira Saída.")
        return
    if tipo == "Segunda Saída" and "Segunda Entrada" not in registros_dia:
        print("Erro: não é possível registrar Segunda Saída sem Segunda Entrada.")
        return

    with open(ARQUIVO_REGISTRO, mode='a', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([nome, data, hora, tipo])
    
    print(f"{tipo} registrada para {nome} em {data} às {hora}.")

def visualizar_registros():
    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = list(csv.reader(arquivo))
            if not leitor:
                print("Não há registros.")
                return

            registros = defaultdict(list)
            for linha in leitor:
                nome, data, hora, tipo = linha
                registros[nome].append((data, hora, tipo))

            for nome in sorted(registros.keys()):
                print(f"\n== {nome.upper()} ==")
                for data, hora, tipo in registros[nome]:
                    print(f"{nome:<20} {data:<12} {hora:<10} {tipo:<20}")

    except FileNotFoundError:
        print("Não há registros.")

def limpar_registros():
    senha_admin = "admin123"  # Altere conforme necessário

    print("\n⚠️  Função de limpeza — acesso apenas para ADMINISTRADORES.")
    senha = input("Digite a senha de administrador: ").strip()

    if senha != senha_admin:
        print("Acesso negado⚠️")
        return

    # Verifica se há registros no arquivo
    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = list(csv.reader(arquivo))
            if not leitor:
                print("Não há registros no sistema.")
                return
    except FileNotFoundError:
        print("Não há registros no sistema.")
        return

    print("\n=== Limpeza de Registros ===")
    print("1. Limpar TODOS os registros")
    print("2. Limpar registros de um FUNCIONÁRIO")
    print("3. Limpar registros de um FUNCIONÁRIO em uma DATA específica")
    print("4. Cancelar")

    escolha = input("Escolha uma opção: ").strip()

    if escolha == "1":
        confirmacao = input("Tem certeza que deseja apagar TODOS os registros? (s/n): ").strip().lower()
        if confirmacao == 's':
            with open(ARQUIVO_REGISTRO, mode='w', newline='') as arquivo:
                pass
            print("Todos os registros foram apagados com sucesso.")
        else:
            print("Ação cancelada.")

    elif escolha == "2":
        nome = input("Digite o nome do funcionário: ").strip()
        registros_existem = False
        novos_registros = []

        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                if linha[0].lower() == nome.lower():
                    registros_existem = True
                else:
                    novos_registros.append(linha)

        if not registros_existem:
            print("Não há registros para esse funcionário.")
            return

        with open(ARQUIVO_REGISTRO, mode='w', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerows(novos_registros)
        print(f"Registros do funcionário '{nome}' foram apagados com sucesso.")

    elif escolha == "3":
        nome = input("Digite o nome do funcionário: ").strip()
        data = input("Digite a data (dd/mm/aaaa): ").strip()
        registros_existem = False
        novos_registros = []

        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                if linha[0].lower() == nome.lower() and linha[1] == data:
                    registros_existem = True
                else:
                    novos_registros.append(linha)

        if not registros_existem:
            print("Não há registros desse funcionário na data informada.")
            return

        with open(ARQUIVO_REGISTRO, mode='w', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerows(novos_registros)
        print(f"Registros de '{nome}' na data '{data}' foram apagados com sucesso.")

    else:
        print("Ação cancelada.")

def menu():
    while True:
        print("\n=== Sistema de Registro de Ponto ===")
        print("1. Registrar Ponto")
        print("2. Visualizar Registros")
        print("3. Limpar Registros")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar_ponto()
        elif opcao == "2":
            visualizar_registros()
        elif opcao == "3":
            limpar_registros()
        elif opcao == "4":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
