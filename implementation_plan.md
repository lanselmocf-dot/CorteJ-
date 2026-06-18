# Plano de Implementação — Cortejá (Python / Lab de Programação)

Sistema de agendamento para barbearias, unificando o projeto Cortejá (Engenharia de Software) com os requisitos do Lab de Programação (Python). Dados em memória, interface via console.

## Proposta de Mudanças

### Estrutura de Pacotes

```
corteja/
├── __init__.py              # Exporta classes principais do pacote
├── usuarios.py              # Usuario (ABC), Cliente, Barbeiro
├── servicos.py              # Servico
├── agendamentos.py          # Agendamento
├── barbearia.py             # Barbearia (orquestra tudo)
├── exceptions.py            # Exceções customizadas
├── utils.py                 # Funções recursivas e utilitárias
main.py                      # Menu interativo (fora do pacote)
```

---

### Conceitos exigidos → Onde aparecem

| Conceito | Arquivo | Implementação |
|---|---|---|
| Módulos/Pacotes | `corteja/` + `__init__.py` | Pacote com 7 módulos |
| `__init__.py` | `corteja/__init__.py` | Exporta classes para `from corteja import ...` |
| Importações | `main.py` | `from corteja import Cliente, Barbeiro, ...` |
| Classe Abstrata (ABC) | `usuarios.py` | `Usuario(ABC)` com `@abstractmethod exibir_perfil()` |
| Herança | `usuarios.py` | `Cliente(Usuario)`, `Barbeiro(Usuario)` |
| Polimorfismo | `usuarios.py` | `exibir_perfil()` diferente em cada subclasse |
| Encapsulamento | `agendamentos.py` | `__status` com `@property` e setter com validação |
| `@property` | `agendamentos.py`, `servicos.py` | Getters/setters validados |
| `@classmethod` | `usuarios.py`, `agendamentos.py` | Contadores de classe |
| `@staticmethod` | `servicos.py`, `agendamentos.py` | Utilitários puros |
| Composição | `barbearia.py` | `Barbearia` **tem** listas de `Barbeiro` e `Agendamento` |
| Dunder `__str__` | Todas as classes | Representação amigável |
| Dunder `__repr__` | Todas as classes | Representação técnica |
| Dunder `__eq__` | `usuarios.py`, `agendamentos.py` | Comparar por ID |
| Dunder `__lt__` | `agendamentos.py` | Ordenar por data/hora |
| Dunder `__len__` | `barbearia.py` | Total de agendamentos |
| Dunder `__iter__` | `barbearia.py` | Iterar sobre agendamentos |
| Dunder `__contains__` | `barbearia.py` | Verificar se barbeiro existe |
| Dunder `__getitem__` | `barbearia.py` | Acessar agendamento por índice |
| Exceções customizadas | `exceptions.py` | `HorarioIndisponivelError`, etc. |
| `try/except/else/finally` | `main.py`, `barbearia.py` | Tratamento em todas as operações |
| Recursão | `utils.py` | Busca de horário disponível, cálculo de faturamento |

---

### Detalhamento por Arquivo

---

#### [NEW] `corteja/__init__.py`

Exporta as classes principais para facilitar importações.

```python
from corteja.usuarios import Usuario, Cliente, Barbeiro
from corteja.servicos import Servico
from corteja.agendamentos import Agendamento
from corteja.barbearia import Barbearia
from corteja.exceptions import (
    HorarioIndisponivelError,
    ServicoNaoEncontradoError,
    CancelamentoInvalidoError,
    DadosInvalidosError
)
```

---

#### [NEW] `corteja/exceptions.py`

Exceções customizadas do sistema — todas herdam de uma base `CortejaError`.

```python
class CortejaError(Exception):
    """Exceção base do sistema Cortejá."""
    pass

class HorarioIndisponivelError(CortejaError):
    """Horário já ocupado por outro agendamento."""
    pass

class ServicoNaoEncontradoError(CortejaError):
    """Serviço não existe no cadastro."""
    pass

class CancelamentoInvalidoError(CortejaError):
    """Tentativa de cancelar agendamento já concluído/cancelado."""
    pass

class DadosInvalidosError(CortejaError):
    """Dados fornecidos são inválidos (nome vazio, email sem @, etc.)."""
    pass
```

> [!NOTE]
> A hierarquia de exceções (`CortejaError` como base) demonstra **herança** aplicada a exceções.

---

#### [NEW] `corteja/usuarios.py`

Contém a classe abstrata `Usuario` e suas filhas `Cliente` e `Barbeiro`.

**Conceitos demonstrados**: ABC, `@abstractmethod`, herança, polimorfismo, encapsulamento, `@property`, `@classmethod`, `__str__`, `__repr__`, `__eq__`.

```python
from abc import ABC, abstractmethod
from corteja.exceptions import DadosInvalidosError

class Usuario(ABC):
    _total_cadastrados = 0  # atributo de classe

    def __init__(self, id, nome, email, telefone):
        self.id = id
        self.nome = nome        # usa @property setter (valida)
        self.email = email      # usa @property setter (valida)
        self.__telefone = telefone
        Usuario._total_cadastrados += 1

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not valor or not valor.strip():
            raise DadosInvalidosError("Nome não pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise DadosInvalidosError(f"Email inválido: {valor}")
        self.__email = valor

    @property
    def telefone(self):
        return self.__telefone

    @classmethod
    def total_cadastrados(cls):
        return cls._total_cadastrados

    @abstractmethod
    def exibir_perfil(self):
        """Cada tipo de usuário exibe perfil de forma diferente."""
        pass

    def __str__(self):
        return f"{self.nome} ({self.email})"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, nome='{self.nome}')"

    def __eq__(self, outro):
        if not isinstance(outro, Usuario):
            return False
        return self.id == outro.id


class Cliente(Usuario):
    def __init__(self, id, nome, email, telefone):
        super().__init__(id, nome, email, telefone)
        self.__historico = []  # lista de agendamentos passados

    @property
    def historico(self):
        return list(self.__historico)  # retorna cópia

    def adicionar_ao_historico(self, agendamento):
        self.__historico.append(agendamento)

    def exibir_perfil(self):  # POLIMORFISMO
        perfil = f"=== Perfil do Cliente ===\n"
        perfil += f"Nome: {self.nome}\n"
        perfil += f"Email: {self.email}\n"
        perfil += f"Telefone: {self.telefone}\n"
        perfil += f"Agendamentos realizados: {len(self.__historico)}"
        return perfil


class Barbeiro(Usuario):
    def __init__(self, id, nome, email, telefone):
        super().__init__(id, nome, email, telefone)
        self.__servicos = []         # COMPOSIÇÃO: Barbeiro TEM Servicos
        self.__horarios_trabalho = [] # ex: ["09:00", "10:00", ...]

    @property
    def servicos(self):
        return list(self.__servicos)

    @property
    def horarios_trabalho(self):
        return list(self.__horarios_trabalho)

    def adicionar_servico(self, servico):
        self.__servicos.append(servico)

    def definir_horarios(self, horarios):
        self.__horarios_trabalho = horarios

    def exibir_perfil(self):  # POLIMORFISMO
        perfil = f"=== Perfil do Barbeiro ===\n"
        perfil += f"Nome: {self.nome}\n"
        perfil += f"Serviços oferecidos: {len(self.__servicos)}\n"
        for s in self.__servicos:
            perfil += f"  - {s}\n"
        perfil += f"Horários: {', '.join(self.__horarios_trabalho)}"
        return perfil
```

---

#### [NEW] `corteja/servicos.py`

**Conceitos demonstrados**: encapsulamento, `@property` com validação, `@staticmethod`, `__str__`, `__repr__`, `__eq__`.

```python
from corteja.exceptions import DadosInvalidosError

class Servico:
    def __init__(self, nome, preco, duracao_minutos):
        self.nome = nome
        self.preco = preco  # usa setter
        self.__duracao_minutos = duracao_minutos

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor):
        if valor < 0:
            raise DadosInvalidosError("Preço não pode ser negativo.")
        self.__preco = valor

    @property
    def duracao_minutos(self):
        return self.__duracao_minutos

    @staticmethod
    def formatar_preco(valor):
        return f"R$ {valor:.2f}"

    def __str__(self):
        return f"{self.nome} - {Servico.formatar_preco(self.__preco)} ({self.__duracao_minutos}min)"

    def __repr__(self):
        return f"Servico('{self.nome}', {self.__preco}, {self.__duracao_minutos})"

    def __eq__(self, outro):
        if not isinstance(outro, Servico):
            return False
        return self.nome == outro.nome
```

---

#### [NEW] `corteja/agendamentos.py`

**Conceitos demonstrados**: encapsulamento com validação de estado, `@property`, `@classmethod`, `@staticmethod`, `__str__`, `__repr__`, `__eq__`, `__lt__`, exceções.

```python
from corteja.exceptions import CancelamentoInvalidoError

class Agendamento:
    _total_realizados = 0
    ESTADOS_VALIDOS = ["agendado", "confirmado", "concluido", "cancelado"]
    TRANSICOES = {
        "agendado": ["confirmado", "cancelado"],
        "confirmado": ["concluido", "cancelado"],
        "concluido": [],
        "cancelado": []
    }

    def __init__(self, id, cliente, barbeiro, servico, data, hora):
        self.id = id
        self.cliente = cliente      # composição
        self.barbeiro = barbeiro    # composição
        self.servico = servico      # composição
        self.data = data            # string "dd/mm/aaaa"
        self.hora = hora            # string "HH:MM"
        self.__status = "agendado"
        Agendamento._total_realizados += 1

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, novo_status):
        if novo_status not in self.ESTADOS_VALIDOS:
            raise CancelamentoInvalidoError(f"Status inválido: {novo_status}")
        if novo_status not in self.TRANSICOES[self.__status]:
            raise CancelamentoInvalidoError(
                f"Não é possível mudar de '{self.__status}' para '{novo_status}'."
            )
        self.__status = novo_status

    def confirmar(self):
        self.status = "confirmado"

    def concluir(self):
        self.status = "concluido"

    def cancelar(self):
        self.status = "cancelado"

    @classmethod
    def total_realizados(cls):
        return cls._total_realizados

    @staticmethod
    def validar_hora(hora):
        partes = hora.split(":")
        if len(partes) != 2:
            return False
        try:
            h, m = int(partes[0]), int(partes[1])
            return 0 <= h <= 23 and 0 <= m <= 59
        except ValueError:
            return False

    def __str__(self):
        return (f"[{self.id}] {self.data} {self.hora} - "
                f"{self.cliente.nome} com {self.barbeiro.nome} "
                f"({self.servico.nome}) [{self.__status}]")

    def __repr__(self):
        return f"Agendamento(id={self.id}, status='{self.__status}')"

    def __eq__(self, outro):
        if not isinstance(outro, Agendamento):
            return False
        return self.id == outro.id

    def __lt__(self, outro):
        # Ordena por data e hora
        if self.data == outro.data:
            return self.hora < outro.hora
        return self.data < outro.data
```

---

#### [NEW] `corteja/barbearia.py`

Classe orquestradora. **Conceitos**: composição, dunder methods (`__len__`, `__iter__`, `__contains__`, `__getitem__`), `try/except`.

```python
from corteja.exceptions import (
    HorarioIndisponivelError,
    ServicoNaoEncontradoError,
    DadosInvalidosError
)
from corteja.agendamentos import Agendamento

class Barbearia:
    def __init__(self, nome):
        self.nome = nome
        self.__barbeiros = []      # composição: TEM barbeiros
        self.__clientes = []       # composição: TEM clientes
        self.__agendamentos = []   # composição: TEM agendamentos
        self.__proximo_id = 1

    # --- Gerenciamento ---
    def cadastrar_barbeiro(self, barbeiro):
        self.__barbeiros.append(barbeiro)

    def cadastrar_cliente(self, cliente):
        self.__clientes.append(cliente)

    def listar_barbeiros(self):
        return list(self.__barbeiros)

    def listar_clientes(self):
        return list(self.__clientes)

    def buscar_barbeiro_por_id(self, id):
        for b in self.__barbeiros:
            if b.id == id:
                return b
        return None

    def buscar_cliente_por_id(self, id):
        for c in self.__clientes:
            if c.id == id:
                return c
        return None

    # --- Agendamento (com validação e exceções) ---
    def agendar(self, cliente, barbeiro, servico, data, hora):
        if not Agendamento.validar_hora(hora):
            raise DadosInvalidosError(f"Hora inválida: {hora}")

        if servico not in barbeiro.servicos:
            raise ServicoNaoEncontradoError(
                f"'{servico.nome}' não é oferecido por {barbeiro.nome}."
            )

        # Verifica conflito de horário
        for ag in self.__agendamentos:
            if (ag.barbeiro == barbeiro and ag.data == data
                    and ag.hora == hora and ag.status != "cancelado"):
                raise HorarioIndisponivelError(
                    f"Horário {hora} em {data} já ocupado com {barbeiro.nome}."
                )

        agendamento = Agendamento(
            self.__proximo_id, cliente, barbeiro, servico, data, hora
        )
        self.__agendamentos.append(agendamento)
        cliente.adicionar_ao_historico(agendamento)
        self.__proximo_id += 1
        return agendamento

    def listar_agendamentos(self, barbeiro=None, data=None):
        resultado = self.__agendamentos
        if barbeiro:
            resultado = [a for a in resultado if a.barbeiro == barbeiro]
        if data:
            resultado = [a for a in resultado if a.data == data]
        return sorted(resultado)  # usa __lt__

    # --- Dunder Methods ---
    def __len__(self):
        return len(self.__agendamentos)

    def __iter__(self):
        return iter(sorted(self.__agendamentos))

    def __contains__(self, item):
        # Verifica se um barbeiro está cadastrado
        if hasattr(item, 'servicos'):  # é barbeiro
            return item in self.__barbeiros
        return item in self.__clientes

    def __getitem__(self, indice):
        return sorted(self.__agendamentos)[indice]

    def __str__(self):
        return (f"Barbearia '{self.nome}' - "
                f"{len(self.__barbeiros)} barbeiro(s), "
                f"{len(self.__agendamentos)} agendamento(s)")
```

---

#### [NEW] `corteja/utils.py`

**Conceitos**: recursão (dois exemplos claros).

```python
def buscar_horario_disponivel(horarios, agendamentos_do_dia, indice=0):
    """
    Busca RECURSIVAMENTE o primeiro horário disponível em uma lista.
    Caso base: encontrou horário livre ou acabou a lista.
    """
    if indice >= len(horarios):
        return None  # caso base: nenhum horário disponível

    horario = horarios[indice]
    ocupado = False
    for ag in agendamentos_do_dia:
        if ag.hora == horario and ag.status != "cancelado":
            ocupado = True
            break

    if not ocupado:
        return horario  # caso base: encontrou!

    # Chamada recursiva: tenta o próximo horário
    return buscar_horario_disponivel(horarios, agendamentos_do_dia, indice + 1)


def calcular_faturamento(agendamentos, indice=0):
    """
    Calcula RECURSIVAMENTE o faturamento total dos agendamentos concluídos.
    Caso base: chegou ao fim da lista.
    """
    if indice >= len(agendamentos):
        return 0.0  # caso base

    ag = agendamentos[indice]
    valor = ag.servico.preco if ag.status == "concluido" else 0.0

    # Chamada recursiva: soma com o restante
    return valor + calcular_faturamento(agendamentos, indice + 1)


def contar_agendamentos_por_status(agendamentos, status, indice=0):
    """
    Conta RECURSIVAMENTE quantos agendamentos têm determinado status.
    """
    if indice >= len(agendamentos):
        return 0  # caso base

    conta = 1 if agendamentos[indice].status == status else 0
    return conta + contar_agendamentos_por_status(agendamentos, status, indice + 1)
```

---

#### [NEW] `main.py`

Menu interativo no console. **Conceitos**: `try/except/else/finally`, importação de pacotes.

O menu terá as opções:
1. Cadastrar Cliente
2. Listar Barbeiros e Serviços
3. Agendar Serviço
4. Visualizar Agenda do Dia
5. Confirmar / Concluir Agendamento
6. Cancelar Agendamento
7. Buscar Próximo Horário Disponível (recursão)
8. Relatório de Faturamento (recursão)
9. Exibir Perfil (polimorfismo)
0. Sair

> [!NOTE]
> O `main.py` já virá pré-carregado com dados de exemplo (2 barbeiros, 5 serviços, 1 cliente) para facilitar a demonstração sem precisar cadastrar tudo manualmente.

---

## Verificação

### Testes manuais no console
Após implementar, rodaremos `python main.py` e testaremos:
1. Cadastrar um cliente → verificar validação de email
2. Agendar serviço → verificar conflito de horário
3. Cancelar agendamento → verificar transição de status inválida
4. Buscar horário disponível → verificar recursão
5. Faturamento → verificar soma recursiva
6. Ordenar agendamentos → verificar `__lt__`
7. `for ag in barbearia:` → verificar `__iter__`
8. `barbeiro in barbearia` → verificar `__contains__`
9. `barbearia[0]` → verificar `__getitem__`
10. `len(barbearia)` → verificar `__len__`

### Checklist de conceitos
- [ ] Módulos/Pacotes com `__init__.py`
- [ ] Classe abstrata (ABC) com `@abstractmethod`
- [ ] Herança (`Cliente` e `Barbeiro` herdam de `Usuario`)
- [ ] Polimorfismo (`exibir_perfil()`)
- [ ] Encapsulamento (`__status` com `@property`)
- [ ] `@classmethod` e `@staticmethod`
- [ ] Composição (Barbearia tem Barbeiro, Agendamento, etc.)
- [ ] Dunder methods (pelo menos 7 diferentes)
- [ ] Exceções customizadas com hierarquia
- [ ] `try/except/else/finally`
- [ ] Recursão (pelo menos 2 funções)
- [ ] Código simples o suficiente para juniores explicarem
