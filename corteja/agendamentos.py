"""
Módulo de agendamentos do sistema Cortejá.

Contém a classe Agendamento que representa uma reserva de serviço
entre um cliente e um barbeiro em determinada data e hora.

Conceitos demonstrados:
- Encapsulamento (__status com máquina de estados via @property)
- Composição (Agendamento TEM Cliente, Barbeiro e Servico)
- @classmethod (total_realizados)
- @staticmethod (validar_hora)
- Dunder methods (__str__, __repr__, __eq__, __lt__)
- Exceções (CancelamentoInvalidoError para transições inválidas)
"""

from corteja.exceptions import CancelamentoInvalidoError


class Agendamento:
    """
    Representa um agendamento de serviço no sistema Cortejá.

    O status do agendamento segue uma máquina de estados:
        agendado → confirmado → concluido
        agendado → cancelado
        confirmado → cancelado

    Atributos:
        id (int): Identificador único do agendamento
        cliente (Cliente): Cliente que fez o agendamento (COMPOSIÇÃO)
        barbeiro (Barbeiro): Barbeiro que atenderá (COMPOSIÇÃO)
        servico (Servico): Serviço a ser realizado (COMPOSIÇÃO)
        data (str): Data no formato "dd/mm/aaaa"
        hora (str): Hora no formato "HH:MM"
        status (str): Status atual (protegido por @property)
    """

    _total_realizados = 0  # Atributo de CLASSE

    # Máquina de estados: define transições válidas
    ESTADOS_VALIDOS = ["agendado", "confirmado", "concluido", "cancelado"]
    TRANSICOES = {
        "agendado": ["confirmado", "cancelado"],
        "confirmado": ["concluido", "cancelado"],
        "concluido": [],     # Estado final — não pode mudar
        "cancelado": [],     # Estado final — não pode mudar
    }

    def __init__(self, id, cliente, barbeiro, servico, data, hora):
        """
        Inicializa um agendamento com status "agendado".

        Parâmetros:
            id (int): Identificador único
            cliente (Cliente): Quem está agendando
            barbeiro (Barbeiro): Profissional escolhido
            servico (Servico): Serviço desejado
            data (str): Data do agendamento ("dd/mm/aaaa")
            hora (str): Hora do agendamento ("HH:MM")
        """
        self.id = id
        self.cliente = cliente      # COMPOSIÇÃO: Agendamento TEM Cliente
        self.barbeiro = barbeiro    # COMPOSIÇÃO: Agendamento TEM Barbeiro
        self.servico = servico      # COMPOSIÇÃO: Agendamento TEM Serviço
        self.data = data
        self.hora = hora
        self.__status = "agendado"  # Status inicial (privado)
        Agendamento._total_realizados += 1

    # --- ENCAPSULAMENTO com @property (máquina de estados) ---

    @property
    def status(self):
        """Retorna o status atual do agendamento."""
        return self.__status

    @status.setter
    def status(self, novo_status):
        """
        Altera o status com VALIDAÇÃO de transição.

        Só permite transições definidas no dicionário TRANSICOES.
        Exemplo: "agendado" pode ir para "confirmado" ou "cancelado",
                 mas NÃO pode ir direto para "concluido".

        Lança:
            CancelamentoInvalidoError: Se a transição for inválida
        """
        if novo_status not in self.ESTADOS_VALIDOS:
            raise CancelamentoInvalidoError(
                f"Status '{novo_status}' não é válido. "
                f"Use: {', '.join(self.ESTADOS_VALIDOS)}"
            )
        if novo_status not in self.TRANSICOES[self.__status]:
            raise CancelamentoInvalidoError(
                f"Não é possível mudar de '{self.__status}' para '{novo_status}'. "
                f"Transições permitidas: {self.TRANSICOES[self.__status]}"
            )
        self.__status = novo_status

    # --- Métodos de conveniência ---

    def confirmar(self):
        """Confirma o agendamento (agendado → confirmado)."""
        self.status = "confirmado"

    def concluir(self):
        """Conclui o agendamento (confirmado → concluido)."""
        self.status = "concluido"

    def cancelar(self):
        """Cancela o agendamento (agendado/confirmado → cancelado)."""
        self.status = "cancelado"

    # --- @classmethod ---

    @classmethod
    def total_realizados(cls):
        """Retorna o total de agendamentos já criados (atributo de classe)."""
        return cls._total_realizados

    # --- @staticmethod ---

    @staticmethod
    def validar_hora(hora):
        """
        Valida se uma string está no formato HH:MM válido.
        Método estático: não depende de nenhuma instância.

        Parâmetros:
            hora (str): String a validar

        Retorna:
            bool: True se válido, False caso contrário
        """
        partes = hora.split(":")
        if len(partes) != 2:
            return False
        try:
            h, m = int(partes[0]), int(partes[1])
            return 0 <= h <= 23 and 0 <= m <= 59
        except ValueError:
            return False

    # --- DUNDER METHODS ---

    def __str__(self):
        """Representação amigável com todos os dados do agendamento."""
        return (
            f"[#{self.id}] {self.data} às {self.hora} - "
            f"{self.cliente.nome} com {self.barbeiro.nome} "
            f"({self.servico.nome}) [{self.__status.upper()}]"
        )

    def __repr__(self):
        """Representação técnica para debug."""
        return f"Agendamento(id={self.id}, status='{self.__status}')"

    def __eq__(self, outro):
        """Dois agendamentos são iguais se têm o mesmo id."""
        if not isinstance(outro, Agendamento):
            return False
        return self.id == outro.id

    def __lt__(self, outro):
        """
        Define ordenação: primeiro por data, depois por hora.
        Permite usar sorted() em listas de agendamentos.
        """
        if self.data == outro.data:
            return self.hora < outro.hora
        # Converte data dd/mm/aaaa para aaaa/mm/dd para ordenação correta
        partes_self = self.data.split("/")
        partes_outro = outro.data.split("/")
        data_self = f"{partes_self[2]}/{partes_self[1]}/{partes_self[0]}"
        data_outro = f"{partes_outro[2]}/{partes_outro[1]}/{partes_outro[0]}"
        return data_self < data_outro
