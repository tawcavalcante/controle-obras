from datetime import date
from controllers.controlador_obra import ControladorObra
from controllers.controlador_financas import ControladorFinancas
from boundaries.dashboard import Dashboard
from entities.enums import CategoriaCusto

ctrl_obra = ControladorObra()
ctrl_financas = ControladorFinancas()
painel = Dashboard()

obra_pai = ctrl_obra.cadastrar_obra(
    nome="Reforma Condomínio Parque das Árvores",
    localizacao="Valparaíso de Goiás",
    orcamento=150000.00,
    data_inicio=date.today()
)

# Adicionando as descrições personalizadas
ctrl_financas.registrar_receita(
    id_obra=obra_pai.id, valor=50000.00, origem="Caixa da Construtora", 
    data=date.today(), descricao="Transferência do cliente via Pix", obra=obra_pai
)

ctrl_financas.registrar_despesa(
    id_obra=obra_pai.id, valor=1500.00, categoria=CategoriaCusto.MATERIAIS, 
    data=date.today(), descricao="50 sacos de cimento Votorantim", obra=obra_pai
)

ctrl_financas.registrar_despesa(
    id_obra=obra_pai.id, valor=3500.00, categoria=CategoriaCusto.MAO_DE_OBRA, 
    data=date.today(), descricao="Pagamento quinzenal dos pedreiros", obra=obra_pai
)

painel.gerar_extrato_financeiro(obra=obra_pai, ctrl_financas=ctrl_financas)