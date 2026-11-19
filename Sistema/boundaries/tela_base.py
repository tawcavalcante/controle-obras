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

    def selecionar_enum(self, enum_class, titulo: str):
        print(f"\n--- {titulo} ---")
        opcoes = list(enum_class)

        for indice, item in enumerate(opcoes, start=1):
            print(f"  {indice}) {item.value}")

        while True:
            escolha = self.ler_inteiro("Escolha uma opção: ")
            if 1 <= escolha <= len(opcoes):
                return opcoes[escolha - 1]
            print(f"[ERRO] Escolha um número entre 1 e {len(opcoes)}.")