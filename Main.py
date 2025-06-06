import csv
from datetime import datetime

ARQUIVO_REGISTRO = "registros.csv"

USUARIOS = {
    "admin": {"senha": "admin123", "tipo": "admin"},
    "danilo": {"senha": "1234", "tipo": "funcionario"},
    "livia": {"senha": "abcd", "tipo": "funcionario"},
}

def login():
    print("=== LOGIN ===")
    nome = input("Usuário (ou digite 'voltar' para sair): ").strip().lower()
    if nome == 'voltar':
        return None
    
    senha = input("Senha (ou digite 'voltar' para sair): ").strip()
    if senha == 'voltar':
        return None

    if nome in USUARIOS and USUARIOS[nome]["senha"] == senha:
        print(f"Bem-vindo, {nome.title()}!")
        return {"nome": nome, "tipo": USUARIOS[nome]["tipo"]}
    else:
        print("Credenciais inválidas.")
        return False  # sinaliza login falhou

def registrar_ponto(usuario):
    nome = usuario["nome"].title()
    tipo = usuario["tipo"]

    data = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")

    print("\nTipos de ponto:")
    opcoes = [
        "Primeira Entrada",
        "Primeira Saída",
        "Segunda Entrada",
        "Segunda Saída"
    ]

    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")

    escolha = input("Escolha o tipo de ponto: ").strip()
    if not escolha.isdigit() or not (1 <= int(escolha) <= 4):
        print("Opção inválida.")
        return

    tipo_ponto = opcoes[int(escolha) - 1]

    # Valida ordem dos registros
    registros_usuario = []
    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                if linha[0].lower() == nome.lower() and linha[1] == data:
                    registros_usuario.append(linha[3])
    except FileNotFoundError:
        pass

    regras = {
        "Primeira Entrada": [],
        "Primeira Saída": ["Primeira Entrada"],
        "Segunda Entrada": ["Primeira Saída"],
        "Segunda Saída": ["Segunda Entrada"]
    }

    requisitos = regras[tipo_ponto]
    for requisito in requisitos:
        if requisito not in registros_usuario:
            print(f"Erro: não é possível registrar '{tipo_ponto}' antes de '{requisito}'.")
            return

    with open(ARQUIVO_REGISTRO, mode='a', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([nome, data, hora, tipo_ponto])
    print("Ponto registrado com sucesso.")

def exibir_registros():
    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = csv.reader(arquivo)
            registros_por_usuario = {}
            for linha in leitor:
                usuario = linha[0]
                registros_por_usuario.setdefault(usuario, []).append(linha)

            if not registros_por_usuario:
                print("Não há registros.")
                return

            for usuario, registros in registros_por_usuario.items():
                print(f"\n== {usuario.upper()} ==")
                for reg in registros:
                    print(f"{reg[0]:<20} {reg[1]}   {reg[2]}   {reg[3]}")
    except FileNotFoundError:
        print("Não há registros.")

def editar_registro(usuario):
    if usuario["tipo"] != "admin":
        print("Acesso negado. Apenas administradores podem editar registros.")
        return

    nome_funcionario = input("Digite o nome do funcionário: ").strip()
    data_alvo = input("Digite a data do registro (dd/mm/aaaa): ").strip()

    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            leitor = list(csv.reader(arquivo))
    except FileNotFoundError:
        print("Arquivo de registros não encontrado.")
        return

    encontrados = []
    for i, linha in enumerate(leitor):
        if linha[0].lower() == nome_funcionario.lower() and linha[1] == data_alvo:
            encontrados.append((i, linha))

    if not encontrados:
        print("Nenhum registro encontrado para esse funcionário nessa data.")
        return

    print(f"\nRegistros de {nome_funcionario} em {data_alvo}:")
    for idx, (indice, linha) in enumerate(encontrados, 1):
        print(f"{idx}. {linha[0]:<15} {linha[1]:<12} {linha[2]:<10} {linha[3]}")

    try:
        escolha = int(input("\nEscolha o número do registro que deseja editar: "))
        if escolha < 1 or escolha > len(encontrados):
            print("Escolha inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return

    indice_original, registro = encontrados[escolha - 1]
    nova_hora = input("Digite a nova hora (hh:mm:ss): ").strip()
    justificativa = input("Digite a justificativa da alteração: ").strip()
    hora_atual = datetime.now().strftime("%H:%M:%S")

    registro[2] = nova_hora
    registro[3] += f" (Editado por: {usuario['nome']} às {hora_atual}. Justificativa: {justificativa})"
    leitor[indice_original] = registro

    with open(ARQUIVO_REGISTRO, mode='w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerows(leitor)

    print("Registro atualizado com sucesso.")

def menu():
    usuario = None
    while usuario is None:
        usuario = login()
        if usuario is None:  # Usuário digitou 'voltar' para sair
            print("Saindo do programa.")
            return
        elif usuario is False:  # Login falhou, tenta novamente
            usuario = None

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1. Registrar ponto")
        print("2. Visualizar registros")
        print("3. Editar registro (Admin)")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            registrar_ponto(usuario)
        elif opcao == "2":
            exibir_registros()
        elif opcao == "3":
            editar_registro(usuario)
        elif opcao == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
