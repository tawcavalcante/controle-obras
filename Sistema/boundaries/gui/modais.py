from datetime import date
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QMessageBox,
)
from database.conexao import obter_conexao
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra
from entities.documento import Documento
from entities.enums import CategoriaCusto, TipoDocumento


def _formatar_enum(enum_val) -> str:
    return enum_val.name.replace("_", " ").title()


class CampoMonetario(QLineEdit):
    """Formata automaticamente os dígitos digitados como moeda BRL (ex: 250.000,00)."""

    def __init__(self, placeholder: str = "0,00", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.textEdited.connect(self._formatar_texto)

    def _formatar_texto(self, texto: str):
        digitos = "".join(ch for ch in texto if ch.isdigit())
        if not digitos:
            self.blockSignals(True)
            self.setText("")
            self.blockSignals(False)
            return

        centavos = int(digitos)
        valor_float = centavos / 100.0
        formatado = f"{valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        self.blockSignals(True)
        self.setText(formatado)
        self.setCursorPosition(len(formatado))
        self.blockSignals(False)

    def valor_float(self) -> float:
        texto = self.text().strip()
        if not texto:
            raise ValueError("Informe um valor numérico válido.")
        return float(texto.replace(".", "").replace(",", "."))


class ModalNovaObra(QDialog):
    def __init__(self, ctrl_obra: ControladorObra, parent=None):
        super().__init__(parent)
        self.ctrl_obra = ctrl_obra
        self.obra_criada = None
        self.setWindowTitle("Cadastrar Nova Obra")
        self.setFixedWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel("Nova Obra")
        titulo.setStyleSheet("font-size: 18px; font-weight: 700; color: #111317;")
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Nome da obra:"))
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Ex: Residencial Gama")
        layout.addWidget(self.input_nome)

        layout.addWidget(QLabel("Localização (endereço ou cidade):"))
        self.input_local = QLineEdit()
        self.input_local.setPlaceholderText("Ex: Valparaíso de Goiás")
        layout.addWidget(self.input_local)

        layout.addWidget(QLabel("Orçamento previsto (R$):"))
        self.input_orcamento = CampoMonetario("Ex: 250.000,00")
        layout.addWidget(self.input_orcamento)

        botoes = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("BtnAcaoSecundario")
        btn_cancelar.clicked.connect(self.reject)

        btn_salvar = QPushButton("Salvar Obra")
        btn_salvar.setObjectName("BtnAcaoPrimario")
        btn_salvar.clicked.connect(self._salvar)

        botoes.addWidget(btn_cancelar)
        botoes.addWidget(btn_salvar)
        layout.addSpacing(8)
        layout.addLayout(botoes)

    def _salvar(self):
        try:
            nome = self.input_nome.text()
            local = self.input_local.text()
            if not local.strip():
                raise ValueError("Informe a localização da obra.")
            orcamento = self.input_orcamento.valor_float()

            self.obra_criada = self.ctrl_obra.cadastrar_obra(
                nome=nome,
                localizacao=local,
                orcamento=orcamento,
                data_inicio=date.today(),
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Dados Inválidos", str(e))


class ModalReceita(QDialog):
    def __init__(self, ctrl_financas: ControladorFinancas, obra: Obra, parent=None):
        super().__init__(parent)
        self.ctrl_financas = ctrl_financas
        self.obra = obra
        self.setWindowTitle("Registrar Receita")
        self.setFixedWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel(f"Nova Receita — {obra.nome}")
        titulo.setStyleSheet("font-size: 17px; font-weight: 700; color: #111317;")
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Valor (R$):"))
        self.input_valor = CampoMonetario("Ex: 50.000,00")
        layout.addWidget(self.input_valor)

        layout.addWidget(QLabel("Origem do recurso:"))
        self.input_origem = QLineEdit()
        self.input_origem.setPlaceholderText("Ex: Aporte Inicial / Cliente")
        layout.addWidget(self.input_origem)

        layout.addWidget(QLabel("Descrição:"))
        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Ex: Primeira parcela da obra")
        layout.addWidget(self.input_desc)

        botoes = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("BtnAcaoSecundario")
        btn_cancelar.clicked.connect(self.reject)

        btn_salvar = QPushButton("Registrar Receita")
        btn_salvar.setObjectName("BtnAcaoPrimario")
        btn_salvar.clicked.connect(self._salvar)

        botoes.addWidget(btn_cancelar)
        botoes.addWidget(btn_salvar)
        layout.addSpacing(8)
        layout.addLayout(botoes)

    def _salvar(self):
        try:
            valor = self.input_valor.valor_float()
            origem = self.input_origem.text().strip()
            desc = self.input_desc.text().strip()
            if not origem or not desc:
                raise ValueError("Preencha origem e descrição.")

            self.ctrl_financas.registrar_receita(
                valor=valor,
                origem=origem,
                data=date.today(),
                descricao=desc,
                obra=self.obra,
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Erro ao Registrar", str(e))


class ModalDespesa(QDialog):
    def __init__(self, ctrl_financas: ControladorFinancas, obra: Obra, parent=None):
        super().__init__(parent)
        self.ctrl_financas = ctrl_financas
        self.obra = obra
        self.setWindowTitle("Registrar Despesa")
        self.setFixedWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel(f"Nova Despesa — {obra.nome}")
        titulo.setStyleSheet("font-size: 17px; font-weight: 700; color: #111317;")
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Valor (R$):"))
        self.input_valor = CampoMonetario("Ex: 12.000,00")
        layout.addWidget(self.input_valor)

        layout.addWidget(QLabel("Categoria de custo:"))
        self.combo_categoria = QComboBox()
        for cat in CategoriaCusto:
            self.combo_categoria.addItem(_formatar_enum(cat), cat)
        layout.addWidget(self.combo_categoria)

        layout.addWidget(QLabel("Descrição:"))
        self.input_desc = QLineEdit()
        self.input_desc.setPlaceholderText("Ex: Compra de cimento e ferragens")
        layout.addWidget(self.input_desc)

        botoes = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("BtnAcaoSecundario")
        btn_cancelar.clicked.connect(self.reject)

        btn_salvar = QPushButton("Registrar Despesa")
        btn_salvar.setObjectName("BtnAcaoPrimario")
        btn_salvar.clicked.connect(self._salvar)

        botoes.addWidget(btn_cancelar)
        botoes.addWidget(btn_salvar)
        layout.addSpacing(8)
        layout.addLayout(botoes)

    def _salvar(self):
        try:
            valor = self.input_valor.valor_float()
            categoria = self.combo_categoria.currentData()
            desc = self.input_desc.text().strip()
            if not desc:
                raise ValueError("Preencha a descrição da despesa.")

            self.ctrl_financas.registrar_despesa(
                valor=valor,
                categoria=categoria,
                data=date.today(),
                descricao=desc,
                obra=self.obra,
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Erro ao Registrar", str(e))


class ModalDocumento(QDialog):
    def __init__(self, obra: Obra, parent=None):
        super().__init__(parent)
        self.obra = obra
        self.setWindowTitle("Anexar Documento")
        self.setFixedWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        titulo = QLabel(f"Anexar Documento — {obra.nome}")
        titulo.setStyleSheet("font-size: 17px; font-weight: 700; color: #111317;")
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Nome do arquivo:"))
        self.input_arquivo = QLineEdit()
        self.input_arquivo.setPlaceholderText("Ex: Alvara_Construcao.pdf")
        layout.addWidget(self.input_arquivo)

        layout.addWidget(QLabel("Tipo de documento:"))
        self.combo_tipo = QComboBox()
        for tipo in TipoDocumento:
            self.combo_tipo.addItem(_formatar_enum(tipo), tipo)
        layout.addWidget(self.combo_tipo)

        botoes = QHBoxLayout()
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setObjectName("BtnAcaoSecundario")
        btn_cancelar.clicked.connect(self.reject)

        btn_salvar = QPushButton("Anexar")
        btn_salvar.setObjectName("BtnAcaoPrimario")
        btn_salvar.clicked.connect(self._salvar)

        botoes.addWidget(btn_cancelar)
        botoes.addWidget(btn_salvar)
        layout.addSpacing(8)
        layout.addLayout(botoes)

    def _salvar(self):
        nome_arquivo = self.input_arquivo.text()
        tipo = self.combo_tipo.currentData()

        doc_temp = Documento(0, nome_arquivo, tipo)
        if not doc_temp.validar_integridade():
            QMessageBox.warning(self, "Arquivo Inválido", "O nome do arquivo não pode estar vazio.")
            return

        nome_limpo = nome_arquivo.strip()
        with obter_conexao() as conn:
            cursor = conn.execute(
                "INSERT INTO documentos (obra_id, nome_arquivo, tipo) VALUES (?, ?, ?)",
                (self.obra.id, nome_limpo, tipo.value),
            )
            novo_id = cursor.lastrowid

        doc = Documento(novo_id, nome_limpo, tipo)
        self.obra.adicionar_documento(doc)
        self.accept()