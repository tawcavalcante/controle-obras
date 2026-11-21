from datetime import date
from database.conexao import obter_conexao
from entities.obra import Obra
from entities.documento import Documento
from entities.receita import Receita
from entities.despesa import Despesa
from entities.enums import StatusObra, TipoDocumento, CategoriaCusto


class ControladorObra:
    @property
    def obras(self) -> list[Obra]:
        with obter_conexao() as conn:
            linhas = conn.execute(
                "SELECT id, nome, localizacao_maps, orcamento_previsto, status FROM obras ORDER BY id"
            ).fetchall()
        return [self._montar_obra(linha) for linha in linhas]

    def cadastrar_obra(self, nome: str, localizacao: str, orcamento: float, data_inicio: date) -> Obra:
        if not nome or not nome.strip():
            raise ValueError("Não é possível cadastrar obra sem nome.")
        if orcamento < 0:
            raise ValueError("O orçamento inicial não pode ser menor que zero.")

        status_inicial = StatusObra.PROJETO
        with obter_conexao() as conn:
            cursor = conn.execute(
                """
                INSERT INTO obras (nome, localizacao_maps, orcamento_previsto, status)
                VALUES (?, ?, ?, ?)
                """,
                (nome.strip(), localizacao.strip(), orcamento, status_inicial.value),
            )
            novo_id = cursor.lastrowid

        return Obra(
            id_obra=novo_id,
            nome=nome.strip(),
            localizacao_maps=localizacao.strip(),
            orcamento_previsto=orcamento,
            status=status_inicial,
        )

    def buscar_obra(self, id_obra: int) -> Obra:
        with obter_conexao() as conn:
            linha = conn.execute(
                "SELECT id, nome, localizacao_maps, orcamento_previsto, status FROM obras WHERE id = ?",
                (id_obra,),
            ).fetchone()

        if not linha:
            raise ValueError("Obra não encontrada.")
        return self._montar_obra(linha)

    def atualizar_status_obra(self, id_obra: int, novo_status: StatusObra) -> bool:
        with obter_conexao() as conn:
            cursor = conn.execute(
                "UPDATE obras SET status = ? WHERE id = ?",
                (novo_status.value, id_obra),
            )
            return cursor.rowcount > 0

    def _montar_obra(self, linha) -> Obra:
        obra = Obra(
            id_obra=linha["id"],
            nome=linha["nome"],
            localizacao_maps=linha["localizacao_maps"],
            orcamento_previsto=linha["orcamento_previsto"],
            status=StatusObra(linha["status"]),
        )

        with obter_conexao() as conn:
            docs = conn.execute(
                "SELECT id, nome_arquivo, tipo FROM documentos WHERE obra_id = ? ORDER BY id",
                (obra.id,),
            ).fetchall()

            movs = conn.execute(
                """
                SELECT id, tipo_mov, valor, data_ocorrencia, descricao, origem_recurso, categoria, id_comprovante
                FROM movimentacoes WHERE obra_id = ? ORDER BY id
                """,
                (obra.id,),
            ).fetchall()

        for d in docs:
            obra.adicionar_documento(
                Documento(
                    id_doc=d["id"],
                    nome_arquivo=d["nome_arquivo"],
                    tipo=TipoDocumento(d["tipo"]),
                )
            )

        for m in movs:
            data_oc = date.fromisoformat(m["data_ocorrencia"])
            if m["tipo_mov"] == "RECEITA":
                mov = Receita(
                    id_mov=m["id"],
                    valor=m["valor"],
                    data_ocorrencia=data_oc,
                    descricao=m["descricao"],
                    origem_recurso=m["origem_recurso"] or "",
                )
            else:
                mov = Despesa(
                    id_mov=m["id"],
                    valor=m["valor"],
                    data_ocorrencia=data_oc,
                    descricao=m["descricao"],
                    categoria=CategoriaCusto(m["categoria"]),
                    id_comprovante=m["id_comprovante"] or 0,
                )
            obra.adicionar_movimentacao(mov)

        return obra

    def excluir_obra(self, id_obra: int) -> bool:
        with obter_conexao() as conn:
            conn.execute("DELETE FROM movimentacoes WHERE obra_id = ?", (id_obra,))
            conn.execute("DELETE FROM documentos WHERE obra_id = ?", (id_obra,))
            cursor = conn.execute("DELETE FROM obras WHERE id = ?", (id_obra,))
            return cursor.rowcount > 0

    def excluir_documento(self, id_doc: int, obra: Obra) -> bool:
        with obter_conexao() as conn:
            cursor = conn.execute("DELETE FROM documentos WHERE id = ?", (id_doc,))
            if cursor.rowcount > 0:
                obra.documentos[:] = [d for d in obra.documentos if d.id != id_doc]
                return True
            return False