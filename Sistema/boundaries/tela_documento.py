from boundaries.tela_base import TelaBase
from database.conexao import obter_conexao
from entities.obra import Obra
from entities.documento import Documento
from entities.enums import TipoDocumento


class TelaDocumento(TelaBase):
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

        doc_temporario = Documento(
            id_doc=0,
            nome_arquivo=nome_arquivo,
            tipo=tipo,
        )

        if not doc_temporario.validar_integridade():
            print("\n[RECUSADO] Nome de arquivo inválido ou vazio.")
            self.pausar()
            return

        nome_limpo = nome_arquivo.strip()
        with obter_conexao() as conn:
            cursor = conn.execute(
                """
                INSERT INTO documentos (obra_id, nome_arquivo, tipo)
                VALUES (?, ?, ?)
                """,
                (obra.id, nome_limpo, tipo.value),
            )
            novo_id = cursor.lastrowid

        doc = Documento(
            id_doc=novo_id,
            nome_arquivo=nome_limpo,
            tipo=tipo,
        )
        obra.adicionar_documento(doc)
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