from entities.movimentacao_financeira import MovimentacaoFinanceira
from entities.enums import CategoriaCusto
from datetime import date

class Despesa(MovimentacaoFinanceira):
    def __init__(self, id_mov: int, valor: float, data_ocorrencia: date, descricao: str, categoria: CategoriaCusto, id_comprovante: int):
        super().__init__(id_mov, valor, data_ocorrencia, descricao)

        self.categoria = categoria
        self.id_comprovante = id_comprovante

    def calcular_impacto_saldo(self) -> float:
        return -self._valor #valor negativo
    