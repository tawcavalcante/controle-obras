from boundaries.tela_base import TelaBase
from boundaries.tela_documento import TelaDocumento
from boundaries.tela_financas import TelaFinancas
from boundaries.dashboard import Dashboard
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra
from entities.enums import StatusObra


class TelaGerenciarObra(TelaBase):
    def __init__(self, ctrl_obra: ControladorObra, ctrl_financas: ControladorFinancas):
        self.ctrl_obra = ctrl_obra
        self.ctrl_financas = ctrl_financas
        self.tela_documento = TelaDocumento()
        self.tela_financas = TelaFinancas(ctrl_financas)
        self.dashboard = Dashboard()

    def exibir(self, obra: Obra):
        while True:
            self.limpar_tela()
            status_str = self.formatar_enum(obra.status)
            self.cabecalho(f"Painel da Obra: {obra.nome} [{status_str}]")
            print(f"  Local: {obra.localizacao_maps} | Orçamento: R$ {obra.orcamento_previsto:.2f}\n")
            print("  1) Finanças")
            print("  2) Documentos")
            print("  3) Atualizar Status da Obra")
            print("  4) Visualizar Dashboard / Extrato")
            print("  0) Voltar ao Menu Principal")
            print()

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                self.tela_financas.exibir(obra)
            elif opcao == 2:
                self.tela_documento.exibir(obra)
            elif opcao == 3:
                self._atualizar_status(obra)
            elif opcao == 4:
                self.limpar_tela()
                self.dashboard.gerar_extrato_financeiro(obra, self.ctrl_financas)
                self.pausar()
            elif opcao == 0:
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 4.")
                self.pausar()

    def _atualizar_status(self, obra: Obra):
        self.cabecalho(f"Atualizar Status — {obra.nome}")
        print(f"Status atual: {self.formatar_enum(obra.status)}")
        novo_status = self.selecionar_enum(StatusObra, f"Novo Status para '{obra.nome}'")

        self.ctrl_obra.atualizar_status_obra(obra.id, novo_status)
        print(f"\n[OK] Status da obra '{obra.nome}' atualizado para '{self.formatar_enum(novo_status)}'.")
        self.pausar()