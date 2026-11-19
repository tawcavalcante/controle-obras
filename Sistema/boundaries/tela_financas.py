from datetime import date
from boundaries.tela_base import TelaBase
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from entities.enums import CategoriaCusto


class TelaFinancas(TelaBase):
    def __init__(self, ctrl_obra: ControladorObra, ctrl_financas: ControladorFinancas):
        self.ctrl_obra = ctrl_obra
        self.ctrl_financas = ctrl_financas

    def exibir(self):
        while True:
            self.limpar_tela()
            self.cabecalho("Gerenciar Finanças")
            print("  1) Registrar Receita")
            print("  2) Registrar Despesa")
            print("  3) Consultar Saldo Atual da Obra")
            print("  0) Voltar ao Menu Principal")
            print("-" * 60)

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                self._registrar_receita()
            elif opcao == 2:
                self._registrar_despesa()
            elif opcao == 3:
                self._consultar_saldo()
            elif opcao == 0:
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 3.")
                self.pausar()

    def _registrar_receita(self):
        self.cabecalho("Registrar Receita")
        obra = self.selecionar_obra(self.ctrl_obra)
        if not obra:
            return

        valor = self.ler_float("Valor da receita (R$): ")
        origem = self.ler_texto("Origem (ex: Caixa Construtora, Cliente): ")
        descricao = self.ler_texto("Descrição: ")

        try:
            self.ctrl_financas.registrar_receita(
                valor=valor,
                origem=origem,
                data=date.today(),
                descricao=descricao,
                obra=obra,
            )
            print(f"\n[OK] Receita de R$ {valor:.2f} registrada na obra '{obra.nome}'.")
        except ValueError as e:
            print(f"\n[RECUSADO] {e}")

        self.pausar()

    def _registrar_despesa(self):
        self.cabecalho("Registrar Despesa")
        obra = self.selecionar_obra(self.ctrl_obra)
        if not obra:
            return

        valor = self.ler_float("Valor da despesa (R$): ")
        categoria = self.selecionar_enum(CategoriaCusto, "Categoria da Despesa")
        descricao = self.ler_texto("Descrição (ex: 50 sacos de cimento): ")

        try:
            self.ctrl_financas.registrar_despesa(
                valor=valor,
                categoria=categoria,
                data=date.today(),
                descricao=descricao,
                obra=obra,
            )
            print(f"\n[OK] Despesa de R$ {valor:.2f} ({self.formatar_enum(categoria)}) registrada na obra '{obra.nome}'.")
        except ValueError as e:
            print(f"\n[RECUSADO] {e}")

        self.pausar()

    def _consultar_saldo(self):
        self.cabecalho("Saldo Atual da Obra")
        obra = self.selecionar_obra(self.ctrl_obra)
        if not obra:
            return

        saldo = self.ctrl_financas.calcular_saldo_atual(obra)
        print(f"\nObra: {obra.nome}")
        print(f"Orçamento Previsto: R$ {obra.orcamento_previsto:.2f}")
        print(f"Saldo Atual em Caixa: R$ {saldo:.2f}")
        self.pausar()