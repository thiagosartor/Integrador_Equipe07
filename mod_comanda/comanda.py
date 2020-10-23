from flask import Blueprint, render_template, request, url_for, jsonify, session, json
import datetime

from mod_login.login import validaSessao
from mod_comanda.comandaBD import Comanda
from mod_comanda.comandaProdutoBD import ComandaProduto
from mod_produto.produtoBD import Produto
from decimalEncoder import DecimalEncoder


bp_comanda = Blueprint('comanda', __name__, url_prefix='/comanda', template_folder='templates')


@bp_comanda.route("/")
@validaSessao
def dashboard():
    comanda = Comanda()
    lista_comandas = comanda.selectAllComandaDashboard()
    return render_template('dashboard.html', lista_comandas = lista_comandas)


@bp_comanda.route("/addComanda", methods=['POST'])
@validaSessao
def addComanda():
    try:
        comanda = Comanda()
        comanda.comanda = request.form['comanda']
        comanda.data_hora = datetime.datetime.now()
        comanda.status_pagamento = 0
        comanda.status_comanda = 0
        comanda.funcionario_id = session['id']

        _mensagem = comanda.insertNumeroComanda()

        return jsonify(erro = False, mensagem = _mensagem)

    except Exception as e:
        if len(e.args) > 1:
            _mensagem, _mensagem_exception = e.args
        else:
            _mensagem = 'Erro no banco'
            _mensagem_exception = e.args
        
        return jsonify(erro = True, mensagem = _mensagem, mensagem_exception = _mensagem_exception)


@bp_comanda.route("/formAddProdutoComanda", methods=['POST'])
@validaSessao
def formAddProdutoComanda():
    _comanda = ComandaProduto()
    _produto = Produto()
    _lista_produto = _produto.selectAll()
    _comanda.comanda_id = request.form['id_comanda']
    comanda_aux = _comanda.selectOneComanda()    
    return render_template('formComanda.html', comanda = comanda_aux, lista_produto = _lista_produto)

@bp_comanda.route("/addProdutoComanda", methods=['POST'])
@validaSessao
def addProdutoComanda():
    try:
        _comanda_produto = ComandaProduto()
        _produto = Produto()
        _produto.id_produto = request.form['id_produto']
        _produto.selectOne()
        _comanda_produto.funcionario_id = session['id']
        _comanda_produto.produto_id = request.form['id_produto']
        _comanda_produto.comanda_id = request.form['id_comanda']
        _comanda_produto.quantidade = request.form['quantidade']
        _comanda_produto.valor_unitario = _produto.valor_unitario

        _mensagem = _comanda_produto.insertProdutoComanda()

        return jsonify(erro = False, mensagem = _mensagem)


    except Exception as e:
        if len(e.args) > 1:
            _mensagem, _mensagem_exception = e.args
        else:
            _mensagem = 'Erro no banco'
            _mensagem_exception = e.args
        
        return jsonify(erro = True, mensagem = _mensagem, mensagem_exception = _mensagem_exception)

