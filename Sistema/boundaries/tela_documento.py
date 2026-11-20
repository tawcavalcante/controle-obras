from boundaries.tela_base import TelaBase
from entities.obra import Obra
from entities.documento import Documento
from entities.enums import TipoDocumento


class TelaDocumento(TelaBase):
    def __init__(self):
        self._proximo_id_doc = 1

    def exibir(self, obra: Obra):
        while True:
            self.limpar_tela()
            self.cabecalho(f"Documentos — {obra.nome}")
            print("  1) Anexar Documento")
            print("  2) Listar e Validar Documentos")
            print("  0) Voltar ao Painel da Obra")
            print()

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                self._anexar_documento(obra)
            elif opcao == 2:
                self._listar_documentos(obra)
            elif opcao == 0:
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 2.")
                self.pausar()

    def _anexar_documento(self, obra: Obra):
        self.cabecalho(f"Anexar Documento — {obra.nome}")
        nome_arquivo = self.ler_texto("Nome do arquivo (ex: Alvara_Construcao.pdf): ")
        tipo = self.selecionar_enum(TipoDocumento, "Tipo de Documento")

        doc = Documento(
            id_doc=self._proximo_id_doc,
            nome_arquivo=nome_arquivo,
            tipo=tipo,
        )

        if not doc.validar_integridade():
            print("\n[RECUSADO] Nome de arquivo inválido ou vazio.")
            self.pausar()
            return

        obra.adicionar_documento(doc)
        self._proximo_id_doc += 1
        print(f"\n[OK] Documento '{doc.nome_arquivo}' ({self.formatar_enum(doc.tipo)}) anexado.")
        self.pausar()

    def _listar_documentos(self, obra: Obra):
        self.cabecalho(f"Documentos — {obra.nome}")
        if not obra.documentos:
            print("Esta obra ainda não possui documentos anexados.")
        else:
            for doc in obra.documentos:
                status = "Válido" if doc.validar_integridade() else "Inválido"
                print(
                    f"  ID: {doc.id} | Arquivo: {doc.nome_arquivo} "
                    f"| Tipo: {self.formatar_enum(doc.tipo)} | Integridade: {status}"
                )
        self.pausar()