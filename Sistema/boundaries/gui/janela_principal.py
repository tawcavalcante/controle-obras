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
)
from PySide6.QtCore import Qt
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra
from entities.receita import Receita
from entities.enums import StatusObra
from boundaries.gui.estilos import ESTILO_GLOBAL
from boundaries.gui.modais import (
    ModalNovaObra,
    ModalReceita,
    ModalDespesa,
    ModalDocumento,
    _formatar_enum,
)


class JanelaPrincipal(QMainWindow):
    def __init__(self, ctrl_obra: ControladorObra, ctrl_financas: ControladorFinancas):
        super().__init__()
        self.ctrl_obra = ctrl_obra
        self.ctrl_financas = ctrl_financas
        self.obra_atual: Obra | None = None

        self.setWindowTitle("Sistema de Gestão de Obras — Desk App IV")
        self.resize(1160, 720)
        self.setStyleSheet(ESTILO_GLOBAL)

        container = QWidget()
        self.setCentralWidget(container)
        layout_raiz = QHBoxLayout(container)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.setSpacing(0)

        # 1. SIDEBAR ESCURA
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(260)
        layout_sidebar = QVBoxLayout(self.sidebar)
        layout_sidebar.setContentsMargins(20, 26, 20, 20)
        layout_sidebar.setSpacing(14)

        logo = QLabel("GESTÃO DE OBRAS")
        logo.setObjectName("LogoTitulo")
        layout_sidebar.addWidget(logo)

        btn_nova_obra = QPushButton("+  Nova Obra")
        btn_nova_obra.setObjectName("BtnNovaObra")
        btn_nova_obra.setCursor(Qt.PointingHandCursor)
        btn_nova_obra.clicked.connect(self._abrir_modal_nova_obra)
        layout_sidebar.addWidget(btn_nova_obra)

        layout_sidebar.addSpacing(8)
        lbl_secao = QLabel("OBRAS CADASTRADAS")
        lbl_secao.setObjectName("SidebarSecao")
        layout_sidebar.addWidget(lbl_secao)

        self.layout_lista_obras = QVBoxLayout()
        self.layout_lista_obras.setSpacing(6)
        layout_sidebar.addLayout(self.layout_lista_obras)
        layout_sidebar.addStretch()

        layout_raiz.addWidget(self.sidebar)

        # 2. ÁREA PRINCIPAL CLARA
        self.area_conteudo = QWidget()
        self.layout_conteudo = QVBoxLayout(self.area_conteudo)
        self.layout_conteudo.setContentsMargins(32, 28, 32, 28)
        self.layout_conteudo.setSpacing(20)

        layout_raiz.addWidget(self.area_conteudo)

        self._carregar_obras_iniciais()

    def _carregar_obras_iniciais(self):
        obras = self.ctrl_obra.obras
        if obras:
            self.obra_atual = obras[0]
        else:
            self.obra_atual = None
        self._atualizar_interface()

    def _atualizar_interface(self):
        # Atualiza lista lateral
        self._limpar_layout(self.layout_lista_obras)
        obras = self.ctrl_obra.obras

        if not obras:
            lbl_vazio = QLabel("Nenhuma obra cadastrada.")
            lbl_vazio.setStyleSheet("color: #6B7280; font-size: 12px;")
            self.layout_lista_obras.addWidget(lbl_vazio)
        else:
            for obra in obras:
                btn = QPushButton(f"  {obra.nome}")
                btn.setCursor(Qt.PointingHandCursor)
                ativo = self.obra_atual is not None and obra.id == self.obra_atual.id
                btn.setObjectName("BtnObraItemAtivo" if ativo else "BtnObraItem")
                btn.clicked.connect(lambda checked=False, o_id=obra.id: self._selecionar_obra(o_id))
                self.layout_lista_obras.addWidget(btn)

        # Atualiza área direita
        self._limpar_layout(self.layout_conteudo)

        if not self.obra_atual:
            lbl_empty = QLabel("Clique em '+ Nova Obra' na barra lateral para começar.")
            lbl_empty.setStyleSheet("color: #6B7280; font-size: 16px;")
            lbl_empty.setAlignment(Qt.AlignCenter)
            self.layout_conteudo.addWidget(lbl_empty)
            return

        # Recarrega dados frescos do SQLite para a obra ativa
        self.obra_atual = self.ctrl_obra.buscar_obra(self.obra_atual.id)
        obra = self.obra_atual

        # HEADER DA OBRA
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

        lbl_status = QLabel("Status:")
        lbl_status.setStyleSheet("color: #6B7280; font-weight: 600; margin-right: 6px;")
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
        self.layout_conteudo.addLayout(header)

        # CARDS SUPERIORES (SALDO + ORÇAMENTO)
        saldo = self.ctrl_financas.calcular_saldo_atual(obra)
        total_despesas = sum(
            m.calcular_impacto_saldo() * -1
            for m in obra.movimentacoes
            if not isinstance(m, Receita)
        )

        row_cards = QHBoxLayout()
        row_cards.setSpacing(18)

        # Card 1: Saldo Atual (Escuro)
        card_saldo = QFrame()
        card_saldo.setObjectName("CardSaldoEscuro")
        card_saldo.setFixedHeight(135)
        l_saldo = QVBoxLayout(card_saldo)
        l_saldo.setContentsMargins(24, 20, 24, 20)

        t1 = QLabel("SALDO ATUAL EM CAIXA")
        t1.setObjectName("CardSaldoTitulo")
        v1 = QLabel(f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        v1.setObjectName("CardSaldoValor")
        r1 = QLabel(f"{len(obra.movimentacoes)} movimentação(ões) registrada(s)")
        r1.setObjectName("CardSaldoRodape")
        if saldo < 0:
            r1.setStyleSheet("color: #F87171; font-size: 12px; font-weight: 600;")

        l_saldo.addWidget(t1)
        l_saldo.addWidget(v1)
        l_saldo.addWidget(r1)
        row_cards.addWidget(card_saldo)

        # Card 2: Orçamento Previsto (Branco)
        card_orc = QFrame()
        card_orc.setObjectName("CardBranco")
        card_orc.setFixedHeight(135)
        l_orc = QVBoxLayout(card_orc)
        l_orc.setContentsMargins(24, 20, 24, 20)

        t2 = QLabel("ORÇAMENTO PREVISTO")
        t2.setObjectName("CardBrancoTitulo")
        v2 = QLabel(f"R$ {obra.orcamento_previsto:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        v2.setObjectName("CardBrancoValor")
        r2 = QLabel(f"Total executado em despesas: R$ {total_despesas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        r2.setObjectName("CardBrancoRodape")

        l_orc.addWidget(t2)
        l_orc.addWidget(v2)
        l_orc.addWidget(r2)
        row_cards.addWidget(card_orc)

        self.layout_conteudo.addLayout(row_cards)

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

        # COLUNAS INFERIORES: MOVIMENTAÇÕES (ESQ) + DOCUMENTOS (DIR)
        row_listas = QHBoxLayout()
        row_listas.setSpacing(18)

        # Card Movimentações
        card_movs = QFrame()
        card_movs.setObjectName("CardBranco")
        l_movs = QVBoxLayout(card_movs)
        l_movs.setContentsMargins(20, 18, 20, 18)
        l_movs.setSpacing(10)

        lbl_m_titulo = QLabel("Movimentações Financeiras")
        lbl_m_titulo.setObjectName("SecaoCardTitulo")
        l_movs.addWidget(lbl_m_titulo)

        scroll_mov = QScrollArea()
        scroll_mov.setWidgetResizable(True)
        cont_mov = QWidget()
        vbox_mov = QVBoxLayout(cont_mov)
        vbox_mov.setContentsMargins(0, 0, 0, 0)
        vbox_mov.setSpacing(8)

        if not obra.movimentacoes:
            vazio_m = QLabel("Nenhuma movimentação registrada.")
            vazio_m.setStyleSheet("color: #9CA3AF; font-size: 13px;")
            vbox_mov.addWidget(vazio_m)
        else:
            for mov in reversed(obra.movimentacoes):
                linha = QFrame()
                linha.setObjectName("LinhaItem")
                hl = QHBoxLayout(linha)
                hl.setContentsMargins(12, 10, 12, 10)

                eh_receita = isinstance(mov, Receita)
                detalhe = mov.origem_recurso if eh_receita else _formatar_enum(mov.categoria)

                col_txt = QVBoxLayout()
                col_txt.setSpacing(2)
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
                lbl_val = QLabel(f"{sinal} R$ {abs(impacto):,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                lbl_val.setStyleSheet(
                    f"font-weight: 700; font-size: 13px; color: {'#15803D' if eh_receita else '#B91C1C'};"
                )

                hl.addLayout(col_txt)
                hl.addStretch()
                hl.addWidget(badge)
                hl.addSpacing(10)
                hl.addWidget(lbl_val)
                vbox_mov.addWidget(linha)

        vbox_mov.addStretch()
        scroll_mov.setWidget(cont_mov)
        l_movs.addWidget(scroll_mov)
        row_listas.addWidget(card_movs, stretch=3)

        # Card Documentos
        card_docs = QFrame()
        card_docs.setObjectName("CardBranco")
        l_docs = QVBoxLayout(card_docs)
        l_docs.setContentsMargins(20, 18, 20, 18)
        l_docs.setSpacing(10)

        lbl_d_titulo = QLabel("Documentos Anexados")
        lbl_d_titulo.setObjectName("SecaoCardTitulo")
        l_docs.addWidget(lbl_d_titulo)

        scroll_doc = QScrollArea()
        scroll_doc.setWidgetResizable(True)
        cont_doc = QWidget()
        vbox_doc = QVBoxLayout(cont_doc)
        vbox_doc.setContentsMargins(0, 0, 0, 0)
        vbox_doc.setSpacing(8)

        if not obra.documentos:
            vazio_d = QLabel("Nenhum documento anexado.")
            vazio_d.setStyleSheet("color: #9CA3AF; font-size: 13px;")
            vbox_doc.addWidget(vazio_d)
        else:
            for doc in reversed(obra.documentos):
                linha = QFrame()
                linha.setObjectName("LinhaItem")
                hl = QHBoxLayout(linha)
                hl.setContentsMargins(12, 10, 12, 10)

                col_doc = QVBoxLayout()
                col_doc.setSpacing(2)
                lbl_arq = QLabel(doc.nome_arquivo)
                lbl_arq.setStyleSheet("font-weight: 600; color: #111317; font-size: 13px;")
                lbl_tipo = QLabel(_formatar_enum(doc.tipo))
                lbl_tipo.setStyleSheet("color: #6B7280; font-size: 11px;")
                col_doc.addWidget(lbl_arq)
                col_doc.addWidget(lbl_tipo)

                badge_doc = QLabel("Válido" if doc.validar_integridade() else "Inválido")
                badge_doc.setObjectName("BadgeDocValido")

                hl.addLayout(col_doc)
                hl.addStretch()
                hl.addWidget(badge_doc)
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