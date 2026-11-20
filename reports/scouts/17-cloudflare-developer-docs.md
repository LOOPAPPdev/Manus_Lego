# Scout 17 — Cloudflare Developer Docs

**Fonte:** Cloudflare Developer Docs  
**Rota de entrada:** https://developers.cloudflare.com/  
**Data da observação:** 2026-11-20  
**Cobertura:** `partial`

## Escopo observado

A rota de entrada apresenta a documentação pública da Cloudflare como um portal de guias, tutoriais, referências e recursos para construir na plataforma. A navegação renderizada separa áreas de início, recursos, ferramentas de desenvolvimento, API & IaC, suporte, construção, proteção/conectividade e observabilidade. Entre os links observados estão `API`, `Directory`, `SDKs`, `Changelog`, `Terraform`, `Pulumi`, `Cloudflare CLI` e diversos produtos. [1]

A página inicial também agrupa produtos em categorias visíveis de alto nível. Foram observados, entre outros, Compute (Workers, Containers, Durable Objects, Queues, Workflows, Browser Run), AI (Workers AI, AI Gateway, Agents, Vectorize, AI Search), Storage & Database (R2, D1, KV, Hyperdrive), Media (Images, Stream, Realtime), Application Security (WAF, SSL/TLS, API Shield, Turnstile), Cloudflare One, Domains & DNS, Networking e Delivery & Performance. Essa é uma amostra da navegação pública da entrada; não é uma afirmação de que todos os produtos ou todas as páginas foram inventariados. [1]

## Índice e navegação de produtos

O arquivo público `https://developers.cloudflare.com/llms.txt` é apresentado pela própria documentação como um índice de documentação. Ele informa que cada produto listado possui seu próprio `llms.txt`, contendo o índice completo das páginas daquele produto e recomendado para exploração específica. O índice observado organiza links por grupos como Application performance, Application security, Cloudflare One, Consumer services, Core platform, Network security, Other e Docs collections. [2]

A página pública Directory fornece filtros por grupo e expõe uma listagem de áreas/produtos com nome, descrição curta e URL. Os grupos observados incluem AI, Analytics, Application performance, Application security, Cloudflare One, Consumer services, Core platform, Developer platform, Docs collections, Media, Network security, Privacy e Storage. A extração retornada mostrou entradas como 1.1.1.1, Access, Account, Agent Memory, Agents, AI, AI Gateway, AI Search, Analytics, API documentation, API Shield e Argo Smart Routing, entre outras. Como a página é uma listagem dinâmica e a extração consultada foi apenas uma seleção, ela serve como evidência de estrutura e descoberta, não como inventário exaustivo. [3]

## APIs públicas e organização da referência

A página `https://developers.cloudflare.com/api/` é uma referência pública extensa. Sua navegação organiza recursos por grupos, incluindo Account & User Management, AI, Certificate Management, Cloudflare One, Data Localization Suite, DNS, Domain/Zone Management, IP Addresses, Media, Networking, Observability, Radar, Routing & Performance, Rules, Security, Storage & Databases, Threat Intelligence e Workers & Pages. Também há recursos avulsos como AutoRAG, Connectivity, Monetization, Organizations, Resource Tagging, Tenants e Zaraz. [4]

A referência apresenta métodos e caminhos de endpoint em páginas de recursos. Foram observados, como exemplos públicos, `GET /accounts`, `GET /zones`, operações de tokens de usuário e conta, endpoints de Pages e recursos de Registrar. Esses caminhos são documentação de interface; não foram chamados durante este scout e não constituem prova de disponibilidade, autorização, sucesso de resposta ou funcionamento em runtime. [4]

A página de visão geral da API afirma que o uso da API requer autenticação e orienta o uso de API tokens, mencionando API keys como alternativa com limitações. Também direciona para Terraform e SDKs oficiais. [5] A página de criação de token descreve permissões, escopos de conta/usuário/zona, expiração e filtragem por IP, e mostra um comando de verificação com placeholder `<API_TOKEN>`. Nenhuma conta, token, dashboard autenticado ou segredo foi acessado. [6]

## SDKs e IaC

A documentação pública de SDKs afirma oferecer SDKs para Go, TypeScript e Python, além de exemplos com `curl`, e aponta para os repositórios públicos correspondentes: `cloudflare/cloudflare-go`, `cloudflare/cloudflare-typescript` e `cloudflare/cloudflare-python`. Esses links foram observados na página de SDKs. Não foram clonados, instalados, executados ou auditados repositórios candidatos. Nenhum branch ou commit/SHA foi observado neste scout, portanto nenhum foi registrado. [7]

A rota de entrada também expõe links públicos para Terraform e Pulumi em API & IaC. A presença desses links comprova a navegação pública para documentação de infraestrutura como código, mas não comprova compatibilidade de uma configuração específica, build, execução ou integração. [1] [5]

## Limites documentados

A página pública de rate limits documenta os seguintes limites de API: Client API por usuário/conta/token de `1200/5 minutes`; Client API por IP de `200/second`; GraphQL variável por custo de consulta com máximo de `320/5 min`; 50 tokens de usuário por usuário; e 500 tokens de conta por conta. A mesma página afirma que o limite global de 1.200 requisições por cinco minutos é cumulativo, independentemente de a requisição vir do dashboard, API key ou API token. Ao exceder esse limite, chamadas de API ficam bloqueadas pelos cinco minutos seguintes e recebem HTTP 429. [8]

A documentação também descreve os cabeçalhos `Ratelimit`, `Ratelimit-Policy` e `retry-after`, e aponta limites específicos em páginas separadas para Cache Purge, GraphQL, Rulesets, Lists e Gateway Lists. Esses limites são documentação operacional pública; não foram testados por chamadas autenticadas ou por carga. [8]

## Registros verificáveis

- **Página pública:** Cloudflare Developer Docs, `https://developers.cloudflare.com/`; estrutura de navegação e links de produtos observados. [1]
- **Índice público:** `https://developers.cloudflare.com/llms.txt`; afirmação observada de que cada produto possui índice próprio `llms.txt`. [2]
- **Diretório público:** `https://developers.cloudflare.com/directory/`; filtros de grupo e entradas de produto observadas. [3]
- **Referência de API:** `https://developers.cloudflare.com/api/`; grupos de recursos e métodos/caminhos documentados observados. [4]
- **Visão geral da API:** `https://developers.cloudflare.com/api/`; autenticação requerida e orientação para tokens observadas. [5]
- **SDKs:** `https://developers.cloudflare.com/fundamentals/api/reference/sdks/`; Go, TypeScript e Python observados, com links para os repositórios públicos correspondentes. [7]
- **Limites:** `https://developers.cloudflare.com/fundamentals/api/reference/limits/`; quotas, bloqueio HTTP 429, cabeçalhos e links para limites específicos observados. [8]
- **Metadados temporais observados:** a página de Workers informa atualização em 2026-10-08; a página de SDKs informa atualização em 2026-04-20; a página de limites informa atualização em 2026-08-25; a página de criação de token informa atualização em 2026-11-06. Esses metadados não são prova de execução. [9] [7] [8] [6]

## O que não foi verificado

Não foi verificada a totalidade das páginas do domínio, a totalidade de cada `llms.txt` de produto, a completude do diretório, a completude da referência de API, a correspondência entre todos os links da navegação e páginas acessíveis, nem a paridade entre documentação e APIs realmente disponíveis. O relatório usa páginas públicas representativas e não assume exaustividade.

Não houve acesso a dashboards privados, contas, tokens, APIs autenticadas ou segredos. Nenhuma chamada de API Cloudflare foi executada. Portanto não há evidência de HTTP 2xx, autenticação bem-sucedida, build, runtime, deploy, segurança efetiva, latência, quotas reais em uma conta, ou funcionamento dos exemplos.

Não foi observado repositório de origem da documentação, branch ou commit/SHA nas páginas consultadas. Consequentemente, não há registro de branch/SHA a atribuir à fonte web. Os repositórios de SDK apenas foram apontados por links públicos na documentação; não foram inspecionados.

## Conclusão

A fonte é verificável como portal público de documentação da Cloudflare com navegação de produtos, índice por produto, referência de API, SDKs e limites documentados. Ela é adequada para descoberta e referência estática, mas a evidência coletada não sustenta cobertura `complete` da documentação nem qualquer afirmação de execução ou funcionamento de runtime. A classificação correta para este scout é `partial`.

## References

[1]: https://developers.cloudflare.com/ "Cloudflare Developer Docs"
[2]: https://developers.cloudflare.com/llms.txt "Cloudflare Developer Documentation index"
[3]: https://developers.cloudflare.com/directory/ "Cloudflare Docs directory"
[4]: https://developers.cloudflare.com/api/ "Cloudflare API Reference"
[5]: https://developers.cloudflare.com/api/overview/ "Cloudflare API overview"
[6]: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/ "Create API token"
[7]: https://developers.cloudflare.com/fundamentals/api/reference/sdks/ "Cloudflare API SDKs"
[8]: https://developers.cloudflare.com/fundamentals/api/reference/limits/ "Cloudflare API rate limits"
[9]: https://developers.cloudflare.com/workers/ "Cloudflare Workers documentation"
