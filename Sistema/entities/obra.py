from entities.enums import StatusObra
from entities.movimentacao_financeira import MovimentacaoFinanceira
from entities.documento import Documento

class Obra:
    def __init__(self, id_obra: int, nome: str, localizacao_maps: str, orcamento_previsto: float, status: StatusObra):
        self.id = id_obra
        self.nome = nome
        self.localizacao_maps = localizacao_maps
        self.orcamento_previsto = orcamento_previsto
        self.status = status

        self.movimentacoes: list[MovimentacaoFinanceira] = []
        self.documentos: list[Documento] = []

    def adicionar_movimentacao(self, movimentacao: MovimentacaoFinanceira) -> None: 
        self.movimentacoes.append(movimentacao)

    def adicionar_documento(self, documento: Documento) -> None:
        self.documentos.append(documento)

