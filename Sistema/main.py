from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from boundaries.menu_principal import MenuPrincipal


def main():
    ctrl_obra = ControladorObra()
    ctrl_financas = ControladorFinancas()

    menu = MenuPrincipal(
        ctrl_obra=ctrl_obra,
        ctrl_financas=ctrl_financas,
    )
    menu.exibir()


if __name__ == "__main__":
    main()