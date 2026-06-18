"""
Módulo de serviços do sistema Cortejá.

Contém a classe Servico que representa os tipos de atendimento
oferecidos pela barbearia (corte, barba, etc.).

Conceitos demonstrados:
- Encapsulamento (__preco com validação via @property)
- @staticmethod (formatar_preco)
- Dunder methods (__str__, __repr__, __eq__)
"""

from corteja.exceptions import DadosInvalidosError


class Servico:
    """
    Representa um serviço oferecido pela barbearia.

    Atributos:
        nome (str): Nome do serviço (ex: "Corte Masculino")
        preco (float): Preço do serviço (validado — não pode ser negativo)
        duracao_minutos (int): Duração estimada em minutos
    """

    def __init__(self, nome, preco, duracao_minutos):
        """
        Inicializa um serviço.

        Parâmetros:
            nome (str): Nome do serviço
            preco (float): Preço do serviço
            duracao_minutos (int): Duração estimada em minutos

        Lança:
            DadosInvalidosError: Se o preço for negativo
        """
        self.__nome = nome
        self.preco = preco  # Usa o setter do @property (valida preço)
        self.__duracao_minutos = duracao_minutos

    # --- ENCAPSULAMENTO com @property ---

    @property
    def nome(self):
        """Retorna o nome do serviço."""
        return self.__nome

    @property
    def preco(self):
        """Retorna o preço do serviço."""
        return self.__preco

    @preco.setter
    def preco(self, valor):
        """
        Define o preço, validando que não seja negativo.
        Exemplo de encapsulamento: protege o dado de valores inválidos.
        """
        if valor < 0:
            raise DadosInvalidosError("Preço não pode ser negativo.")
        self.__preco = valor

    @property
    def duracao_minutos(self):
        """Retorna a duração estimada do serviço em minutos."""
        return self.__duracao_minutos

    # --- @staticmethod ---

    @staticmethod
    def formatar_preco(valor):
        """
        Formata um valor numérico como preço em Reais.
        Método estático: não depende de nenhuma instância.

        Parâmetros:
            valor (float): Valor a formatar

        Retorna:
            str: Valor formatado (ex: "R$ 35.00")
        """
        return f"R$ {valor:.2f}"

    # --- DUNDER METHODS ---

    def __str__(self):
        """Representação amigável (usada em print)."""
        return f"{self.__nome} - {Servico.formatar_preco(self.__preco)} ({self.__duracao_minutos}min)"

    def __repr__(self):
        """Representação técnica para debug."""
        return f"Servico('{self.__nome}', {self.__preco}, {self.__duracao_minutos})"

    def __eq__(self, outro):
        """Dois serviços são iguais se têm o mesmo nome."""
        if not isinstance(outro, Servico):
            return False
        return self.__nome == outro.__nome
