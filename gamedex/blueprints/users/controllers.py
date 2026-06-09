from flask import render_template, request, redirect, url_for, flash, session
from .dao import UserDAO
from .models import User, Comum, Admin
import bcrypt

class UserController:

    def __init__(self):
        self.__dao = UserDAO()


    # CADASTRAR
    def cadastrar_user(self):
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha = bcrypt.hashpw(bytes, salt)
        tipo = request.form.get("tipo")
        usuarios = self.__dao.carregar_user()

        if not email or not senha or not nome:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return self.preparar_cadastro()
        
        for user in usuarios:
            if user.email == email:
                flash("Erro: Email já existente!", "danger")
                return redirect(url_for("user.cadastrar_user"))

        try:
            if tipo == "comum":
                novo_user = Comum(
                    nome,
                    email,
                    senha
                )
                self.__dao.salvar_user(novo_user,tipo)
            else:
                autorizacao = request.form.get("aut")
                if autorizacao == "root":
                    novo_user = Admin(
                        nome,
                        email,
                        senha
                    )
                    self.__dao.salvar_user(novo_user, tipo)
            flash(f"Sucesso: O email '{email}' foi cadastrado!", "success")
            return redirect(url_for("user.index"))

        except Exception as e:
            flash(f"Erro ao cadastrar usuário: {str(e)}", "danger")
            return redirect(url_for("user.cadastrar_user"))

        
    def preparar_cadastro(self):
        return render_template("users/cadastro.html")


    def index(self):
        return render_template("index.html")
    
    def login(self):
        email = request.form.get("email")
        senha = request.form.get("senha")
        if not email or not senha:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for("user.login"))
        users = self.__dao.carregar_user()
        for user in users:
            senha_status = bcrypt.checkpw(senha.encode('utf-8'), user.senha.encode('utf-8'),)
            if user.email == email and senha_status == True:
                if user.tipo() == "comum":
                        session['usuario'] = user.nome
                        session['user_id'] = user.id
                        session['admin'] = False
                        
                        flash(f"Sucesso: logou no email '{email}' !", "success")
                        return redirect(url_for("user.index"))
                else: 
                        session['usuario'] = user.nome
                        session['user_id'] = user.id
                        session['admin'] = True
                        flash(f"Sucesso: logou no email '{email}' !", "success")
                        return redirect(url_for("user.index"))
        flash("Erro: Usúario não existente ou senha errada", "danger")
        return redirect(url_for("user.login"))
        
    def preparar_login(self):
        return render_template("users/login.html")
    
    def encerrar(self):
        session.pop('usuario', None)
        session.pop('admin', None)
        return self.index()


    def erro(self):
        return render_template("erro.html")

    #REMOVER
    def remover_user(self, id):
        self.__dao.remover_user(id)
        flash("Sucesso: User removido com sucesso!", "success")
        if (session.get("admin")):
            return redirect(url_for("user.admin_user"))
        else:
            return self.encerrar()
    def admin(self):
        if not session.get("admin"):
            flash("Acesso negado", "danger")
            return redirect(url_for("user.index"))
        return render_template("admin/admin.html")
    
    def creditos(self):
        return render_template("creditos.html")
    
    def painel(self):
        id = session.get("user_id")
        users = self.__dao.carregar_user()
        for user in users:
            if user.id == id:
                return render_template("users/painel.html", user = user )
    def preparar_edicao(self,id):
        user = self.__dao.buscar_user_por_id(id)
        return render_template("users/editar.html", user = user)

    def editar_user(self, id):
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        tipo = session.get("Admin")
        bytes = senha.encode('utf-8')
        salt = bcrypt.gensalt()
        senha = bcrypt.hashpw(bytes, salt)

        try:
            if tipo == "False":
                user_att = Comum(
                nome,
                email,
                senha,
                id
                )
            else:
                user_att = Admin(
                    nome,
                    email,
                    senha,
                    id
                )
            session["usuario"] = user_att.nome
            self.__dao.editar_user(user_att)
            return render_template("users/painel.html", user = user_att)
        except Exception as e:
            flash(f"Erro ao atualizar user: {str(e)}", "danger")
            return redirect(url_for("user.editar_user", id=id))

    def admin_user(self):
        users = self.__dao.carregar_user()
        return render_template("admin/usuarios.html", users=users)