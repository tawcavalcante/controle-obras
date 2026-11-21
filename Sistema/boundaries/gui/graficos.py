from collections import defaultdict
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra
from entities.despesa import Despesa


class PainelGraficos(QWidget):
    def __init__(self, ctrl_financas: ControladorFinancas, obra: Obra, parent=None):
        super().__init__(parent)
        self.ctrl_financas = ctrl_financas
        self.obra = obra

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Gráfico 1: Gastos por Categoria (Rosca com Valor + %)
        box_cat = QVBoxLayout()
        lbl_cat = QLabel("Gastos por Categoria")
        lbl_cat.setStyleSheet("font-size: 13px; font-weight: 700; color: #111317;")
        box_cat.addWidget(lbl_cat)
        box_cat.addWidget(self._criar_canvas_categorias())

        # Gráfico 2: Total Gasto por Dia (Linha)
        box_linha = QVBoxLayout()
        lbl_linha = QLabel("Total Gasto por Dia")
        lbl_linha.setStyleSheet("font-size: 13px; font-weight: 700; color: #111317;")
        box_linha.addWidget(lbl_linha)
        box_linha.addWidget(self._criar_canvas_evolucao_gastos())

        layout.addLayout(box_cat, stretch=1)
        layout.addLayout(box_linha, stretch=1)

    def _criar_canvas_categorias(self) -> FigureCanvas:
        fig = Figure(figsize=(4.4, 2.3), dpi=100)
        fig.patch.set_facecolor("#FFFFFF")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#FFFFFF")

        dados = self.ctrl_financas.resumo_gastos_por_categoria(self.obra)
        if not dados:
            ax.text(
                0.5, 0.5, "Sem despesas registradas",
                ha="center", va="center", color="#9CA3AF", fontsize=10
            )
            ax.axis("off")
        else:
            labels = list(dados.keys())
            valores = list(dados.values())
            total = sum(valores)
            cores = ["#2563EB", "#181A20", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

            wedges, _ = ax.pie(
                valores,
                startangle=90,
                colors=cores[: len(valores)],
                wedgeprops={"width": 0.42, "edgecolor": "#FFFFFF", "linewidth": 2},
            )

            legendas = []
            for l, v in zip(labels, valores):
                pct = (v / total * 100) if total > 0 else 0
                val_fmt = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                legendas.append(f"{l}: R$ {val_fmt} ({pct:.1f}%)")

            ax.legend(
                wedges,
                legendas,
                loc="center left",
                bbox_to_anchor=(0.92, 0.5),
                frameon=False,
                fontsize=8,
            )
            fig.subplots_adjust(left=0.02, right=0.50, top=0.95, bottom=0.05)

        return FigureCanvas(fig)

    def _criar_canvas_evolucao_gastos(self) -> FigureCanvas:
        fig = Figure(figsize=(4.4, 2.3), dpi=100)
        fig.patch.set_facecolor("#FFFFFF")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#FFFFFF")

        despesas = [m for m in self.obra.movimentacoes if isinstance(m, Despesa)]
        if not despesas:
            ax.text(
                0.5, 0.5, "Sem histórico de gastos",
                ha="center", va="center", color="#9CA3AF", fontsize=10
            )
            ax.axis("off")
            return FigureCanvas(fig)

        # Soma todas as despesas do mesmo dia em um único ponto
        por_data: dict = defaultdict(float)
        for d in sorted(despesas, key=lambda x: x.data_ocorrencia):
            por_data[d.data_ocorrencia] += d.valor

        datas_str = [dt.strftime("%d/%m") for dt in por_data.keys()]
        valores = list(por_data.values())
        indices = list(range(len(datas_str)))

        ax.plot(
            indices,
            valores,
            color="#2563EB",
            linewidth=2.4,
            marker="o",
            markersize=6,
            markerfacecolor="#2563EB",
            markeredgecolor="#FFFFFF",
            markeredgewidth=1.5,
            zorder=4,
        )

        if len(indices) > 1:
            ax.fill_between(indices, valores, color="#2563EB", alpha=0.10, zorder=3)

        ax.set_xticks(indices)
        ax.set_xticklabels(datas_str)
        ax.grid(axis="y", linestyle="--", alpha=0.35, zorder=0)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#E5E7EB")
        ax.spines["bottom"].set_color("#E5E7EB")
        ax.tick_params(axis="both", labelsize=8.5, colors="#4B5563")

        topo = max(valores) if max(valores) > 0 else 1000
        ax.set_ylim(0, topo * 1.28)
        ax.set_xlim(-0.4, max(len(indices) - 0.6, 0.4))

        for i, v in enumerate(valores):
            val_fmt = f"{v:,.0f}".replace(",", ".")
            ax.text(
                i,
                v + (topo * 0.05),
                f"R$ {val_fmt}",
                ha="center",
                va="bottom",
                fontsize=8,
                fontweight="bold",
                color="#111317",
            )

        fig.tight_layout()
        return FigureCanvas(fig)