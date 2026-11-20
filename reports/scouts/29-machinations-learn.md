# Scout 29 — Machinations learning resources

- **Fonte / source_id:** `machinations-learn`
- **Rota de entrada:** https://machinations.io/learn
- **Organização observada:** Machinations; o rodapé das páginas consultadas identifica `© 2026 Machinations S.àr.l`.
- **Acesso observado:** páginas públicas HTTPS acessíveis sem login, matrícula, compra ou execução externa. A consulta foi somente de leitura.
- **Coverage:** `partial`
- **Data da consulta:** 2026-11-20

## Síntese

A rota pública se apresenta como um percurso de aprendizagem de modelagem de sistemas: “From your first loop to balanced economies”. A página declara lições guiadas que começam em uma tela vazia, passam pelos fundamentos e usam diagramas reais. Ela anuncia **Machinations essentials**, com **19 lições em ordem**, e **Tutorials**, descritos como **4 séries** que constroem um modelo e **10 lições individuais**. Esses números e a lista abaixo são afirmações editoriais da própria página; não são uma prova de que todas as páginas, exercícios, diagramas incorporados ou funcionalidades funcionam em runtime. [1]

O escopo público observável cobre recursos, regras, feedback, construção de diagramas, Play passo a passo, simulação, previsões/KPIs e exemplos de economias de jogos, além de exemplos de tokenomics/Web3. A trilha introdutória diz que o aluno constrói um diagrama de loot e crafting e que as ideias de modelagem também se aplicam a sistemas de recursos, regras e feedback fora de jogos. [2]

A documentação oficial diretamente ligada amplia o escopo para a linguagem visual, nós, conexões, variáveis/parâmetros, aleatoriedade, expressões Math.js, JSON externo, feeds de mercado, Google Sheets, modos de Play, gráficos, precisão, Monte Carlo, debugger, colaboração, diagramas públicos, MCP, API Services, sincronização em tempo real e integração com Unity. A página de documentação é um índice de tópicos públicos, não uma demonstração de execução completa de cada tópico. [3]

## Inventário público observado na rota `/learn`

### Machinations essentials — 19 lições declaradas

A página de entrada lista as seguintes partes e caminhos relativos:

1. `Pathway introduction` — `/learn/pathway-introduction`
2. `Overview` — `/learn/machinations-fundamentals`
3. `What is Machinations?` — `/learn/what-is-machinations`
4. `Interface basics` — `/learn/interface-basics`
5. `Simulation models in Machinations` — `/learn/simulation-models-in-machinations`
6. `Steps` — `/learn/steps`
7. `Resources` — `/learn/resources`
8. `Preliminary analysis` — `/learn/preliminary-analysis`
9. `Running simulations` — `/learn/running-simulations`
10. `Project: Loot and Craft` — `/learn/project-loot-and-craft`
11. `Project overview` — `/learn/project-overview`
12. `Creating a new diagram` — `/learn/creating-a-new-diagram`
13. `Pools: Storing resources` — `/learn/pools-storing-resources`
14. `Sources: Generating resources` — `/learn/sources-generating-resources`
15. `Resource connections: Transferring resources` — `/learn/resource-connections-transferring-resources`
16. `Converters: Creating houses` — `/learn/converters-creating-houses`
17. `Changing styles` — `/learn/changing-styles`
18. `Forecasts: Estimating KPIs` — `/learn/predictions-estimating-kpis`
19. `Machinations essentials quiz` — `/learn/machinations-essentials-quiz`

A página individual da introdução confirma que o percurso começa com um diagrama de loot e crafting, ensina componentes centrais, conexão de recursos, Play passo a passo e exploração de como diferentes pressupostos alteram o resultado. [2]

### Séries de tutoriais listadas

A página `/learn` lista quatro séries de construção de modelos:

- **Loot & Craft** — 8 páginas: introdução; crafting & converters; gates & randomness; delays, queues & intervals; state connections; registers; sinks & end conditions; chart & simulations. Entrada: `/learn/loot-craft`.
- **Level progression** — 10 páginas: introdução; leveling up; atualização do custo de level-up; fórmulas de custo; XP por nível; forecasts com simulações; skill points; alocação de atributos; cálculo de stats; perda de saúde em batalhas. Entrada: `/learn/level-progression`.
- **Loot boxes & card packs** — 10 páginas: introdução; fundamentos; charts e forecasts; itens duplicados; reembolso por duplicatas; comportamento simples; comportamento avançado; diagramas legíveis; parâmetros; integração com planilhas. Entrada: `/learn/loot-boxes-card-packs`.
- **Web3: Constant product market maker** — 5 páginas: introdução; pool de liquidez de produto constante; função de swap; conexão entre gatilho e funções de swap; compra de A e venda de B. Entrada: `/learn/web3-constant-product-market-maker`.

Essas contagens são a enumeração visível no inventário editorial da página de entrada. Não foram tratados como comprovação de completude de cada série nem como prova de que todos os diagramas embutidos podem ser executados. [1]

### Lições individuais listadas

A mesma página lista 10 lições “One question, one diagram” ou equivalentes: `Answering questions with Machinations`, `Level progress planning`, `Modeling a gacha box`, `Player skill`, `Balancing a battle pass`, `Video tutorials`, `Increase base stats`, `Artificial players with agents`, `Infinite runner game loop` e `Balancing difficulty and score`. Os caminhos observados incluem `/learn/answering-questions-with-machinations`, `/learn/level-progress-planning`, `/learn/modelling-a-gacha-box`, `/learn/player-skill`, `/learn/simulating-for-game-balance`, `/learn/video-tutorials`, `/learn/increase-base-stats`, `/learn/artificial-player`, `/learn/infinite-runner-game-loop` e `/learn/balancing-difficulty-score`. [1]

## Evidência detalhada de modelagem e sistemas

O tutorial público `Loot & Craft` descreve um modelo de economia básica para um jogo de gestão de recursos/crafting. Ele diz que o tutorial é dividido em etapas que introduzem componentes e aumentam a complexidade, recomenda seguir a ordem e afirma que os fundamentos são aplicáveis a mecânicas de crafting em geral. [4]

Nesse tutorial, a descrição editorial explica `Source` como gerador de recursos, `Pool` como armazenador e `Resource Connection` como ligação que informa origem, destino e quantidade transferida. Também explica que o modelo é executado em `Steps`, que podem representar unidade de tempo ou ação de jogo, e que o usuário pode alterar a duração e a velocidade do Play. Isso documenta conceitos e instruções textuais; não constitui execução independente deste scout. [4]

A documentação de Monte Carlo explica a diferença entre probabilidade teórica e experimental, amostragem aleatória repetida, Lei dos Grandes Números, efeito do número de amostras e um exemplo de estimativa de Pi. A página mostra números editoriais de exemplo para Plays de 1000 e 3000 lançamentos, mas não foram reproduzidos aqui e, portanto, não são classificados como resultado verificado de execução. [5]

O glossário público se apresenta como uma linguagem compartilhada para ideias de economia e sistemas em finanças, energia, saúde, operações, tokenomics e jogos. A página declara **258 termos definidos** e **258 diagramas de exemplo**. Entre os termos observados estão `Abstracting`, `Agent-based modeling (ABM)`, `Balancing feedback loop`, `Causal loop diagram (CLD)`, `Continuous simulation`, `Monte Carlo`/conceitos de simulação, `Bottleneck`, `Churn rate`, `Bonding curve` e `Digital twin`. O inventário é o que a página pública exibiu no momento da consulta; não foi feita uma auditoria independente de todos os 258 verbetes ou diagramas. [6]

## Documentação e recursos técnicos públicos relacionados

A página `/docs` organiza os materiais nas categorias `Getting started`, `Nodes`, `Nodes properties`, `Connections`, `Custom variables`, `Play & forecast`, `Collaboration`, `Machinations MCP and integrations`, `Tips`, `Account & billing` e `Resources`. Entre os caminhos diretamente observados estão:

- Fundamentos: `/docs/what-is-machinations-systems-simulation-tool`, `/docs/interface-basics`, `/docs/how-to-read-a-machinations-diagram`, `/docs/framework-basics`, `/docs/faq`.
- Componentes: `/docs/sources`, `/docs/pools`, `/docs/drains`, `/docs/converters-traders`, `/docs/gates`, `/docs/registers`, `/docs/delays-queues-2`, `/docs/end-conditions`.
- Ligações e propriedades: `/docs/resource-connections`, `/docs/state-connections`, `/docs/activators`, `/docs/triggers`, `/docs/node-modifiers`, `/docs/label-modifiers`.
- Variáveis e matemática: `/docs/what-are-custom-variables`, `/docs/randomness`, `/docs/math-expression`, `/docs/advanced-math-js-structures`, `/docs/math-js-functions`, `/docs/external-json`, `/docs/live-market-feeds`, `/docs/google-sheets-public-private`.
- Execução e análise: `/docs/play-modes`, `/docs/charts`, `/docs/accuracy-indicator`, `/docs/the-monte-carlo-simulations`, `/docs/debugger`.
- Integrações: `/docs/mcp`, `/docs/quick-start`, `/docs/key-features`, `/docs/local-cache`, `/docs/data-formats-handoff`, `/docs/api-services`, `/docs/real-time-sync`, `/docs/game-engine-plugin`, `/docs/integration-guide`.

A própria documentação apresenta MCP como uma forma de permitir que um assistente de IA construa, edite e faça Play em modelos. Isso é descrição da capacidade/documentação pública. Não houve conexão, autenticação, alteração de diagrama ou execução por este scout. [3]

## Atualidade pública observada

O changelog público consultado exibe entradas datadas. Em **13 de agosto de 2026**, registra Artificial Agents, um Forecast Exploration Dashboard, melhorias no AI Builder, recursos customizados sem ícones e suporte ao russo, além de correções de bugs. Em **2 de julho de 2026**, registra a renomeação de Custom Variables para Parameters, uma aba Live Data para conectores JSON e Google Sheets, referências de valores de nós em fórmulas, suporte a decimais em conexões e modo de visualização móvel, entre outras mudanças. Em **3 de junho de 2026**, registra idiomas adicionais, temas, cores de diagramas, um nó Queue dedicado e melhorias em gráficos/playbar. Essas entradas são evidência de histórico editorial público, não um teste dos recursos. [7]

A página também informa que mudanças recentes ficam em “What’s new” dentro do aplicativo. Assim, o changelog público não deve ser interpretado como inventário exaustivo de toda mudança, versão interna, estado de disponibilidade por plano ou compatibilidade. [7]

## Registros verificados

- Rota de entrada HTTPS pública acessível: `https://machinations.io/learn`.
- Organização/rodapé observados: `Machinations S.àr.l`, copyright exibido como 2026 nas páginas consultadas.
- Página `/learn` observada com 19 lições de Machinations essentials, 4 séries e 10 lições individuais declaradas.
- Percurso `/learn/pathway-introduction` observado com foco em loot/crafting, componentes centrais, recursos, regras, feedback, Play e pressupostos.
- Tutorial `/learn/loot-craft` observado com Source, Pool, Resource Connection, Steps, Play e instruções de montagem de um diagrama.
- Índice `/docs` observado com categorias públicas para nós, conexões, parâmetros/variáveis, matemática, Play/forecast, colaboração e integrações.
- Página `/docs/the-monte-carlo-simulations` observada com explicação de amostragem aleatória, número de amostras e estimativa de Pi.
- Página `/glossary` observada com 258 termos e 258 diagramas de exemplo declarados.
- `/docs/changelog` observado com entradas datadas até 13 de agosto de 2026 no conteúdo consultado.

## Limitações e não verificações

- `coverage` é **partial**: o escopo foi a rota pública indicada e páginas oficiais diretamente relacionadas; não há prova de cobertura completa de todo o site, de todos os recursos, de todas as páginas dinâmicas ou de todos os diagramas.
- Não houve login, matrícula, compra, uso de conta, conexão MCP, alteração de modelo, Play, Forecast, execução de simulação, teste de integração ou avaliação de qualidade pedagógica.
- O texto e a taxonomia públicos comprovam descrição editorial/documental, mas não runtime, correção, completude, acessibilidade ou manutenção uniforme de cada página.
- Não foi observado repositório público, caminho de repositório, branch ou commit/SHA associado aos materiais de aprendizagem; nenhum foi inventado ou atribuído.
- Não foi observada licença explícita para copiar os textos, diagramas ou imagens; o relatório preserva links e metadados descritivos, sem copiar código ou ativos.
- Não foram observados preços, requisitos de plano, limites de créditos ou permissões efetivas de uso além das referências documentais públicas; a presença de `/pricing` ou de “Start modeling free” não foi usada como prova de condições comerciais.
- Os números editoriais (19 lições, 4 séries, 10 lições individuais, 258 termos e 258 diagramas) são snapshots da página consultada e podem mudar.
- A página de changelog orienta o leitor a consultar “What’s new” no aplicativo; portanto, seu inventário público pode não ser exaustivo.

## References

[1]: https://machinations.io/learn "Learn systems modeling - Machinations"
[2]: https://machinations.io/learn/pathway-introduction "Pathway introduction - Machinations Learn"
[3]: https://machinations.io/docs "Documentation - Machinations"
[4]: https://machinations.io/learn/loot-craft "Loot & Craft - Machinations Learn"
[5]: https://machinations.io/docs/the-monte-carlo-simulations "Monte Carlo Simulations - Machinations Docs"
[6]: https://machinations.io/glossary "Economics and systems thinking glossary - Machinations"
[7]: https://machinations.io/docs/changelog "Changelog - Machinations Docs"
