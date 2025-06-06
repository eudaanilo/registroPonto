import csv
from datetime import datetime

ARQUIVO_REGISTRO = "registro_ponto.csv"

def registrar_ponto(tipo):
    nome = input("Digite o nome do funcionário: ").strip()
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
            print(f"{'Nome':<20} {'Data':<12} {'Hora':<10} {'Tipo':<10}")
            print("-" * 55)
            for linha in leitor:
                print(f"{linha[0]:<20} {linha[1]:<12} {linha[2]:<10} {linha[3]:<10}")
    except FileNotFoundError:
        print("Nenhum registro encontrado.")

def menu():
    while True:
        print("\n=== Sistema de Registro de Ponto ===")
        print("1. Registrar Entrada")
        print("2. Registrar Saida")
        print("3. Visualizar Registros")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar_ponto("Entrada")
        elif opcao == "2":
            registrar_ponto("Saida")
        elif opcao == "3":
            visualizar_registros()
        elif opcao == "4":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
