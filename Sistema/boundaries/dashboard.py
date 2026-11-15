from controllers.controlador_financas import ControladorFinancas
from entities.obra import Obra
from entities.despesa import Despesa

class Dashboard:
    def gerar_extrato_financeiro(self, obra: Obra, ctrl_financas: ControladorFinancas) -> None:
        total_entradas = 0.0
        total_saidas = 0.0
        gastos_por_categoria = {}

        for mov in obra.movimentacoes:
            impacto = mov.calcular_impacto_saldo()
            
            if impacto > 0:
                total_entradas += impacto
            else:
                total_saidas += abs(impacto)
                if isinstance(mov, Despesa):
                    cat_nome = mov.categoria.name
                    gastos_por_categoria[cat_nome] = gastos_por_categoria.get(cat_nome, 0.0) + abs(impacto)

        saldo_final = obra.orcamento_previsto + total_entradas - total_saidas

        print(f"\n- DASHBOARD: {obra.nome.upper()}")
        print("-" * 65)
        print(f"  Localização      : {obra.localizacao_maps}")
        print(f"  Status Atual     : {obra.status.name}")
        print(f"  Orçamento Inicial: R$ {obra.orcamento_previsto:10.2f}")
        print(f"  (+) Entradas     : R$ {total_entradas:10.2f}")
        print(f"  (-) Saídas       : R$ {total_saidas:10.2f}")
        print(f"  (=) Saldo Atual  : R$ {saldo_final:10.2f}")
        
        print("\n♦ PANORAMA DE CUSTOS")
        if not gastos_por_categoria:
            print("    Nenhuma despesa registrada.")
        else:
            for categoria, valor in gastos_por_categoria.items():
                print(f"    - {categoria.ljust(15)}: R$ {valor:.2f}")

        print("\n♦ DOCUMENTOS ANEXADOS")
        if not obra.documentos:
            print("    Nenhum documento anexado.")
        else:
            for doc in obra.documentos:
                print(f"    - [{doc.tipo.name}] {doc.nome_arquivo}")
        
        print("\n♦ EXTRATO DETALHADO")
        if not obra.movimentacoes:
            print("    Nenhuma movimentação registrada.")
        else:
            for mov in obra.movimentacoes:
                impacto = mov.calcular_impacto_saldo()
                sinal = "+" if impacto > 0 else "-"
                tipo = "Receita" if impacto > 0 else "Despesa"
                print(f"    [{mov._data_ocorrencia}] {tipo.ljust(7)} | R$ {sinal}{abs(impacto):8.2f} | {mov._descricao}")
        print("-" * 65 + "\n")