# Scout — Vercel backend

**Rota:** `https://vercel.com/templates/backend`  
**Tipo:** public Vercel category route  
**Data da observação:** 2026-11-20  
**Cobertura:** `partial`

A rota pública respondeu com o título “Backend templates and examples” e 34 cartões de templates na representação HTML/Markdown pública obtida. A própria página não expôs controles de paginação na resposta observada. A variante `https://vercel.com/templates/backend?page=2` retornou o mesmo conjunto e não demonstrou uma segunda página; isso é evidência de que o parâmetro não alterou o conteúdo observado, não prova de que a galeria seja finita ou de que não existam outros itens. A página geral `https://vercel.com/templates/page/2` existe e lista templates de outra página da galeria, mas não oferece um inventário completo específico da categoria backend.

A lista observada na categoria foi: Express on Bun; Hono on Bun; Python Queue Subscribers Starter; Express.js on Vercel; Hono + AI SDK; Hono and Next.js Starter; Rust Wait Until; Hono MCP remote server; xmcp boilerplate; Nitro - Cached HTTP handler; Go API Starter; Fastify on Vercel; Go Gin Hello World; HyperFrames on Vercel; Claude Managed Agents with Chat SDK; Hono on Vercel; Nitro - Plugins; Nitro Starter; Nitro - Route Rules; eve with Vercel Drives; Next.js Convex Template; Node.js Serverless Function; Elysia on Vercel; Starlette Starter; Express + AI SDK; NestJS on Vercel; eve Data Analyst; AI SDK with Flask; Remotion on Vercel; Stark Industries HQ - Agentic Email Assistants; Flask Hello World; SaaS Microservices; Python Celery Starter; eve Agent with Python. A contagem acima é 34, pois a resposta pública observada contém 34 links; portanto, o número confiável para este snapshot é **34 entradas**. [1]

## Registros com fonte e commit verificáveis

Os registros abaixo foram conferidos na página pública individual da Vercel e no endpoint público de commits do GitHub. O SHA é o commit mais recente retornado para o caminho consultado no momento da coleta; ele fixa o estado do diretório, mas não constitui teste de build, deploy ou runtime.

- **Express on Bun** — Vercel: `https://vercel.com/templates/express/express-on-bun`; repositório `https://github.com/vercel/examples`; caminho relativo `framework-boilerplates/express-bun`; SHA `36bd4c68429db33f88a8779dd5d365fb75b07626`; commit `https://github.com/vercel/examples/commit/36bd4c68429db33f88a8779dd5d365fb75b07626`. A página individual expõe o link de repositório e um demo público. [2] [12]
- **Hono on Bun** — Vercel: `https://vercel.com/templates/hono/hono-on-bun`; repositório `https://github.com/vercel/examples`; caminho `framework-boilerplates/hono-bun`; SHA `36bd4c68429db33f88a8779dd5d365fb75b07626`; commit `https://github.com/vercel/examples/commit/36bd4c68429db33f88a8779dd5d365fb75b07626`. [3] [12]
- **Python Queue Subscribers Starter** — Vercel: `https://vercel.com/templates/python/python-queue-subscribers-starter`; repositório `https://github.com/vercel/examples`; caminho `python/queue-subscribers`; SHA `9c3684689cf9651dd8befacb9d1e8743e02bbf74`; commit `https://github.com/vercel/examples/commit/9c3684689cf9651dd8befacb9d1e8743e02bbf74`. [4] [12]
- **Express.js on Vercel** — Vercel: `https://vercel.com/templates/other/express-js-on-vercel`; repositório `https://github.com/vercel/examples`; caminho `solutions/express`; SHA `bd574c126457282b99b3625b1cb37675d5429b03`; commit `https://github.com/vercel/examples/commit/bd574c126457282b99b3625b1cb37675d5429b03`. [5] [12]
- **Hono on Vercel** — Vercel: `https://vercel.com/templates/hono/hono-on-vercel`; repositório `https://github.com/vercel/examples`; caminho `framework-boilerplates/hono`; SHA `61378c659fffe9ce8d9678513f2752c4302bd2af`; commit `https://github.com/vercel/examples/commit/61378c659fffe9ce8d9678513f2752c4302bd2af`. [6] [12]
- **Go API Starter** — Vercel: `https://vercel.com/templates/go/go-api-starter`; a página aponta `https://github.com/vercel/examples/tree/main/go/api`; caminho `go/api`; SHA `f0bb27b59f8c3554789fa6d36e944d616866dec8`; commit `https://github.com/vercel/examples/commit/f0bb27b59f8c3554789fa6d36e944d616866dec8`. A descrição da página também contém uma referência histórica alternativa a `vercel/vercel/examples/go-api`; essa alternativa não produziu commits no endpoint consultado e não foi usada como registro confirmado. [7] [12]
- **Starlette Starter** — Vercel: `https://vercel.com/templates/python/starlette-starter`; repositório `https://github.com/vercel/examples`; caminho `python/starlette`; SHA `11bdb298f578d9543c3d4ea029fd6715cab1ee03`; commit `https://github.com/vercel/examples/commit/11bdb298f578d9543c3d4ea029fd6715cab1ee03`. A página mostra owner, repositório, caso de uso Backend e licença MIT do monorepo. [8] [12]
- **NestJS on Vercel** — Vercel: `https://vercel.com/templates/other/nestjs-on-vercel`; repositório `https://github.com/vercel/vercel`; caminho `examples/nestjs`; SHA `8b3d46ac62a0c46c6040016cbc8e7c7412d565ff`; commit `https://github.com/vercel/vercel/commit/8b3d46ac62a0c46c6040016cbc8e7c7412d565ff`. [9] [12]
- **Nitro Starter** — Vercel: `https://vercel.com/templates/nitro/nitro-starter`; repositório `https://github.com/vercel/examples`; caminho `framework-boilerplates/nitro`; SHA `36a2f3b6662fd7cd9fec80aeaba4ebc672519a3a`; commit `https://github.com/vercel/examples/commit/36a2f3b6662fd7cd9fec80aeaba4ebc672519a3a`. [10] [13]
- **Fastify on Vercel** — Vercel: `https://vercel.com/templates/other/fastify-on-vercel`; repositório `https://github.com/vercel/vercel`; caminho `examples/fastify`; SHA `6e280306bfeeeaab248f06e52882abd8c2ee2001`; commit `https://github.com/vercel/vercel/commit/6e280306bfeeeaab248f06e52882abd8c2ee2001`. [11] [13]

## Evidência sobre a fonte oficial

O repositório `vercel/examples` é público, tem branch padrão `main`, licença MIT declarada na página do GitHub e documenta que exemplos com front matter podem virar templates da galeria. A própria documentação do repositório diz que a galeria inclui exemplos e que nem todos os templates são necessariamente apenas diretórios desse monorepo; por isso a descoberta da categoria e a resolução da fonte devem permanecer separadas. [12]

A rota observada inclui também entradas apontando para `vercel/vercel`, além de `vercel/examples`, e várias entradas com namespaces de rota distintos (`express`, `hono`, `python`, `nitro`, `other`, `next.js`, `eve`). Isso confirma que o slug da categoria backend é uma classificação de galeria, não um prefixo de URL que determine o caminho do código-fonte.

## Limitações e status de evidência

- A coleta é um snapshot de conteúdo público renderizado. Não há garantia de exaustividade da galeria, especialmente porque a documentação local alerta que a galeria é dinâmica e pode paginar/renderizar conteúdo de forma incompleta. Portanto, `coverage=partial`, nunca `complete`.
- A resposta pública da categoria lista links e descrições, mas não fornece um inventário completo de SHAs, árvores ou licenças por item. Apenas os dez registros acima foram elevados a “verificados” porque tiveram página individual com caminho GitHub e commit consultável.
- Os outros itens observados permanecem como descobertos, não verificados: Hono + AI SDK; Hono and Next.js Starter; Rust Wait Until; Hono MCP remote server; xmcp boilerplate; Nitro - Cached HTTP handler; Go Gin Hello World; HyperFrames on Vercel; Claude Managed Agents with Chat SDK; Nitro - Plugins; Nitro - Route Rules; eve with Vercel Drives; Next.js Convex Template; Node.js Serverless Function; Elysia on Vercel; Express + AI SDK; eve Data Analyst; AI SDK with Flask; Remotion on Vercel; Stark Industries HQ - Agentic Email Assistants; Flask Hello World; SaaS Microservices; Python Celery Starter; eve Agent with Python.
- A existência de demos e comandos nos READMEs/páginas não foi tratada como prova de funcionamento em runtime. Nenhum projeto candidato foi clonado, instalado, executado ou implantado.
- O sitemap público foi grande e retornou truncado na leitura disponível; não foi usado para alegar cobertura completa nem como substituto de um inventário específico da categoria. [14]
- Não foram acessados dashboards privados, credenciais, tokens ou URLs privadas.

## References

[1]: https://vercel.com/templates/backend "Vercel Backend templates and examples"
[2]: https://vercel.com/templates/express/express-on-bun "Vercel Express on Bun template"
[3]: https://vercel.com/templates/hono/hono-on-bun "Vercel Hono on Bun template"
[4]: https://vercel.com/templates/python/python-queue-subscribers-starter "Vercel Python Queue Subscribers Starter template"
[5]: https://vercel.com/templates/other/express-js-on-vercel "Vercel Express.js on Vercel template"
[6]: https://vercel.com/templates/hono/hono-on-vercel "Vercel Hono on Vercel template"
[7]: https://vercel.com/templates/go/go-api-starter "Vercel Go API Starter template"
[8]: https://vercel.com/templates/python/starlette-starter "Vercel Starlette Starter template"
[9]: https://vercel.com/templates/other/nestjs-on-vercel "Vercel NestJS on Vercel template"
[10]: https://vercel.com/templates/nitro/nitro-starter "Vercel Nitro Starter template"
[11]: https://vercel.com/templates/other/fastify-on-vercel "Vercel Fastify on Vercel template"
[12]: https://github.com/vercel/examples "Vercel examples repository"
[13]: https://github.com/vercel/vercel "Vercel monorepo"
[14]: https://vercel.com/sitemap.xml "Vercel public sitemap"
