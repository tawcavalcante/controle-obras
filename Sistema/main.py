from datetime import date
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from boundaries.dashboard import Dashboard
from entities.enums import CategoriaCusto, TipoDocumento
from entities.documento import Documento

def cabecalho(texto):
    print("\n" + "-"*90)
    print(f" {texto}")

def pausar():
    input("\n[ENTER para continuar]\n")

registrar_obra = ControladorObra()
registrar_financa = ControladorFinancas()
painel = Dashboard()

pausar()


# 1. CADASTRAR OBRA

cabecalho("1. Cadastrar Obra\n")

obra1 = registrar_obra.cadastrar_obra(
    nome="Condominio Norris", localizacao="Valparaíso de Goiás", orcamento=800000.0, data_inicio=date.today()
)

obra2 = registrar_obra.cadastrar_obra(
    nome="Predio Alvorada II", localizacao="Gama", orcamento=200000.0, data_inicio=date.today()
)

print("[OK] Obra cadastrada")
print(f"  1) {obra1.nome} - Orçamento Previsto: R$ {obra1.orcamento_previsto:.2f}")
print(f"  2) {obra2.nome} - Orçamento Previsto: R$ {obra2.orcamento_previsto:.2f}")

try:
    registrar_obra.cadastrar_obra(nome="Obra Fantasma", localizacao="Local", orcamento=-500.0, data_inicio=date.today())
except Exception as e:
    print(f"[RECUSADO] {e}")

try:
    registrar_obra.cadastrar_obra(nome="   ", localizacao="Local", orcamento=1000.0, data_inicio=date.today())
except Exception as e:
    print(f"[RECUSADO] {e}")

pausar()


# 2. DOCUMENTO

cabecalho("2. Documento\n")

doc_alvara = Documento(id_doc=1, nome_arquivo="Alvara_Construcao.pdf", tipo=TipoDocumento.ALVARA)
obra1.adicionar_documento(doc_alvara)

print(f"[OK] Documento '{doc_alvara.nome_arquivo}' anexado à obra {obra1.nome}")

integridade = "Válido" if doc_alvara.validar_integridade() else "Inválido"
print(f"[OK] Integridade do arquivo verificada: {integridade}")

pausar()


# 3. FINANÇAS

cabecalho("3. Finanças\n")

registrar_financa.registrar_receita(
    valor=50000.0, origem="Caixa Construtora", 
    data=date.today(), descricao="Transferência via Pix", obra=obra1
)

registrar_financa.registrar_despesa(
    valor=1500.0, categoria=CategoriaCusto.MATERIAIS, 
    data=date.today(), descricao="50 sacos de cimento Votorantim", obra=obra1
)

registrar_financa.registrar_despesa(
    valor=3500.0, categoria=CategoriaCusto.MAO_DE_OBRA, 
    data=date.today(), descricao="Pagamento quinzenal dos pedreiros", obra=obra1
)

print("[OK] 3 movimentações financeiras registradas")

try:
    registrar_financa.registrar_despesa(
        valor=-100.0, categoria=CategoriaCusto.MATERIAIS, 
        data=date.today(), descricao="Fraude", obra=obra1
    )
except Exception as e:
    print(f"[RECUSADO] {e}")

pausar()


# 4. DASHBOARD

cabecalho("4. Dashboard e Extrato")

painel.gerar_extrato_financeiro(obra=obra1, ctrl_financas=registrar_financa)

painel.gerar_extrato_financeiro(obra=obra2, ctrl_financas=registrar_financa)

pausar()