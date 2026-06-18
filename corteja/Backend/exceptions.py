"""
Módulo de exceções customizadas do sistema Cortejá.

Todas as exceções do sistema herdam de CortejaError,
permitindo capturar qualquer erro do sistema com um único except.

Hierarquia:
    CortejaError
    ├── HorarioIndisponivelError
    ├── ServicoNaoEncontradoError
    ├── CancelamentoInvalidoError
    └── DadosInvalidosError
"""


class CortejaError(Exception):
    """Exceção base do sistema Cortejá."""
    pass


class HorarioIndisponivelError(CortejaError):
    """Lançada quando o horário já está ocupado por outro agendamento."""
    pass


class ServicoNaoEncontradoError(CortejaError):
    """Lançada quando o serviço solicitado não existe no cadastro do barbeiro."""
    pass


class CancelamentoInvalidoError(CortejaError):
    """Lançada ao tentar uma transição de status inválida no agendamento."""
    pass


class DadosInvalidosError(CortejaError):
    """Lançada quando dados fornecidos são inválidos (nome vazio, email sem @, etc.)."""
    pass
