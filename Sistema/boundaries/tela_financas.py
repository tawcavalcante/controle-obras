from datetime import date
from boundaries.tela_base import TelaBase
from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra
from entities.enums import CategoriaCusto


class TelaFinancas(TelaBase):
    def __init__(self, ctrl_financas: ControladorFinancas):
        self.ctrl_financas = ctrl_financas

    def exibir(self, obra: Obra):
        while True:
            self.limpar_tela()
            self.cabecalho(f"Finanças — {obra.nome}")
            print("  1) Registrar Receita")
            print("  2) Registrar Despesa")
            print("  3) Consultar Saldo Atual")
            print("  0) Voltar ao Painel da Obra")
            print()

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                self._registrar_receita(obra)
            elif opcao == 2:
                self._registrar_despesa(obra)
            elif opcao == 3:
                self._consultar_saldo(obra)
            elif opcao == 0:
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 3.")
                self.pausar()

    def _registrar_receita(self, obra: Obra):
        self.cabecalho(f"Registrar Receita — {obra.nome}")
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
            print(f"\n[OK] Receita de R$ {valor:.2f} registrada.")
        except ValueError as e:
            print(f"\n[RECUSADO] {e}")

        self.pausar()

    def _registrar_despesa(self, obra: Obra):
        self.cabecalho(f"Registrar Despesa — {obra.nome}")
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
            print(f"\n[OK] Despesa de R$ {valor:.2f} ({self.formatar_enum(categoria)}) registrada.")
        except ValueError as e:
            print(f"\n[RECUSADO] {e}")

        self.pausar()

    def _consultar_saldo(self, obra: Obra):
        self.cabecalho(f"Saldo Atual — {obra.nome}")
        saldo = self.ctrl_financas.calcular_saldo_atual(obra)
        print(f"Orçamento Previsto: R$ {obra.orcamento_previsto:.2f}")
        print(f"Saldo Atual em Caixa: R$ {saldo:.2f}")
        self.pausar()