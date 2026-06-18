"""
Módulo de funções utilitárias com RECURSÃO.

Contém funções recursivas para:
- Buscar o próximo horário disponível
- Calcular faturamento total
- Contar agendamentos por status
"""


def buscar_horario_disponivel(horarios, agendamentos_do_dia, indice=0):
    """
    Busca RECURSIVAMENTE o primeiro horário disponível em uma lista.

    Parâmetros:
        horarios (list): Lista de horários possíveis (ex: ["09:00", "10:00", ...])
        agendamentos_do_dia (list): Lista de agendamentos já feitos no dia
        indice (int): Índice atual na busca (usado pela recursão)

    Retorna:
        str ou None: O primeiro horário livre encontrado, ou None se todos ocupados.

    Exemplo:
        >>> horarios = ["09:00", "10:00", "11:00"]
        >>> buscar_horario_disponivel(horarios, agendamentos)
        "10:00"  # se 09:00 já estiver ocupado
    """
    # CASO BASE 1: acabaram os horários para verificar
    if indice >= len(horarios):
        return None

    horario = horarios[indice]

    # Verifica se este horário está ocupado
    ocupado = False
    for ag in agendamentos_do_dia:
        if ag.hora == horario and ag.status != "cancelado":
            ocupado = True
            break

    # CASO BASE 2: encontrou um horário livre!
    if not ocupado:
        return horario

    # CHAMADA RECURSIVA: tenta o próximo horário
    return buscar_horario_disponivel(horarios, agendamentos_do_dia, indice + 1)


def calcular_faturamento(agendamentos, indice=0):
    """
    Calcula RECURSIVAMENTE o faturamento total dos agendamentos concluídos.

    Parâmetros:
        agendamentos (list): Lista de objetos Agendamento
        indice (int): Índice atual na soma (usado pela recursão)

    Retorna:
        float: Soma dos preços dos agendamentos com status "concluido".

    Exemplo:
        >>> calcular_faturamento(lista_agendamentos)
        150.0
    """
    # CASO BASE: chegou ao fim da lista
    if indice >= len(agendamentos):
        return 0.0

    ag = agendamentos[indice]

    # Só conta se o agendamento foi concluído
    valor = ag.servico.preco if ag.status == "concluido" else 0.0

    # CHAMADA RECURSIVA: soma com o restante da lista
    return valor + calcular_faturamento(agendamentos, indice + 1)


def contar_agendamentos_por_status(agendamentos, status, indice=0):
    """
    Conta RECURSIVAMENTE quantos agendamentos possuem determinado status.

    Parâmetros:
        agendamentos (list): Lista de objetos Agendamento
        status (str): Status a buscar ("agendado", "confirmado", "concluido", "cancelado")
        indice (int): Índice atual na contagem (usado pela recursão)

    Retorna:
        int: Quantidade de agendamentos com o status informado.

    Exemplo:
        >>> contar_agendamentos_por_status(agendamentos, "concluido")
        3
    """
    # CASO BASE: chegou ao fim da lista
    if indice >= len(agendamentos):
        return 0

    # Conta 1 se o status bate, 0 se não
    conta = 1 if agendamentos[indice].status == status else 0

    # CHAMADA RECURSIVA: soma com o restante
    return conta + contar_agendamentos_por_status(agendamentos, status, indice + 1)
