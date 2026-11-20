# Scout 36 — LangChain official ecosystem

**Fonte de entrada:** [docs.langchain.com](https://docs.langchain.com)  
**Organização observada:** LangChain / `langchain-ai`  
**Data da consulta:** 2026-11-20  
**Coverage:** `partial`

## Conclusão

A fonte pública apresenta um ecossistema em camadas para engenharia de agentes. A documentação oficial descreve LangChain como framework de agentes, LangGraph como runtime/orquestração de baixo nível, Deep Agents como harness opinativo sobre LangChain/LangGraph e LangSmith como plataforma para tracing, avaliação, deployment e monitoramento. A página inicial organiza o ciclo em Build, Test, Deploy e Monitor e também lista produtos como LLM Gateway, Tool Gateway, Fleet, Engine e Deep Agents Code [1].

A cobertura é `partial`, não `complete`: o índice `llms.txt` declara 1.506 páginas no bloco Agent Development Lifecycle e 227 páginas em Products and Setup, enquanto esta verificação leu páginas representativas e metadados de quatro repositórios. O extrator marcou a página de Deep Agents como truncada. Não foi feito clone, instalação, execução de código, login, matrícula, compra ou teste de runtime.

## Componentes e relações verificadas

### LangChain

A página “LangChain overview” descreve `create_agent` como um harness mínimo e configurável, composto por modelo, ferramentas, prompt e middleware. Ela recomenda LangGraph para necessidades avançadas de orquestração e LangSmith para tracing, debugging e avaliação [2]. A documentação também afirma que os agentes de LangChain são construídos sobre LangGraph, e mostra caminhos de instalação e exemplos documentais para múltiplos provedores. Esses exemplos são documentação; não constituem prova de que foram executados nesta pesquisa.

No repositório oficial `langchain-ai/langchain`, a descrição é “The agent engineering platform”. Foram observados os arquivos de topo `README.md`, `LICENSE`, `AGENTS.md`, `CITATION.cff`, `libs/` e diretórios de configuração. O README descreve LangChain como framework para agentes e aplicações alimentadas por LLM, com componentes interoperáveis e integrações de terceiros, e aponta Deep Agents, LangGraph e LangSmith como partes do ecossistema [3].

- Repositório: `https://github.com/langchain-ai/langchain`
- Branch observado: `master`
- Commit observado via API: `e8a78d547970628c35cf5f3c7b054766099ea0bc`
- Caminhos observados: `README.md`, `LICENSE`, `libs/`
- Licença declarada pelo GitHub/API e página do repositório: MIT (`MIT License`)
- Proveniência: organização GitHub `langchain-ai`; o endpoint de repositório marcou o projeto como público e não-fork.

### LangGraph

A documentação oficial descreve LangGraph como framework e runtime de baixo nível para agentes long-running e stateful. O modelo é um grafo de estado compartilhado, nós e arestas, com combinação de etapas determinísticas e orientadas por LLM. São explicitamente listados durable execution, streaming, human-in-the-loop, persistência e memória [4]. A mesma página afirma que LangGraph pode ser usado sem LangChain.

O repositório oficial `langchain-ai/langgraph` descreve o projeto como low-level orchestration framework para agentes stateful e lista durable execution, human-in-the-loop, memória, debugging com LangSmith e deployment. Foram observados os diretórios `docs/`, `examples/`, `libs/` e os arquivos `README.md`, `LICENSE`, `Makefile` e `AGENTS.md` [5].

- Repositório: `https://github.com/langchain-ai/langgraph`
- Branch observado: `main`
- Commit observado via API: `08a2016953789a4f579b4d36bd1967941ec62012`
- Caminhos observados: `README.md`, `LICENSE`, `docs/`, `examples/`, `libs/`
- Versão explicitamente visível no commit consultado: `langgraph` 1.2.22 em `libs/langgraph/pyproject.toml` (o commit é uma release commit)
- Licença declarada pelo GitHub/API e página do repositório: MIT (`MIT License`)
- Proveniência: organização GitHub `langchain-ai`; o README diz que o projeto é construído pela LangChain Inc. e pode ser usado sem LangChain.

### Deep Agents

A documentação oficial define Deep Agents como harness para trabalho complexo e multi-etapas. Ela descreve planejamento, filesystem virtual para contexto, spawning de subagentes e memória de longo prazo sobre LangChain e LangGraph. A página separa Managed Deep Agents de Deep Agents SDK self-hosted e lista ferramentas, conexão a dados, gestão de contexto, paralelização e aprovação humana [6]. O extrator retornou a página como `partial`/truncada; portanto, não foi tratado como inventário completo de capacidades.

O README do repositório oficial chama Deep Agents de open-source agent harness, opinativo, extensível e model-agnostic. Entre os itens descritos estão sub-agents, filesystem, context management, shell access, persistent memory, human-in-the-loop, skills e ferramentas/MCP. O README também afirma que o projeto é construído sobre LangGraph e integra tracing, avaliação e deployment via LangSmith [7]. São alegações editoriais do README, não resultado de execução aqui.

- Repositório: `https://github.com/langchain-ai/deepagents`
- Branch observado: `main`
- Commit observado via API: `f5324db305c8ce6040a97b678e60fb82a43ce968`
- Caminhos observados: `README.md`, `LICENSE`, `libs/`, `examples/`, `.github/`, `openwiki/`
- Licença declarada pelo GitHub/API e página do repositório: MIT (`MIT License`)
- Proveniência: organização GitHub `langchain-ai`; repositório público e não-fork segundo API.

### LangSmith

A página oficial de observabilidade define LangSmith como plataforma framework-agnostic para instrumentar aplicações LLM, investigar traces e monitorar performance em produção. Descreve traces como registros do que agentes fizeram e lista visualização de traces, dashboards, alertas, regras/webhooks, feedback, avaliações online e LangSmith Engine [8]. A página informa opções de instância cloud, hybrid ou self-hosted, mas nenhum ambiente foi configurado nem acessado nesta pesquisa.

A página inicial dos docs também posiciona LangSmith para testar, implantar, monitorar e melhorar agentes ao longo do ciclo de desenvolvimento, além de listar Agent Registry, LLM Gateway, Tool Gateway, Fleet, Engine e setup/governance [1]. Essas páginas são documentação editorial do fornecedor; não provam disponibilidade, preço, SLA, desempenho ou cobertura funcional em um ambiente específico.

- Página de entrada: `https://docs.langchain.com/langsmith/observability`
- Caminho documental observado no repositório de docs: `src/langsmith/observability.mdx` (link “Edit this page”)
- Repositório documental: `https://github.com/langchain-ai/docs`
- Branch observado: `main`
- Commit observado via API: `484c77db5cceef78e73236b8bfef9b1c66e666c8`
- Licença do repositório de docs declarada pela GitHub/API: MIT (`MIT License`)

## Proveniência, commits e licenças

A organização pública `https://github.com/langchain-ai` foi observada com website `https://www.langchain.com`, tópicos relacionados a LangChain/LangGraph/agentes e links para os repositórios `langchain-ai/langchain`, `langchain-ai/langgraph` e `langchain-ai/docs` [9]. Os SHAs acima são os valores retornados pelos endpoints públicos de commit no momento da consulta; não são uma garantia de que os branches permanecerão imutáveis depois disso.

Para documentação, os caminhos de edição observados incluem `src/oss/langchain/overview.mdx`, `src/oss/langgraph/overview.mdx`, `src/oss/concepts/products.mdx` e `src/langsmith/observability.mdx`. A página de produtos confirma a divisão conceitual entre runtime, framework e harness e compara LangGraph, LangChain e Deep Agents em memória, skills, subagentes, human-in-the-loop e streaming [10].

As licenças registradas aqui são apenas as declaradas no metadata público do GitHub/API para os repositórios. Isso não substitui uma revisão de licença de dependências, integrações, exemplos ou conteúdo de terceiros antes de qualquer reutilização. Nenhum código foi copiado para o catálogo.

## O que não foi verificado

- Não foi executado nenhum snippet das documentações, nenhum agente, workflow, trace, avaliação, deployment ou comando de instalação.
- Não houve instalação de pacotes, clone de repositórios, chamada a serviços autenticados ou uso de API keys.
- Não foi verificada qualidade pedagógica, completude dos tutoriais, compatibilidade entre versões, comportamento em produção, latência, custo, limites, segurança operacional ou disponibilidade dos produtos.
- Não foi inventariado todo o GitHub da organização, todas as integrações, todas as páginas dos índices ou todas as linguagens/SDKs.
- O índice `llms.txt` é um mapa documental dinâmico e indica grandes contagens de páginas; a consulta desta tarefa foi uma amostra direcionada aos componentes do escopo. Por isso, coverage permanece `partial`.

## Registros verificados

1. `docs.langchain.com` — título: “The open agent engineering ecosystem”; organização/autoria editorial: LangChain; data de publicação não exibida; ciclo Build/Test/Deploy/Monitor e produtos listados [1].
2. `docs.langchain.com/oss/python/langchain/overview` — título: “LangChain overview”; organização: LangChain; data não exibida; `create_agent`, relação com LangGraph/Deep Agents/LangSmith e exemplos documentais [2].
3. `docs.langchain.com/oss/python/langgraph/overview` — título: “LangGraph overview”; organização: LangChain; data não exibida; runtime, orquestração, persistência, streaming e HITL [4].
4. `docs.langchain.com/oss/python/deepagents/overview` — título: “Deep Agents overview”; organização: LangChain; data não exibida; harness, SDK, managed mode e capacidades; página retornada truncada [6].
5. `docs.langchain.com/langsmith/observability` — título: “LangSmith Observability”; organização: LangChain; data não exibida; tracing, investigação, dashboards, automações e feedback [8].
6. `langchain-ai/langchain` — branch `master`, SHA `e8a78d547970628c35cf5f3c7b054766099ea0bc`, MIT; caminhos `README.md`, `LICENSE`, `libs/` [3].
7. `langchain-ai/langgraph` — branch `main`, SHA `08a2016953789a4f579b4d36bd1967941ec62012`, MIT; caminhos `README.md`, `LICENSE`, `docs/`, `examples/`, `libs/` [5].
8. `langchain-ai/deepagents` — branch `main`, SHA `f5324db305c8ce6040a97b678e60fb82a43ce968`, MIT; caminhos `README.md`, `LICENSE`, `libs/`, `examples/` [7].
9. `langchain-ai/docs` — branch `main`, SHA `484c77db5cceef78e73236b8bfef9b1c66e666c8`, MIT; caminhos documentais observados via links de edição [10].

## References

[1]: https://docs.langchain.com/ "Home — Docs by LangChain"
[2]: https://docs.langchain.com/oss/python/langchain/overview "LangChain overview"
[3]: https://github.com/langchain-ai/langchain "langchain-ai/langchain — GitHub repository"
[4]: https://docs.langchain.com/oss/python/langgraph/overview "LangGraph overview"
[5]: https://github.com/langchain-ai/langgraph "langchain-ai/langgraph — GitHub repository"
[6]: https://docs.langchain.com/oss/python/deepagents/overview "Deep Agents overview"
[7]: https://github.com/langchain-ai/deepagents "langchain-ai/deepagents — GitHub repository"
[8]: https://docs.langchain.com/langsmith/observability "LangSmith Observability"
[9]: https://github.com/langchain-ai "LangChain organization on GitHub"
[10]: https://docs.langchain.com/oss/python/concepts/products "Runtimes, frameworks, and harnesses"
[11]: https://docs.langchain.com/llms.txt "Documentation index — Docs by LangChain"
[12]: https://api.github.com/repos/langchain-ai/langchain/commits/master "Current master commit — langchain"
[13]: https://api.github.com/repos/langchain-ai/langgraph/commits/main "Current main commit — langgraph"
[14]: https://api.github.com/repos/langchain-ai/deepagents/commits/main "Current main commit — deepagents"
[15]: https://api.github.com/repos/langchain-ai/docs/commits/main "Current main commit — docs"
