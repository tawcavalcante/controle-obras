from datetime import date
from boundaries.tela_base import TelaBase
from boundaries.tela_gerenciar_obra import TelaGerenciarObra
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas


class MenuPrincipal(TelaBase):
    def __init__(self, ctrl_obra: ControladorObra, ctrl_financas: ControladorFinancas):
        self.ctrl_obra = ctrl_obra
        self.ctrl_financas = ctrl_financas
        self.tela_gerenciar_obra = TelaGerenciarObra(ctrl_obra, ctrl_financas)

    def exibir(self):
        while True:
            self.limpar_tela()
            self.cabecalho("Sistema de Gestão de Obras — Menu Principal")
            print("  1) Cadastrar Nova Obra")
            print("  2) Listar Obras Cadastradas")
            print("  3) Acessar Painel de uma Obra")
            print("  0) Sair do Sistema")
            print()

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                self._cadastrar_obra()
            elif opcao == 2:
                self._listar_obras()
            elif opcao == 3:
                self._acessar_painel_obra()
            elif opcao == 0:
                print("\nEncerrando o Sistema de Gestão de Obras...")
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 3.")
                self.pausar()

    def _cadastrar_obra(self):
        self.cabecalho("Cadastrar Nova Obra")
        nome = self.ler_texto("Nome da obra: ")
        localizacao = self.ler_texto("Localização (endereço/cidade): ")
        orcamento = self.ler_float("Orçamento previsto (R$): ")

        try:
            obra = self.ctrl_obra.cadastrar_obra(
                nome=nome,
                localizacao=localizacao,
                orcamento=orcamento,
                data_inicio=date.today(),
            )
            print(f"\n[OK] Obra '{obra.nome}' cadastrada com ID {obra.id}!")
        except ValueError as e:
            print(f"\n[RECUSADO] {e}")

        self.pausar()

    def _listar_obras(self):
        self.cabecalho("Obras Cadastradas")
        if not self.ctrl_obra.obras:
            print("Nenhuma obra cadastrada no momento.")
        else:
            for obra in self.ctrl_obra.obras:
                print(
                    f"  [{obra.id}] {obra.nome} | Local: {obra.localizacao_maps} "
                    f"| Orçamento: R$ {obra.orcamento_previsto:.2f} "
                    f"| Status: {self.formatar_enum(obra.status)}"
                )
        self.pausar()

    def _acessar_painel_obra(self):
        obra = self.selecionar_obra(self.ctrl_obra)
        if obra:
            self.tela_gerenciar_obra.exibir(obra)