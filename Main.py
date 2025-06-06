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
            leitor = csv.reader(arquivo)
            registros = defaultdict(list)
            for linha in leitor:
                nome, data, hora, tipo = linha
                registros[nome].append((data, hora, tipo))

            for nome in sorted(registros.keys()):
                print(f"\n== {nome.upper()} ==")
                for data, hora, tipo in registros[nome]:
                    print(f"{nome:<20} {data:<12} {hora:<10} {tipo:<20}")

    except FileNotFoundError:
        print("Nenhum registro encontrado.")

def menu():
    while True:
        print("\n=== Sistema de Registro de Ponto ===")
        print("1. Registrar Ponto")
        print("2. Visualizar Registros")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar_ponto()
        elif opcao == "2":
            visualizar_registros()
        elif opcao == "3":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
