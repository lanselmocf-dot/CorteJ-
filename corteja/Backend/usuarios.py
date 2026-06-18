"""
Módulo de usuários do sistema Cortejá.

Contém a classe abstrata Usuario e suas subclasses Cliente e Barbeiro.

Conceitos demonstrados:
- ABC e @abstractmethod (Abstração)
- Herança (Cliente e Barbeiro herdam de Usuario)
- Polimorfismo (exibir_perfil() diferente em cada subclasse)
- Encapsulamento (__nome, __email, __telefone com @property)
- @classmethod (total_cadastrados)
- Dunder methods (__str__, __repr__, __eq__)
"""

from abc import ABC, abstractmethod
from corteja.exceptions import DadosInvalidosError


class Usuario(ABC):
    """
    Classe ABSTRATA base para todos os usuários do sistema.

    Não pode ser instanciada diretamente — obriga as subclasses
    a implementarem o método exibir_perfil().

    Atributos:
        id (int): Identificador único do usuário
        nome (str): Nome completo (validado — não pode ser vazio)
        email (str): Email (validado — deve conter @)
        telefone (str): Telefone de contato
    """

    _total_cadastrados = 0  # Atributo de CLASSE (compartilhado entre todas as instâncias)

    def __init__(self, id, nome, email, telefone):
        """
        Inicializa um usuário.

        Parâmetros:
            id (int): Identificador único
            nome (str): Nome completo
            email (str): Endereço de email
            telefone (str): Telefone de contato

        Lança:
            DadosInvalidosError: Se nome vazio ou email sem @
        """
        self.id = id
        self.nome = nome          # Usa o setter do @property (valida)
        self.email = email        # Usa o setter do @property (valida)
        self.__telefone = telefone
        Usuario._total_cadastrados += 1

    # --- ENCAPSULAMENTO com @property ---

    @property
    def nome(self):
        """Retorna o nome do usuário."""
        return self.__nome

    @nome.setter
    def nome(self, valor):
        """Define o nome, validando que não seja vazio."""
        if not valor or not valor.strip():
            raise DadosInvalidosError("Nome não pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def email(self):
        """Retorna o email do usuário."""
        return self.__email

    @email.setter
    def email(self, valor):
        """Define o email, validando que contenha @."""
        if "@" not in valor:
            raise DadosInvalidosError(f"Email inválido: {valor}")
        self.__email = valor

    @property
    def telefone(self):
        """Retorna o telefone do usuário."""
        return self.__telefone

    # --- @classmethod ---

    @classmethod
    def total_cadastrados(cls):
        """Retorna o total de usuários cadastrados (atributo de classe)."""
        return cls._total_cadastrados

    # --- MÉTODO ABSTRATO (obriga subclasses a implementar) ---

    @abstractmethod
    def exibir_perfil(self):
        """
        Exibe o perfil do usuário.
        Cada subclasse implementa de forma diferente (POLIMORFISMO).
        """
        pass

    # --- DUNDER METHODS ---

    def __str__(self):
        """Representação amigável para o usuário (usada em print)."""
        return f"{self.nome} ({self.email})"

    def __repr__(self):
        """Representação técnica para debug."""
        return f"{self.__class__.__name__}(id={self.id}, nome='{self.nome}')"

    def __eq__(self, outro):
        """Dois usuários são iguais se têm o mesmo id."""
        if not isinstance(outro, Usuario):
            return False
        return self.id == outro.id


class Cliente(Usuario):
    """
    Representa um cliente da barbearia.
    Herda de Usuario e implementa exibir_perfil().

    Atributos adicionais:
        historico (list): Lista de agendamentos realizados pelo cliente
    """

    def __init__(self, id, nome, email, telefone):
        """Inicializa o cliente chamando o construtor do pai com super()."""
        super().__init__(id, nome, email, telefone)
        self.__historico = []  # Lista privada de agendamentos passados

    @property
    def historico(self):
        """Retorna uma cópia do histórico (protege a lista original)."""
        return list(self.__historico)

    def adicionar_ao_historico(self, agendamento):
        """Adiciona um agendamento ao histórico do cliente."""
        self.__historico.append(agendamento)

    def exibir_perfil(self):
        """
        POLIMORFISMO: Exibe perfil com foco nos agendamentos do cliente.
        Diferente do perfil do Barbeiro, que mostra serviços e horários.
        """
        perfil = "=" * 35 + "\n"
        perfil += "      PERFIL DO CLIENTE\n"
        perfil += "=" * 35 + "\n"
        perfil += f"  Nome:      {self.nome}\n"
        perfil += f"  Email:     {self.email}\n"
        perfil += f"  Telefone:  {self.telefone}\n"
        perfil += f"  Agendamentos: {len(self.__historico)}\n"
        perfil += "=" * 35
        return perfil


class Barbeiro(Usuario):
    """
    Representa um barbeiro/profissional da barbearia.
    Herda de Usuario e implementa exibir_perfil().

    Atributos adicionais:
        servicos (list): Serviços oferecidos (COMPOSIÇÃO: Barbeiro TEM Serviços)
        horarios_trabalho (list): Horários disponíveis para atendimento
    """

    def __init__(self, id, nome, email, telefone):
        """Inicializa o barbeiro chamando o construtor do pai com super()."""
        super().__init__(id, nome, email, telefone)
        self.__servicos = []           # COMPOSIÇÃO: Barbeiro TEM Serviços
        self.__horarios_trabalho = []  # Lista de horários (ex: ["09:00", "10:00"])

    @property
    def servicos(self):
        """Retorna uma cópia da lista de serviços."""
        return list(self.__servicos)

    @property
    def horarios_trabalho(self):
        """Retorna uma cópia da lista de horários de trabalho."""
        return list(self.__horarios_trabalho)

    def adicionar_servico(self, servico):
        """Adiciona um serviço à lista de serviços oferecidos pelo barbeiro."""
        self.__servicos.append(servico)

    def definir_horarios(self, horarios):
        """Define os horários de trabalho do barbeiro."""
        self.__horarios_trabalho = horarios

    def exibir_perfil(self):
        """
        POLIMORFISMO: Exibe perfil com foco nos serviços e horários.
        Diferente do perfil do Cliente, que mostra histórico de agendamentos.
        """
        perfil = "=" * 35 + "\n"
        perfil += "      PERFIL DO BARBEIRO\n"
        perfil += "=" * 35 + "\n"
        perfil += f"  Nome:      {self.nome}\n"
        perfil += f"  Email:     {self.email}\n"
        perfil += f"  Telefone:  {self.telefone}\n"
        perfil += f"\n  Serviços oferecidos:\n"
        for s in self.__servicos:
            perfil += f"    • {s}\n"
        perfil += f"\n  Horários de trabalho:\n"
        perfil += f"    {', '.join(self.__horarios_trabalho)}\n"
        perfil += "=" * 35
        return perfil
