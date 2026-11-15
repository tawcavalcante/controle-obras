from entities.obra import Obra
from entities.enums import StatusObra
from datetime import date

class ControladorObra:
    def __init__(self):
        self.obras: list[Obra] = []
        self._proximo_id = 1

    def cadastrar_obra(self, nome:str, localizacao: str, orcamento: float, data_inicio: date) -> Obra:
        # validacao
        if not nome or not nome.strip():
            raise ValueError("Não é possível cadastrar obra sem nome.")
        if orcamento < 0:
            raise ValueError("O orçamento inicial não pode ser menor que zero.")

        nova_obra = Obra (
            id_obra=self._proximo_id,
            nome=nome,
            localizacao_maps=localizacao,
            orcamento_previsto=orcamento,
            status=StatusObra.PROJETO
        )

        self.obras.append(nova_obra)
        self._proximo_id +=1
        return nova_obra

    def buscar_obra(self, id_obra: int) -> Obra:
        for obra in self.obras:
            if obra.id == id_obra:
                return obra
        raise ValueError("Obra não encontrada.")

    def atualizar_status_obra(self, id_obra: int, novo_status:StatusObra) -> bool:
        obra = self.buscar_obra(id_obra)
        if obra:
            obra.status = novo_status
            return True
        return False