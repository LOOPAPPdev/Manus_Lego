# Scout 16 — Cloudflare home

- **source_id:** `cloudflare-home`
- **rota de entrada:** https://www.cloudflare.com/
- **provedor/fonte:** Cloudflare official website e documentação pública oficial vinculada pela Cloudflare
- **data da consulta:** 2026-11-20
- **coverage:** `partial`

## Conclusão

A rota pública da Cloudflare apresenta a empresa como uma plataforma para construir, proteger e conectar aplicações, com uma taxonomia pública que agrupa produtos em Compute, Storage, AI, Media, Security, Network e SASE / Zero Trust. A página oficial de produtos lista nomes de produtos e links oficiais; a documentação de desenvolvedores fornece descrições técnicas, guias e referências de API. Essas páginas são evidência de escopo público, documentação e metadados de oferta. Não são, por si só, prova de que um deployment foi executado, que um build passou, que uma propriedade de segurança foi testada ou que um serviço está disponível para uma conta específica.

A cobertura é `partial`, não `complete`: a página de produtos é uma enumeração oficial observada naquele endpoint, mas a exploração não verificou cada página individual, cada plano, cada endpoint da API ou toda a documentação dinâmica. A consulta também não acessou dashboards privados, contas, tokens ou segredos.

## Evidências observadas

### 1. Rota inicial e posicionamento público

A página inicial foi acessada em [cloudflare.com](https://www.cloudflare.com/). O conteúdo público descreve uma plataforma serverless global e associa a oferta a compute, storage, AI e serviços de rede. A mesma página apresenta Workers como plataforma serverless e liga a produtos como Workers, Containers, Durable Objects, Browser Run, Workflows, R2, Hyperdrive, D1, KV, Queues, Workers AI, AI Gateway, Vectorize, Images, Stream, DNS, CDN, WAF, Load Balancing, Rate Limiting e Bot Mitigation. O conteúdo também expõe links públicos para documentação, pricing e cadastro.

Essa evidência sustenta somente posicionamento, nomes e links públicos apresentados pela própria Cloudflare. Não sustenta uma medição independente de latência, cold starts, disponibilidade, escala, segurança ou execução.

### 2. Catálogo público de produtos

A página [Cloudflare Products](https://www.cloudflare.com/products/) apresenta as categorias e os produtos abaixo.

- **Compute:** Browser Run, Cloudflare Pages, Containers, Durable Objects, Email Service, Sandboxes, Workers, Workers for Platforms, Workers Observability e Workflows.
- **Storage:** Artifacts, Basin, Cache Reserve, D1, Hyperdrive, K2, KV, Queues e R2.
- **AI:** Agents, AI Gateway, AI Search, Vectorize, Web3 e Workers AI.
- **Media:** Images, RealtimeKit e Stream.
- **Security:** Bot Management, Client-Side Security, DDoS Protection, Magic Transit, Network Firewall, Rate Limiting, SSL, Turnstile e WAF.
- **Network:** Advanced Certificate Manager, Analytics, API Shield, Argo Smart Routing, CDN, China Network, Custom Domain Protection, DDoS for Web, DNS, Email Routing, Keyless SSL, Load Balancing, Log Explorer, Network Flow, Network Interconnect, Page Shield, RDP, Spectrum, Spectrum for Minecraft, TURN / SFU e Waiting Room.
- **SASE / Zero Trust:** Access, AI Security for Apps, Browser Isolation, CASB, Data Loss Prevention, Email Security, Gateway, Mesh, Secure Web Gateway e WAN.

A página também liga para a documentação oficial `https://developers.cloudflare.com/` e para cadastro público em `https://dash.cloudflare.com/sign-up`. O catálogo é evidência de que esses nomes e categorias são publicados na página naquele momento. A presença na lista não prova maturidade, disponibilidade geográfica, compatibilidade, performance, certificação, segurança efetiva ou estado de produto além do que a página/documentação afirma.

### 3. Documentação pública para desenvolvedores

A [Cloudflare Developer Docs](https://developers.cloudflare.com/) organiza o escopo técnico em primitives de Compute, AI, Storage & Databases e Media. A página documenta, entre outros, Workers, Containers, Durable Objects, Queues, Workers AI, AI Gateway, AI Search, Agents, Vectorize, Browser Run, R2, Basin, K2, D1, KV, Hyperdrive, Images, Stream e Realtime. Também apresenta links para WAF, SSL/TLS, Turnstile, Tunnel, Access, Gateway, DNS, CDN, Cache, Speed, Web Analytics e o diretório de documentação.

A documentação contém exemplos de comandos públicos como `npm create cloudflare@latest my-app`, `cf ai run ...`, `npx wrangler ai models` e `npx wrangler d1 create my-database`. Esses exemplos são documentação de uso e não foram executados nesta exploração. Nenhum pacote ou código de candidato foi instalado ou executado.

O [Docs directory](https://developers.cloudflare.com/directory/) lista grupos como AI, Analytics, Application performance, Application security, Cloudflare One, Core platform, Developer platform, Media, Network security, Privacy e Storage. Entre as entradas observadas estão 1.1.1.1, Access, Agents, AI Gateway, AI Search, API documentation, API Shield, Argo Smart Routing, Artifacts, Basin, Browser Isolation, Browser Run, Cache, Cloudflare CLI, Cloudflare Images, Cloudflare One, Cloudflare Tunnel, Containers, D1, DNS e Durable Objects. O diretório é amplo e dinâmico; a exploração não tratou sua listagem como inventário imutável ou prova de cobertura total.

### 4. Workers: documentação técnica versus prova de execução

A página [Cloudflare Workers docs](https://developers.cloudflare.com/workers/) descreve Workers como plataforma serverless para construir, publicar e escalar aplicações na rede global da Cloudflare. A documentação liga frameworks como React, Vue, Svelte, Next, Astro e React Router; linguagens como JavaScript, TypeScript, Python e Rust; observabilidade; static assets; CDN/cache; Smart Placement; cron jobs; Workflows; Queues; bindings; Durable Objects; D1; KV; Hyperdrive; Workers AI; Vectorize; R2; Browser Run e Images.

Isso comprova que as capacidades estão documentadas publicamente e que existem guias e links oficiais para elas. Não comprova que um app específico foi publicado, que uma função rodou com os resultados esperados, que uma métrica de escala foi atingida ou que um teste de integração/build foi concluído. Também não foi registrada uma branch, commit/SHA ou caminho relativo de repositório porque essa exploração foi limitada à fonte web oficial solicitada; não houve inspeção de um repositório de código como evidência desta fonte.

### 5. API pública

A [API Reference](https://developers.cloudflare.com/api/) expõe uma referência pública com bibliotecas TypeScript, Python, Go e Terraform, links para repositórios públicos e operações documentadas para contas, membros, tokens, Pages, assets e Registrar. A própria documentação informa pré-requisitos de conta Cloudflare, perfil de billing e autenticação por API token ou API key para operações que exigem autorização.

A existência de uma referência pública e de rotas documentadas é evidência de documentação de API. Não foi feita chamada autenticada nem tentativa de manipular recursos. Portanto, não há prova de autorização, execução, resposta de endpoint, sucesso de operação, estado de conta ou configuração de segurança.

### 6. Pages e preços públicos

A página [Cloudflare Pages](https://www.cloudflare.com/products/pages/) classifica Pages como oferta de compute dentro da plataforma Workers e aponta para a documentação completa em `https://developers.cloudflare.com/pages/`. Isso confirma o posicionamento e o link oficial, mas não prova deploy.

A página [Pricing](https://www.cloudflare.com/plans/) organiza preços em Compute & Storage, Network & CDN e SASE / Zero Trust. Foram observadas referências públicas para Workers, Containers, Durable Objects, Browser Rendering, Workflows, R2, Workers KV, D1, Queues, Hyperdrive, Basin, TURN / SFU, Images, Stream, Vectorize, Workers AI e observabilidade. Valores, limites e disponibilidade comercial podem mudar; neste relatório eles são tratados como metadados observados na página, não como garantia contratual ou medição de consumo.

## Registros realmente verificados

1. `https://www.cloudflare.com/` — página pública inicial acessível; posiciona Cloudflare como plataforma global/serverless e fornece links de produtos e documentação.
2. `https://www.cloudflare.com/products/` — catálogo público acessível; categorias e nomes acima foram observados no conteúdo da página.
3. `https://developers.cloudflare.com/` — documentação oficial acessível; seções públicas de Compute, AI, Storage & Databases, Media, segurança e performance foram observadas.
4. `https://developers.cloudflare.com/directory/` — diretório público acessível; grupos e entradas de produtos foram observados.
5. `https://developers.cloudflare.com/workers/` — documentação pública acessível; frameworks, linguagens, bindings, observabilidade e integrações foram observados.
6. `https://developers.cloudflare.com/api/` — referência pública acessível; bibliotecas, operações e requisitos de autenticação foram observados.
7. `https://www.cloudflare.com/products/pages/` — página pública acessível; Pages foi observado como oferta de compute ligada à documentação.
8. `https://www.cloudflare.com/plans/` — página pública acessível; estrutura de preços e referências de serviços foram observadas.
9. Não foi observado, nesta fonte, um repositório, caminho relativo, branch ou commit/SHA que devesse ser registrado. Nenhum desses campos foi inventado.

## Limitações e separação de evidência

- A fonte foi limitada às páginas públicas oficiais Cloudflare e documentação oficial vinculada. Não foram usados blogs de terceiros, dashboards privados, contas, tokens, segredos ou endpoints privados.
- Marketing, descrições de produto, listas de recursos e tabelas de preço foram tratados como afirmações/metadados da própria Cloudflare. Eles não equivalem a prova independente de execução, disponibilidade, build, segurança, compliance, performance ou runtime.
- Exemplos de CLI e API foram apenas lidos. Não houve instalação de dependências, execução de código, deploy, chamada autenticada, criação de recurso ou teste de integração.
- A documentação e o catálogo são extensos e sujeitos a mudanças. Não foi possível demonstrar cobertura completa de cada produto, subproduto, endpoint, região, plano ou página vinculada.
- A página de API inclui referências a operações que requerem conta e autenticação; nenhuma autorização foi presumida.
- Não foram encontrados, nem procurados em áreas privadas, identificadores de conta, URLs privadas, tokens ou credenciais.
- Por não haver evidência de runtime ou de um repositório específico nesta exploração, não há status `enriched` ou `verified runtime` a atribuir a qualquer implementação.

## References

[1]: https://www.cloudflare.com/ "Cloudflare official home page"
[2]: https://www.cloudflare.com/products/ "Cloudflare Products"
[3]: https://developers.cloudflare.com/ "Cloudflare Developer Docs"
[4]: https://developers.cloudflare.com/directory/ "Cloudflare Docs directory"
[5]: https://developers.cloudflare.com/workers/ "Cloudflare Workers documentation"
[6]: https://developers.cloudflare.com/api/ "Cloudflare API Reference"
[7]: https://www.cloudflare.com/products/pages/ "Cloudflare Pages product page"
[8]: https://www.cloudflare.com/plans/ "Cloudflare pricing"
