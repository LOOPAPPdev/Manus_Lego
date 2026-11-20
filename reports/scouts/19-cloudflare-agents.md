# Scout: `cloudflare/agents`

- **Rota de entrada:** https://developers.cloudflare.com/agents/
- **Tipo:** documentação pública oficial da Cloudflare, com repositório público oficial no GitHub
- **Data da verificação:** 2026-11-20
- **Coverage:** `partial`. A documentação e os metadados abaixo foram verificados para o escopo Agents SDK, Durable Objects, estado, tarefas, streaming e execução durável. Isso não é um inventário exaustivo de todas as páginas, APIs, exemplos ou versões do SDK, nem prova de execução, build, segurança ou runtime.

## Conclusão

A documentação pública descreve o Agents SDK como um runtime em que cada agente executa dentro de um Durable Object. O runtime combina `Lifecycle`, roteamento e capacidades anexadas, enquanto o Lifecycle coordena inicialização, requests, eventos WebSocket, fila durável de jobs e o alarme único do objeto [1] [2]. A rota de entrada lista explicitamente estado, WebSockets, agendamento, MCP, harnesses, ferramentas e canais de comunicação [1].

O estado persistente documentado é um valor JSON validado armazenado no SQLite do Durable Object. A capacidade `State` carrega o valor na primeira leitura, mantém cache em memória, valida cada mudança e pode sincronizar mudanças com clientes conectados por WebSockets; a própria página informa que cada alteração reescreve o valor inteiro e que dados grandes ou relacionais devem usar tabelas próprias [3].

As tarefas aparecem em duas camadas verificáveis. `Scheduler` registra callbacks nomeados para execução atrasada, em uma data, por cron ou em intervalo; esses schedules são jobs da fila do Lifecycle e sobrevivem a eviction [4]. A fila de jobs armazena nome da função, horário e payload JSON no SQLite, e o alarme desperta o objeto quando o job vence [5]. A classe `Agent` expõe os atalhos `schedule()`, `scheduleEvery()`, consulta e cancelamento [6].

Para streaming, `Streams` é documentado como experimental. Ele armazena chunks em log ordenado no SQLite, permite replay desde um cursor e acompanha novos chunks; `sseResponse()` usa `Last-Event-ID` para retomar uma conexão SSE sem lógica adicional no cliente [7]. A documentação descreve também o uso para preservar resposta parcial quando o cliente desconecta ou o Durable Object reinicia, mas isso é evidência documental da capacidade, não um teste executado neste scout [7].

Para trabalho longo, a documentação da classe `Agent` apresenta `runFiber()`, `startFiber()`, `keepAlive()` e `onFiberRecovered()`. Fibers persistem metadados e checkpoints em SQLite e podem recuperar uma execução interrompida após eviction; `startFiber()` oferece aceite durável, idempotência, inspeção e cancelamento [8]. A mesma documentação diferencia fibers de Workflows: fibers são para trabalho próprio da execução do agente, enquanto Workflows são indicados para trabalho independente com retries por etapa e orquestração multi-step [8].

## Proveniência e metadados verificáveis

- **Provider/repositório:** GitHub, `cloudflare/agents`.
- **Repositório:** https://github.com/cloudflare/agents.
- **Branch observada:** `main`.
- **Commit observado:** `e981dac54a6616c59b76b69e3ae2da00345e1361`, obtido pela API pública de commits para `main` em 2026-11-20 [10].
- **Licença declarada pelo GitHub:** MIT (`spdx_id: MIT`) no metadado público do repositório [9]. Isso é metadado do repositório e não uma revisão das licenças de dependências ou de terceiros.
- **Caminhos relativos observados na API:** `packages/agents/` (inclui `README.md`, `package.json`, `src/` e `vitest.config.ts`) [11]; diretório `examples/` com, entre outros, `examples/ai-chat/`, `examples/agents-as-tools/`, `examples/workflows/` e `examples/resumable-stream-chat/` conforme o índice público e o README do repositório [12] [13].
- **Natureza da evidência:** páginas de documentação, respostas JSON da API pública do GitHub, README e listagens de caminhos. Nenhum código foi clonado, instalado ou executado.

O README do repositório descreve agentes como ambientes persistentes e stateful apoiados por Durable Objects, e mostra um exemplo textual de estado persistente, métodos `@callable()` e sincronização com `useAgent`. O mesmo README enumera recursos como scheduling, WebSockets, chat persistente, streaming resumível, Workflows e SQL [13]. Essas afirmações foram tratadas como documentação de projeto, não como prova de funcionamento.

## Registros realmente verificados

1. **Runtime Agents SDK / Durable Object** — documentação em `https://developers.cloudflare.com/agents/runtime/`; ref documental observada com atualização de 2026-11-10. A página afirma que cada agente roda em um Durable Object e identifica `Lifecycle`, roteamento, capacidades e observabilidade. Também mostra a composição com `Lifecycle.install(this)`, `Scheduler`, `WebSockets` e `routeAgentRequest()` [2]. Status de runtime: **não verificado**.

2. **State capability** — documentação em `https://developers.cloudflare.com/agents/runtime/capabilities/state/`; caminho conceitual `agents/state`. Evidência observada: armazenamento em SQLite, `get()`, `set(next, source?)`, `validateStateChange`, `onChanged`, integração com `WebSockets` e tabela `cf_agents_state` [3]. Status de runtime: **não verificado**.

3. **Scheduler capability** — documentação em `https://developers.cloudflare.com/agents/runtime/capabilities/scheduler/`; caminho conceitual `agents/schedules`. Evidência observada: `set()` para delay, `Date` ou cron; `every()` para intervalos; callbacks nomeados; retry; idempotência; `get()`, `list()` e `cancel()` [4]. Status de runtime: **não verificado**.

4. **Lifecycle jobs and alarms** — documentação em `https://developers.cloudflare.com/agents/runtime/lifecycle/job-queue/`; evidência observada de fila `cf_agents_jobs`, alarme único do Durable Object, jobs duráveis, payload serializável, `push()`, `cancel()`, `reschedule()`, retries e resultado `rescheduleAt`/`yield` [5]. Status de runtime: **não verificado**.

5. **Agent schedule tasks** — documentação em `https://developers.cloudflare.com/agents/agent-class/schedule-tasks/`; evidência observada de `schedule()`, `scheduleEvery()`, `getScheduleById()`, `listSchedules()` e `cancelSchedule()`, além da ressalva de que `keepAlive()` previne eviction ociosa, mas não substitui recuperação após deploy ou crash [6]. Status de runtime: **não verificado**.

6. **Streams capability** — documentação em `https://developers.cloudflare.com/agents/runtime/capabilities/streams/`; evidência observada de status **Experimental**, `open()`, `append()`, `close()`, `error()`, cursor durável, `read()`, `readBatches()`, `sseResponse()`, replay e `Last-Event-ID` [7]. Status de runtime: **não verificado**.

7. **Durable execution with fibers** — documentação em `https://developers.cloudflare.com/agents/agent-class/durable-execution/`; evidência observada de `runFiber()`, `startFiber()`, `inspectFiber()`, `cancelFiber()`, `stash()` e `onFiberRecovered()`, além da distinção documentada entre `keepAlive`, fibers e Workflows [8]. Status de runtime: **não verificado**.

8. **Repositório oficial e caminhos públicos** — `cloudflare/agents`, branch `main`, commit `e981dac54a6616c59b76b69e3ae2da00345e1361`. A API do repositório reporta público, não fork, não arquivado, branch padrão `main`, linguagem TypeScript e licença MIT [9] [10]. A API de contents confirma `packages/agents/README.md`, `packages/agents/package.json`, `packages/agents/src/` e arquivos associados no mesmo repositório [11]. Status de código: **reference_only**; não foi feita execução.

## Limitações e decisão de coverage

- `partial` é apropriado porque foram verificadas a rota de entrada e as páginas centrais do escopo pedido, mas não todas as páginas listadas em `llms.txt`, todos os exports, todos os exemplos, todas as releases ou todas as combinações de capacidades.
- A documentação é um snapshot temporal e pode mudar depois da consulta. O SHA do GitHub deve ser repinado para qualquer integração futura.
- A documentação não foi usada como prova de build, testes, deploy, disponibilidade de serviço, latência, durabilidade efetiva em produção, segurança ou compatibilidade entre versões.
- A listagem da API de `examples/` foi truncada pela ferramenta de extração; portanto não sustenta uma contagem ou enumeração completa de exemplos [12].
- `Streams` está explicitamente marcado como experimental [2] [7]. A documentação também chama o Pi Durable de experimental na rota de entrada [1]. Não se deve inferir estabilidade de produção a partir da presença dessas APIs.
- O metadado MIT é do repositório; não substitui análise de licenças de dependências, subdiretórios, pacotes incorporados ou conteúdo de terceiros.
- Não foram executados `npm`, `pnpm`, scripts, testes, builds, servidores, deploys ou código dos candidatos. Não foi feita instalação de dependências e nenhum código foi clonado.
- Não foram acessados dashboards privados, contas Cloudflare, tokens, identificadores de conta, segredos ou endpoints autenticados.
- A API pública do GitHub confirmou o commit e alguns caminhos, mas não foi usada para afirmar que cada caminho compila ou que cada exemplo está operacional.

## References

[1]: https://developers.cloudflare.com/agents/ "Cloudflare Agents documentation entry route"
[2]: https://developers.cloudflare.com/agents/runtime/ "Cloudflare Agents SDK Runtime documentation"
[3]: https://developers.cloudflare.com/agents/runtime/capabilities/state/ "Cloudflare Agents State capability documentation"
[4]: https://developers.cloudflare.com/agents/runtime/capabilities/scheduler/ "Cloudflare Agents Scheduler capability documentation"
[5]: https://developers.cloudflare.com/agents/runtime/lifecycle/job-queue/ "Cloudflare Agents Lifecycle jobs and alarms documentation"
[6]: https://developers.cloudflare.com/agents/agent-class/schedule-tasks/ "Cloudflare Agents schedule tasks documentation"
[7]: https://developers.cloudflare.com/agents/runtime/capabilities/streams/ "Cloudflare Agents Streams capability documentation"
[8]: https://developers.cloudflare.com/agents/agent-class/durable-execution/ "Cloudflare Agents durable execution with fibers documentation"
[9]: https://api.github.com/repos/cloudflare/agents "GitHub repository metadata for cloudflare/agents"
[10]: https://api.github.com/repos/cloudflare/agents/commits/main "GitHub main branch commit metadata for cloudflare/agents"
[11]: https://api.github.com/repos/cloudflare/agents/contents/packages/agents?ref=e981dac54a6616c59b76b69e3ae2da00345e1361 "GitHub contents metadata for packages/agents at observed commit"
[12]: https://api.github.com/repos/cloudflare/agents/contents/examples?ref=main "GitHub public contents listing for examples"
[13]: https://github.com/cloudflare/agents/blob/e981dac54a6616c59b76b69e3ae2da00345e1361/README.md "Cloudflare Agents README at observed commit"
