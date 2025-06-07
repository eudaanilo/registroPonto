import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os
from datetime import datetime

ARQUIVO_USUARIOS = "usuarios.csv"
ARQUIVO_REGISTROS = "registros.csv"

def inicializar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, mode='w', newline='') as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(["usuario", "senha", "tipo", "ultimo_login"])
            escritor.writerow(["admin", "admin123", "admin", "nunca"])

def carregar_usuarios():
    usuarios = {}
    with open(ARQUIVO_USUARIOS, mode='r') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            usuarios[linha["usuario"]] = {
                "senha": linha["senha"],
                "tipo": linha["tipo"],
                "ultimo_login": linha["ultimo_login"]
            }
    return usuarios

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, mode='w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["usuario", "senha", "tipo", "ultimo_login"])
        for usuario, dados in usuarios.items():
            escritor.writerow([usuario, dados["senha"], dados["tipo"], dados.get("ultimo_login", "nunca")])

def registrar_ultimo_login(nome_usuario):
    usuarios = carregar_usuarios()
    if nome_usuario in usuarios:
        usuarios[nome_usuario]["ultimo_login"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        salvar_usuarios(usuarios)

def registrar_ponto(usuario, tipo_ponto):
    with open(ARQUIVO_REGISTROS, mode='a', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        data = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")
        escritor.writerow([usuario, data, hora, tipo_ponto])

def carregar_registros():
    registros = []
    if not os.path.exists(ARQUIVO_REGISTROS):
        return registros
    with open(ARQUIVO_REGISTROS, mode='r') as arquivo:
        leitor = csv.reader(arquivo)
        for linha in leitor:
            registros.append(linha)
    return registros

def limpar_registros():
    open(ARQUIVO_REGISTROS, 'w').close()

class SistemaPonto:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Ponto")
        self.usuario_atual = None
        self.tela_login()

    def tela_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Usuário:").pack()
        self.entrada_usuario = tk.Entry(self.root)
        self.entrada_usuario.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.entrada_senha = tk.Entry(self.root, show="*")
        self.entrada_senha.pack()

        tk.Button(self.root, text="Entrar", command=self.login).pack(pady=10)

    def login(self):
        nome = self.entrada_usuario.get()
        senha = self.entrada_senha.get()
        usuarios = carregar_usuarios()

        if nome in usuarios and usuarios[nome]["senha"] == senha:
            self.usuario_atual = {"nome": nome, "tipo": usuarios[nome]["tipo"]}
            registrar_ultimo_login(nome)
            if self.usuario_atual["tipo"] == "admin":
                self.menu_admin()
            else:
                self.menu_funcionario()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def logout(self):
        self.usuario_atual = None
        self.tela_login()

    def menu_admin(self):
        self.menu_base("admin")

    def menu_funcionario(self):
        self.menu_base("funcionario")

    def menu_base(self, tipo_usuario):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Bem-vindo, {self.usuario_atual['nome']}!").pack()

        botoes = []

        if tipo_usuario == "admin":
            botoes = [
                ("Registrar 1ª Entrada", lambda: self.registrar_ponto_gui("1ª Entrada")),
                ("Registrar 1ª Saída", lambda: self.registrar_ponto_gui("1ª Saída")),
                ("Registrar 2ª Entrada", lambda: self.registrar_ponto_gui("2ª Entrada")),
                ("Registrar 2ª Saída", lambda: self.registrar_ponto_gui("2ª Saída")),
                ("Exibir Registros", self.exibir_registros),
                ("Cadastrar Usuário", self.cadastrar_usuario),
                ("Listar Usuários", self.listar_usuarios),
                ("Limpar Registros", self.confirmar_limpeza_registros),
                ("Logout", self.logout)
            ]
        else:
            botoes = [
                ("Registrar 1ª Entrada", lambda: self.registrar_ponto_gui("1ª Entrada")),
                ("Registrar 1ª Saída", lambda: self.registrar_ponto_gui("1ª Saída")),
                ("Registrar 2ª Entrada", lambda: self.registrar_ponto_gui("2ª Entrada")),
                ("Registrar 2ª Saída", lambda: self.registrar_ponto_gui("2ª Saída")),
                ("Logout", self.logout)
            ]

        for texto, comando in botoes:
            tk.Button(self.root, text=texto, width=30, command=comando).pack(pady=2)

    def registrar_ponto_gui(self, tipo_ponto):
        registrar_ponto(self.usuario_atual["nome"], tipo_ponto)
        messagebox.showinfo("Sucesso", f"{tipo_ponto} registrada com sucesso!")

    def exibir_registros(self):
        registros = carregar_registros()
        if not registros:
            messagebox.showinfo("Registros", "Não há registros.")
            return

        janela = tk.Toplevel(self.root)
        janela.title("Registros de Ponto")

        texto = tk.Text(janela, width=80, height=25)
        texto.pack()

        registros_por_usuario = {}
        for r in registros:
            usuario = r[0]
            registros_por_usuario.setdefault(usuario, []).append(r)

        for usuario, linhas in registros_por_usuario.items():
            texto.insert(tk.END, f"
== {usuario.upper()} ==
")
            for linha in linhas:
                texto.insert(tk.END, f"{linha[0]:20s} {linha[1]}   {linha[2]}   {linha[3]}
")

    def cadastrar_usuario(self):
        novo_usuario = simpledialog.askstring("Cadastro", "Novo usuário:")
        nova_senha = simpledialog.askstring("Cadastro", "Senha:")
        tipo = simpledialog.askstring("Cadastro", "Tipo (admin/funcionario):")

        if not novo_usuario or not nova_senha or tipo not in ["admin", "funcionario"]:
            messagebox.showerror("Erro", "Dados inválidos.")
            return

        usuarios = carregar_usuarios()
        if novo_usuario in usuarios:
            messagebox.showerror("Erro", "Usuário já existe.")
            return

        usuarios[novo_usuario] = {"senha": nova_senha, "tipo": tipo, "ultimo_login": "nunca"}
        salvar_usuarios(usuarios)
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")

    def listar_usuarios(self):
        usuarios = carregar_usuarios()
        janela = tk.Toplevel(self.root)
        janela.title("Usuários")

        texto = tk.Text(janela, width=60, height=25)
        texto.pack()

        texto.insert(tk.END, f"Total de usuários: {len(usuarios)}\n\n")
        for nome, dados in usuarios.items():
            texto.insert(tk.END, f"Usuário: {nome}\n")
            texto.insert(tk.END, f"Tipo: {dados['tipo']}\n")
            texto.insert(tk.END, f"Último login: {dados['ultimo_login']}\n\n")

    def confirmar_limpeza_registros(self):
        registros = carregar_registros()
        if not registros:
            messagebox.showinfo("Info", "Não há registros para limpar.")
            return

        confirm = messagebox.askyesno("Confirmação", "Deseja limpar todos os registros?")
        if confirm:
            limpar_registros()
            messagebox.showinfo("Sucesso", "Registros apagados.")

if __name__ == "__main__":
    inicializar_usuarios()
    root = tk.Tk()
    app = SistemaPonto(root)
    root.mainloop()
