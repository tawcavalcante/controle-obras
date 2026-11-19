from boundaries.tela_base import TelaBase
from controllers.controlador_obra import ControladorObra
from entities.documento import Documento
from entities.enums import TipoDocumento


class TelaDocumento(TelaBase):
    def __init__(self, ctrl_obra: ControladorObra):
        self.ctrl_obra = ctrl_obra
        self._proximo_id_doc = 1

    def exibir(self):
        while True:
            self.limpar_tela()
            self.cabecalho("Gerenciar Documentos")
            print("  1) Anexar Documento a uma Obra")
            print("  2) Listar e Validar Documentos de uma Obra")
            print("  0) Voltar ao Menu Principal")
            print("-" * 60)

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                self._anexar_documento()
            elif opcao == 2:
                self._listar_documentos()
            elif opcao == 0:
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 2.")
                self.pausar()

    def _anexar_documento(self):
        self.cabecalho("Anexar Documento")
        obra = self.selecionar_obra(self.ctrl_obra)
        if not obra:
            return

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
        print(f"\n[OK] Documento '{doc.nome_arquivo}' ({self.formatar_enum(doc.tipo)}) anexado à obra '{obra.nome}'.")
        self.pausar()

    def _listar_documentos(self):
        self.cabecalho("Documentos da Obra")
        obra = self.selecionar_obra(self.ctrl_obra)
        if not obra:
            return

        if not obra.documentos:
            print(f"\nA obra '{obra.nome}' ainda não possui documentos anexados.")
        else:
            print(f"\nDocumentos de '{obra.nome}':")
            for doc in obra.documentos:
                status = "Válido" if doc.validar_integridade() else "Inválido"
                print(
                    f"  ID: {doc.id} | Arquivo: {doc.nome_arquivo} "
                    f"| Tipo: {self.formatar_enum(doc.tipo)} | Integridade: {status}"
                )
        self.pausar()