# Planejamento das Atividades Restantes: Rumo à Entrega Final

## 1. Visão Geral do Planejamento
O objetivo destas próximas fases é transformar o "Core" (motor de regras) atual do **Cortejá** em um protótipo visualmente atrativo e funcional. Como trata-se de um projeto acadêmico com foco no mercado, o escopo foi ajustado para entregar o máximo de valor visual e técnico, mas sem adicionar complexidades desnecessárias que atrapalhariam o prazo de entrega.

## 2. Cronograma de Atividades

### Fase 1: Persistência de Dados Leve e Eficiente
*Substituir o armazenamento temporário (RAM) por um banco de dados real, porém simplificado.*
- **Ação:** Implementação do **SQLite**.
- **Justificativa:** O SQLite é perfeito para este estágio. Ele funciona como um banco de dados real (usando linguagem SQL), é excelente para pequenas barbearias e elimina a necessidade de instalar servidores pesados no dia da apresentação na universidade.
- **Entregável:** O sistema não perderá mais os dados quando o terminal for fechado.

### Fase 2: Interface Visual (Frontend)
*Sair da tela preta do terminal e dar uma "cara" comercial ao sistema.*
- **Ação:** Criar uma interface gráfica simples, limpa e funcional.
- **Abordagem:** Utilizar um micro-framework web em Python (como **Flask** ou **FastAPI**) junto com páginas em HTML/CSS/JavaScript.
- **Telas Prioritárias:**
  1. **Tela de Agendamento do Cliente:** Onde ele escolhe o barbeiro e o horário.
  2. **Painel do Barbeiro:** Para ele ver sua agenda do dia.
  3. **Tela de Fechamento (Caixa):** Para concluir o atendimento.

### Fase 3: Aprimoramento da Simulação de Pagamentos
*Demonstrar a regra de negócio do caixa sem a burocracia de APIs financeiras reais.*
- **Ação:** Melhorar a experiência da etapa de pagamento na interface visual.
- **Justificativa:** Integrar APIs reais (como Stripe/MercadoPago) exige contas bancárias e aprovações demoradas. Para a banca avaliadora, a simulação bem feita tem o mesmo peso didático.
- **Entregável:** Na tela de checkout, o sistema vai gerar um QR Code fictício de Pix na tela e, ao finalizar, exibirá um "Cupom Fiscal Eletrônico" visualmente idêntico a um recibo de maquininha.

### Fase 4: Bateria de Testes e Roteiro de Apresentação
*Preparar a demonstração para impressionar a banca e evitar falhas ao vivo.*
- **Ação:** Criação de casos de teste específicos para a apresentação.
- **O que será testado:**
  - Tentar marcar dois clientes no mesmo horário (para mostrar a proteção do sistema).
  - Tentar cancelar um atendimento já pago (para mostrar a robustez da máquina de estados).
- **Entregável:** Um roteiro de apresentação passo a passo garantindo que todas as validações do código sejam demonstradas com sucesso aos professores.

## 3. Conclusão
Com este planejamento, a equipe foca seus esforços no que realmente importa: criar uma **experiência visual** para o usuário final, utilizando um **banco de dados real** de fácil configuração, e garantindo que no dia da apresentação o sistema rode de forma fluida, segura e impressionante.
