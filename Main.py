import csv
from datetime import datetime

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
    
    with open(ARQUIVO_REGISTRO, mode='a', newline='') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow([nome, data, hora, tipo])
    
    print(f"{tipo} registrada para {nome} em {data} às {hora}.")

def visualizar_registros():
    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = csv.reader(arquivo)
            print(f"{'Nome':<20} {'Data':<12} {'Hora':<10} {'Turno':<20}")
            print("-" * 65)
            for linha in leitor:
                print(f"{linha[0]:<20} {linha[1]:<12} {linha[2]:<10} {linha[3]:<20}")
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
