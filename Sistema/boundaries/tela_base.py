import os


class TelaBase:
    def limpar_tela(self):
        os.system("cls" if os.name == "nt" else "clear")

    def cabecalho(self, titulo: str):
        print("\n" + "=" * 60)
        print(f" {titulo.upper()}")
        print("=" * 60)

    def pausar(self):
        input("\n[Pressione ENTER para continuar]")

    def ler_texto(self, mensagem: str) -> str:
        return input(mensagem).strip()

    def ler_inteiro(self, mensagem: str) -> int:
        while True:
            try:
                return int(input(mensagem))
            except ValueError:
                print("[ERRO] Entrada inválida. Digite apenas números inteiros.")

    def ler_float(self, mensagem: str) -> float:
        while True:
            entrada = input(mensagem).replace(",", ".")
            try:
                return float(entrada)
            except ValueError:
                print("[ERRO] Valor inválido. Digite um número (ex: 1500.50).")

    def formatar_enum(self, item) -> str:
        if isinstance(item.value, str):
            return item.value
        return item.name.replace("_", " ").title()

    def selecionar_enum(self, enum_class, titulo: str):
        print(f"\n--- {titulo} ---")
        opcoes = list(enum_class)

        for indice, item in enumerate(opcoes, start=1):
            print(f"  {indice}) {self.formatar_enum(item)}")

        while True:
            escolha = self.ler_inteiro("Escolha uma opção: ")
            if 1 <= escolha <= len(opcoes):
                return opcoes[escolha - 1]
            print(f"[ERRO] Escolha um número entre 1 e {len(opcoes)}.")

    def selecionar_obra(self, ctrl_obra):
        if not ctrl_obra.obras:
            print("\nNenhuma obra cadastrada. Cadastre uma obra primeiro.")
            self.pausar()
            return None

        print("\n--- Obras Disponíveis ---")
        for obra in ctrl_obra.obras:
            print(f"  [{obra.id}] {obra.nome} ({self.formatar_enum(obra.status)})")

        entrada = self.ler_texto("\nDigite o ID ou o nome da obra: ")

        if entrada.isdigit():
            try:
                return ctrl_obra.buscar_obra(int(entrada))
            except ValueError as e:
                print(f"\n[ERRO] {e}")
                self.pausar()
                return None

        termo = entrada.lower()
        encontradas = [o for o in ctrl_obra.obras if termo in o.nome.lower()]

        if len(encontradas) == 1:
            return encontradas[0]
        elif len(encontradas) > 1:
            print("\nMais de uma obra encontrada. Especifique pelo ID:")
            for obra in encontradas:
                print(f"  [{obra.id}] {obra.nome}")
            id_obra = self.ler_inteiro("ID da obra: ")
            try:
                return ctrl_obra.buscar_obra(id_obra)
            except ValueError as e:
                print(f"\n[ERRO] {e}")
                self.pausar()
                return None
        else:
            print("\n[ERRO] Nenhuma obra encontrada com esse nome.")
            self.pausar()
            return None