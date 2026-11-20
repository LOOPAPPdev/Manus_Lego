# Scout 20 — Cloudflare Remote MCP

## Escopo e conclusão

A rota de entrada é a documentação pública da Cloudflare para construir um servidor MCP remoto: `https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/`. A documentação descreve servidores remotos em Workers usando Streamable HTTP, com opção sem autenticação ou com OAuth e autorização por escopos. A cobertura deste scout é **partial**: a documentação e os metadados públicos consultados sustentam os registros abaixo, mas não constituem inventário exaustivo da plataforma nem prova de execução, build, deployment, segurança efetiva ou runtime.

Nenhum token, dashboard privado, conta ou segredo foi acessado. Nenhum repositório foi clonado, instalado ou executado.

## Evidência documental

A documentação de construção diz que o caminho recomendado usa `createMcpHandler` do Agents SDK com uma fábrica de `McpServer`. O handler é stateless: cada requisição cria um servidor novo; portanto, dados que sobrevivem à requisição devem ficar em uma binding como KV, D1 ou Durable Object. O endpoint de exemplo é `/mcp` e o transporte remoto documentado é Streamable HTTP. [1]

A mesma rota oferece dois modelos: servidor público sem login, ou autenticação/autorização. No modelo autenticado, a Cloudflare documenta um authorization server Worker com `OAuthAuthorizationServer` e um MCP resource server com `OAuthResourceServer` envolvendo `createMcpHandler`. O cliente descobre o authorization server a partir de uma resposta `401`, completa o login e reenvia a requisição com token. As ferramentas podem obter o contexto do usuário por `getMcpAuthContext()`. [1]

A página de autorização afirma que o MCP usa um subconjunto de OAuth 2.1. O authorization server emite tokens e o resource server valida esses tokens por Service Binding. A documentação registra os endpoints conceituais `/authorize` e `/oauth/token`, além de descoberta, registro de cliente e PKCE; o código de exemplo também declara escopos como `mcp:read`, `mcp:write` e `offline_access`. Esses são elementos do desenho documentado, não observação de um serviço implantado. [2]

A documentação de segurança exige que a página de consentimento mostre nome do cliente, escopos e hostname para o qual os tokens serão enviados. Ela descreve `describeConsent`, `beginConsent`, `approveConsent`, `denyConsent` e `isConsentRemembered`, além de proteção contra framing e uso de cookie `__Host-`. Também alerta que strings fornecidas pelo cliente devem ser escapadas ao renderizar HTML. [3]

Ferramentas são registradas em `McpServer` com `server.registerTool()`. A documentação requer nome, descrição, schema de entrada e handler; mostra Zod/Valibot para validação e `content` como retorno. `outputSchema` e `structuredContent` são documentados como opção para resultados estruturados. `isError: true` sinaliza falha de ferramenta ao cliente/LLM. A própria documentação recomenda descrições específicas e honestas sobre limitações. [4]

## Limites e semântica documentados

O handler stateless documentado tem estes defaults/opções observáveis: `route` padrão `/mcp`; CORS wildcard por padrão; `legacy` padrão `"stateless"`; `responseMode` padrão `"auto"`; `maxSubscriptions` padrão **1.024** streams de listen concorrentes; e `keepAliveMs` padrão **15.000 ms**. Esses valores são limites/opções do handler documentado, não medições independentes. [5]

A documentação declara que a compatibilidade legada stateless não é uma sessão completa: cada POST cria novo servidor e transporte; GET e DELETE HTTP retornam `405`; não há MCP session ID persistente; pushed elicitation, sampling e roots falham imediatamente; streams autônomos, retomada, replay e exclusão de sessão não estão disponíveis; e tarefas experimentais publicadas não são suportadas nesse caminho. [5]

Também é documentado que o handler valida cada `Origin` de navegador presente e rejeita Origins malformadas, opacas ou não HTTP com `403`; clientes MCP sem Origin continuam válidos. Para domínio customizado, os allowlists `allowedHostnames` e `allowedOriginHostnames` devem ser definidos explicitamente. CORS não é autenticação; OAuth ou outra camada deve proteger o endpoint. [5]

O transporte remoto recomendado é Streamable HTTP. SSE é descrito como anteriormente usado para conexões remotas, mas depreciado em favor de Streamable HTTP; `createMcpHandler` serve somente Streamable HTTP. A documentação de teste informa ainda que conexões remotas autorizadas são uma parte em evolução da especificação MCP e que nem todos os clientes suportam conexões remotas. [6] [7]

Não foi encontrada, nas páginas públicas consultadas dentro deste escopo, uma cota global de requisições, limite de tamanho de payload, SLA ou limite de duração específico do serviço “remote MCP”. Portanto, nenhum desses valores é afirmado aqui. O limite de aproximadamente 6.000 tokens encontrado na documentação de Code Mode é específico do publisher de respostas do Code Mode, não deve ser atribuído genericamente a todo servidor remote MCP. [8]

## Registros públicos realmente verificados

### Registro documental

- **Provider:** Cloudflare Developers.
- **Rota de entrada:** `https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/`.
- **Capacidade documentada:** construir e implantar um servidor MCP remoto em Workers com Streamable HTTP, sem autenticação ou com OAuth/autorização.
- **Ferramentas documentadas:** `McpServer.registerTool`, schemas de entrada/saída, `content`, `structuredContent` e `isError`.
- **OAuth documentado:** `OAuthAuthorizationServer`, `OAuthResourceServer`, `validateToken` por Service Binding, resource metadata, PKCE, consentimento e escopos.
- **Estado documentado:** handler stateless; persistência entre requisições deve usar KV, D1, Durable Object ou outra binding apropriada.
- **Limites documentados:** defaults e restrições listados na seção anterior.
- **Status de prova:** documentação pública; não é prova de runtime, deployment ou segurança operacional.

### Registro de repositório público

Foi observada a página pública do repositório `cloudflare/ai`, branch `main`, no caminho relativo `demos/remote-mcp-authless`. A página lista `src/`, `README.md`, `package.json`, `wrangler.jsonc` e demais arquivos do exemplo authless. [9]

A API pública do GitHub retornou para `main` o commit/SHA observado `34a8f4c00c0871883215a7114e9a7f3e7747ee1b`. No mesmo commit, o arquivo `demos/remote-mcp-authless/src/index.ts` foi observado com blob SHA `38068594da345eccb5f57c887258a4df27496f28`; `demos/remote-mcp-authless/package.json` foi observado com blob SHA `45e1d3c1a92f62eef434da85358512bdd1489a91`. [10] [11]

O README público do exemplo descreve um servidor remoto stateless sem autenticação, com endpoint de formato `...workers.dev/mcp`, personalização de ferramentas em `src/index.ts` via `server.registerTool(...)` e conexão por AI Playground ou clientes compatíveis. Isso é metadata/documentação do exemplo. Não foi feita execução, instalação de dependências, build, deployment, inspeção de comportamento HTTP ou chamada de ferramenta. [9]

A API pública do GitHub identificou o arquivo de licença do repositório como **MIT License**, SPDX `MIT`, com blob SHA `728fb8923413d23dd588873a85371b229df8887c` na referência `main`. A observação vale para o repositório, não constitui uma análise de compatibilidade de dependências nem autorização para copiar código. [12]

## Limitações e classificação

- **Coverage:** `partial`. A amostra cobre a rota canônica e páginas diretamente relacionadas a transporte, handler, ferramentas, autorização, segurança e teste, além de um exemplo público. Não sustenta cobertura completa de todos os produtos Cloudflare, todos os clientes MCP, todas as quotas da plataforma ou todo o histórico do repositório.
- As páginas de autorização, segurança, ferramentas e handler foram retornadas parcialmente pelo extrator em alguns casos; as afirmações usadas acima estão limitadas ao conteúdo visível retornado e às páginas Markdown públicas indicadas pela própria documentação.
- A presença de código e comandos na documentação não foi tratada como prova de execução. Não houve `npm`, `pnpm`, `wrangler`, clone, build, teste, deployment, inspector, AI Playground ou chamada MCP.
- Não foi verificado runtime do exemplo, disponibilidade de URL `workers.dev`, latência, throughput, quotas de conta, comportamento de tokens, integração com IdP ou eficácia de controles de segurança.
- O SHA do repositório foi observado via API pública para `main` no momento da consulta; não é uma garantia de imutabilidade futura do branch. Os caminhos e blob SHAs acima são os valores efetivamente retornados pela API.
- Não foram armazenados tokens, identificadores de conta Cloudflare, URLs privadas ou credenciais.

## References

[1]: https://developers.cloudflare.com/agents/model-context-protocol/guides/remote-mcp-server/ "Build a Remote MCP server"
[2]: https://developers.cloudflare.com/agents/model-context-protocol/protocol/authorization/ "Authorization"
[3]: https://developers.cloudflare.com/agents/model-context-protocol/guides/securing-mcp-server/ "Securing MCP servers"
[4]: https://developers.cloudflare.com/agents/model-context-protocol/protocol/tools/ "Tools"
[5]: https://developers.cloudflare.com/agents/model-context-protocol/apis/handler-api/ "MCP Server handler API"
[6]: https://developers.cloudflare.com/agents/model-context-protocol/protocol/transport/ "Transport"
[7]: https://developers.cloudflare.com/agents/model-context-protocol/guides/test-remote-mcp-server/ "Test a Remote MCP Server"
[8]: https://developers.cloudflare.com/agents/model-context-protocol/guides/build-codemode-mcp-server/ "Build a Code Mode MCP server"
[9]: https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless "cloudflare/ai remote-mcp-authless example"
[10]: https://api.github.com/repos/cloudflare/ai/commits/main "GitHub API commit metadata for cloudflare/ai main"
[11]: https://api.github.com/repos/cloudflare/ai/contents/demos/remote-mcp-authless/src?ref=34a8f4c00c0871883215a7114e9a7f3e7747ee1b "GitHub API source directory metadata"
[12]: https://api.github.com/repos/cloudflare/ai/license "GitHub API license metadata"
