import sys
from PySide6.QtWidgets import QApplication
from database.conexao import inicializar_banco
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from boundaries.gui.janela_principal import JanelaPrincipal


def main():
    inicializar_banco()

    app = QApplication(sys.argv)

    ctrl_obra = ControladorObra()
    ctrl_financas = ControladorFinancas()

    janela = JanelaPrincipal(ctrl_obra=ctrl_obra, ctrl_financas=ctrl_financas)
    janela.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()