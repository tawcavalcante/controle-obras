from boundaries.tela_base import TelaBase
from boundaries.dashboard import Dashboard
from boundaries.tela_obra import TelaObra
from boundaries.tela_documento import TelaDocumento
from boundaries.tela_financas import TelaFinancas
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

        self.tela_obra = TelaObra(self.ctrl_obra)
        self.tela_documento = TelaDocumento(self.ctrl_obra)
        self.tela_financas = TelaFinancas(self.ctrl_obra, self.ctrl_financas)

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
                self.tela_obra.exibir()
            elif opcao == 2:
                self.tela_documento.exibir()
            elif opcao == 3:
                self.tela_financas.exibir()
            elif opcao == 4:
                self._exibir_dashboard()
            elif opcao == 0:
                print("\nEncerrando o sistema...")
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 4.")
                self.pausar()

    def _exibir_dashboard(self):
        self.limpar_tela()
        self.cabecalho("Dashboard / Extrato Financeiro")
        obra = self.selecionar_obra(self.ctrl_obra)
        if not obra:
            return

        self.dashboard.gerar_extrato_financeiro(
            obra=obra,
            ctrl_financas=self.ctrl_financas,
        )
        self.pausar()