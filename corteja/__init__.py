"""
Pacote Cortejá — Sistema de Agendamento para Barbearias.

Este arquivo __init__.py transforma a pasta corteja/ em um PACOTE Python,
permitindo importações como:
    from corteja import Cliente, Barbeiro, Servico, Barbearia

Conceitos demonstrados:
- Pacotes Python (pasta com __init__.py)
- Tipos de importação (from ... import ...)
"""

# Importa as classes dos módulos internos para facilitar o uso
from corteja.usuarios import Usuario, Cliente, Barbeiro
from corteja.servicos import Servico
from corteja.agendamentos import Agendamento
from corteja.barbearia import Barbearia
from corteja.exceptions import (
    CortejaError,
    HorarioIndisponivelError,
    ServicoNaoEncontradoError,
    CancelamentoInvalidoError,
    DadosInvalidosError,
)
from corteja.utils import (
    buscar_horario_disponivel,
    calcular_faturamento,
    contar_agendamentos_por_status,
)

# Define o que é exportado quando alguém faz: from corteja import *
__all__ = [
    "Usuario",
    "Cliente",
    "Barbeiro",
    "Servico",
    "Agendamento",
    "Barbearia",
    "CortejaError",
    "HorarioIndisponivelError",
    "ServicoNaoEncontradoError",
    "CancelamentoInvalidoError",
    "DadosInvalidosError",
    "buscar_horario_disponivel",
    "calcular_faturamento",
    "contar_agendamentos_por_status",
]
