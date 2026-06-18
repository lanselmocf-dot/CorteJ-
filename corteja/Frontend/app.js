/**
 * app.js - Sistema CorteJá Frontend
 * 
 * Implementação da lógica de negócios e interface com o usuário.
 * Demonstra conceitos de Orientação a Objetos em JavaScript,
 * máquina de estados para agendamentos e algoritmos recursivos.
 */

// ============================================================================
//  CLASSES DO DOMÍNIO (POO)
// ============================================================================

class CortejaError extends Error {
    constructor(mensagem) {
        super(mensagem);
        this.name = "CortejaError";
    }
}

class DadosInvalidosError extends CortejaError {
    constructor(mensagem) {
        super(mensagem);
        this.name = "DadosInvalidosError";
    }
}

class HorarioIndisponivelError extends CortejaError {
    constructor(mensagem) {
        super(mensagem);
        this.name = "HorarioIndisponivelError";
    }
}

class ServicoNaoEncontradoError extends CortejaError {
    constructor(mensagem) {
        super(mensagem);
        this.name = "ServicoNaoEncontradoError";
    }
}

class CancelamentoInvalidoError extends CortejaError {
    constructor(mensagem) {
        super(mensagem);
        this.name = "CancelamentoInvalidoError";
    }
}

// ----------------------------------------------------
// Classe Servico
// ----------------------------------------------------
class Servico {
    constructor(nome, preco, duracaoMinutos) {
        this._nome = nome;
        this.preco = preco; // Chama o setter
        this._duracaoMinutos = duracaoMinutos;
    }

    get nome() {
        return this._nome;
    }

    get preco() {
        return this._preco;
    }

    set preco(valor) {
        if (valor < 0) {
            throw new DadosInvalidosError("Preço do serviço não pode ser negativo.");
        }
        this._preco = valor;
    }

    get duracaoMinutos() {
        return this._duracaoMinutos;
    }

    // Dunder estático correspondente
    static formatarPreco(valor) {
        return `R$ ${valor.toFixed(2).replace('.', ',')}`;
    }

    toString() {
        return `${this._nome} - ${Servico.formatarPreco(this._preco)} (${this._duracaoMinutos}min)`;
    }

    repr() {
        return `Servico('${this._nome}', ${this._preco}, ${this._duracaoMinutos})`;
    }
}

// ----------------------------------------------------
// Classes de Usuários (Abstração, Herança e Polimorfismo)
// ----------------------------------------------------
class Usuario {
    constructor(id, nome, email, telefone) {
        if (this.constructor === Usuario) {
            throw new Error("Classe Abstrata 'Usuario' não pode ser instanciada diretamente.");
        }
        this.id = parseInt(id);
        this.nome = nome;       // Usa o setter
        this.email = email;     // Usa o setter
        this.telefone = telefone;
        
        // Atributo estático / contador simulado
        Usuario.totalCadastrados = (Usuario.totalCadastrados || 0) + 1;
    }

    get nome() {
        return this._nome;
    }

    set nome(valor) {
        if (!valor || valor.trim() === "") {
            throw new DadosInvalidosError("Nome do usuário não pode ser vazio.");
        }
        this._nome = valor.trim();
    }

    get email() {
        return this._email;
    }

    set email(valor) {
        if (!valor || !valor.includes("@")) {
            throw new DadosInvalidosError(`E-mail inválido: "${valor}". Deve conter "@".`);
        }
        this._email = valor.trim();
    }

    // Método Abstrato a ser implementado pelas filhas
    exibirPerfil() {
        throw new Error("Método abstrato 'exibirPerfil()' deve ser implementado.");
    }

    toString() {
        return `${this.nome} (${this.email})`;
    }

    repr() {
        return `${this.constructor.name}(id=${this.id}, nome='${this.nome}')`;
    }
}

class Cliente extends Usuario {
    constructor(id, nome, email, telefone) {
        super(id, nome, email, telefone);
        this._historico = [];
    }

    get historico() {
        return [...this._historico];
    }

    adicionarAoHistorico(agendamento) {
        this._historico.push(agendamento);
    }

    // POLIMORFISMO
    exibirPerfil() {
        return `===================================
      PERFIL DO CLIENTE
===================================
  Nome:      ${this.nome}
  Email:     ${this.email}
  Telefone:  ${this.telefone}
  Agendamentos: ${this._historico.length}
===================================`;
    }
}

class Barbeiro extends Usuario {
    constructor(id, nome, email, telefone) {
        super(id, nome, email, telefone);
        this._servicos = [];
        this._horariosTrabalho = [];
    }

    get servicos() {
        return [...this._servicos];
    }

    get horariosTrabalho() {
        return [...this._horariosTrabalho];
    }

    adicionarServico(servico) {
        this._servicos.push(servico);
    }

    definirHorarios(horarios) {
        this._horariosTrabalho = horarios;
    }

    // POLIMORFISMO
    exibirPerfil() {
        const servicosStr = this._servicos.map(s => `    • ${s.nome} (${Servico.formatarPreco(s.preco)})`).join('\n');
        const horariosStr = this._horariosTrabalho.join(', ');
        return `===================================
      PERFIL DO BARBEIRO
===================================
  Nome:      ${this.nome}
  Email:     ${this.email}
  Telefone:  ${this.telefone}

  Serviços oferecidos:
${servicosStr || '    Nenhum serviço'}

  Horários de trabalho:
    ${horariosStr || 'Nenhum horário'}
===================================`;
    }
}

// ----------------------------------------------------
// Classe Agendamento (Máquina de Estados e Composição)
// ----------------------------------------------------
class Agendamento {
    constructor(id, cliente, barbeiro, servico, data, hora) {
        this.id = parseInt(id);
        this.cliente = cliente;     // Composição: Agendamento tem Cliente
        this.barbeiro = barbeiro;   // Composição: Agendamento tem Barbeiro
        this.servico = servico;     // Composição: Agendamento tem Servico
        this.data = data;
        this.hora = hora;
        this._status = "agendado";  // Status inicial

        Agendamento.totalRealizados = (Agendamento.totalRealizados || 0) + 1;
    }

    get status() {
        return this._status;
    }

    set status(novoStatus) {
        const ESTADOS_VALIDOS = ["agendado", "confirmado", "concluido", "cancelado"];
        const TRANSICOES = {
            "agendado": ["confirmado", "cancelado"],
            "confirmado": ["concluido", "cancelado"],
            "concluido": [],
            "cancelado": []
        };

        if (!ESTADOS_VALIDOS.includes(novoStatus)) {
            throw new CancelamentoInvalidoError(
                `Status "${novoStatus}" é inválido. Use: ${ESTADOS_VALIDOS.join(', ')}`
            );
        }

        if (!TRANSICOES[this._status].includes(novoStatus)) {
            throw new CancelamentoInvalidoError(
                `Não é possível mudar o status de "${this._status.toUpperCase()}" para "${novoStatus.toUpperCase()}".`
            );
        }

        this._status = novoStatus;
    }

    confirmar() {
        this.status = "confirmado";
    }

    concluir() {
        this.status = "concluido";
    }

    cancelar() {
        this.status = "cancelado";
    }

    static validarHora(hora) {
        if (!hora || !hora.includes(":")) return false;
        const partes = hora.split(":");
        if (partes.length !== 2) return false;
        const h = parseInt(partes[0]);
        const m = parseInt(partes[1]);
        return h >= 0 && h <= 23 && m >= 0 && m <= 59;
    }

    // Dunder equivalente para comparação menor-que (__lt__) para ordenação cronológica
    compareTo(outro) {
        if (this.data === outro.data) {
            return this.hora.localeCompare(outro.hora);
        }
        // Converte DD/MM/AAAA ou YYYY-MM-DD para o formato comparável YYYY-MM-DD
        const parseDate = (dStr) => {
            if (dStr.includes("-")) return dStr; // Já está em aaaa-mm-dd
            const partes = dStr.split("/");
            return `${partes[2]}-${partes[1]}-${partes[0]}`; // dd/mm/aaaa -> aaaa-mm-dd
        };
        return parseDate(this.data).localeCompare(parseDate(outro.data));
    }

    toString() {
        return `[#${this.id}] ${appState.formatarDataBr(this.data)} às ${this.hora} - ${this.cliente.nome} com ${this.barbeiro.nome} (${this.servico.nome}) [${this.status.toUpperCase()}]`;
    }

    repr() {
        return `Agendamento(id=${this.id}, status='${this.status}')`;
    }
}

// ----------------------------------------------------
// Classe Barbearia (Orquestradora / Composição)
// ----------------------------------------------------
class Barbearia {
    constructor(nome) {
        this.nome = nome;
        this.barbeiros = [];
        this.clientes = [];
        this.agendamentos = [];
        this._proximoAgendamentoId = 1;
    }

    cadastrarBarbeiro(barbeiro) {
        this.barbeiros.push(barbeiro);
    }

    cadastrarCliente(cliente) {
        this.clientes.push(cliente);
    }

    buscarBarbeiro(id) {
        return this.barbeiros.find(b => b.id === parseInt(id)) || null;
    }

    buscarCliente(id) {
        return this.clientes.find(c => c.id === parseInt(id)) || null;
    }

    buscarAgendamento(id) {
        return this.agendamentos.find(a => a.id === parseInt(id)) || null;
    }

    agendar(cliente, barbeiro, servico, data, hora) {
        // Valida hora
        if (!Agendamento.validarHora(hora)) {
            throw new DadosInvalidosError(`Hora inválida: "${hora}". Use formato HH:MM.`);
        }

        // Valida se o barbeiro oferece o serviço
        if (!barbeiro.servicos.some(s => s.nome === servico.nome)) {
            throw new ServicoNaoEncontradoError(`O profissional ${barbeiro.nome} não realiza o serviço "${servico.nome}".`);
        }

        // Verifica conflitos
        const conflito = this.agendamentos.some(ag => 
            ag.barbeiro.id === barbeiro.id &&
            ag.data === data &&
            ag.hora === hora &&
            ag.status !== "cancelado"
        );

        if (conflito) {
            throw new HorarioIndisponivelError(`O horário ${hora} na data ${appState.formatarDataBr(data)} já está ocupado com ${barbeiro.nome}.`);
        }

        const novoAg = new Agendamento(this._proximoAgendamentoId, cliente, barbeiro, servico, data, hora);
        this.agendamentos.push(novoAg);
        cliente.adicionarAoHistorico(novoAg);
        this._proximoAgendamentoId++;
        return novoAg;
    }

    obterAgendamentosOrdenados() {
        return [...this.agendamentos].sort((a, b) => a.compareTo(b));
    }
}


// ============================================================================
//  ALGORITMOS RECURSIVOS (utils.py equivalentes em JS)
// ============================================================================

/**
 * Busca RECURSIVAMENTE o primeiro horário disponível de um barbeiro.
 */
function buscarHorarioDisponivelRecursivo(horarios, agendamentosDoDia, indice = 0) {
    // CASO BASE 1: Acabaram os horários
    if (indice >= horarios.length) {
        return null;
    }

    const horarioTestado = horarios[indice];

    // Verifica se esse horário está ocupado
    const ocupado = agendamentosDoDia.some(ag => ag.hora === horarioTestado && ag.status !== "cancelado");

    // CASO BASE 2: Encontrou um livre!
    if (!ocupado) {
        return horarioTestado;
    }

    // CHAMADA RECURSIVA: passa para o próximo índice
    return buscarHorarioDisponivelRecursivo(horarios, agendamentosDoDia, indice + 1);
}

/**
 * Calcula RECURSIVAMENTE o faturamento total acumulado dos agendamentos concluídos.
 */
function calcularFaturamentoRecursivo(agendamentos, indice = 0) {
    // CASO BASE: Fim da lista
    if (indice >= agendamentos.length) {
        return 0.0;
    }

    const ag = agendamentos[indice];
    const valor = ag.status === "concluido" ? ag.servico.preco : 0.0;

    // CHAMADA RECURSIVA: valor atual + faturamento do restante da lista
    return valor + calcularFaturamentoRecursivo(agendamentos, indice + 1);
}

/**
 * Conta RECURSIVAMENTE quantos agendamentos possuem determinado status.
 */
function contarAgendamentosPorStatusRecursivo(agendamentos, status, indice = 0) {
    // CASO BASE: Fim da lista
    if (indice >= agendamentos.length) {
        return 0;
    }

    const ag = agendamentos[indice];
    const conta = ag.status === status ? 1 : 0;

    // CHAMADA RECURSIVA: conta atual + soma dos restantes
    return conta + contarAgendamentosPorStatusRecursivo(agendamentos, status, indice + 1);
}


// ============================================================================
//  ESTADO DA APLICAÇÃO E INICIALIZAÇÃO DE DADOS
// ============================================================================

const appState = {
    barbearia: new Barbearia("Cortejá Recife"),
    activeBarberId: null,
    checkoutAppointmentId: null,
    selectedPaymentMethod: 'pix',

    // Helper: Formata data de YYYY-MM-DD para DD/MM/YYYY
    formatarDataBr(dataStr) {
        if (!dataStr) return "-";
        if (dataStr.includes("/")) return dataStr; // Já em BR
        const partes = dataStr.split("-");
        if (partes.length === 3) {
            return `${partes[2]}/${partes[1]}/${partes[0]}`;
        }
        return dataStr;
    },

    // Inicializa dados idênticos ao main.py do Python
    inicializarDados() {
        // 1. Serviços
        const corte = new Servico("Corte Degradê", 40.00, 30);
        const barba = new Servico("Barba Terapia", 30.00, 20);
        const combo = new Servico("Combo Corte & Barba", 60.00, 50);
        const sobrancelha = new Servico("Design de Sobrancelha", 15.00, 15);
        const selagem = new Servico("Selagem Capilar", 80.00, 60);

        // 2. Barbeiros
        const pedro = new Barbeiro(1, "Pedro Silva", "pedro@corteja.com.br", "(81) 99999-1111");
        pedro.adicionarServico(corte);
        pedro.adicionarServico(combo);
        pedro.adicionarServico(sobrancelha);
        pedro.definirHorarios(["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]);
        this.barbearia.cadastrarBarbeiro(pedro);

        const lucas = new Barbeiro(2, "Lucas Souza", "lucas@corteja.com.br", "(81) 99999-2222");
        lucas.adicionarServico(corte);
        lucas.adicionarServico(barba);
        lucas.adicionarServico(selagem);
        lucas.definirHorarios(["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"]);
        this.barbearia.cadastrarBarbeiro(lucas);

        // 3. Clientes
        const carlos = new Cliente(10, "Carlos Andrade", "carlos@gmail.com", "(81) 98888-3333");
        const bruno = new Cliente(11, "Bruno Costa", "bruno@hotmail.com", "(81) 98888-4444");
        this.barbearia.cadastrarCliente(carlos);
        this.barbearia.cadastrarCliente(bruno);

        // Define contadores iniciais de cadastro de usuários (são 2 barbeiros + 2 clientes = 4)
        Usuario.totalCadastrados = 4;

        // 4. Agendamentos
        // Ag1: Carlos com Pedro (Corte degradê), Data 26/05/2026 às 09:00
        this.barbearia.agendar(carlos, pedro, corte, "2026-05-26", "09:00");

        // Ag2: Bruno com Lucas (Barba), Concluído
        const ag2 = this.barbearia.agendar(bruno, lucas, barba, "2026-05-26", "10:00");
        ag2.confirmar();
        ag2.concluir();

        // Ag3: Carlos com Lucas (Selagem), Cancelado
        const ag3 = this.barbearia.agendar(carlos, lucas, selagem, "2026-05-27", "14:00");
        ag3.cancelar();
        
        // Atribui contadores iniciais para o painel de classe
        Agendamento.totalRealizados = 3;

        // Ativa o barbeiro padrão
        this.activeBarberId = pedro.id;
    }
};


// ============================================================================
//  GERENCIAMENTO E NAVEGAÇÃO DOS PAINÉIS (DOM)
// ============================================================================

const dom = {
    // Painéis
    panels: {
        home: document.getElementById('panel-home'),
        client: document.getElementById('panel-client'),
        barber: document.getElementById('panel-barber'),
        manager: document.getElementById('panel-manager')
    },
    
    // Botões de navegação
    navButtons: {
        toClient: document.getElementById('btn-role-client'),
        toBarber: document.getElementById('btn-role-barber'),
        toManager: document.getElementById('btn-role-manager'),
        toHome: document.querySelectorAll('.btn-to-home'),
        logo: document.getElementById('logo-home')
    },

    initNavigation() {
        // Eventos de clique para abrir painéis
        this.navButtons.toClient.addEventListener('click', () => this.switchPanel('client'));
        this.navButtons.toBarber.addEventListener('click', () => {
            this.switchPanel('barber');
            this.renderBarberSelection();
        });
        this.navButtons.toManager.addEventListener('click', () => {
            this.switchPanel('manager');
            this.updateManagerPanel();
        });

        // Botões de voltar
        this.navButtons.toHome.forEach(btn => {
            btn.addEventListener('click', () => this.switchPanel('home'));
        });
        this.navButtons.logo.addEventListener('click', () => this.switchPanel('home'));

        // Configuração de Abas internas (Cliente e Gestor)
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const parent = e.target.closest('.panel');
                const tabId = e.target.dataset.tab;
                
                // Remove classe active de todos os botões e abas no painel atual
                parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                parent.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Ativa a aba e o botão correspondente
                e.target.classList.add('active');
                const targetContent = document.getElementById(`tab-${tabId}`);
                if (targetContent) {
                    targetContent.classList.add('active');
                }

                // Ações específicas de recarga de aba
                if (tabId === 'manager-finance') {
                    this.updateFinanceTab();
                } else if (tabId === 'manager-agenda') {
                    this.renderManagerAgenda();
                }
            });
        });
    },

    switchPanel(panelName) {
        Object.keys(this.panels).forEach(key => {
            this.panels[key].classList.remove('active');
        });
        this.panels[panelName].classList.add('active');
        
        // Atualiza Badges e dados na navegação
        this.updateHeaderBadge();
    },

    updateHeaderBadge() {
        const ags = appState.barbearia.agendamentos;
        const totalFaturamento = calcularFaturamentoRecursivo(ags);
        const badge = document.getElementById('quick-stats-badge');
        
        badge.innerText = `💰 Faturamento: ${Servico.formatarPreco(totalFaturamento)}`;
        badge.style.display = totalFaturamento > 0 ? 'inline-flex' : 'none';
        
        badge.onclick = () => {
            this.switchPanel('manager');
            // Clica na aba de faturamento
            const finTabBtn = document.querySelector('.tab-btn[data-tab="manager-finance"]');
            if (finTabBtn) finTabBtn.click();
        };
    },


    // ========================================================================
    //  PAINEL DO CLIENTE (Agendamento, Perfil, Busca Recursiva)
    // ========================================================================

    initClientPanel() {
        const selectClient = document.getElementById('booking-client');
        const selectBarber = document.getElementById('booking-barber');
        const selectService = document.getElementById('booking-service');
        const selectProfileClient = document.getElementById('profile-select-client');
        const selectSearchBarber = document.getElementById('search-barber');
        
        // Popula os seletores de cliente e profissional
        this.populateClientSelectors(selectClient, selectProfileClient);
        this.populateBarberSelectors(selectBarber, selectSearchBarber);

        // Ao mudar o barbeiro no agendamento, carrega os respectivos serviços dele
        selectBarber.addEventListener('change', (e) => {
            const bId = e.target.value;
            selectService.innerHTML = '<option value="">Escolha o serviço...</option>';
            
            if (bId) {
                const barber = appState.barbearia.buscarBarbeiro(bId);
                barber.servicos.forEach(s => {
                    const opt = document.createElement('option');
                    opt.value = s.nome;
                    opt.innerText = s.toString();
                    selectService.appendChild(opt);
                });
                selectService.removeAttribute('disabled');
            } else {
                selectService.setAttribute('disabled', 'true');
            }
        });

        // Formulário de Cadastro de Cliente
        const handleRegister = (formId, nameId, emailId, phoneId) => {
            return (e) => {
                e.preventDefault();
                const name = document.getElementById(nameId).value;
                const email = document.getElementById(emailId).value;
                const phone = document.getElementById(phoneId).value;

                try {
                    // Validação local seguindo as regras da classe Usuario/Cliente
                    if (!email.includes("@")) {
                        throw new DadosInvalidosError(`Email inválido: "${email}". Deve conter "@".`);
                    }
                    if (!name.trim()) {
                        throw new DadosInvalidosError("Nome do cliente não pode ser vazio.");
                    }

                    // Encontra o próximo ID disponível
                    const idsExistentes = [
                        ...appState.barbearia.clientes.map(c => c.id),
                        ...appState.barbearia.barbeiros.map(b => b.id)
                    ];
                    const nextId = Math.max(...idsExistentes, 0) + 1;

                    const novoCli = new Cliente(nextId, name, email, phone);
                    appState.barbearia.cadastrarCliente(novoCli);

                    alert(`✅ Cliente registrado com sucesso!\nID Gerado: ${nextId}\n\nTotal de usuários: ${Usuario.totalCadastrados}`);
                    document.getElementById(formId).reset();
                    
                    // Atualiza dropdowns
                    this.populateClientSelectors(selectClient, selectProfileClient);
                } catch (err) {
                    alert(`❌ Falha no Cadastro: ${err.message}`);
                }
            };
        };

        // Bind nos formulários de cadastro
        document.getElementById('form-register-client').addEventListener('submit', handleRegister('form-register-client', 'reg-name', 'reg-email', 'reg-phone'));
        document.getElementById('form-manager-reg-client').addEventListener('submit', handleRegister('form-manager-reg-client', 'm-reg-name', 'm-reg-email', 'm-reg-phone'));

        // Formulário de Criação de Agendamento
        document.getElementById('form-booking').addEventListener('submit', (e) => {
            e.preventDefault();
            const cliId = selectClient.value;
            const barbId = selectBarber.value;
            const servNome = selectService.value;
            const date = document.getElementById('booking-date').value;
            const time = document.getElementById('booking-time').value;

            try {
                const cliente = appState.barbearia.buscarCliente(cliId);
                const barbeiro = appState.barbearia.buscarBarbeiro(barbId);
                const servico = barbeiro.servicos.find(s => s.nome === servNome);

                if (!cliente || !barbeiro || !servico) {
                    throw new DadosInvalidosError("Por favor, selecione opções válidas.");
                }

                // Tenta agendar (validará conflito e formato)
                const ag = appState.barbearia.agendar(cliente, barbeiro, servico, date, time);
                alert(`✅ Agendamento Realizado!\n\nDetalhes: ${ag.toString()}`);
                document.getElementById('form-booking').reset();
                selectService.innerHTML = '<option value="">Escolha um profissional primeiro...</option>';
                selectService.setAttribute('disabled', 'true');
                
                this.updateHeaderBadge();
            } catch (err) {
                alert(`❌ Falha ao Agendar: ${err.message}`);
            }
        });

        // Aba: Consultar Perfil / Histórico
        document.getElementById('btn-load-profile').addEventListener('click', () => {
            const cliId = selectProfileClient.value;
            if (!cliId) return;

            const cliente = appState.barbearia.buscarCliente(cliId);
            if (!cliente) return;

            // Roda o Polimorfismo chamando exibirPerfil()
            const consoleText = cliente.exibirPerfil();
            console.log(consoleText); // Exibe no devtools

            // Renderiza na tela
            document.getElementById('p-client-id').innerText = cliente.id;
            document.getElementById('p-client-name').innerText = cliente.nome;
            document.getElementById('p-client-email').innerText = cliente.email;
            document.getElementById('p-client-phone').innerText = cliente.telefone;
            document.getElementById('p-client-count').innerText = cliente.historico.length;

            const listArea = document.getElementById('client-history-list');
            listArea.innerHTML = "";

            if (cliente.historico.length === 0) {
                listArea.innerHTML = '<p style="color: var(--text-muted); font-size: 0.9rem;">Nenhum agendamento realizado.</p>';
            } else {
                // Ordena histórico
                const historicoOrdenado = [...cliente.historico].sort((a, b) => a.compareTo(b));
                historicoOrdenado.forEach(ag => {
                    const row = document.createElement('div');
                    row.className = 'list-item';
                    row.innerHTML = `
                        <div class="list-item-info">
                            <h4>${ag.servico.nome} com ${ag.barbeiro.nome}</h4>
                            <p>Reserva: ${this.formatarDataBr(ag.data)} às ${ag.hora}</p>
                        </div>
                        <div class="list-item-meta">
                            <span class="badge badge-${ag.status}">${ag.status}</span>
                            <span style="font-weight: 600;">${Servico.formatarPreco(ag.servico.preco)}</span>
                        </div>
                    `;
                    listArea.appendChild(row);
                });
            }

            document.getElementById('client-profile-result').style.display = 'block';
        });

        // Aba: Busca Inteligente (Recursão)
        document.getElementById('btn-search-recursive').addEventListener('click', () => {
            const bId = selectSearchBarber.value;
            const date = document.getElementById('search-date').value;

            if (!bId || !date) {
                alert("Selecione o profissional e a data para pesquisar.");
                return;
            }

            const barbeiro = appState.barbearia.buscarBarbeiro(bId);
            const agendamentosDia = appState.barbearia.agendamentos.filter(ag => 
                ag.barbeiro.id === barbeiro.id &&
                ag.data === date
            );

            // Chama algoritmo recursivo idêntico ao utils.py
            const horarioLivre = buscarHorarioDisponivelRecursivo(barbeiro.horariosTrabalho, agendamentosDia);

            const resultBox = document.getElementById('search-result-box');
            const resultText = document.getElementById('search-result-text');

            if (horarioLivre) {
                resultText.innerHTML = `Excelente! O primeiro horário livre recursivamente encontrado para <strong>${barbeiro.nome}</strong> no dia <strong>${this.formatarDataBr(date)}</strong> é: <strong style="color: var(--accent); font-size: 1.1rem;">${horarioLivre}</strong>`;
            } else {
                resultText.innerHTML = `Infelizmente todos os horários padrão de trabalho para <strong>${barbeiro.nome}</strong> no dia <strong>${this.formatarDataBr(date)}</strong> estão ocupados.`;
            }

            resultBox.style.display = 'block';
        });
    },

    populateClientSelectors(...selectors) {
        selectors.forEach(sel => {
            sel.innerHTML = '<option value="">Selecione o Cliente...</option>';
            appState.barbearia.clientes.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c.id;
                opt.innerText = `[ID ${c.id}] ${c.nome}`;
                sel.appendChild(opt);
            });
        });
    },

    populateBarberSelectors(...selectors) {
        selectors.forEach(sel => {
            sel.innerHTML = '<option value="">Selecione o Barbeiro...</option>';
            appState.barbearia.barbeiros.forEach(b => {
                const opt = document.createElement('option');
                opt.value = b.id;
                opt.innerText = b.nome;
                sel.appendChild(opt);
            });
        });
    },


    // ========================================================================
    //  PAINEL DO BARBEIRO (Agenda, Perfil e status)
    // ========================================================================

    renderBarberSelection() {
        const container = document.getElementById('barber-chips-container');
        container.innerHTML = "";

        appState.barbearia.barbeiros.forEach(b => {
            const chip = document.createElement('div');
            chip.className = `barber-chip ${appState.activeBarberId === b.id ? 'active' : ''}`;
            chip.innerHTML = `💈 ${b.nome}`;
            chip.addEventListener('click', () => {
                appState.activeBarberId = b.id;
                this.renderBarberSelection();
                this.loadBarberAgenda();
            });
            container.appendChild(chip);
        });

        // Set default filter date to today or specific demo date (2026-05-26)
        const dateInput = document.getElementById('barber-filter-date');
        if (!dateInput.value) {
            dateInput.value = "2026-05-26";
        }
        
        dateInput.onchange = () => this.loadBarberAgenda();

        this.loadBarberAgenda();
    },

    loadBarberAgenda() {
        const bId = appState.activeBarberId;
        if (!bId) return;

        const barbeiro = appState.barbearia.buscarBarbeiro(bId);
        if (!barbeiro) return;

        // Render Profile
        const profBox = document.getElementById('barber-profile-box');
        profBox.innerHTML = `
            <div class="profile-field">
                <span>Nome:</span>
                <span>${barbeiro.nome}</span>
            </div>
            <div class="profile-field">
                <span>E-mail:</span>
                <span>${barbeiro.email}</span>
            </div>
            <div class="profile-field">
                <span>Telefone:</span>
                <span>${barbeiro.telefone}</span>
            </div>
            <div class="profile-field">
                <span>Horários de Trabalho:</span>
                <span style="font-size: 0.8rem;">${barbeiro.horariosTrabalho.join(', ')}</span>
            </div>
        `;

        // Services
        const servList = document.getElementById('barber-services-list');
        servList.innerHTML = "";
        barbeiro.servicos.forEach(s => {
            const row = document.createElement('div');
            row.className = 'list-item';
            row.style.padding = '0.5rem 1rem';
            row.innerHTML = `
                <span>${s.nome}</span>
                <span style="color: var(--accent); font-weight: 600;">${Servico.formatarPreco(s.preco)}</span>
            `;
            servList.appendChild(row);
        });

        // Agenda List
        const agendaList = document.getElementById('barber-agenda-list');
        agendaList.innerHTML = "";

        const filterDate = document.getElementById('barber-filter-date').value;
        
        // Obter agendamentos filtrados
        let ags = appState.barbearia.agendamentos.filter(ag => ag.barbeiro.id === barbeiro.id);
        if (filterDate) {
            ags = ags.filter(ag => ag.data === filterDate);
        }

        // Ordenação usando compateTo (LT)
        ags.sort((a, b) => a.compareTo(b));

        if (ags.length === 0) {
            agendaList.innerHTML = `<p style="color: var(--text-muted); font-size: 0.9rem; text-align: center; padding: 2rem 0;">Nenhum agendamento encontrado para o dia ${this.formatarDataBr(filterDate)}.</p>`;
        } else {
            ags.forEach(ag => {
                const item = document.createElement('div');
                item.className = 'list-item';
                
                let actionBtns = '';
                if (ag.status === 'agendado') {
                    actionBtns = `
                        <button class="btn btn-primary btn-sm" onclick="dom.alterarStatus(${ag.id}, 'confirmar')">Confirmar</button>
                        <button class="btn btn-danger btn-sm" onclick="dom.alterarStatus(${ag.id}, 'cancelar')">Cancelar</button>
                    `;
                } else if (ag.status === 'confirmado') {
                    actionBtns = `
                        <button class="btn btn-danger btn-sm" onclick="dom.alterarStatus(${ag.id}, 'cancelar')">Cancelar</button>
                    `;
                }

                item.innerHTML = `
                    <div class="list-item-info">
                        <h4>${ag.cliente.nome}</h4>
                        <p>Horário: <strong style="color: var(--accent);">${ag.hora}</strong> | Serviço: ${ag.servico.nome}</p>
                        <p style="font-size:0.75rem;">Status: <span class="badge badge-${ag.status}" style="font-size:0.65rem; padding: 0.15rem 0.4rem;">${ag.status}</span></p>
                    </div>
                    <div class="list-item-meta">
                        <div style="display:flex; gap:0.5rem;">
                            ${actionBtns}
                        </div>
                    </div>
                `;
                agendaList.appendChild(item);
            });
        }

        document.getElementById('barber-panel-content').style.display = 'block';
    },

    alterarStatus(id, acao) {
        try {
            const ag = appState.barbearia.buscarAgendamento(id);
            if (!ag) return;

            if (acao === 'confirmar') {
                ag.confirmar();
                alert(`✅ Reserva #${id} confirmada com sucesso!`);
            } else if (acao === 'cancelar') {
                if (confirm(`Deseja realmente cancelar o agendamento #${id}?`)) {
                    ag.cancelar();
                    alert(`❌ Reserva #${id} cancelada.`);
                }
            }

            this.loadBarberAgenda();
            this.updateHeaderBadge();
        } catch (err) {
            alert(`❌ Erro de transição: ${err.message}`);
        }
    },


    // ========================================================================
    //  PAINEL DO GESTOR (Faturamento, checkout e caixa)
    // ========================================================================

    updateManagerPanel() {
        // Popula filtros
        const filterBarb = document.getElementById('m-filter-barber');
        filterBarb.innerHTML = '<option value="">Todos os Barbeiros</option>';
        appState.barbearia.barbeiros.forEach(b => {
            const opt = document.createElement('option');
            opt.value = b.id;
            opt.innerText = b.nome;
            filterBarb.appendChild(opt);
        });

        // Bind nos filtros
        filterBarb.onchange = () => this.renderManagerAgenda();
        document.getElementById('m-filter-date').onchange = () => this.renderManagerAgenda();
        document.getElementById('m-filter-status').onchange = () => this.renderManagerAgenda();
        
        document.getElementById('btn-clear-filters').onclick = () => {
            filterBarb.value = "";
            document.getElementById('m-filter-date').value = "";
            document.getElementById('m-filter-status').value = "";
            this.renderManagerAgenda();
        };

        this.renderManagerAgenda();
        this.updateFinanceTab();
    },

    renderManagerAgenda() {
        const bId = document.getElementById('m-filter-barber').value;
        const date = document.getElementById('m-filter-date').value;
        const status = document.getElementById('m-filter-status').value;

        const listArea = document.getElementById('manager-agenda-list');
        listArea.innerHTML = "";

        let ags = appState.barbearia.obterAgendamentosOrdenados();

        if (bId) {
            ags = ags.filter(a => a.barbeiro.id === parseInt(bId));
        }
        if (date) {
            ags = ags.filter(a => a.data === date);
        }
        if (status) {
            ags = ags.filter(a => a.status === status);
        }

        if (ags.length === 0) {
            listArea.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: 2.5rem 0;">Nenhum registro encontrado.</p>';
            return;
        }

        ags.forEach(ag => {
            const item = document.createElement('div');
            item.className = 'list-item';
            
            let actions = '';
            if (ag.status === 'agendado') {
                actions = `
                    <button class="btn btn-secondary btn-sm" onclick="dom.managerConfirmar(${ag.id})">Confirmar</button>
                    <button class="btn btn-danger btn-sm" onclick="dom.managerCancelar(${ag.id})">Cancelar</button>
                `;
            } else if (ag.status === 'confirmado') {
                actions = `
                    <button class="btn btn-primary btn-sm" onclick="dom.abrirCheckout(${ag.id})">💵 Concluir / Checkout</button>
                    <button class="btn btn-danger btn-sm" onclick="dom.managerCancelar(${ag.id})">Cancelar</button>
                `;
            }

            item.innerHTML = `
                <div class="list-item-info">
                    <h4>#${ag.id} - ${ag.cliente.nome}</h4>
                    <p>Profissional: <strong>${ag.barbeiro.nome}</strong> | Serviço: ${ag.servico.nome}</p>
                    <p>Data: ${this.formatarDataBr(ag.data)} às <strong>${ag.hora}</strong></p>
                </div>
                <div class="list-item-meta">
                    <span class="badge badge-${ag.status}" style="margin-bottom: 0.5rem;">${ag.status}</span>
                    <span style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem; display:block;">${Servico.formatarPreco(ag.servico.preco)}</span>
                    <div style="display:flex; gap:0.5rem;">
                        ${actions}
                    </div>
                </div>
            `;
            listArea.appendChild(item);
        });
    },

    managerConfirmar(id) {
        try {
            const ag = appState.barbearia.buscarAgendamento(id);
            ag.confirmar();
            this.renderManagerAgenda();
            this.updateHeaderBadge();
        } catch (e) {
            alert(e.message);
        }
    },

    managerCancelar(id) {
        if (confirm(`Deseja cancelar o agendamento #${id}?`)) {
            try {
                const ag = appState.barbearia.buscarAgendamento(id);
                ag.cancelar();
                this.renderManagerAgenda();
                this.updateHeaderBadge();
            } catch (e) {
                alert(e.message);
            }
        }
    },

    // Aba: Relatório Estatístico via Recursão
    updateFinanceTab() {
        const ags = appState.barbearia.agendamentos;
        
        // Chamadas recursivas para calcular os valores da UI
        const faturamento = calcularFaturamentoRecursivo(ags);
        const agendados = contarAgendamentosPorStatusRecursivo(ags, "agendado");
        const confirmados = contarAgendamentosPorStatusRecursivo(ags, "confirmado");
        const concluidos = contarAgendamentosPorStatusRecursivo(ags, "concluido");
        const cancelados = contarAgendamentosPorStatusRecursivo(ags, "cancelado");

        // Atualiza dom
        document.getElementById('stat-faturamento').innerText = Servico.formatarPreco(faturamento);
        document.getElementById('stat-agendados').innerText = agendados;
        document.getElementById('stat-confirmados').innerText = confirmados;
        document.getElementById('stat-concluidos').innerText = concluidos;
        document.getElementById('stat-cancelados').innerText = cancelados;
        
        this.updateHeaderBadge();
    },


    // ========================================================================
    //  FLUXO DE CAIXA: CHECKOUT & CUPOM FISCAL
    // ========================================================================

    abrirCheckout(id) {
        const ag = appState.barbearia.buscarAgendamento(id);
        if (!ag) return;

        appState.checkoutAppointmentId = id;
        appState.selectedPaymentMethod = 'pix';

        // Detalhes do Checkout
        const det = document.getElementById('checkout-details');
        det.innerHTML = `
            <div class="profile-box" style="background: rgba(255, 255, 255, 0.02); margin-bottom: 0;">
                <div class="profile-field">
                    <span>Agendamento Ref:</span>
                    <strong>#${ag.id}</strong>
                </div>
                <div class="profile-field">
                    <span>Cliente:</span>
                    <span>${ag.cliente.nome}</span>
                </div>
                <div class="profile-field">
                    <span>Profissional:</span>
                    <span>${ag.barbeiro.nome}</span>
                </div>
                <div class="profile-field">
                    <span>Serviço realizado:</span>
                    <span>${ag.servico.nome}</span>
                </div>
                <div class="profile-field" style="border:none; padding-bottom:0; margin-bottom:0;">
                    <span>Subtotal:</span>
                    <strong style="color: var(--accent); font-size:1.15rem;">${Servico.formatarPreco(ag.servico.preco)}</strong>
                </div>
            </div>
        `;

        // Ativa Pix como inicial
        document.querySelectorAll('.payment-method').forEach(m => m.classList.remove('active'));
        document.querySelector('.payment-method[data-method="pix"]').classList.add('active');
        this.switchPaymentMode('pix', ag.servico.preco);

        // Abre modal overlay
        document.getElementById('modal-checkout').classList.add('active');
    },

    initCheckoutModal() {
        const overlay = document.getElementById('modal-checkout');
        
        // Fechar botões
        document.getElementById('btn-close-checkout').onclick = () => overlay.classList.remove('active');
        document.getElementById('btn-cancel-checkout').onclick = () => overlay.classList.remove('active');

        // Escolha de métodos de pagamento
        document.querySelectorAll('.payment-method').forEach(methodBtn => {
            methodBtn.onclick = (e) => {
                document.querySelectorAll('.payment-method').forEach(m => m.classList.remove('active'));
                const btn = e.target.closest('.payment-method');
                btn.classList.add('active');
                
                const method = btn.dataset.method;
                appState.selectedPaymentMethod = method;

                const ag = appState.barbearia.buscarAgendamento(appState.checkoutAppointmentId);
                this.switchPaymentMode(method, ag.servico.preco);
            };
        });

        // Ação de confirmar Checkout
        document.getElementById('btn-confirm-checkout').onclick = () => {
            const ag = appState.barbearia.buscarAgendamento(appState.checkoutAppointmentId);
            if (!ag) return;

            // Validação de pagamento por dinheiro
            let troco = 0.0;
            let desconto = 0.0;
            let totalPago = ag.servico.preco;

            if (appState.selectedPaymentMethod === 'dinheiro') {
                const received = parseFloat(document.getElementById('cash-received').value);
                if (isNaN(received) || received < ag.servico.preco) {
                    alert("❌ Erro: Valor em dinheiro insuficiente ou inválido.");
                    return;
                }
                troco = received - ag.servico.preco;
            } else if (appState.selectedPaymentMethod === 'pix') {
                desconto = ag.servico.preco * 0.05;
                totalPago = ag.servico.preco - desconto;
            }

            // Transição na máquina de estados (agendamento passa de confirmado -> concluído)
            try {
                ag.concluir();
                
                // Fecha checkout e abre Cupom
                overlay.classList.remove('active');
                this.abrirCupom(ag, desconto, totalPago, troco);
            } catch (err) {
                alert(`❌ Erro no fechamento: ${err.message}`);
            }
        };
    },

    switchPaymentMode(method, preco) {
        // Esconde todos
        document.querySelectorAll('.checkout-pay-mode').forEach(d => d.style.display = 'none');

        if (method === 'pix') {
            const desconto = preco * 0.05;
            const total = preco - desconto;
            document.getElementById('pix-simulated-value').innerText = `Total com desconto: ${Servico.formatarPreco(total)}`;
            document.getElementById('pay-mode-pix').style.display = 'block';
        } else if (method === 'credito' || method === 'debito') {
            document.getElementById('pay-mode-card').style.display = 'block';
            const statusText = document.getElementById('card-status-text');
            statusText.innerText = "Conectando à maquininha...";
            
            // Simula delay de cartão
            setTimeout(() => {
                statusText.innerHTML = "🔓 Senha verificada...<br><span style='color: var(--success); font-weight:600;'>✅ Transação APROVADA!</span>";
            }, 1800);
        } else if (method === 'dinheiro') {
            const cashInput = document.getElementById('cash-received');
            const changeBox = document.getElementById('cash-change-box');
            const changeVal = document.getElementById('cash-change-value');
            
            cashInput.value = "";
            changeBox.style.display = 'none';

            cashInput.oninput = () => {
                const val = parseFloat(cashInput.value);
                if (!isNaN(val) && val >= preco) {
                    const diff = val - preco;
                    changeVal.innerText = Servico.formatarPreco(diff);
                    changeBox.style.display = 'block';
                } else {
                    changeBox.style.display = 'none';
                }
            };
            document.getElementById('pay-mode-cash').style.display = 'block';
        }
    },

    abrirCupom(ag, desconto, totalPago, troco) {
        const printArea = document.getElementById('cupom-print-area');
        const dStr = new Date().toLocaleDateString('pt-BR');
        
        let metodosDesc = {
            'pix': 'Pix (Aplicativo)',
            'credito': 'Cartão de Crédito',
            'debito': 'Cartão de Débito',
            'dinheiro': 'Dinheiro Físico'
        };

        // Formata data do agendamento
        const dataAgBr = this.formatarDataBr(ag.data);

        printArea.innerHTML = `
            <div class="cupom-header">
                <div class="cupom-logo">✂️ CUPOM FISCAL DE SERVIÇO ✂️</div>
                <div>BARBEARIA CORTEJÁ - RECIFE</div>
                <div style="font-size:0.7rem; color:#666; margin-top:0.25rem;">Impressão: ${dStr} às ${new Date().toLocaleTimeString('pt-BR')}</div>
            </div>
            
            <div class="cupom-row">
                <span>Data do Atendimento:</span>
                <span>${dataAgBr} às ${ag.hora}</span>
            </div>
            <div class="cupom-row">
                <span>Ref Agendamento:</span>
                <span>#${ag.id}</span>
            </div>
            <div class="cupom-row">
                <span>Cliente:</span>
                <span>${ag.cliente.nome} (ID: ${ag.cliente.id})</span>
            </div>
            <div class="cupom-row">
                <span>Profissional:</span>
                <span>${ag.barbeiro.nome}</span>
            </div>
            <div class="cupom-row">
                <span>Serviço realizado:</span>
                <span>${ag.servico.nome}</span>
            </div>
            
            <div class="cupom-divider"></div>
            
            <div class="cupom-row">
                <span>Subtotal:</span>
                <span>${Servico.formatarPreco(ag.servico.preco)}</span>
            </div>
            ${desconto > 0 ? `
            <div class="cupom-row" style="color: #c0392b;">
                <span>Desconto Aplicado (5%):</span>
                <span>-${Servico.formatarPreco(desconto)}</span>
            </div>
            ` : ''}
            <div class="cupom-row cupom-total">
                <span>TOTAL PAGO:</span>
                <span>${Servico.formatarPreco(totalPago)}</span>
            </div>
            <div class="cupom-row">
                <span>Forma de Pagamento:</span>
                <span>${metodosDesc[appState.selectedPaymentMethod]}</span>
            </div>
            ${troco > 0 ? `
            <div class="cupom-row">
                <span>Troco Devolvido:</span>
                <span>${Servico.formatarPreco(troco)}</span>
            </div>
            ` : ''}
            
            <div class="cupom-divider"></div>

            <div style="font-size: 0.7rem; color: #555; text-align: center; margin-bottom: 0.5rem;">
                <strong>Representação Técnica Dunder (POO):</strong>
            </div>
            <div style="background: #f0f0f0; border-radius:3px; padding: 0.4rem; font-size:0.68rem; word-break: break-all; margin-bottom:0.5rem; text-align:left;">
                __str__:<br>${ag.toString()}<br><br>
                __repr__:<br>${ag.repr()}
            </div>
            
            <div class="cupom-footer">
                <div>OBRIGADO PELA PREFERÊNCIA!</div>
                <div style="font-weight:bold; margin-top:0.25rem;">Sua Barba, Sua Assinatura.</div>
            </div>
        `;

        document.getElementById('modal-cupom').classList.add('active');
    },

    initCupomModal() {
        const overlay = document.getElementById('modal-cupom');
        
        const closeFlow = () => {
            overlay.classList.remove('active');
            // Retorna ao painel do gestor e recarrega
            this.switchPanel('manager');
            this.updateManagerPanel();
        };

        document.getElementById('btn-close-cupom').onclick = closeFlow;
        document.getElementById('btn-finish-flow').onclick = closeFlow;

        document.getElementById('btn-print-receipt').onclick = () => {
            // Simula comando físico
            alert("🖨️ Comando enviado para a impressora térmica simulada! Impressão concluída.");
        };
    }
};

// ============================================================================
//  PONTO DE ENTRADA / INICIALIZAÇÃO GERAL
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Inicializa os dados em memória idênticos ao do console Python
    appState.inicializarDados();

    // Configura navegação do DOM e de abas
    dom.initNavigation();

    // Configura fluxos do painel do cliente
    dom.initClientPanel();

    // Configura modais
    dom.initCheckoutModal();
    dom.initCupomModal();

    // Atualiza estado do faturamento rápido no header
    dom.updateHeaderBadge();
});
