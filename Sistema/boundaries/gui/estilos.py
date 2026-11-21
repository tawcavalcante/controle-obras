ESTILO_GLOBAL = """
QMainWindow, QDialog {
    background-color: #F5F6FA;
    font-family: "Segoe UI", "Inter", sans-serif;
    color: #181A20;
}

/* SIDEBAR ESCURA */
QFrame#Sidebar {
    background-color: #111317;
    border: none;
}

QLabel#LogoTitulo {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

QLabel#SidebarSecao {
    color: #7A828E;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

QPushButton#BtnNovaObra {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 11px 16px;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
}

QPushButton#BtnNovaObra:hover {
    background-color: #1D4ED8;
}

QPushButton#BtnObraItem {
    background-color: transparent;
    color: #A0A8B5;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    text-align: left;
}

QPushButton#BtnObraItem:hover {
    background-color: #1C2026;
    color: #FFFFFF;
}

QPushButton#BtnObraItemAtivo {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 600;
    text-align: left;
}

/* ÁREA PRINCIPAL */
QLabel#TituloObra {
    color: #111317;
    font-size: 22px;
    font-weight: 700;
}

QLabel#SubtituloObra {
    color: #6B7280;
    font-size: 13px;
}

QComboBox#ComboStatus {
    background-color: #FFFFFF;
    color: #111317;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 600;
    min-width: 150px;
}

/* CARDS SUPERIORES */
QFrame#CardSaldoEscuro {
    background-color: #181A20;
    border-radius: 18px;
}

QLabel#CardSaldoTitulo {
    color: #9CA3AF;
    font-size: 12px;
    font-weight: 600;
}

QLabel#CardSaldoValor {
    color: #FFFFFF;
    font-size: 28px;
    font-weight: 700;
}

QLabel#CardSaldoRodape {
    color: #34D399;
    font-size: 12px;
    font-weight: 600;
}

QFrame#CardBranco {
    background-color: #FFFFFF;
    border: 1px solid #ECEEF2;
    border-radius: 18px;
}

QLabel#CardBrancoTitulo {
    color: #6B7280;
    font-size: 12px;
    font-weight: 600;
}

QLabel#CardBrancoValor {
    color: #111317;
    font-size: 28px;
    font-weight: 700;
}

QLabel#CardBrancoRodape {
    color: #6B7280;
    font-size: 12px;
}

/* BOTÕES DE AÇÃO RÁPIDA (PÍLULAS) */
QPushButton#BtnAcaoPrimario {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 11px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#BtnAcaoPrimario:hover {
    background-color: #1D4ED8;
}

QPushButton#BtnAcaoSecundario {
    background-color: #FFFFFF;
    color: #111317;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 11px 18px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton#BtnAcaoSecundario:hover {
    background-color: #F9FAFB;
    border-color: #D1D5DB;
}

/* LISTAS E BADGES */
QLabel#SecaoCardTitulo {
    color: #111317;
    font-size: 15px;
    font-weight: 700;
}

QFrame#LinhaItem {
    background-color: #F9FAFB;
    border-radius: 10px;
}

QLabel#BadgeReceita {
    background-color: #DCFCE7;
    color: #15803D;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}

QLabel#BadgeDespesa {
    background-color: #FEE2E2;
    color: #B91C1C;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}

QLabel#BadgeDocValido {
    background-color: #DBEAFE;
    color: #1D4ED8;
    border-radius: 8px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 700;
}

/* INPUTS NOS MODAIS */
QLineEdit, QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #D1D5DB;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    color: #111317;
}

QLineEdit:focus, QComboBox:focus {
    border: 1.5px solid #2563EB;
}

QScrollArea {
    border: none;
    background: transparent;
}
"""