from entities.obra import Obra
from entities.receita import Receita
from entities.despesa import Despesa
from entities.enums import CategoriaCusto
from datetime import date

class ControladorFinancas:
    def __init__(self):
        self._proximo_id_mov = 1

    def registrar_receita(self, id_obra: int, valor: float, origem: str, data: date,descricao: str, obra: Obra) -> None:
        nova_receita = Receita(self._proximo_id_mov, valor, data, descricao, origem)
        obra.adicionar_movimentacao(nova_receita)
        self._proximo_id_mov += 1

    def registrar_despesa(self, id_obra: int, valor: float, categoria: CategoriaCusto, data: date, descricao: str, obra: Obra) -> None:
        nova_despesa = Despesa(self._proximo_id_mov, valor, data,descricao, categoria, 0)
        obra.adicionar_movimentacao(nova_despesa)
        self._proximo_id_mov += 1

    def calcular_saldo_atual(self, id_obra: int, obra: Obra) -> float:
        saldo = 0.0
        for mov in obra.movimentacoes:
            saldo += mov.calcular_impacto_saldo()
        return saldo