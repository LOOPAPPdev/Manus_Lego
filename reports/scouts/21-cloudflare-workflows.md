# Scout: Cloudflare Workflows

- **Rota:** https://developers.cloudflare.com/workflows/
- **Fonte única:** documentação pública oficial Cloudflare Workflows
- **Tipo:** documentação técnica pública e referências públicas de API
- **Data da verificação:** 2026-11-20
- **Coverage:** `partial`. A documentação oficial e seu índice público foram acessados, e as páginas diretamente relacionadas a execução durável, steps, retries, limites, eventos, lifecycle, integrações e observabilidade foram verificadas. Esta classificação não afirma cobertura completa de todas as páginas, versões, APIs ou comportamentos de runtime. Não houve acesso a conta, dashboard, token, deployment ou execução real.

## Conclusão

Cloudflare Workflows é documentado como um mecanismo de execução durável para aplicações multi-step sobre Workers. A página de entrada afirma que workflows podem encadear steps, fazer retry automático e persistir estado por minutos, horas ou semanas, sem infraestrutura gerenciada pelo usuário [1]. O índice público `llms.txt` enumera as áreas de documentação verificadas, incluindo Workers API, regras de durabilidade, sleeping/retrying, eventos, limites, concurrency, chamadas a Pages, observabilidade, exemplos e REST API [2].

A unidade de execução é o step. A referência Workers API exige que uma definição estenda `WorkflowEntrypoint` e tenha um método `run` com ao menos uma chamada de step. `step.do` recebe nome, callback e configuração opcional de retry; o callback pode retornar estado serializável para persistência. A API também documenta `step.sleep`, `step.sleepUntil`, `step.waitForEvent` e operações de instância como `status`, `pause`, `resume`, `terminate` e `restart` [3].

A durabilidade documentada não deve ser confundida com uma garantia de que qualquer variável em memória sobreviverá. As regras oficiais dizem que cada step é autocontido e individualmente retryable, e que o Workflow pode hibernar, perdendo estado em memória fora dos retornos de steps. O estado que precisa atravessar lifetimes deve ser produzido por retornos de `step.do` ou mantido em armazenamento externo apropriado [4]. A mesma página recomenda idempotência porque um step pode ser executado novamente depois de falha de rede, infraestrutura ou destino externo [4]. Isso é orientação de projeto documentada, não resultado de um teste independente.

## Execução durável e steps

- `WorkflowEntrypoint.run(event, step)` é o ponto de entrada documentado. O evento inclui payload opcional, timestamp, `instanceId`, nome do Workflow e, para instâncias agendadas, metadados do cron [3].
- `step.do(name, callback)` cria um step individualmente executável e retryable. O nome pode ter até 256 caracteres. O callback pode retornar estado serializável; a documentação informa limite de 1 MiB para valores estruturados e recomenda referências a armazenamento externo para artefatos grandes [3].
- O retorno de `run` pode ser disponibilizado no status da instância, na Workers API, na REST API e no dashboard [3]. Isso é um contrato documental de API, não evidência de uma instância observada.
- Steps podem rodar em paralelo com primitivas JavaScript como `Promise.all`, e o fluxo pode usar condicionais, loops e `try/catch`, conforme a referência da API [3].
- `step.sleep` aceita duração relativa em milissegundos ou unidades legíveis como segundo, minuto, hora, dia, semana, mês e ano. `step.sleepUntil` aceita uma data ou timestamp Unix [5].
- `step.waitForEvent` permite aguardar eventos externos durante a execução; eventos podem ser enviados por binding Workers ou pelo endpoint de eventos da REST API. O tipo do evento deve coincidir e pode ter até 100 caracteres; o timeout padrão documentado é 24 horas, com faixa de 1 segundo a 365 dias [6].

## Retries, falhas e compensação

A configuração padrão documentada para `step.do` é `retries.limit: 5`, atraso de 10.000 ms, backoff exponencial e timeout de 10 minutos por tentativa [5]. A configuração pode alterar o limite, atraso fixo ou função de atraso dinâmico, algoritmo `constant`, `linear` ou `exponential`, e timeout por tentativa. A página declara limite de até 10.000 retries por step [5] [7].

Um atraso dinâmico recebe o contexto atual, incluindo o número da tentativa, e o erro que provocou a repetição. A documentação mostra uso para rate limits e recuperação de provedores downstream [5]. `NonRetryableError` interrompe o retry do step e faz a instância falhar imediatamente; steps posteriores não são invocados [5].

Exceções não capturadas no nível superior, ou steps que esgotam seu limite, levam a instância ao estado `Errored`. Um `try/catch` em torno de steps pode tratar a falha e permitir que o Workflow continue com steps de limpeza ou lógica condicional [5]. A API também documenta rollback handlers para compensação estilo saga, executados em ordem reversa dos steps registrados, com configuração própria de retry e timeout [3] [5].

As regras oficiais alertam que chamadas não idempotentes precisam de verificação de estado antes da operação. Um exemplo de cobrança verifica se a operação já ocorreu antes de fazer a chamada que pode ser repetida [4]. A documentação também recomenda separar chamadas a serviços diferentes em steps distintos para limitar efeitos de retries parciais [4]. Essas recomendações são evidência de desenho e segurança operacional documentados; não são prova de uma auditoria de segurança nem de execução contra um processador de pagamentos.

## Limites observados

A página oficial de limites foi acessada e os seguintes valores foram observados [7]:

- Tamanho máximo do script com classes de Workflow: 3 MB no Workers Free e 10 MB no Workers Paid.
- Tempo de CPU ativo por step: 10 ms no Free; 30 segundos no Paid por padrão, configurável até 5 minutos. Duração de wall-clock por step é documentada como ilimitada, inclusive quando há espera por I/O.
- Resultado não-stream por step: 1 MiB em ambos os planos.
- Payload máximo de evento: 1 MiB.
- Estado máximo persistido por instância: 100 MB no Free e 1 GB no Paid.
- Duração máxima de `step.sleep`: 365 dias.
- Número máximo de steps: 1.024 no Free; 10.000 no Paid por padrão, configurável até 25.000.
- Execuções máximas: 100.000 por dia no Free, compartilhadas com o limite diário de Workers; ilimitadas no Paid.
- Instâncias concorrentes por conta: 100 no Free e 50.000 no Paid.
- Taxa máxima de criação de instâncias: 100 por segundo no Free; 300 por segundo por conta no Paid e 100 por segundo por Workflow.
- Instâncias enfileiradas: 100.000 no Free e 2.000.000 no Paid.
- Retenção de estado de instâncias concluídas: 3 dias no Free; 7 dias por padrão no Paid, configurável até 30 dias.
- Subrequests por instância: 50 por request no Free; 10.000 por request no Paid por padrão, configurável até 10 milhões.
- Retries por step: 10.000 em ambos os planos.

A mesma página diz que instâncias em `waiting`, por sleep, retry ou `waitForEvent`, não contam para os limites de concorrência enquanto aguardam. Ela também documenta que payloads e resultados grandes devem ser tratados com cuidado e que artefatos grandes ou duradouros podem ser colocados em R2, retornando uma referência [7]. Os limites são documentação de produto; não foram medidos nem exercitados neste scout.

## Integrações públicas verificadas

- **Workers bindings, CLI e REST API:** a documentação de eventos e trigger informa que uma instância pode ser criada por binding, `wrangler` ou REST API. A referência de trigger mostra criação, consulta de status, pause, resume, terminate e restart por binding [6] [8].
- **Eventos externos e webhooks:** a página de eventos documenta payload JSON serializável no disparo e `waitForEvent` para eventos durante a execução [6]. O exemplo oficial de webhook descreve Worker receptor, verificação de assinatura, Queue e criação de uma instância por evento; usa IDs idempotentes e trata entrega at-least-once [9]. O exemplo inclui respostas locais de teste, mas não constitui execução observada neste scout.
- **Pages Functions:** a página oficial documenta chamada a Workflows por Service Binding ou `fetch`. Ela exige que o Workflow seja implantado como Worker separado quando chamado a partir de Pages Functions e recomenda Service Bindings para chamadas internas, pois não expõem endpoint público nem exigem autenticação HTTP [10].
- **R2, D1 e cron:** o exemplo oficial de backup de D1 descreve iniciar exportação via API, aguardar disponibilidade, baixar o dump e armazená-lo em R2; usa `schedules` para criar instâncias automaticamente e os retries padrão por step [11]. O exemplo expõe um token como secret no código de configuração, mas nenhum segredo foi acessado ou armazenado neste scout.
- **Twilio:** a página oficial de exemplos referencia um repositório público externo `craigsdennis/twilio-cloudflare-workflow` e descreve integração com APIs e webhooks de Twilio [12]. Como a tarefa restringe a fonte a Cloudflare Workflows docs e não permite clonar, instalar ou executar candidatos, o repositório foi registrado apenas como link citado pela documentação, sem inferir commit, licença, runtime ou segurança.
- **Observabilidade:** a documentação informa métricas de execução, erros, steps e duração por dashboard ou GraphQL Analytics API. Os eventos documentados incluem estados de Workflow, steps, tentativas, sleep e rollback. A retenção indicada é de 31 dias para as métricas consultáveis [13]. A consulta GraphQL requer filtro `accountTag`; nenhum identificador de conta foi usado ou armazenado.

## Registros realmente verificados

1. **`cloudflare-workflows-overview`** — rota relativa `/workflows/`; página pública de entrada acessível. Verificados: execução multi-step, retries automáticos, persistência de estado, espera por eventos, lifecycle e exemplos de integração com R2 e Workers AI [1].
2. **`cloudflare-workflows-doc-index`** — rota relativa `/workflows/llms.txt`; índice público acessível. Verificadas as categorias e URLs listadas para Workers API, sleeping/retrying, events, limits, trigger, Pages, examples, observability e REST API [2].
3. **`cloudflare-workflows-workers-api`** — rota relativa `/workflows/build/workers-api/`; API pública acessível. Verificados `WorkflowEntrypoint`, `run`, `WorkflowEvent`, `step.do`, retorno serializável, configuração de retry, rollback e operações de instância [3].
4. **`cloudflare-workflows-rules`** — rota relativa `/workflows/build/rules-of-workflows/`; regras públicas acessíveis. Verificados autocontenção/retry de steps, hibernação, perda de estado em memória fora de steps e recomendação de idempotência [4].
5. **`cloudflare-workflows-sleep-retry`** — rota relativa `/workflows/build/sleeping-and-retrying/`; verificados sleep relativo/absoluto, defaults, backoff, atraso dinâmico, `NonRetryableError`, catch e rollback [5].
6. **`cloudflare-workflows-events`** — rota relativa `/workflows/build/events-and-parameters/`; verificados parâmetros de criação, `waitForEvent`, `sendEvent`, timeouts e correspondência de tipos [6].
7. **`cloudflare-workflows-limits`** — rota relativa `/workflows/reference/limits/`; tabela de limites Free/Paid e comportamento de instâncias `waiting` acessados [7].
8. **`cloudflare-workflows-trigger`** — rota relativa `/workflows/build/trigger-workflows/`; verificados status possíveis e operações de lifecycle [8].
9. **`cloudflare-workflows-webhook-example`** — rota relativa `/workflows/examples/trigger-from-webhook/`; exemplo público acessível, com assinatura, Queue, criação em lote, idempotência e tratamento de 429 documentados [9].
10. **`cloudflare-workflows-pages`** — rota relativa `/workflows/build/call-workflows-from-pages/`; Service Binding e `fetch` a partir de Pages Functions documentados [10].
11. **`cloudflare-workflows-d1-r2-example`** — rota relativa `/workflows/examples/backup-d1/`; D1 REST API, R2, schedule e retry documentados [11].
12. **`cloudflare-workflows-twilio-example`** — rota relativa `/workflows/examples/twilio/`; referência documental ao repositório público `craigsdennis/twilio-cloudflare-workflow`, sem verificação do repositório [12].
13. **`cloudflare-workflows-metrics`** — rota relativa `/workflows/observability/metrics-analytics/`; GraphQL Analytics API, dimensões, eventos e retenção documental verificados [13].
14. **`cloudflare-workflows-rest-list`** — rota pública `https://developers.cloudflare.com/api/resources/workflows/methods/list/`; endpoint documentado como `GET /accounts/{account_id}/workflows`, com paginação e autenticação exigida. Não foi chamado porque isso exigiria uma conta e credencial [14].

Não foi observado repositório Cloudflare, branch ou commit/SHA para a documentação nesta tarefa. O único repositório citado por uma página de exemplo foi `craigsdennis/twilio-cloudflare-workflow`; não foi clonado, aberto via API ou tratado como registro verificado. Portanto, não há SHA, branch ou licença de repositório a registrar.

## Limitações, segurança e interpretação

- `partial` é intencional: o índice público lista muitas páginas, mas este scout verificou as páginas diretamente relacionadas ao foco solicitado; não foi feita auditoria exaustiva de cada página, idioma, versão ou changelog.
- A fonte é documentação e referência de API. Ela prova que contratos, exemplos e limites estão publicados, mas não prova build, deploy, execução real, disponibilidade regional, comportamento sob carga, correção de integração ou segurança de uma aplicação concreta.
- Nenhuma conta Cloudflare, dashboard privado, account ID, API token, secret ou endpoint autenticado foi acessado. A REST API foi apenas lida como referência pública; não houve requisição autenticada.
- Nenhum código candidato foi clonado, instalado ou executado. Exemplos TypeScript/JavaScript foram tratados como documentação, não como resultados de teste.
- Os exemplos de D1/R2, webhook, Pages e Twilio demonstram padrões publicados. Eles não estabelecem compatibilidade automática com um projeto Manus LEGO nem autorizam importar código.
- A página de métricas menciona dashboard e exige `accountTag` para GraphQL; esses requisitos foram registrados sem armazenar identificadores privados.
- Valores de limites podem mudar com atualizações da documentação. As páginas foram observadas em 2026-11-20 e devem ser reconsultadas antes de uma decisão de integração.

## References

[1]: https://developers.cloudflare.com/workflows/ "Cloudflare Workflows overview"
[2]: https://developers.cloudflare.com/workflows/llms.txt "Cloudflare Workflows public documentation index"
[3]: https://developers.cloudflare.com/workflows/build/workers-api/ "Cloudflare Workflows Workers API"
[4]: https://developers.cloudflare.com/workflows/build/rules-of-workflows/ "Rules of Workflows"
[5]: https://developers.cloudflare.com/workflows/build/sleeping-and-retrying/ "Sleeping and retrying"
[6]: https://developers.cloudflare.com/workflows/build/events-and-parameters/ "Events and parameters"
[7]: https://developers.cloudflare.com/workflows/reference/limits/ "Cloudflare Workflows limits"
[8]: https://developers.cloudflare.com/workflows/build/trigger-workflows/ "Trigger Workflows"
[9]: https://developers.cloudflare.com/workflows/examples/trigger-from-webhook/ "Trigger a Workflow from a webhook"
[10]: https://developers.cloudflare.com/workflows/build/call-workflows-from-pages/ "Call Workflows from Pages"
[11]: https://developers.cloudflare.com/workflows/examples/backup-d1/ "Export and save D1 database"
[12]: https://developers.cloudflare.com/workflows/examples/twilio/ "Integrate Workflows with Twilio"
[13]: https://developers.cloudflare.com/workflows/observability/metrics-analytics/ "Metrics and analytics"
[14]: https://developers.cloudflare.com/api/resources/workflows/methods/list/ "List all Workflows REST API"
