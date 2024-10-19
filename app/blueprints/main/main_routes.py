from flask import render_template
from app.blueprints.main import main_bp

@main_bp.route("/")
def main():
    return render_template('InicialPageFiles/inicialPage.html')