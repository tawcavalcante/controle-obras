from abc import ABC, abstractmethod
from datetime import date

class MovimentacaoFinanceira(ABC):
    def __init__(self, id_mov: int, valor: float, data_ocorrencia: date, descricao: str):
        self._id = id_mov
        self._valor = valor
        self._data_ocorrencia = data_ocorrencia
        self._descricao = descricao

    @abstractmethod
    def calcular_impacto_saldo(self) -> float:
        pass

