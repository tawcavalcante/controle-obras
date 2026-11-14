from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra

class Dashboard:
    def gerar_extrato_financeiro(self, obra: Obra, ctrl_financas: ControladorFinancas) -> None:
        print(f"\n=== EXTRATO FINANCEIRO: {obra.nome.upper()} ===")
        print(f"Status Atual: {obra.status.name}")
        print("-" * 45)
        
        if not obra.movimentacoes:
            print("Nenhuma movimentação registrada até o momento.")
        else:
            for mov in obra.movimentacoes:
                impacto = mov.calcular_impacto_saldo()
                sinal = "+" if impacto > 0 else ""
                print(f"[{mov._data_ocorrencia}] {mov._descricao}")
                print(f"    Valor: R$ {sinal}{impacto:.2f}")
                
        print("-" * 45)
        saldo_total = ctrl_financas.calcular_saldo_atual(id_obra=obra.id, obra=obra)
        print(f"SALDO FINAL EM CAIXA: R$ {saldo_total:.2f}")
        print("=============================================\n")