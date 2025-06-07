import csv
import os
import sys
from datetime import datetime


ARQUIVO_REGISTRO = "registros.csv"
ARQUIVO_USUARIOS = "usuarios.csv"

# Se arquivo de usuários não existe, cria um admin padrão
def inicializar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, mode='w', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["usuario", "senha", "tipo", "ultimo_login"])
            escritor.writerow(["admin", "admin123", "admin", "nunca"])

def carregar_usuarios():
    usuarios = {}
    try:
        with open(ARQUIVO_USUARIOS, mode='r') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                usuarios[linha["usuario"]] = {
                    "senha": linha["senha"],
                    "tipo": linha["tipo"],
                    "ultimo_login": linha.get("ultimo_login", "nunca")
                }
    except FileNotFoundError:
        inicializar_usuarios()
        return carregar_usuarios()
    return usuarios

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, mode='w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["usuario", "senha", "tipo", "ultimo_login"])
        for usuario, dados in usuarios.items():
            escritor.writerow([usuario, dados["senha"], dados["tipo"], dados.get("ultimo_login", "nunca")])

def login():
    usuarios = carregar_usuarios()
    print("=== LOGIN ===")
    nome = input("Usuário (ou digite 'voltar' para sair): ").strip().lower()
    if nome == 'voltar':
        return None

    senha = input_senha_com_asteriscos("Senha: ").strip()
    if senha == 'voltar':
        return None

    if nome in usuarios and usuarios[nome]["senha"] == senha:
        usuarios[nome]["ultimo_login"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        salvar_usuarios(usuarios)
        print(f"Bem-vindo, {nome.title()}!")
        return {"nome": nome, "tipo": usuarios[nome]["tipo"]}
    else:
        print("Credenciais inválidas.")
        return False

def registrar_ponto(usuario):
    nome = usuario["nome"].title()
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

def limpar_registros(usuario):
    if usuario["tipo"] != "admin":
        print("Apenas administradores podem limpar registros.")
        return

    try:
        with open(ARQUIVO_REGISTRO, mode='r') as arquivo:
            linhas = arquivo.readlines()
            if not linhas:
                print("Não há registros para limpar.")
                return
    except FileNotFoundError:
        print("Não há registros para limpar.")
        return

    confirmar = input("Tem certeza que deseja limpar todos os registros? (s/n): ").strip().lower()
    if confirmar == 's':
        with open(ARQUIVO_REGISTRO, mode='w') as arquivo:
            arquivo.write('')
        print("Registros limpos com sucesso.")
    else:
        print("Operação cancelada.")

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

def cadastrar_usuario(usuario):
    if usuario["tipo"] != "admin":
        print("Acesso negado. Apenas administradores podem cadastrar usuários.")
        return

    usuarios = carregar_usuarios()
    novo_usuario = input("Digite o nome do novo usuário: ").strip().lower()

    if novo_usuario in usuarios:
        print("Usuário já existe.")
        return

    nova_senha = input_senha_com_asteriscos("Senha: ").strip()
    tipo = input("Tipo do usuário (admin/funcionario): ").strip().lower()
    if tipo not in ["admin", "funcionario"]:
        print("Tipo inválido.")
        return

    usuarios[novo_usuario] = {"senha": nova_senha, "tipo": tipo}
    salvar_usuarios(usuarios)
    print(f"Usuário '{novo_usuario}' criado com sucesso.")

def mostrar_usuarios(usuario):
    if usuario["tipo"] != "admin":
        print("Apenas administradores podem visualizar essa informação.")
        return

    usuarios = carregar_usuarios()

    print("\n=== LISTA DE USUÁRIOS ===")
    print(f"Total de usuários: {len(usuarios)}\n")
    for nome, dados in usuarios.items():
        print(f"Usuário: {nome}")
        print(f"Tipo: {dados['tipo']}")
        print(f"Último login: {dados.get('ultimo_login', 'nunca')}\n")

def alterar_senha(usuario):
    usuarios = carregar_usuarios()
    nome = usuario["nome"]
    print(f"Alterando senha para o usuário {nome}")

    senha_atual = input_senha_com_asteriscos("Digite sua senha atual: ").strip()
    if senha_atual != usuarios[nome]["senha"]:
        print("Senha atual incorreta.")
        return

    nova_senha = input_senha_com_asteriscos("Digite a nova senha: ").strip()
    confirmar_senha = input_senha_com_asteriscos("Confirme a nova senha: ").strip()
    if nova_senha != confirmar_senha:
        print("As senhas não coincidem.")
        return

    usuarios[nome]["senha"] = nova_senha
    salvar_usuarios(usuarios)
    print("Senha alterada com sucesso.")

def input_senha_com_asteriscos(prompt="Senha: "):
    print(prompt, end='', flush=True)
    senha = ''
    if os.name == 'nt':
        import msvcrt
        while True:
            tecla = msvcrt.getch()
            if tecla in {b'\r', b'\n'}:
                print()
                break
            elif tecla == b'\x08':  # backspace
                if len(senha) > 0:
                    senha = senha[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            elif tecla == b'\x03':  # Ctrl+C
                raise KeyboardInterrupt
            else:
                senha += tecla.decode('utf-8', 'ignore')
                sys.stdout.write('*')
                sys.stdout.flush()
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                tecla = sys.stdin.read(1)
                if tecla in ('\r', '\n'):
                    print()
                    break
                elif tecla == '\x7f':  # backspace
                    if len(senha) > 0:
                        senha = senha[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                elif tecla == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                else:
                    senha += tecla
                    sys.stdout.write('*')
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return senha

def menu_admin(usuario):
    while True:
        print("\n=== MENU ADMINISTRADOR ===")
        print("1. Registrar ponto")
        print("2. Exibir registros")
        print("3. Editar registro")
        print("4. Limpar registros")
        print("5. Cadastrar usuário")
        print("6. Alterar minha senha")
        print("7. Listar usuários do sistema")
        print("8. Logout")
        
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            registrar_ponto(usuario)
        elif escolha == '2':
            exibir_registros()
        elif escolha == '3':
            editar_registro(usuario)
        elif escolha == '4':
            limpar_registros(usuario)
        elif escolha == '5':
            cadastrar_usuario(usuario)
        elif escolha == '6':
            alterar_senha(usuario)
        elif escolha == '7':
            mostrar_usuarios(usuario)
            break
        elif escolha == '8':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

def menu_funcionario(usuario):
    while True:
        print(f"\n=== MENU FUNCIONÁRIO ({usuario['nome'].title()}) ===")
        print("1. Registrar ponto")
        print("2. Alterar minha senha")
        print("3. Logout")
        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            registrar_ponto(usuario)
        elif escolha == '2':
            alterar_senha(usuario)
        elif escolha == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

def main():
    inicializar_usuarios()
    while True:
        resultado = login()
        if resultado is None:
            print("Voltando...")
            break
        if resultado is False:
            continue
        usuario = resultado
        if usuario["tipo"] == "admin":
            menu_admin(usuario)
        else:
            menu_funcionario(usuario)

if __name__ == "__main__":
    main()