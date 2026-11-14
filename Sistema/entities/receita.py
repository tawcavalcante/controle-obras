from entities.movimentacao_financeira import MovimentacaoFinanceira
from datetime import date

class Receita(MovimentacaoFinanceira):
    def __init__(self, id_mov: int, valor: float, data_ocorrencia: date, descricao: str, origem_recurso: str):
        super().__init__(id_mov, valor, data_ocorrencia, descricao)

        self.origem_recurso = origem_recurso

    def calcular_impacto_saldo(self) -> float:
        return self._valor #Valor positivo
