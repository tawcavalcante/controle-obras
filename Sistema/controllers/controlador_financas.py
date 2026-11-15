from entities.obra import Obra
from entities.receita import Receita
from entities.despesa import Despesa
from entities.enums import CategoriaCusto
from datetime import date

class ControladorFinancas:
    def __init__(self):
        self._proximo_id_mov = 1

    def registrar_receita(self, valor: float, origem: str, data: date,descricao: str, obra: Obra) -> None:
        # segurança se o valor for negarivo
        if valor <= 0:
            raise ValueError("O valor da movimentação deve ser positivo.")
            
        nova_receita = Receita(self._proximo_id_mov, valor, data, descricao, origem)
        obra.adicionar_movimentacao(nova_receita)
        self._proximo_id_mov += 1

    def registrar_despesa(self, valor: float, categoria: CategoriaCusto, data: date, descricao: str, obra: Obra) -> None:
        # segurança se o valor for negativo
        if valor <= 0:
            raise ValueError("O valor da movimentação deve ser positivo.")
            
        nova_despesa = Despesa(self._proximo_id_mov, valor, data,descricao, categoria, 0)
        obra.adicionar_movimentacao(nova_despesa)
        self._proximo_id_mov += 1

    def calcular_saldo_atual(self, obra: Obra) -> float:
        saldo = 0.0
        for mov in obra.movimentacoes:
            saldo += mov.calcular_impacto_saldo()
        return saldo