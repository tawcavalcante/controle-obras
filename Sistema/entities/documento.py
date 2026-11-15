from entities.enums import TipoDocumento

class Documento:
    def __init__(self, id_doc:int, nome_arquivo: str, tipo: TipoDocumento):
        self.id  = id_doc
        self.nome_arquivo = nome_arquivo
        self.tipo = tipo

    def validar_integridade(self) -> bool:
        if not self.nome_arquivo.strip():
            return False
        return True

    