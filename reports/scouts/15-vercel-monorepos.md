# Scout Vercel — categoria pública Monorepos

**Rota:** https://vercel.com/templates/monorepos  
**Data da observação:** 2026-11-20  07:17–07:18 (-03:00)  
**Coverage:** `partial`

A página pública da categoria renderizada no momento da consulta enumerou 15 entradas visíveis. Essa enumeração é observável e reproduzível pela própria página, mas não é tratada como completa: o projeto documenta que a galeria Vercel pode ser dinâmica/paginada e não há garantia de uma API pública exaustiva. O sitemap público consultado também foi retornado truncado pelo mecanismo de leitura; portanto, não serve como prova de completude.[1] [2]

Os registros abaixo preservam a URL da página Vercel, o repositório público e o caminho relativo indicados pela própria página. O SHA é o commit observado no branch público `main` (ou `canary` quando explicitamente indicado) pela API do GitHub na mesma exploração. A licença só é informada quando a API do repositório confirmou SPDX `MIT`. Nenhum demo, README, metadado de galeria ou link de deploy foi usado como prova de funcionamento em runtime.

## Registros observados

1. **Monorepo with Nx** — página: https://vercel.com/templates/next.js/monorepo-nx. Origem: `vercel/examples`, caminho `solutions/nx-monorepo`, commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8` (branch `main`), licença MIT confirmada pelo repositório.[3] [18]
2. **Next.js + FastAPI Starter** — página: https://vercel.com/templates/fast-api/next-js-fastapi-starter. Origem: `vercel/examples`, caminho `python/nextjs-fastapi`, commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`, licença MIT confirmada.[4] [18]
3. **Next.js + FastAPI + Bindings Starter** — página: https://vercel.com/templates/next.js/next-js-fastapi-bindings-starter. Origem: `vercel/examples`, caminho `python/nextjs-fastapi-bindings`, commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`, licença MIT confirmada.[5] [18]
4. **Next.js + Gin Starter** — página: https://vercel.com/templates/next.js/next-js-gin-starter. Origem: `vercel/examples`, caminho `go/nextjs-go`, commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`, licença MIT confirmada.[6] [18]
5. **Design System with Turborepo** — página: https://vercel.com/templates/react/turborepo-design-system. Origem: `vercel/turborepo`, caminho `examples/design-system`, commit `99233190d0dd77d9ae6ea897297a5adc20244ef6` (branch `main`), licença MIT confirmada pelo repositório.[7] [19]
6. **Turborepo & SvelteKit Starter** — página: https://vercel.com/templates/svelte/turborepo-sveltekit-starter. Origem: `vercel/turborepo`, caminho `examples/with-svelte`, commit `99233190d0dd77d9ae6ea897297a5adc20244ef6`, licença MIT confirmada.[8] [19]
7. **Turborepo + Hono** — página: https://vercel.com/templates/hono/turborepo-with-hono. Origem: `vercel/examples`, caminho `starter/turborepo-with-hono`, commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`, licença MIT confirmada.[9] [18]
8. **Turborepo & Gatsby Starter** — página: https://vercel.com/templates/gatsby/turborepo-gatsby-starter. Origem: `vercel/turborepo`, caminho `examples/with-gatsby`, commit `99233190d0dd77d9ae6ea897297a5adc20244ef6`, licença MIT confirmada.[10] [19]
9. **Turborepo & Next.js Starter** — página: https://vercel.com/templates/next.js/turborepo-next-basic. Origem: `vercel/turborepo`, caminho `examples/basic`, commit `99233190d0dd77d9ae6ea897297a5adc20244ef6`, licença MIT confirmada.[11] [19]
10. **Vite + FastAPI Starter** — página: https://vercel.com/templates/react/vite-fastapi-starter. Origem: `vercel/examples`, caminho `python/vite-fastapi`, commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`, licença MIT confirmada.[12] [18]
11. **next-forge** — página: https://vercel.com/templates/next.js/next-forge. Origem: `haydenbleasel/next-forge` (a API identifica o repositório como `vercel/next-forge`), caminho relativo `.`, commit `f189de79ceef7c1ef69f61f12e272f99b4cdb699` (branch `main`), licença MIT confirmada.[13] [20]
12. **Monorepo with Turborepo** — página: https://vercel.com/templates/next.js/monorepo-turborepo. Origem: `vercel/turborepo`, caminho `examples/basic`, commit `99233190d0dd77d9ae6ea897297a5adc20244ef6`, licença MIT confirmada.[14] [19]
13. **Turborepo & React Native Starter** — página: https://vercel.com/templates/next.js/turborepo-react-native. Origem: `vercel/turborepo`, caminho `examples/with-react-native-web`, commit `99233190d0dd77d9ae6ea897297a5adc20244ef6`, licença MIT confirmada.[15] [19]
14. **Catalyst by BigCommerce** — página: https://vercel.com/templates/next.js/catalyst-by-bigcommerce. Origem: `bigcommerce/catalyst`, caminho relativo `.`, commit `6b122042c4b9918e8e1da85e6456074dcd915917` do branch padrão `canary`, licença MIT confirmada. A página aponta para a raiz do repositório, sem subcaminho.[16] [21]
15. **SaaS Microservices** — página: https://vercel.com/templates/next.js/saas-microservices. Origem: `vercel/examples`, caminho `microfrontends/saas-microservices`, commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`, licença MIT confirmada.[17] [18]

## O que foi verificado e o que não foi

Foi verificada a presença pública da rota da categoria, os 15 links de entrada exibidos no HTML/texto público da categoria e, para cada entrada, o campo público `links.repository`. Foram verificadas as referências de commit dos branches públicos pela API do GitHub. Os repositórios `vercel/examples`, `vercel/turborepo`, `vercel/next-forge` e `bigcommerce/catalyst` retornaram licença SPDX `MIT` na API pública.[18] [19] [20] [21]

Não foi executado nenhum projeto, instalado dependência, testado demo ou inferida funcionalidade runtime. Não foi feita cópia de código. Não foi usado dashboard privado, credencial ou segredo. O caminho relativo é o subcaminho explicitamente presente no link público da Vercel; para `next-forge` e `catalyst`, a origem pública é a raiz do repositório. A API retornou `vercel/next-forge` para a URL de origem apresentada pela página como `haydenbleasel/next-forge`; essa divergência foi preservada como observação, não normalizada por analogia.

## Limitações

- `partial` é obrigatório: a página enumera 15 entradas observáveis, mas não há evidência independente de que sejam todas as entradas da categoria.
- O sitemap público `https://vercel.com/sitemap.xml` foi retornado como conteúdo parcial/truncado durante a leitura; não foi usado para afirmar completude.[2]
- Os SHAs são pontas de branch observadas durante esta exploração, não uma afirmação de que a página Vercel esteja historicamente fixada nesses commits. A página aponta para URLs com `main` ou para a raiz do repositório.
- A existência de README, demo, comandos, badges ou links de deploy não prova funcionamento em runtime; runtime permanece não verificado.
- Não foram consultados endpoints internos ou APIs não documentadas da galeria.

## References

[1]: https://vercel.com/templates/monorepos "Vercel public Monorepos category"
[2]: https://vercel.com/sitemap.xml "Vercel public sitemap"
[3]: https://vercel.com/templates/next.js/monorepo-nx "Vercel Monorepo with Nx template"
[4]: https://vercel.com/templates/fast-api/next-js-fastapi-starter "Vercel Next.js + FastAPI Starter template"
[5]: https://vercel.com/templates/next.js/next-js-fastapi-bindings-starter "Vercel Next.js + FastAPI + Bindings Starter template"
[6]: https://vercel.com/templates/next.js/next-js-gin-starter "Vercel Next.js + Gin Starter template"
[7]: https://vercel.com/templates/react/turborepo-design-system "Vercel Design System with Turborepo template"
[8]: https://vercel.com/templates/svelte/turborepo-sveltekit-starter "Vercel Turborepo SvelteKit Starter template"
[9]: https://vercel.com/templates/hono/turborepo-with-hono "Vercel Turborepo + Hono template"
[10]: https://vercel.com/templates/gatsby/turborepo-gatsby-starter "Vercel Turborepo Gatsby Starter template"
[11]: https://vercel.com/templates/next.js/turborepo-next-basic "Vercel Turborepo Next.js Starter template"
[12]: https://vercel.com/templates/react/vite-fastapi-starter "Vercel Vite + FastAPI Starter template"
[13]: https://vercel.com/templates/next.js/next-forge "Vercel next-forge template"
[14]: https://vercel.com/templates/next.js/monorepo-turborepo "Vercel Monorepo with Turborepo template"
[15]: https://vercel.com/templates/next.js/turborepo-react-native "Vercel Turborepo React Native Starter template"
[16]: https://vercel.com/templates/next.js/catalyst-by-bigcommerce "Vercel Catalyst by BigCommerce template"
[17]: https://vercel.com/templates/next.js/saas-microservices "Vercel SaaS Microservices template"
[18]: https://api.github.com/repos/vercel/examples/branches/main "GitHub API vercel/examples main branch and repository metadata"
[19]: https://api.github.com/repos/vercel/turborepo/branches/main "GitHub API vercel/turborepo main branch and repository metadata"
[20]: https://api.github.com/repos/haydenbleasel/next-forge/branches/main "GitHub API next-forge main branch and repository metadata"
[21]: https://api.github.com/repos/bigcommerce/catalyst/branches/canary "GitHub API bigcommerce/catalyst canary branch"
