from flask import render_template, request, redirect, url_for, flash, session
import os
from .dao import JogoDAO
from blueprints.categorias.dao import CategoriaDAO
from .models import Jogo, Fisico, Digital
from werkzeug.utils import secure_filename


class JogoController:

    def __init__(self):
        self.__dao = JogoDAO()
        self.__categoria_dao = CategoriaDAO()

    # LISTAR
    def listar_jogos(self):
            lista = self.__dao.carregar_jogos()
            return render_template("jogos.html", jogos=lista)

    # CADASTRAR
    def cadastrar_jogo(self):
            diretorio = "static/uploads/games"
            nome = request.form.get("nome")
            dev = request.form.get("dev")
            data = request.form.get("data")
            genero = request.form.get("genero")
            sinopse = request.form.get("sinopse")
            categoria_id = request.form.getlist("categorias")
            img = request.files.get("img")
            plat = request.form.get("plataforma")
            tipo = request.form.get("tipo")
            autor = session.get("user_id")
            if session["admin"] == True:
                status = "aprovado"
            else:
                status = "pendente"
            

            if not nome or not dev or not data or not genero or not categoria_id or not img or not plat or img.filename == "":
                flash("Erro: Preencha todos os campos obrigatórios!", "danger")
                return self.preparar_cadastro()

            try:
                filename = secure_filename(img.filename)
                caminho = os.path.join(diretorio, filename)
                if tipo == "fisico":
                    midia = request.form.get("midia")
                    console = request.form.get("console")
                    novo_jogo = Fisico(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat,
                        filename,
                        midia,
                        console,
                        categoria_id,
                        status,
                        autor
                    )
                else:
                    distribuicao = request.form.get("distribuicao")
                    tamanho = int(request.form.get("tamanho"))
                    novo_jogo = Digital(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat,
                        filename,
                        distribuicao,
                        tamanho,
                        categoria_id,
                        status,
                        autor
                    )                   
                self.__dao.salvar_jogo(novo_jogo,categoria_id, autor)
                img.save(caminho)

                flash(f"Sucesso: O jogo '{nome}' foi cadastrado!", "success")
                return redirect(url_for("games.listar_jogos"))
            

            except Exception as e:
                flash(f"Erro ao cadastrar jogo: {str(e)}", "danger")
                return self.preparar_cadastro()

    def preparar_cadastro(self):
        if 'usuario' not in session:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        else:
            categorias = self.__categoria_dao.carregar_categorias()
            return render_template("cadastrar.html", categorias = categorias)

    # PREPARAR EDIÇÃO
    def preparar_edicao(self, id):
        if 'usuario' not in session:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        else:
            jogo = self.__dao.buscar_jogo_por_id(id)
            categorias = self.__categoria_dao.carregar_categorias()

            if not jogo:
                flash("Erro: Jogo não encontrado!", "danger")
                return redirect(url_for("games.listar_jogos"))

            return render_template("editar.html", jogo=jogo, categorias = categorias)

    # EDITAR
    def editar_jogo(self, id):
        diretorio = "static/uploads/games"
        nome = request.form.get("nome")
        dev = request.form.get("dev")
        data = request.form.get("data")
        genero = request.form.get("genero")
        sinopse = request.form.get("sinopse")
        categoria_id = request.form.getlist("categorias")
        img = request.files.get("img")
        plat = request.form.get("plataforma")
        tipo = request.form.get("tipo")
        autor = session.get("user_id")
        status = "aprovado"
        if not nome or not dev or not data or not genero or not categoria_id or not plat or not tipo or not autor:
            flash("Erro: Preencha todos os campos obrigatórios!", "danger")
            return redirect(url_for("games.editar_jogo", id=id))

        try:
            jogo_antigo = self.__dao.buscar_jogo_por_id(id)

            if img and img.filename != "":
                filename = secure_filename(img.filename)
                caminho = os.path.join(diretorio, filename)
                img.save(caminho)
            else:
                filename = jogo_antigo.img
            if tipo == "fisico":
                    midia = request.form.get("midia")
                    console = request.form.get("console")
                    jogo_atualizado = Fisico(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat,
                        filename,
                        midia,
                        console,
                        categoria_id,
                        status,
                        autor
                    )
            else:
                    distribuicao = request.form.get("distribuicao")
                    tamanho = int(request.form.get("tamanho"))
                    jogo_atualizado = Digital(
                        nome,
                        dev,
                        data,
                        genero,
                        sinopse,
                        plat,
                        filename,
                        distribuicao,
                        tamanho,
                        categoria_id,
                        status,
                        autor
                    )                 

            self.__dao.atualizar_jogo(jogo_atualizado,id)
            flash(f"Sucesso: O jogo '{nome}' foi atualizado!", "success")
            return redirect(url_for("games.listar_jogos"))

        except Exception as e:
            flash(f"Erro ao atualizar jogo: {str(e)}", "danger")
            return redirect(url_for("games.editar_jogo", id=id))

    # REMOVER
    def remover_jogo(self, id):
        if 'usuario' not in session:
                flash("Erro: deve estar logado para essa função", "danger")
                return redirect(url_for("user.erro"))
        else:
                self.__dao.remover_jogo(id)
                flash("Sucesso: Jogo removido com sucesso!", "success")
                return redirect(url_for("games.listar_jogos"))
    

    def index(self):
        return render_template("index.html" )
    


    
    def busca(self):
        nome = request.form.get("nome")
        jogos = self.__dao.carregar_jogos()
        jogos_certo = []
        for jogo in jogos:
            if nome.lower() in jogo.nome.lower():
                jogos_certo.append(jogo)

        return render_template("jogos.html", jogos=jogos_certo)
    
    def detalhe(self, id):
        jogo = self.__dao.buscar_jogo_por_id(id)
        comentarios = self.__dao.selecionar_comentario(id)
        return render_template("detalhe.html", jogo=jogo, comentarios=comentarios)
    
    def enviar_comentario(self):
        if session.get("usuario"):
            comentario = request.form.get("comentario")
            id_autor = session.get("user_id")
            id_jogo = int(request.form.get("id_jogo"))

            
            print("Autor:", session.get("usuario"))
            print("ID Autor:", id_autor)
            print("Comentario:", comentario)
            print("ID Jogo:", id_jogo)
            self.__dao.enviar_comentario(
                session.get("usuario"),
                comentario,
                session.get('user_id'),
                id_jogo
            )

            comentarios = self.__dao.selecionar_comentario(id_jogo)
            jogo = self.__dao.buscar_jogo_por_id(id_jogo)

            return render_template("detalhe.html", jogo=jogo, comentarios=comentarios)
        else:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
    
    def excluir_comentario(self, id):
        if session.get("usuario"):        
            id_jogo = int(request.form.get("id_jogo"))  
            self.__dao.excluir_comentario(id)
            flash("Sucesso: Comentário removido com sucesso!", "success")
            return redirect(url_for("games.detalhe", id=id_jogo))
        else:
            flash("Erro: deve estar logado para essa função", "danger")
            return redirect(url_for("user.erro"))
        
    def admin_jogos(self):
            lista = self.__dao.carregar_jogos()
            pendentes = []
            for jogo in lista:
                if jogo.status == "pendente":
                    pendentes.append(jogo)
            return render_template("admin/jogos.html", jogos=pendentes)
    
    def status(self,id,response):
        if not session.get("admin"):
            flash("Acesso Negado","danger")
            return redirect(url_for("user.index"))
        self.__dao.status(id,response)
        return redirect(url_for("games.admin_jogos"))