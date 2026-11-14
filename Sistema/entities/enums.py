from enum import Enum

class StatusObra(Enum):
    PROJETO = 1
    FUNDACAO = 2
    ESTRUTURA = 3
    ACABAMENTO = 4
    FINALIZADO = 6
    ENTREGUE = 7

class CategoriaCusto(Enum):
    MAP_DE_OBRA = 1
    MATERIAIS = 2
    EQUIPAMENTO = 3
    TAXAS = 4

class TipoDocumento(Enum):
    PLANTA = 1
    ALVARA = 2
    CONTRATO = 3
    RECIBO = 4
    OUTRO = 5

    