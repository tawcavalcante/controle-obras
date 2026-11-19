from boundaries.tela_base import TelaBase
from boundaries.dashboard import Dashboard
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas


class MenuPrincipal(TelaBase):
    def __init__(
        self,
        ctrl_obra: ControladorObra,
        ctrl_financas: ControladorFinancas,
        dashboard: Dashboard,
    ):
        self.ctrl_obra = ctrl_obra
        self.ctrl_financas = ctrl_financas
        self.dashboard = dashboard

    def exibir(self):
        while True:
            self.limpar_tela()
            self.cabecalho("Sistema de Gestão de Obras - Menu Principal")
            print("  1) Gerenciar Obras")
            print("  2) Gerenciar Documentos")
            print("  3) Gerenciar Finanças")
            print("  4) Visualizar Dashboard / Extrato")
            print("  0) Sair do Sistema")
            print("-" * 60)

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                print("\n[INFO] Submenu de Obras em construção...")
                self.pausar()
            elif opcao == 2:
                print("\n[INFO] Submenu de Documentos em construção...")
                self.pausar()
            elif opcao == 3:
                print("\n[INFO] Submenu de Finanças em construção...")
                self.pausar()
            elif opcao == 4:
                print("\n[INFO] Dashboard em construção...")
                self.pausar()
            elif opcao == 0:
                print("\nEncerrando o sistema...")
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 4.")
                self.pausar()