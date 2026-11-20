# Controle de Obras

Sistema de gerenciamento de obras e controle financeiro, desenvolvido em **Python** para a disciplina **Orientação a Objetos** do **Prof. Henrique Moura** (UnB).

## Finalidade

Simular a rotina de gestão de obras de uma construtora: cadastro de obras, controle de documentos, registro de movimentações financeiras e geração de extratos.

O projeto aplica herança, polimorfismo, composição, associação e dependência, com modelagem em UML no padrão de arquitetura **ECB** (Entity, Control, Boundary).

## Níveis do projeto

| Nível | Propósito | Interface | Vídeo         | Commit de entrega    | Status |
|:---:|---|---|---------------|----------------------|:---:|
| **1** | Modelagem em UML (diagrama de classes) e implementação das classes, testando todas as funcionalidades por meio de um roteiro de testes | Terminal (`main.py`) | [Link](https://youtu.be/dPLwghKrh_U) | `A definir` | Concluído |
| **2** | Menu funcional: o usuário navega pelas funcionalidades do sistema | Terminal (menu) | [Link](https://youtu.be/zrEqKtMB_hY) | `A definir` | Enviado |
| **3** | Persistência dos dados em banco de dados (PostgreSQL) | Terminal (menu) | [Em breve]() | `A definir` | Pendente |
| **4** | Interface gráfica, com o sistema funcionando em janelas | Janelas (GUI) | [Em breve]()      | `A definir` | Pendente |

### Nível 1: Modelagem e testes no terminal

**Propósito:** apresentar a modelagem do sistema e provar que todas as funcionalidades operam corretamente na memória.

- Diagrama de classes com herança, polimorfismo, composição, associação e dependência.
- Roteiro de testes (`main.py`) que percorre o cadastro da obra, registro de despesas/receitas personalizadas e exibe o extrato no painel.

**Vídeo de apresentação (até 3 min):** *link em breve*

### Nível 2: Menu funcional

**Propósito:** permitir que o usuário use o sistema por conta própria, escolhendo as opções em um menu interativo no terminal.

- Telas interativas para o gestor gerenciar múltiplas obras simultaneamente.
- Menu de cadastro de novos projetos, injeção de capital e lançamento de notas de material e mão de obra.

**Vídeo de apresentação (até 6 min):** *link em breve*

### Nível 3: Banco de dados

**Propósito:** guardar obras, documentos e movimentações financeiras de forma permanente, para que os dados continuem existindo depois de fechar o programa.

- Banco **PostgreSQL** com tabelas para obras, despesas e receitas.
- Um **DAO** por tabela. Os controladores deixam de usar listas em memória e passam a chamar os DAOs.

**Vídeo de apresentação (até 6 min):** *link em breve*

### Nível 4: Interface gráfica

**Propósito:** substituir o terminal por janelas, mantendo as mesmas funcionalidades.

**Vídeo de apresentação (até 6 min):** *link em breve*

## Funcionalidades (Base)

- **Obras:** cadastrar com informações de orçamento previsto, localização e status (ex: PROJETO, EM ANDAMENTO).
- **Finanças:** registro de entradas (Receitas) e saídas (Despesas) de caixa. Permite descrições personalizadas (ex: "50 sacos de cimento Votorantim") e aplica polimorfismo para calcular os impactos positivos ou negativos no saldo.
- **Documentos:** anexação lógica de documentos específicos geridos internamente pela obra (Composição).
- **Extrato (Dashboard):** exibição formatada do histórico de movimentações e saldo total gerado.

## Arquitetura (MVC/ECB + DAO)

| Papel | O que faz | Onde está |
|---|---|---|
| **Entity / Model** | Guarda os dados e as regras do próprio objeto (ex: herança entre MovimentacaoFinanceira, Receita e Despesa) | `Sistema/entities/` |
| **Control** | Coordena as ações e faz a gestão dos objetos em listas na memória (ex: ControladorObra, ControladorFinancas) | `Sistema/controllers/` |
| **Boundary / View** | Interação com o usuário: processa o relatório final e exibe os extratos para leitura humana (ex: Dashboard) | `Sistema/boundaries/` |
| **DAO** | Único lugar com SQL: grava e busca os objetos no banco (Aplicado a partir do Nível 3) | `Sistema/dao/` |

O fluxo de uma ação no sistema atual é:

    Controlador  →  Entidades (memória)  →  Fronteira (Dashboard)

No Nível 1, o próprio `main.py` serve apenas para iniciar as dependências e rodar o roteiro de testes.

## Diagramas UML

Os diagramas do sistema estão na pasta `UML/`:

- Diagrama de classes refletindo a arquitetura atual.

## Estrutura

    Sistema/
    ├── boundaries/     Fronteiras: as telas de exibição e dashboards (View)
    ├── controllers/    Controladores responsáveis pelas regras de negócio (Control)
    ├── dao/            DAOs: o acesso ao banco de cada entidade (Níveis 3 e 4)
    ├── database/       Configurações e scripts do banco de dados (Níveis 3 e 4)
    ├── entities/       Entidades do domínio (Obra, Documento, Receita, Despesa)
    └── main.py         Ponto de entrada: roda o roteiro de testes
    UML/                Diagrama de classes exportado
    requirements.txt    Bibliotecas do projeto
    .env.example        Modelo do arquivo de variáveis
    LICENSE             Licença MIT

As pastas `controllers/` e `entities/` concentram o núcleo do sistema e são reaproveitadas em todos os níveis. O que muda futuramente é a forma de interagir com elas (menus e interfaces gráficas) e onde os dados são salvos (`dao/`).

## Autor
[GitHub: @tawcavalcante](https://github.com/tawcavalcante)
