import Main
def login():
    print("=== LOGIN ===")
    nome = input("Usuário: ").strip().lower()
    senha = input("Senha: ").strip()

    if nome in Main.USUARIOS and Main.USUARIOS[nome]["senha"] == senha:
        print(f"Bem-vindo, {nome.title()}!")
        return {"nome": nome, "tipo": Main.USUARIOS[nome]["tipo"]}
    else:
        print("Credenciais inválidas.")
        return None