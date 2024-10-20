from flask import render_template
from app.blueprints.main import main_bp

@main_bp.route("/")
def main():
    return render_template('InicialPageFiles/inicialPage.html')

@main_bp.route("/central")
def central():
    return render_template('CentralPageFiles/index.html')

"""
@main_bp.route("/nome_da_rota")
def nome_da_funcao():
    return render_template('pasta/arquivo') #caminho

"""