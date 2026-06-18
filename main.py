#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Interface de Console Interativa para o sistema Cortejá.

Este arquivo centraliza o controle do sistema, oferecendo um menu completo
para demonstrar todas as funcionalidades e conceitos de POO exigidos na disciplina:
- Módulos e Pacotes (Importações do pacote 'corteja')
- Herança e Polimorfismo (Clientes, Barbeiros e perfis)
- Encapsulamento e Validações
- Tratamento estruturado de exceções (try/except/else/finally)
- Recursão (faturamento, contagem de status e busca de horários)
- Dunder methods (interação avançada com a Barbearia)

O sistema inicia pré-carregado com dados para facilitar a demonstração imediata.
"""

import sys
from corteja import (
    Barbearia,
    Cliente,
    Barbeiro,
    Servico,
    CortejaError,
    HorarioIndisponivelError,
    ServicoNaoEncontradoError,
    CancelamentoInvalidoError,
    DadosInvalidosError
)
from corteja.utils import (
    buscar_horario_disponivel,
    calcular_faturamento,
    contar_agendamentos_por_status
)


def inicializar_dados_exemplo(barbearia):
    """Pré-carrega a barbearia com serviços, barbeiros, clientes e agendamentos."""
    # 1. Criação dos Serviços
    corte = Servico("Corte Degradê", 40.00, 30)
    barba = Servico("Barba Terapia", 30.00, 20)
    combo = Servico("Combo Corte & Barba", 60.00, 50)
    sobrancelha = Servico("Design de Sobrancelha", 15.00, 15)
    selagem = Servico("Selagem Capilar", 80.00, 60)

    # 2. Cadastro dos Barbeiros
    # Pedro Silva (ID: 1) oferece corte, combo e sobrancelha
    pedro = Barbeiro(1, "Pedro Silva", "pedro@corteja.com.br", "(81) 99999-1111")
    pedro.adicionar_servico(corte)
    pedro.adicionar_servico(combo)
    pedro.adicionar_servico(sobrancelha)
    pedro.definir_horarios(["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"])
    barbearia.cadastrar_barbeiro(pedro)

    # Lucas Souza (ID: 2) oferece corte, barba e selagem
    lucas = Barbeiro(2, "Lucas Souza", "lucas@corteja.com.br", "(81) 99999-2222")
    lucas.adicionar_servico(corte)
    lucas.adicionar_servico(barba)
    lucas.adicionar_servico(selagem)
    lucas.definir_horarios(["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"])
    barbearia.cadastrar_barbeiro(lucas)

    # 3. Cadastro dos Clientes
    carlos = Cliente(10, "Carlos Andrade", "carlos@gmail.com", "(81) 98888-3333")
    bruno = Cliente(11, "Bruno Costa", "bruno@hotmail.com", "(81) 98888-4444")
    barbearia.cadastrar_cliente(carlos)
    barbearia.cadastrar_cliente(bruno)

    # 4. Criação de Agendamentos iniciais
    # Agendamento 1: Carlos com Pedro (Corte degradê)
    ag1 = barbearia.agendar(carlos, pedro, corte, "26/05/2026", "09:00")
    
    # Agendamento 2: Bruno com Lucas (Barba) - Já concluído para fins de faturamento
    ag2 = barbearia.agendar(bruno, lucas, barba, "26/05/2026", "10:00")
    ag2.confirmar()
    ag2.concluir()

    # Agendamento 3: Carlos com Lucas (Selagem) - Agendamento cancelado
    ag3 = barbearia.agendar(carlos, lucas, selagem, "27/05/2026", "14:00")
    ag3.cancelar()


def limpar_tela():
    """Imprime linhas em branco para separar as telas no console."""
    print("\n" * 2)


def exibir_cabecalho(titulo):
    """Exibe um cabeçalho bonito no console."""
    print("=" * 60)
    print(f" {titulo.upper():^58}")
    print("=" * 60)


def ler_inteiro(mensagem):
    """Lê um número inteiro de forma segura, tratando erros de entrada."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("❌ Erro: Digite um número inteiro válido!")


def menu_principal():
    """Exibe o menu principal e retorna a opção escolhida."""
    exibir_cabecalho("Cortejá - Agendamento Inteligente")
    print(" 1 👤 Cadastrar Novo Cliente")
    print(" 2 💈 Listar Barbeiros e Serviços Oferecidos")
    print(" 3 📅 Agendar Novo Serviço")
    print(" 4 📋 Visualizar Agenda Completa (Ordenada)")
    print(" 5  Confirmar / Concluir Agendamento")
    print(" 6 ❌ Cancelar um Agendamento")
    print(" 7 🔍 Buscar Próximo Horário Disponível (Recursivo)")
    print(" 8 💰 Relatório Financeiro e de Status (Recursivo)")
    print(" 9 👁️  Visualizar Perfil de Usuário (Polimorfismo)")
    print(" 0 🚪 Sair do Sistema")
    print("-" * 60)
    return ler_inteiro("👉 Escolha uma opção: ")


def cadastrar_cliente_interface(barbearia):
    exibir_cabecalho("Cadastrar Novo Cliente")
    try:
        id_cli = ler_inteiro("Digite o ID (Número): ")
        
        # Verifica se ID já existe
        if barbearia.buscar_cliente_por_id(id_cli) or barbearia.buscar_barbeiro_por_id(id_cli):
            raise DadosInvalidosError(f"O ID {id_cli} já está em uso por outro usuário.")
            
        nome = input("Digite o nome completo: ")
        email = input("Digite o e-mail: ")
        telefone = input("Digite o telefone (ex: (81) 98888-8888): ")
        
        novo_cliente = Cliente(id_cli, nome, email, telefone)
        barbearia.cadastrar_cliente(novo_cliente)
        
    except DadosInvalidosError as err:
        print(f"\n❌ Erro de Validação: {err}")
    except Exception as err:
        print(f"\n❌ Erro Inesperado: {err}")
    else:
        print(f"\n✅ Cliente '{nome}' cadastrado com sucesso!")
    finally:
        print(f"ℹ️  Total de usuários cadastrados no sistema: {Cliente.total_cadastrados()}")


def listar_barbeiros_interface(barbearia):
    exibir_cabecalho("Barbeiros e Serviços Cadastrados")
    barbeiros = barbearia.listar_barbeiros()
    if not barbeiros:
        print("Nenhum barbeiro cadastrado.")
        return

    for idx, b in enumerate(barbeiros, 1):
        print(f"\n💈 [{idx}] Barbeiro ID {b.id}: {b.nome}")
        print(f"   📞 Telefone: {b.telefone} | ✉️  E-mail: {b.email}")
        print("   ✂️  Serviços oferecidos:")
        for s in b.servicos:
            print(f"      - {s.nome} ({Servico.formatar_preco(s.preco)} - {s.duracao_minutos}min)")
        print(f"   📅 Horários padrão: {', '.join(b.horarios_trabalho)}")
    print("-" * 60)


def agendar_servico_interface(barbearia):
    exibir_cabecalho("Agendar Novo Serviço")
    try:
        # 1. Identifica o Cliente
        id_cli = ler_inteiro("Digite o ID do Cliente: ")
        cliente = barbearia.buscar_cliente_por_id(id_cli)
        if not cliente:
            raise DadosInvalidosError(f"Cliente com ID {id_cli} não foi encontrado.")

        # 2. Identifica o Barbeiro
        print("\nBarbeiros Disponíveis:")
        for b in barbearia.listar_barbeiros():
            print(f"  [{b.id}] - {b.nome}")
        id_barb = ler_inteiro("\nDigite o ID do Barbeiro: ")
        barbeiro = barbearia.buscar_barbeiro_por_id(id_barb)
        if not barbeiro:
            raise DadosInvalidosError(f"Barbeiro com ID {id_barb} não foi encontrado.")

        # 3. Escolhe o Serviço
        print(f"\nServiços que o(a) {barbeiro.nome} realiza:")
        servicos = barbeiro.servicos
        for idx, s in enumerate(servicos, 1):
            print(f"  [{idx}] - {s}")
        
        opt_serv = ler_inteiro("\nEscolha o número do serviço: ")
        if opt_serv < 1 or opt_serv > len(servicos):
            raise ServicoNaoEncontradoError("Opção de serviço inválida!")
        servico = servicos[opt_serv - 1]

        # 4. Define Data e Hora
        data = input("Digite a data (dd/mm/aaaa): ")
        if len(data.split("/")) != 3:
            raise DadosInvalidosError("Formato de data inválido! Use dd/mm/aaaa.")
            
        hora = input("Digite o horário (HH:MM): ")

        # 5. Tenta efetuar o agendamento
        agendamento = barbearia.agendar(cliente, barbeiro, servico, data, hora)

    except CortejaError as err:
        print(f"\n❌ Falha no Agendamento: {err}")
    except Exception as err:
        print(f"\n❌ Ocorreu um erro no sistema: {err}")
    else:
        print(f"\n✅ Agendamento realizado com sucesso!")
        print(f"   Detalhes: {agendamento}")


def visualizar_agenda_interface(barbearia):
    exibir_cabecalho("Agenda Completa de Atendimentos")
    
    # Demonstração de dunder __len__
    print(f"Total de agendamentos no sistema: {len(barbearia)}")
    
    # Demonstração de dunder __iter__ (os agendamentos aparecem ordenados pelo __lt__)
    agendamentos = list(barbearia)
    if not agendamentos:
        print("\nNenhum agendamento registrado até o momento.")
        return

    print("\nLista Completa (Ordenada por Data/Hora):")
    print("-" * 60)
    for ag in barbearia:
        print(ag)
    print("-" * 60)
    
    # Demonstração de dunder __getitem__
    try:
        primeiro = barbearia[0]
        print(f"💡 Primeiro agendamento da fila: {primeiro.data} às {primeiro.hora} (ID {primeiro.id})")
    except IndexError:
        pass


def gerenciar_status_interface(barbearia):
    exibir_cabecalho("Atualizar Status do Agendamento")
    try:
        id_ag = ler_inteiro("Digite o ID do Agendamento: ")
        ag = barbearia.buscar_agendamento_por_id(id_ag)
        if not ag:
            raise DadosInvalidosError(f"Agendamento #{id_ag} não encontrado.")
            
        print(f"\nAgendamento encontrado: {ag}")
        print("Opções de Status:")
        print("  [1] Confirmar Atendimento")
        print("  [2] Concluir Atendimento e Realizar Pagamento")
        
        opcao = ler_inteiro("\nEscolha a ação: ")
        
        if opcao == 1:
            ag.confirmar()
            print("\n✅ Agendamento CONFIRMADO com sucesso!")
        elif opcao == 2:
            # Primeiro valida a transição de estado na máquina de estados de agendamentos
            # Lembrete: agendado -> confirmado -> concluido
            ag.concluir()
            
            # --- FLUXO DE PAGAMENTO SIMULADO ---
            limpar_tela()
            exibir_cabecalho("💳 Tela de Pagamento (Simulação)")
            valor_original = ag.servico.preco
            print(f" Cliente:      {ag.cliente.nome}")
            print(f" Profissional: {ag.barbeiro.nome}")
            print(f" Serviço:      {ag.servico.nome}")
            print(f" Valor Total:  {Servico.formatar_preco(valor_original)}")
            print("-" * 60)
            print(" Formas de Pagamento Disponíveis:")
            print("   [1] 📱 Pix (5% de desconto)")
            print("   [2] 💳 Cartão de Crédito")
            print("   [3] 💳 Cartão de Débito")
            print("   [4] 💵 Dinheiro")
            print("-" * 60)
            
            metodo = ler_inteiro("👉 Escolha a forma de pagamento: ")
            
            desconto = 0.0
            pago = valor_original
            troco = 0.0
            forma_str = ""
            
            if metodo == 1:
                forma_str = "Pix (App)"
                desconto = valor_original * 0.05
                pago = valor_original - desconto
                print(f"\n📱 Desconto Pix de 5%: -{Servico.formatar_preco(desconto)}")
                print(f"   Total com Desconto: {Servico.formatar_preco(pago)}")
                print("\n   [ QR CODE PIX SIMULADO ]")
                print("   █▀▀▀▀▀█ █ █▀▀ ▄▀ █▀▀▀▀▀█")
                print("   █ ███ █ █▄ █ ▄▀  █ ███ █")
                print("   █ ▀▀▀ █  ▀  ▄  ▄ █ ▀▀▀ █")
                print("   ▀▀▀▀▀▀▀ ▀ ▀▀▀▀▀▀ ▀▀▀▀▀▀▀")
                print("   corteja-pagamentos-pix-chave-aleatoria@corteja.com")
                print("\n⌛ Aguardando confirmação do Pix...")
                print("✅ Pagamento Pix confirmado e recebido instantaneamente!")
                
            elif metodo == 2 or metodo == 3:
                forma_str = "Cartão de Crédito" if metodo == 2 else "Cartão de Débito"
                print(f"\n⌛ Processando transação de {Servico.formatar_preco(pago)} na maquininha...")
                print("💳 Aproxime ou insira o cartão...")
                # Simula um delay rápido
                import time
                time.sleep(1)
                print("🔓 Senha verificada...")
                print("✅ Transação APROVADA pela operadora!")
                
            elif metodo == 4:
                forma_str = "Dinheiro (Físico)"
                while True:
                    dinheiro_recebido = float(input(f"\n💵 Digite o valor entregue pelo cliente (Min: {Servico.formatar_preco(pago)}): "))
                    if dinheiro_recebido >= pago:
                        troco = dinheiro_recebido - pago
                        break
                    else:
                        print("❌ Valor insuficiente! O cliente precisa pagar o valor total da conta.")
                
                if troco > 0:
                    print(f"💰 Troco do cliente: {Servico.formatar_preco(troco)}")
                print("✅ Dinheiro guardado no caixa!")
                
            else:
                forma_str = "Outros"
                print("\n⚠️ Forma de pagamento não identificada. Registrado como 'Outros'.")
            
            # --- IMPRESSÃO DO CUPOM FISCAL ---
            limpar_tela()
            print("=" * 60)
            print(f"{'✂️  CUPOM FISCAL DE SERVIÇO  ✂️':^60}")
            print(f"{'BARBEARIA CORTEJÁ - RECIFE':^60}")
            print("=" * 60)
            print(f" Data: {ag.data} às {ag.hora}")
            print(f" Agendamento Ref: #{ag.id}")
            print(f" Cliente: {ag.cliente.nome} (ID: {ag.cliente.id})")
            print(f" Profissional: {ag.barbeiro.nome}")
            print(f" Serviço realizado: {ag.servico.nome}")
            print("-" * 60)
            print(f" Subtotal:                 {Servico.formatar_preco(valor_original)}")
            if desconto > 0:
                print(f" Desconto aplicado:       -{Servico.formatar_preco(desconto)}")
            print(f" TOTAL PAGO:               {Servico.formatar_preco(pago)}")
            print(f" Forma de Pagamento:       {forma_str}")
            if troco > 0:
                print(f" Troco devolvido:          {Servico.formatar_preco(troco)}")
            print("=" * 60)
            print(f"{'OBRIGADO PELA PREFERÊNCIA!':^60}")
            print(f"{'Sua Barba, Sua Assinatura.':^60}")
            print("=" * 60)
            print("\n✅ Agendamento CONCLUÍDO e faturado no sistema!")
            
        else:
            print("\n❌ Opção inválida!")
            
    except CortejaError as err:
        print(f"\n❌ Erro na transição de status: {err}")
        print("   Lembre-se da máquina de estados: AGENDADO -> CONFIRMADO -> CONCLUIDO")
    except Exception as err:
        print(f"\n❌ Erro: {err}")


def cancelar_agendamento_interface(barbearia):
    exibir_cabecalho("Cancelar Agendamento")
    try:
        id_ag = ler_inteiro("Digite o ID do Agendamento a ser CANCELADO: ")
        ag = barbearia.buscar_agendamento_por_id(id_ag)
        if not ag:
            raise DadosInvalidosError(f"Agendamento #{id_ag} não encontrado.")
            
        print(f"\nAgendamento encontrado: {ag}")
        confirmar = input("Tem certeza que deseja cancelar? (s/n): ").strip().lower()
        if confirmar == 's':
            ag.cancelar()
            print("\n✅ Agendamento cancelado com sucesso!")
        else:
            print("\nOperação abortada.")
            
    except CortejaError as err:
        print(f"\n❌ Falha ao cancelar: {err}")
    except Exception as err:
        print(f"\n❌ Erro: {err}")


def buscar_horario_recursivo_interface(barbearia):
    exibir_cabecalho("Busca Inteligente de Horário (Recursão)")
    try:
        id_barb = ler_inteiro("Digite o ID do Barbeiro: ")
        barbeiro = barbearia.buscar_barbeiro_por_id(id_barb)
        if not barbeiro:
            raise DadosInvalidosError(f"Barbeiro com ID {id_barb} não encontrado.")
            
        data = input("Digite a data para a busca (dd/mm/aaaa): ")
        if len(data.split("/")) != 3:
            raise DadosInvalidosError("Data inválida. Use dd/mm/aaaa.")

        # Busca todos os agendamentos já registrados para esse barbeiro na data informada
        agendamentos_dia = barbearia.listar_agendamentos(barbeiro=barbeiro, data=data)
        
        # Pega a lista de todos os horários que o barbeiro trabalha
        horarios_possiveis = barbeiro.horarios_trabalho
        
        print("\n🔍 Analisando agenda de forma recursiva...")
        # Chamada da função recursiva de utils.py
        horario_livre = buscar_horario_disponivel(horarios_possiveis, agendamentos_dia)
        
        if horario_livre:
            print(f"✨ Excelente! O primeiro horário livre recursivamente encontrado é: {horario_livre}")
        else:
            print("❌ Que pena! Todos os horários deste barbeiro já estão ocupados neste dia.")
            
    except DadosInvalidosError as err:
        print(f"\n❌ Erro: {err}")
    except Exception as err:
        print(f"\n❌ Erro inesperado: {err}")


def relatorio_recursivo_interface(barbearia):
    exibir_cabecalho("Relatórios do Sistema (Algoritmos Recursivos)")
    
    agendamentos = barbearia.obter_todos_agendamentos()
    
    # 1. Demonstração de recursão para faturamento
    faturamento_total = calcular_faturamento(agendamentos)
    
    # 2. Demonstração de recursão para contagem de status
    agendados = contar_agendamentos_por_status(agendamentos, "agendado")
    confirmados = contar_agendamentos_por_status(agendamentos, "confirmado")
    concluidos = contar_agendamentos_por_status(agendamentos, "concluido")
    cancelados = contar_agendamentos_por_status(agendamentos, "cancelado")
    
    print(f"📊 Total acumulado de agendamentos: {len(barbearia)}")
    print(f"💰 Faturamento total realizado: {Servico.formatar_preco(faturamento_total)}")
    print("\n📋 Distribuição dos status (Contados recursivamente):")
    print(f"   ⏳ Agendados:   {agendados}")
    print(f"   ✅ Confirmados: {confirmados}")
    print(f"   🏆 Concluídos:  {concluidos}")
    print(f"   ❌ Cancelados:  {cancelados}")
    print("-" * 60)


def exibir_perfil_polimorfico_interface(barbearia):
    exibir_cabecalho("Visualizar Perfil (Demonstração de Polimorfismo)")
    id_usuario = ler_inteiro("Digite o ID do Usuário (Cliente ou Barbeiro): ")
    
    usuario = None
    
    # Procura na lista de Clientes
    usuario = barbearia.buscar_cliente_por_id(id_usuario)
    
    # Se não achou, procura na de Barbeiros
    if not usuario:
        usuario = barbearia.buscar_barbeiro_por_id(id_usuario)
        
    if not usuario:
        print(f"\n❌ Usuário com ID {id_usuario} não foi cadastrado no sistema.")
        return
        
    # Demonstração de dunder __contains__
    if usuario in barbearia:
        print("💡 Confirmação via 'in': Usuário está devidamente registrado na barbearia!")
    
    print("\nChamando método polimórfico exibir_perfil()...\n")
    # POLIMORFISMO EM AÇÃO:
    # A variável 'usuario' pode conter um 'Cliente' ou um 'Barbeiro'.
    # O Python decidirá dinamicamente em tempo de execução qual método executar!
    print(usuario.exibir_perfil())
    print("\n💡 Representação técnica (__repr__):")
    print(f"   {repr(usuario)}")
    print("-" * 60)


def main():
    # Inicializa a barbearia orquestradora
    minha_barbearia = Barbearia("Cortejá Recife")
    inicializar_dados_exemplo(minha_barbearia)
    
    while True:
        limpar_tela()
        opcao = menu_principal()
        
        limpar_tela()
        if opcao == 1:
            cadastrar_cliente_interface(minha_barbearia)
        elif opcao == 2:
            listar_barbeiros_interface(minha_barbearia)
        elif opcao == 3:
            agendar_servico_interface(minha_barbearia)
        elif opcao == 4:
            visualizar_agenda_interface(minha_barbearia)
        elif opcao == 5:
            gerenciar_status_interface(minha_barbearia)
        elif opcao == 6:
            cancelar_agendamento_interface(minha_barbearia)
        elif opcao == 7:
            buscar_horario_recursivo_interface(minha_barbearia)
        elif opcao == 8:
            relatorio_recursivo_interface(minha_barbearia)
        elif opcao == 9:
            exibir_perfil_polimorfico_interface(minha_barbearia)
        elif opcao == 0:
            exibir_cabecalho("Obrigado por usar o Cortejá!")
            print("🚀 Desenvolvido pela equipe de desenvolvedores juniores & Antigravity.")
            print("👋 Até a próxima!")
            break
        else:
            print("❌ Opção inválida! Escolha uma opção de 0 a 9.")
            
        input("\nPressione [Enter] para continuar...")


if __name__ == "__main__":
    main()
