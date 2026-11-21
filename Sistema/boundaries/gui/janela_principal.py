from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QComboBox,
    QScrollArea,
    QMessageBox,
)
from PySide6.QtCore import Qt
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra
from entities.receita import Receita
from entities.despesa import Despesa
from entities.enums import StatusObra
from boundaries.gui.estilos import ESTILO_GLOBAL
from boundaries.gui.graficos import PainelGraficos
from boundaries.gui.modais import (
    ModalNovaObra,
    ModalReceita,
    ModalDespesa,
    ModalDocumento,
    _formatar_enum,
)


def _brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class CardObraSidebar(QFrame):
    def __init__(self, obra: Obra, ativo: bool, callback_selecionar):
        super().__init__()
        self.obra_id = obra.id
        self.callback = callback_selecionar
        self.setObjectName("ItemObraSidebarAtivo" if ativo else "ItemObraSidebar")
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(3)

        lbl_nome = QLabel(obra.nome)
        lbl_nome.setStyleSheet("color: #FFFFFF; font-size: 13px; font-weight: 700; background: transparent;")

        status_txt = _formatar_enum(obra.status)
        lbl_meta = QLabel(f"{status_txt} • {obra.localizacao_maps}")
        lbl_meta.setStyleSheet(
            f"color: {'#DBEAFE' if ativo else '#8B949E'}; font-size: 11px; background: transparent;"
        )

        layout.addWidget(lbl_nome)
        layout.addWidget(lbl_meta)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.callback(self.obra_id)


class JanelaPrincipal(QMainWindow):
    def __init__(self, ctrl_obra: ControladorObra, ctrl_financas: ControladorFinancas):
        super().__init__()
        self.ctrl_obra = ctrl_obra
        self.ctrl_financas = ctrl_financas
        self.obra_atual: Obra | None = None

        self.setWindowTitle("Sistema de Gestão de Obras — Desk App IV")
        self.resize(1240, 780)
        self.setStyleSheet(ESTILO_GLOBAL)

        container = QWidget()
        self.setCentralWidget(container)
        layout_raiz = QHBoxLayout(container)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # 1. SIDEBAR ESCURA
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(270)
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(18, 24, 18, 20)
        layout_sidebar.setSpacing(14)

        logo = QLabel("GESTÃO DE OBRAS")
        logo.setObjectName("LogoTitulo")
        layout_sidebar.addWidget(logo)

        btn_nova_obra = QPushButton("+  Nova Obra")
        btn_nova_obra.setObjectName("BtnNovaObra")
        btn_nova_obra.setCursor(Qt.PointingHandCursor)
        btn_nova_obra.clicked.connect(self._abrir_modal_nova_obra)
        layout_sidebar.addWidget(btn_nova_obra)

        layout_sidebar.addSpacing(6)
        lbl_secao = QLabel("OBRAS CADASTRADAS")
        lbl_secao.setObjectName("SidebarSecao")
        layout_sidebar.addWidget(lbl_secao)

        self.layout_lista_obras = QVBoxLayout()
        self.layout_lista_obras.setSpacing(8)
        layout_sidebar.addLayout(self.layout_lista_obras)
        layout_sidebar.addStretch()

        layout_raiz.addWidget(self.sidebar)

        # 2. ÁREA PRINCIPAL CLARA
        self.area_conteudo = QWidget()
        self.layout_conteudo = QVBoxLayout(self.area_conteudo)
        self.layout_conteudo.setContentsMargins(28, 22, 28, 22)
        self.layout_conteudo.setSpacing(16)

        layout_raiz.addWidget(self.area_conteudo)

        self._carregar_obras_iniciais()

    def _carregar_obras_iniciais(self):
        obras = self.ctrl_obra.obras
        self.obra_atual = obras[0] if obras else None
        self._atualizar_interface()

    def _atualizar_interface(self):
        self._limpar_layout(self.layout_lista_obras)
        obras = self.ctrl_obra.obras

        if not obras:
            lbl_vazio = QLabel("Nenhuma obra cadastrada.")
            lbl_vazio.setStyleSheet("color: #6B7280; font-size: 12px;")
            self.layout_lista_obras.addWidget(lbl_vazio)
        else:
            for obra in obras:
                ativo = self.obra_atual is not None and obra.id == self.obra_atual.id
                card_sb = CardObraSidebar(obra, ativo, self._selecionar_obra)
                self.layout_lista_obras.addWidget(card_sb)

        self._limpar_layout(self.layout_conteudo)

        if not self.obra_atual:
            lbl_empty = QLabel("Clique em '+ Nova Obra' na barra lateral para começar.")
            lbl_empty.setStyleSheet("color: #6B7280; font-size: 16px;")
            lbl_empty.setAlignment(Qt.AlignCenter)
            self.layout_conteudo.addWidget(lbl_empty)
            return

        self.obra_atual = self.ctrl_obra.buscar_obra(self.obra_atual.id)
        obra = self.obra_atual

        saldo = self.ctrl_financas.calcular_saldo_atual(obra)
        total_entradas = sum(m.valor for m in obra.movimentacoes if isinstance(m, Receita))
        total_saidas = sum(m.valor for m in obra.movimentacoes if isinstance(m, Despesa))
        pct_orcamento = (total_saidas / obra.orcamento_previsto * 100) if obra.orcamento_previsto > 0 else 0

        # HEADER DA OBRA + ORÇAMENTO PREVISTO NO CANTO
        header = QHBoxLayout()
        info_obra = QVBoxLayout()
        info_obra.setSpacing(2)

        lbl_titulo = QLabel(obra.nome)
        lbl_titulo.setObjectName("TituloObra")
        lbl_sub = QLabel(f"ID #{obra.id}  •  Localização: {obra.localizacao_maps}")
        lbl_sub.setObjectName("SubtituloObra")

        info_obra.addWidget(lbl_titulo)
        info_obra.addWidget(lbl_sub)
        header.addLayout(info_obra)
        header.addStretch()

        # Badge discreta de Orçamento Previsto no canto direito
        pill_orc = QFrame()
        pill_orc.setStyleSheet(
            "background-color: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px;"
        )
        l_pill = QVBoxLayout(pill_orc)
        l_pill.setContentsMargins(14, 6, 14, 6)
        l_pill.setSpacing(1)
        lbl_orc_t = QLabel("ORÇAMENTO PREVISTO")
        lbl_orc_t.setStyleSheet("color: #6B7280; font-size: 10px; font-weight: 700; border: none;")
        lbl_orc_v = QLabel(f"{_brl(obra.orcamento_previsto)}  ({pct_orcamento:.0f}% usado)")
        lbl_orc_v.setStyleSheet("color: #111317; font-size: 12px; font-weight: 700; border: none;")
        l_pill.addWidget(lbl_orc_t)
        l_pill.addWidget(lbl_orc_v)
        header.addWidget(pill_orc)
        header.addSpacing(10)

        lbl_status = QLabel("Status:")
        lbl_status.setStyleSheet("color: #6B7280; font-weight: 600; margin-right: 4px;")
        header.addWidget(lbl_status)

        combo_status = QComboBox()
        combo_status.setObjectName("ComboStatus")
        for idx, st in enumerate(StatusObra):
            combo_status.addItem(_formatar_enum(st), st)
            if st == obra.status:
                combo_status.setCurrentIndex(idx)
        combo_status.currentIndexChanged.connect(
            lambda _, cb=combo_status: self._alterar_status(cb.currentData())
        )
        header.addWidget(combo_status)
        header.addSpacing(8)

        btn_excluir_obra = QPushButton("Excluir Obra")
        btn_excluir_obra.setObjectName("BtnExcluirObra")
        btn_excluir_obra.setCursor(Qt.PointingHandCursor)
        btn_excluir_obra.clicked.connect(self._confirmar_exclusao_obra)
        header.addWidget(btn_excluir_obra)

        self.layout_conteudo.addLayout(header)

        # 3 CARDS SUPERIORES: SALDO ATUAL | ENTRADAS | SAÍDAS
        row_cards = QHBoxLayout()
        row_cards.setSpacing(16)

        # Card 1: Saldo Atual (Destaque Escuro)
        card_saldo = QFrame()
        card_saldo.setObjectName("CardSaldoEscuro")
        card_saldo.setFixedHeight(112)
        l_saldo = QVBoxLayout(card_saldo)
        l_saldo.setContentsMargins(20, 14, 20, 14)

        t1 = QLabel("SALDO ATUAL")
        t1.setObjectName("CardSaldoTitulo")
        v1 = QLabel(_brl(saldo))
        v1.setObjectName("CardSaldoValor")
        v1.setStyleSheet("color: #FFFFFF; font-size: 24px; font-weight: 700;")
        r1 = QLabel("Disponível em caixa")
        r1.setObjectName("CardSaldoRodape")
        if saldo < 0:
            r1.setText("Saldo negativo em caixa")
            r1.setStyleSheet("color: #F87171; font-size: 12px; font-weight: 600;")

        l_saldo.addWidget(t1)
        l_saldo.addWidget(v1)
        l_saldo.addWidget(r1)
        row_cards.addWidget(card_saldo)

        # Card 2: Entradas (Branco)
        card_ent = QFrame()
        card_ent.setObjectName("CardBranco")
        card_ent.setFixedHeight(112)
        l_ent = QVBoxLayout(card_ent)
        l_ent.setContentsMargins(20, 14, 20, 14)

        qtd_rec = sum(1 for m in obra.movimentacoes if isinstance(m, Receita))
        t2 = QLabel("ENTRADAS (RECEITAS)")
        t2.setObjectName("CardBrancoTitulo")
        v2 = QLabel(_brl(total_entradas))
        v2.setStyleSheet("color: #15803D; font-size: 24px; font-weight: 700;")
        r2 = QLabel(f"{qtd_rec} aporte(s) registrado(s)")
        r2.setObjectName("CardBrancoRodape")

        l_ent.addWidget(t2)
        l_ent.addWidget(v2)
        l_ent.addWidget(r2)
        row_cards.addWidget(card_ent)

        # Card 3: Saídas (Branco)
        card_sai = QFrame()
        card_sai.setObjectName("CardBranco")
        card_sai.setFixedHeight(112)
        l_sai = QVBoxLayout(card_sai)
        l_sai.setContentsMargins(20, 14, 20, 14)

        qtd_desp = sum(1 for m in obra.movimentacoes if isinstance(m, Despesa))
        t3 = QLabel("SAÍDAS (DESPESAS)")
        t3.setObjectName("CardBrancoTitulo")
        v3 = QLabel(_brl(total_saidas))
        v3.setStyleSheet("color: #B91C1C; font-size: 24px; font-weight: 700;")
        r3 = QLabel(f"{qtd_desp} despesa(s) lançada(s)")
        r3.setObjectName("CardBrancoRodape")

        l_sai.addWidget(t3)
        l_sai.addWidget(v3)
        l_sai.addWidget(r3)
        row_cards.addWidget(card_sai)

        self.layout_conteudo.addLayout(row_cards)

        # CARD DE GRÁFICOS DINÂMICOS
        card_graficos = QFrame()
        card_graficos.setObjectName("CardBranco")
        card_graficos.setFixedHeight(225)
        l_graf = QVBoxLayout(card_graficos)
        l_graf.setContentsMargins(18, 12, 18, 10)
        l_graf.addWidget(PainelGraficos(self.ctrl_financas, obra))
        self.layout_conteudo.addWidget(card_graficos)

        # BARRA DE AÇÕES RÁPIDAS
        row_acoes = QHBoxLayout()
        row_acoes.setSpacing(12)

        btn_receita = QPushButton("+  Registrar Receita")
        btn_receita.setObjectName("BtnAcaoPrimario")
        btn_receita.setCursor(Qt.PointingHandCursor)
        btn_receita.clicked.connect(self._abrir_modal_receita)

        btn_despesa = QPushButton("-  Registrar Despesa")
        btn_despesa.setObjectName("BtnAcaoSecundario")
        btn_despesa.setCursor(Qt.PointingHandCursor)
        btn_despesa.clicked.connect(self._abrir_modal_despesa)

        btn_doc = QPushButton("+  Anexar Documento")
        btn_doc.setObjectName("BtnAcaoSecundario")
        btn_doc.setCursor(Qt.PointingHandCursor)
        btn_doc.clicked.connect(self._abrir_modal_documento)

        row_acoes.addWidget(btn_receita)
        row_acoes.addWidget(btn_despesa)
        row_acoes.addWidget(btn_doc)
        row_acoes.addStretch()
        self.layout_conteudo.addLayout(row_acoes)

        # COLUNAS INFERIORES: MOVIMENTAÇÕES + DOCUMENTOS
        row_listas = QHBoxLayout()
        row_listas.setSpacing(16)

        # Movimentações
        card_movs = QFrame()
        card_movs.setObjectName("CardBranco")
        l_movs = QVBoxLayout(card_movs)
        l_movs.setContentsMargins(18, 14, 18, 14)
        l_movs.setSpacing(8)

        lbl_m_titulo = QLabel("Movimentações Financeiras")
        lbl_m_titulo.setObjectName("SecaoCardTitulo")
        l_movs.addWidget(lbl_m_titulo)

        scroll_mov = QScrollArea()
        scroll_mov.setWidgetResizable(True)
        cont_mov = QWidget()
        vbox_mov = QVBoxLayout(cont_mov)
        vbox_mov.setContentsMargins(0, 0, 0, 0)
        vbox_mov.setSpacing(6)

        if not obra.movimentacoes:
            vazio_m = QLabel("Nenhuma movimentação registrada.")
            vazio_m.setStyleSheet("color: #9CA3AF; font-size: 13px;")
            vbox_mov.addWidget(vazio_m)
        else:
            for mov in reversed(obra.movimentacoes):
                linha = QFrame()
                linha.setObjectName("LinhaItem")
                hl = QHBoxLayout(linha)
                hl.setContentsMargins(12, 8, 10, 8)

                eh_receita = isinstance(mov, Receita)
                detalhe = mov.origem_recurso if eh_receita else _formatar_enum(mov.categoria)

                col_txt = QVBoxLayout()
                col_txt.setSpacing(1)
                lbl_d = QLabel(mov.descricao)
                lbl_d.setStyleSheet("font-weight: 600; color: #111317; font-size: 13px;")
                lbl_sub_m = QLabel(f"{mov.data_ocorrencia.strftime('%d/%m/%Y')} • {detalhe}")
                lbl_sub_m.setStyleSheet("color: #6B7280; font-size: 11px;")
                col_txt.addWidget(lbl_d)
                col_txt.addWidget(lbl_sub_m)

                badge = QLabel("Receita" if eh_receita else "Despesa")
                badge.setObjectName("BadgeReceita" if eh_receita else "BadgeDespesa")

                impacto = mov.calcular_impacto_saldo()
                sinal = "+" if impacto >= 0 else "-"
                lbl_val = QLabel(f"{sinal} {_brl(abs(impacto))}")
                lbl_val.setStyleSheet(
                    f"font-weight: 700; font-size: 13px; color: {'#15803D' if eh_receita else '#B91C1C'};"
                )

                btn_del_mov = QPushButton("×")
                btn_del_mov.setObjectName("BtnExcluirLinha")
                btn_del_mov.setToolTip("Excluir movimentação")
                btn_del_mov.setCursor(Qt.PointingHandCursor)
                btn_del_mov.clicked.connect(
                    lambda checked=False, m_id=mov.id, desc=mov.descricao: self._confirmar_exclusao_movimentacao(m_id, desc)
                )

                hl.addLayout(col_txt)
                hl.addStretch()
                hl.addWidget(badge)
                hl.addSpacing(8)
                hl.addWidget(lbl_val)
                hl.addSpacing(4)
                hl.addWidget(btn_del_mov)
                vbox_mov.addWidget(linha)

        vbox_mov.addStretch()
        scroll_mov.setWidget(cont_mov)
        l_movs.addWidget(scroll_mov)
        row_listas.addWidget(card_movs, stretch=3)

        # Documentos
        card_docs = QFrame()
        card_docs.setObjectName("CardBranco")
        l_docs = QVBoxLayout(card_docs)
        l_docs.setContentsMargins(18, 14, 18, 14)
        l_docs.setSpacing(8)

        lbl_d_titulo = QLabel("Documentos Anexados")
        lbl_d_titulo.setObjectName("SecaoCardTitulo")
        l_docs.addWidget(lbl_d_titulo)

        scroll_doc = QScrollArea()
        scroll_doc.setWidgetResizable(True)
        cont_doc = QWidget()
        vbox_doc = QVBoxLayout(cont_doc)
        vbox_doc.setContentsMargins(0, 0, 0, 0)
        vbox_doc.setSpacing(6)

        if not obra.documentos:
            vazio_d = QLabel("Nenhum documento anexado.")
            vazio_d.setStyleSheet("color: #9CA3AF; font-size: 13px;")
            vbox_doc.addWidget(vazio_d)
        else:
            for doc in reversed(obra.documentos):
                linha = QFrame()
                linha.setObjectName("LinhaItem")
                hl = QHBoxLayout(linha)
                hl.setContentsMargins(12, 8, 10, 8)

                col_doc = QVBoxLayout()
                col_doc.setSpacing(1)
                lbl_arq = QLabel(doc.nome_arquivo)
                lbl_arq.setStyleSheet("font-weight: 600; color: #111317; font-size: 13px;")
                lbl_tipo = QLabel(_formatar_enum(doc.tipo))
                lbl_tipo.setStyleSheet("color: #6B7280; font-size: 11px;")
                col_doc.addWidget(lbl_arq)
                col_doc.addWidget(lbl_tipo)

                badge_doc = QLabel("Válido" if doc.validar_integridade() else "Inválido")
                badge_doc.setObjectName("BadgeDocValido")

                btn_del_doc = QPushButton("×")
                btn_del_doc.setObjectName("BtnExcluirLinha")
                btn_del_doc.setToolTip("Excluir documento")
                btn_del_doc.setCursor(Qt.PointingHandCursor)
                btn_del_doc.clicked.connect(
                    lambda checked=False, d_id=doc.id, nome=doc.nome_arquivo: self._confirmar_exclusao_documento(d_id, nome)
                )

                hl.addLayout(col_doc)
                hl.addStretch()
                hl.addWidget(badge_doc)
                hl.addSpacing(4)
                hl.addWidget(btn_del_doc)
                vbox_doc.addWidget(linha)

        vbox_doc.addStretch()
        scroll_doc.setWidget(cont_doc)
        l_docs.addWidget(scroll_doc)
        row_listas.addWidget(card_docs, stretch=2)

        self.layout_conteudo.addLayout(row_listas)

    def _selecionar_obra(self, id_obra: int):
        self.obra_atual = self.ctrl_obra.buscar_obra(id_obra)
        self._atualizar_interface()

    def _alterar_status(self, novo_status: StatusObra):
        if self.obra_atual and novo_status != self.obra_atual.status:
            self.ctrl_obra.atualizar_status_obra(self.obra_atual.id, novo_status)
            self._atualizar_interface()

    def _confirmar_exclusao_obra(self):
        if not self.obra_atual:
            return
        resp = QMessageBox.question(
            self,
            "Excluir Obra",
            f"Tem certeza que deseja apagar '{self.obra_atual.nome}' e todos os seus registros?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp == QMessageBox.Yes:
            self.ctrl_obra.excluir_obra(self.obra_atual.id)
            self._carregar_obras_iniciais()

    def _confirmar_exclusao_movimentacao(self, id_mov: int, descricao: str):
        if not self.obra_atual:
            return
        resp = QMessageBox.question(
            self,
            "Excluir Movimentação",
            f"Deseja remover a movimentação '{descricao}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp == QMessageBox.Yes:
            self.ctrl_financas.excluir_movimentacao(id_mov, self.obra_atual)
            self._atualizar_interface()

    def _confirmar_exclusao_documento(self, id_doc: int, nome_arquivo: str):
        if not self.obra_atual:
            return
        resp = QMessageBox.question(
            self,
            "Excluir Documento",
            f"Deseja remover o documento '{nome_arquivo}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if resp == QMessageBox.Yes:
            self.ctrl_obra.excluir_documento(id_doc, self.obra_atual)
            self._atualizar_interface()

    def _abrir_modal_nova_obra(self):
        modal = ModalNovaObra(self.ctrl_obra, self)
        if modal.exec() and modal.obra_criada:
            self.obra_atual = modal.obra_criada
            self._atualizar_interface()

    def _abrir_modal_receita(self):
        if not self.obra_atual:
            return
        modal = ModalReceita(self.ctrl_financas, self.obra_atual, self)
        if modal.exec():
            self._atualizar_interface()

    def _abrir_modal_despesa(self):
        if not self.obra_atual:
            return
        modal = ModalDespesa(self.ctrl_financas, self.obra_atual, self)
        if modal.exec():
            self._atualizar_interface()

    def _abrir_modal_documento(self):
        if not self.obra_atual:
            return
        modal = ModalDocumento(self.obra_atual, self)
        if modal.exec():
            self._atualizar_interface()

    def _limpar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self._limpar_layout(item.layout())