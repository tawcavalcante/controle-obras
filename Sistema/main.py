from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from boundaries.dashboard import Dashboard
from boundaries.menu_principal import MenuPrincipal


def main():
    ctrl_obra = ControladorObra()
    ctrl_financas = ControladorFinancas()
    dashboard = Dashboard()

    menu = MenuPrincipal(
        ctrl_obra=ctrl_obra,
        ctrl_financas=ctrl_financas,
        dashboard=dashboard,
    )
    menu.exibir()


if __name__ == "__main__":
    main()