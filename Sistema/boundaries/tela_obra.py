from datetime import date
from boundaries.tela_base import TelaBase
from controllers.controlador_obra import ControladorObra
from entities.enums import StatusObra


class TelaObra(TelaBase):
    def __init__(self, ctrl_obra: ControladorObra):
        self.ctrl_obra = ctrl_obra

    def exibir(self):
        while True:
            self.limpar_tela()
            self.cabecalho("Gerenciar Obras")
            print("  1) Cadastrar Obra")
            print("  2) Listar Obras Cadastradas")
            print("  3) Buscar Obra por ID")
            print("  4) Atualizar Status da Obra")
            print("  0) Voltar ao Menu Principal")
            print("-" * 60)

            opcao = self.ler_inteiro("Escolha uma opção: ")

            if opcao == 1:
                self._cadastrar_obra()
            elif opcao == 2:
                self._listar_obras()
            elif opcao == 3:
                self._buscar_obra()
            elif opcao == 4:
                self._atualizar_status()
            elif opcao == 0:
                break
            else:
                print("\n[ERRO] Opção inválida. Escolha entre 0 e 4.")
                self.pausar()

    def _cadastrar_obra(self):
        self.cabecalho("Cadastrar Nova Obra")
        nome = self.ler_texto("Nome da obra: ")
        localizacao = self.ler_texto("Localização (endereço/cidade): ")
        orcamento = self.ler_float("Orçamento previsto (R$): ")

        try:
            obra = self.ctrl_obra.cadastrar_obra(
                nome=nome,
                localizacao=localizacao,
                orcamento=orcamento,
                data_inicio=date.today(),
            )
            print(f"\n[OK] Obra '{obra.nome}' cadastrada com ID {obra.id}!")
        except ValueError as e:
            print(f"\n[RECUSADO] {e}")

        self.pausar()

    def _listar_obras(self):
        self.cabecalho("Obras Cadastradas")
        if not self.ctrl_obra.obras:
            print("Nenhuma obra cadastrada no momento.")
        else:
            for obra in self.ctrl_obra.obras:
                print(
                    f"ID: {obra.id} | {obra.nome} | Local: {obra.localizacao_maps} "
                    f"| Orçamento: R$ {obra.orcamento_previsto:.2f} | Status: {obra.status.value}"
                )
        self.pausar()

    def _buscar_obra(self):
        self.cabecalho("Buscar Obra")
        if not self.ctrl_obra.obras:
            print("Nenhuma obra cadastrada.")
            self.pausar()
            return

        id_obra = self.ler_inteiro("Digite o ID da obra: ")
        try:
            obra = self.ctrl_obra.buscar_obra(id_obra)
            print("\n--- Detalhes da Obra ---")
            print(f"ID: {obra.id}")
            print(f"Nome: {obra.nome}")
            print(f"Localização: {obra.localizacao_maps}")
            print(f"Orçamento Previsto: R$ {obra.orcamento_previsto:.2f}")
            print(f"Status Atual: {obra.status.value}")
            print(f"Documentos Anexados: {len(obra.documentos)}")
            print(f"Movimentações Financeiras: {len(obra.movimentacoes)}")
        except ValueError as e:
            print(f"\n[ERRO] {e}")

        self.pausar()

    def _atualizar_status(self):
        self.cabecalho("Atualizar Status da Obra")
        if not self.ctrl_obra.obras:
            print("Nenhuma obra cadastrada.")
            self.pausar()
            return

        for obra in self.ctrl_obra.obras:
            print(f"  ID {obra.id}: {obra.nome} (Atual: {obra.status.value})")

        id_obra = self.ler_inteiro("\nDigite o ID da obra que deseja atualizar: ")
        try:
            obra = self.ctrl_obra.buscar_obra(id_obra)
            novo_status = self.selecionar_enum(StatusObra, f"Novo Status para '{obra.nome}'")
            self.ctrl_obra.atualizar_status_obra(id_obra, novo_status)
            print(f"\n[OK] Status da obra '{obra.nome}' atualizado para '{novo_status.value}'.")
        except ValueError as e:
            print(f"\n[ERRO] {e}")

        self.pausar()