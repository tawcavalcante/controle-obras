from datetime import date
from database.conexao import obter_conexao
from entities.obra import Obra
from entities.receita import Receita
from entities.despesa import Despesa
from entities.enums import CategoriaCusto


class ControladorFinancas:
    def registrar_receita(self, valor: float, origem: str, data: date, descricao: str, obra: Obra) -> None:
        if valor <= 0:
            raise ValueError("O valor da movimentação deve ser positivo.")

        data_iso = data.isoformat()
        origem_limpa = origem.strip()
        desc_limpa = descricao.strip()

        with obter_conexao() as conn:
            cursor = conn.execute(
                """
                INSERT INTO movimentacoes (
                    obra_id, tipo_mov, valor, data_ocorrencia, descricao, origem_recurso
                ) VALUES (?, 'RECEITA', ?, ?, ?, ?)
                """,
                (obra.id, valor, data_iso, desc_limpa, origem_limpa),
            )
            novo_id = cursor.lastrowid

        nova_receita = Receita(novo_id, valor, data, desc_limpa, origem_limpa)
        obra.adicionar_movimentacao(nova_receita)

    def registrar_despesa(self, valor: float, categoria: CategoriaCusto, data: date, descricao: str, obra: Obra) -> None:
        if valor <= 0:
            raise ValueError("O valor da movimentação deve ser positivo.")

        data_iso = data.isoformat()
        desc_limpa = descricao.strip()
        id_comprovante = 0

        with obter_conexao() as conn:
            cursor = conn.execute(
                """
                INSERT INTO movimentacoes (
                    obra_id, tipo_mov, valor, data_ocorrencia, descricao, categoria, id_comprovante
                ) VALUES (?, 'DESPESA', ?, ?, ?, ?, ?)
                """,
                (obra.id, valor, data_iso, desc_limpa, categoria.value, id_comprovante),
            )
            novo_id = cursor.lastrowid

        nova_despesa = Despesa(novo_id, valor, data, desc_limpa, categoria, id_comprovante)
        obra.adicionar_movimentacao(nova_despesa)

    def calcular_saldo_atual(self, obra: Obra) -> float:
        saldo = 0.0
        for mov in obra.movimentacoes:
            saldo += mov.calcular_impacto_saldo()
        return saldo

    def excluir_movimentacao(self, id_mov: int, obra: Obra) -> bool:
        with obter_conexao() as conn:
            cursor = conn.execute("DELETE FROM movimentacoes WHERE id = ?", (id_mov,))
            if cursor.rowcount > 0:
                obra.movimentacoes[:] = [m for m in obra.movimentacoes if m.id != id_mov]
                return True
            return False

    def resumo_gastos_por_categoria(self, obra: Obra) -> dict[str, float]:
        totais: dict[str, float] = {}
        for mov in obra.movimentacoes:
            if isinstance(mov, Despesa):
                nome_cat = mov.categoria.name.replace("_", " ").title()
                totais[nome_cat] = totais.get(nome_cat, 0.0) + mov.valor
        return totais