# 🚀 Entrega do Sistema Cortejá — Versão em Python

O sistema **Cortejá** foi completamente implementado e estruturado como um pacote Python profissional (`corteja`), com o ponto de entrada principal no arquivo `main.py`. O design do código foi pensado especificamente para **desenvolvedores juniores**, sendo limpo, modular, amplamente documentado com docstrings em português e cobrindo **100% dos requisitos** de Programação Orientada a Objetos da disciplina de Laboratório de Programação.

---

## 📁 Estrutura de Arquivos Gerados

O projeto foi organizado com a seguinte estrutura de diretórios e arquivos dentro da pasta do workspace:

```
Projeto unidade 02_Lab_Prog/
├── corteja/                      # 📦 PACOTE PRINCIPAL DO SISTEMA
│   ├── __init__.py               # Define o diretório como pacote e expõe as classes
│   ├── exceptions.py             # ⚠️ Hierarquia de exceções customizadas
│   ├── usuarios.py               # 👥 Classes Usuario (ABC), Cliente e Barbeiro
│   ├── servicos.py               # ✂️ Classe Servico (Encapsulamento e Formatação)
│   ├── agendamentos.py           # 📅 Classe Agendamento (Máquina de Estados)
│   ├── barbearia.py              # 🏢 Classe Barbearia (Orquestrador / Composição)
│   └── utils.py                  # 🔄 Funções Utilitárias com Recursão
├── main.py                       # 💻 Interface interativa via Console
└── [Slides de Aula]              # Arquivos pptx de referência da disciplina
```

---

## 🧩 Onde os Conceitos de POO Estão Implementados

Para ajudar a equipe junior na explicação para o professor, veja exatamente onde cada conceito foi aplicado:

### 1. Pacote Python e Importações (`corteja/__init__.py` e `main.py`)
- **Onde encontrar**: O arquivo [__init__.py](file:///c:/Users/lanse/Downloads/Projeto%20unidade%2002_Lab_Prog/corteja/__init__.py) inicializa a pasta `corteja/` como pacote e simplifica as importações para `from corteja import Cliente, Barbeiro, ...` em [main.py](file:///c:/Users/lanse/Downloads/Projeto%20unidade%2002_Lab_Prog/main.py).

### 2. Classe Abstrata (ABC) e Polimorfismo (`corteja/usuarios.py`)
- **Onde encontrar**: A classe `Usuario` herda de `ABC` (Abstract Base Class) e define o método abstrato `exibir_perfil()` com o decorador `@abstractmethod`.
- **Explicação**: `Usuario` não pode ser instanciada diretamente. As subclasses `Cliente` e `Barbeiro` herdam dela e implementam o método `exibir_perfil()` de formas diferentes (Polimorfismo). No menu `main.py`, a opção **9** chama esse método dinamicamente baseado no tipo de objeto retornado.

### 3. Encapsulamento, Validações e `@property` (`corteja/agendamentos.py`, `usuarios.py` e `servicos.py`)
- **Onde encontrar**:
  - `Usuario` encapsula `nome` e `email` usando `@property` e setters para validar que o nome não seja vazio e que o e-mail contenha `@`.
  - `Servico` encapsula o `preco` para garantir que o valor não seja negativo.
  - `Agendamento` encapsula o `__status` com uma **máquina de estados**. A alteração do status valida se a transição é permitida (ex.: `agendado` ➔ `confirmado` ➔ `concluido`).

### 4. Atributos e Métodos de Classe (`@classmethod`) e Estáticos (`@staticmethod`)
- **Onde encontrar**:
  - `@classmethod total_cadastrados` em `Usuario` e `total_realizados` em `Agendamento` controlam contadores globais.
  - `@staticmethod validar_hora` em `Agendamento` valida o formato de hora `HH:MM` de forma genérica.
  - `@staticmethod formatar_preco` em `Servico` retorna a string monetária no padrão brasileiro (`R$ XX.XX`).

### 5. Dunder Methods (Métodos Mágicos)
O sistema implementou **9 métodos mágicos** que enriquecem o comportamento das classes Python:
- `__str__`: Representação textual amigável em todas as classes.
- `__repr__`: Representação técnica para depuração.
- `__eq__`: Comparação de igualdade (`Usuario` e `Agendamento` comparam IDs, `Servico` compara o nome).
- `__lt__` (Less Than): Implementado em `Agendamento` para ordenar cronologicamente por data e hora.
- `__len__`: Em `Barbearia` permite fazer `len(barbearia)` para obter o total de agendamentos.
- `__iter__`: Em `Barbearia` permite percorrer a agenda com `for agendamento in barbearia`.
- `__contains__`: Em `Barbearia` permite verificar se um cliente ou barbeiro está cadastrado usando o operador `in`.
- `__getitem__`: Em `Barbearia` permite indexação direta como `barbearia[0]` para obter o primeiro agendamento ordenado.

### 6. Tratamento de Exceções Customizadas (`corteja/exceptions.py`)
- **Onde encontrar**: Foi definida uma hierarquia de erros herdando de `CortejaError` (que por sua vez herda de `Exception`):
  - `HorarioIndisponivelError`: Lançado se houver conflito de horário na agenda.
  - `ServicoNaoEncontradoError`: Lançado se o barbeiro escolhido não realizar o serviço desejado.
  - `CancelamentoInvalidoError`: Lançado se houver tentativa de cancelar um agendamento já concluído/cancelado.
  - `DadosInvalidosError`: Lançado se dados cadastrais estiverem incorretos.
- **Na prática**: O `main.py` trata todos os erros com blocos `try/except/else/finally` impedindo a quebra do sistema e fornecendo feedback ao usuário.

### 7. Recursão (`corteja/utils.py`)
Foram implementados **3 algoritmos recursivos** claros e intuitivos (ideais para demonstrar o conhecimento de caso base e passo recursivo):
- `buscar_horario_disponivel`: Percorre a lista de horários de trabalho de um barbeiro e encontra o primeiro horário vago no dia (usado na opção **7**).
- `calcular_faturamento`: Soma recursivamente os valores de todos os serviços com status `concluido` na agenda (usado na opção **8**).
- `contar_agendamentos_por_status`: Conta recursivamente quantos agendamentos estão em um determinado estado (usado na opção **8**).

---

## 🛠️ Como Executar e Testar o Sistema

O sistema já vem pré-carregado com dados de exemplo (2 barbeiros com serviços e horários configurados, 2 clientes cadastrados e 3 agendamentos históricos) para que você não precise digitar tudo para testar.

### Passo 1: Executando o Menu
Abra o prompt de comando (CMD/PowerShell ou Terminal da IDE) no diretório do projeto `Projeto unidade 02_Lab_Prog` e execute:
```bash
python main.py
```

### Roteiro de Demonstração (Sugestão de Testes)

1. **Testar Cadastro e Validação (Opção 1)**
   - Tente cadastrar um cliente com e-mail sem `@` (ex: `carlos_email.com`). O sistema disparará `DadosInvalidosError` e exibirá a mensagem amigável de erro.
   - Cadastre com os dados corretos e veja que a inserção funciona. Ao final, a seção `finally` imprimirá o total acumulado de usuários.

2. **Verificar Serviços por Barbeiro (Opção 2)**
   - Lista todos os barbeiros, mostrando que cada um tem serviços e agendas configurados de forma independente.

3. **Verificar Conflitos de Agenda e Validações (Opção 3)**
   - Tente fazer um agendamento para o barbeiro **Pedro Silva (ID: 1)** no dia **26/05/2026** às **09:00**.
   - O sistema impedirá o agendamento lançando a exceção `HorarioIndisponivelError`, pois esse horário exato já foi pré-carregado no sistema com outro cliente.

4. **Visualizar Agenda Ordenada (Opção 4)**
   - Exibe a lista completa de atendimentos. Note que eles aparecem ordenados de forma cronológica automática, demonstrando o funcionamento interno do dunder `__lt__` e `__iter__`.

5. **Testar a Máquina de Estados e Fluxo de Pagamento Simulado (Opção 5 e Opção 6)**
   - Tente concluir um agendamento que está como `agendado` (sem confirmar antes). O sistema acusará que a transição de estado é inválida (obedecendo a máquina de estados).
   - Para simular o fluxo de pagamento completo, primeiro escolha um agendamento (como o ID 1) e **Confirme** o atendimento (Opção 5 -> Escolha a Ação 1).
   - Em seguida, acesse a Opção 5 novamente para o mesmo ID de agendamento e selecione a Ação 2 **"Concluir Atendimento e Realizar Pagamento"**.
   - O sistema abrirá a tela de fechamento simulada, onde você poderá testar diferentes formas de pagamento:
     - **Pix**: Calcula 5% de desconto e exibe um QR Code em arte ASCII.
     - **Cartão (Crédito/Débito)**: Simula o processamento e comunicação com a maquininha.
     - **Dinheiro**: Solicita o valor entregue e calcula o troco do cliente de forma dinâmica.
   - O fluxo finaliza imprimindo na tela um **Cupom Fiscal Simulado** em formato de recibo de texto que é muito bonito de se ver!
   - Tente cancelar um agendamento que já está marcado como `concluido` (ID 2). O sistema lançará `CancelamentoInvalidoError`, bloqueando a operação de forma segura.

6. **Algoritmos Recursivos (Opção 7 e Opção 8)**
   - **Opção 7**: Digite o ID do barbeiro **1** e a data **26/05/2026**. O sistema buscará recursivamente e informará que o primeiro horário vago é às **10:00** (já que as 09:00 está ocupado).
   - **Opção 8**: Exibe o faturamento total acumulado e a quantidade de agendamentos por status, todos calculados recursivamente de ponta a ponta da lista.

7. **Demonstrar Polimorfismo e Dunder `in` (Opção 9)**
   - Digite o ID **10** (Cliente). Veja o cabeçalho personalizado de cliente.
   - Digite o ID **1** (Barbeiro). Veja a exibição completamente diferente mostrando os serviços e horários. Ambos usam a chamada dinâmica da mesma linha de código: `usuario.exibir_perfil()`.

---

## 💡 Dicas de Ouro para a Apresentação Acadêmica

Quando a equipe for apresentar o projeto ao professor:
1. **Destaque a Integração de Requisitos**: Mostre como o tema "Agendamento" (Cortejá da disciplina de Eng. Software) foi o cenário perfeito para aplicar Programação Orientada a Objetos em Python de forma fluida.
2. **Defenda a Escolha de Recursão**: Explique que a recursão em `calcular_faturamento` substitui um laço simples (`for`) apenas para demonstrar domínio técnico sobre pilhas de chamada e caso base, o que é um diferencial em avaliações acadêmicas.
3. **Explique a Máquina de Estados**: O controle rígido de status no setter de `Agendamento` é uma excelente prática arquitetural que impressiona professores, pois evita inconsistências no banco de dados (no caso, em memória).
