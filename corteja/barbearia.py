"""
Módulo principal do sistema Cortejá — Classe Barbearia.

A Barbearia é a classe orquestradora que gerencia todos os
barbeiros, clientes e agendamentos do sistema.

Conceitos demonstrados:
- Composição (Barbearia TEM listas de Barbeiro, Cliente e Agendamento)
- Dunder methods (__len__, __iter__, __contains__, __getitem__, __str__)
- Tratamento de exceções (try/except ao agendar)
"""

from corteja.exceptions import (
    HorarioIndisponivelError,
    ServicoNaoEncontradoError,
    DadosInvalidosError,
)
from corteja.agendamentos import Agendamento


class Barbearia:
    """
    Classe orquestradora do sistema Cortejá.

    Gerencia o cadastro de barbeiros e clientes, e controla
    o fluxo de agendamentos (criar, listar, cancelar).

    Atributos:
        nome (str): Nome da barbearia
        barbeiros (list): Lista de barbeiros cadastrados (COMPOSIÇÃO)
        clientes (list): Lista de clientes cadastrados (COMPOSIÇÃO)
        agendamentos (list): Lista de todos os agendamentos (COMPOSIÇÃO)
    """

    def __init__(self, nome):
        """
        Inicializa a barbearia.

        Parâmetros:
            nome (str): Nome da barbearia
        """
        self.nome = nome
        self.__barbeiros = []       # COMPOSIÇÃO: Barbearia TEM barbeiros
        self.__clientes = []        # COMPOSIÇÃO: Barbearia TEM clientes
        self.__agendamentos = []    # COMPOSIÇÃO: Barbearia TEM agendamentos
        self.__proximo_id = 1       # Auto-incremento de ID dos agendamentos

    # =========================================================
    #  GERENCIAMENTO DE CADASTROS
    # =========================================================

    def cadastrar_barbeiro(self, barbeiro):
        """Adiciona um barbeiro à barbearia."""
        self.__barbeiros.append(barbeiro)

    def cadastrar_cliente(self, cliente):
        """Adiciona um cliente à barbearia."""
        self.__clientes.append(cliente)

    def listar_barbeiros(self):
        """Retorna cópia da lista de barbeiros."""
        return list(self.__barbeiros)

    def listar_clientes(self):
        """Retorna cópia da lista de clientes."""
        return list(self.__clientes)

    def buscar_barbeiro_por_id(self, id):
        """
        Busca um barbeiro pelo seu ID.

        Retorna:
            Barbeiro ou None: O barbeiro encontrado, ou None se não existe.
        """
        for b in self.__barbeiros:
            if b.id == id:
                return b
        return None

    def buscar_cliente_por_id(self, id):
        """
        Busca um cliente pelo seu ID.

        Retorna:
            Cliente ou None: O cliente encontrado, ou None se não existe.
        """
        for c in self.__clientes:
            if c.id == id:
                return c
        return None

    # =========================================================
    #  AGENDAMENTO (com validação e exceções)
    # =========================================================

    def agendar(self, cliente, barbeiro, servico, data, hora):
        """
        Cria um novo agendamento com validações completas.

        Verificações:
        1. Se a hora é válida (formato HH:MM)
        2. Se o serviço é oferecido pelo barbeiro
        3. Se o horário não está ocupado

        Parâmetros:
            cliente (Cliente): Quem está agendando
            barbeiro (Barbeiro): Profissional escolhido
            servico (Servico): Serviço desejado
            data (str): Data ("dd/mm/aaaa")
            hora (str): Hora ("HH:MM")

        Retorna:
            Agendamento: O agendamento criado

        Lança:
            DadosInvalidosError: Se a hora for inválida
            ServicoNaoEncontradoError: Se o barbeiro não oferece o serviço
            HorarioIndisponivelError: Se o horário já está ocupado
        """
        # Validação 1: Hora válida
        if not Agendamento.validar_hora(hora):
            raise DadosInvalidosError(f"Hora inválida: '{hora}'. Use o formato HH:MM.")

        # Validação 2: Barbeiro oferece o serviço
        if servico not in barbeiro.servicos:
            raise ServicoNaoEncontradoError(
                f"O serviço '{servico.nome}' não é oferecido por {barbeiro.nome}."
            )

        # Validação 3: Horário disponível (verifica conflito)
        for ag in self.__agendamentos:
            if (ag.barbeiro == barbeiro
                    and ag.data == data
                    and ag.hora == hora
                    and ag.status != "cancelado"):
                raise HorarioIndisponivelError(
                    f"Horário {hora} em {data} já está ocupado com {barbeiro.nome}."
                )

        # Tudo validado — cria o agendamento
        agendamento = Agendamento(
            self.__proximo_id, cliente, barbeiro, servico, data, hora
        )
        self.__agendamentos.append(agendamento)
        cliente.adicionar_ao_historico(agendamento)
        self.__proximo_id += 1
        return agendamento

    def buscar_agendamento_por_id(self, id):
        """
        Busca um agendamento pelo seu ID.

        Retorna:
            Agendamento ou None
        """
        for ag in self.__agendamentos:
            if ag.id == id:
                return ag
        return None

    def listar_agendamentos(self, barbeiro=None, data=None):
        """
        Lista agendamentos com filtros opcionais.

        Parâmetros:
            barbeiro (Barbeiro, opcional): Filtrar por barbeiro
            data (str, opcional): Filtrar por data

        Retorna:
            list: Lista de agendamentos ordenados (usa __lt__)
        """
        resultado = self.__agendamentos
        if barbeiro:
            resultado = [a for a in resultado if a.barbeiro == barbeiro]
        if data:
            resultado = [a for a in resultado if a.data == data]
        return sorted(resultado)  # sorted() usa __lt__ de Agendamento

    def obter_todos_agendamentos(self):
        """Retorna cópia de todos os agendamentos (para uso em utils.py)."""
        return list(self.__agendamentos)

    # =========================================================
    #  DUNDER METHODS
    # =========================================================

    def __len__(self):
        """
        Permite usar len(barbearia) para saber o total de agendamentos.
        Exemplo: print(f"Total: {len(barbearia)} agendamentos")
        """
        return len(self.__agendamentos)

    def __iter__(self):
        """
        Permite iterar sobre os agendamentos com for.
        Exemplo: for ag in barbearia: print(ag)
        """
        return iter(sorted(self.__agendamentos))

    def __contains__(self, item):
        """
        Permite usar 'in' para verificar se um barbeiro ou cliente está cadastrado.
        Exemplo: if barbeiro in barbearia: ...
        """
        if hasattr(item, "servicos"):  # É um Barbeiro (tem atributo servicos)
            return item in self.__barbeiros
        return item in self.__clientes

    def __getitem__(self, indice):
        """
        Permite acessar agendamentos por índice: barbearia[0], barbearia[1], etc.
        Os agendamentos são retornados ordenados por data/hora.
        """
        return sorted(self.__agendamentos)[indice]

    def __str__(self):
        """Representação amigável da barbearia."""
        return (
            f"✂️  Barbearia '{self.nome}' — "
            f"{len(self.__barbeiros)} barbeiro(s), "
            f"{len(self.__clientes)} cliente(s), "
            f"{len(self.__agendamentos)} agendamento(s)"
        )
