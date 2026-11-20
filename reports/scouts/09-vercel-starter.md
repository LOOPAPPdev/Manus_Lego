# Scout — Vercel Starter Templates

- **Rota:** `https://vercel.com/templates/starter`
- **Tipo:** public Vercel category route
- **Data da observação:** 2026-11-20
- **Coverage:** `partial`

A rota pública respondeu e renderizou o título “Find your Starter Templates”, a descrição da categoria e uma lista de links de templates. A resposta extraída contém várias entradas públicas, incluindo `Jev x AI SDK Form Router`, `Next.js App Router Playground`, `Nuxt.js 3 Boilerplate`, `Next.js Contentlayer Blog Starter`, `Precedent – Next.js Starter`, `React Router Boilerplate`, `HTML Starter`, `Angular Boilerplate` e outras. A própria extração sinaliza conteúdo omitido com `[...]`; portanto, ela demonstra descoberta observada, mas não sustenta uma contagem total nem cobertura completa da categoria. [1]

A página individual de `Next.js App Router Playground` fornece metadados de front matter com o repositório `https://github.com/vercel/app-playground` e demonstração pública `https://app-dir.vercel.app/`. A API pública do GitHub redireciona esse alias para `vercel/next-app-router-playground`, confirma que o repositório é público, informa licença MIT e permite fixar a branch `main` no commit `b5c0f7eaf1ed070d20aa29f435ce22a48b987684`. O caminho relativo verificado para a entrada é a raiz do repositório (`/`); nenhum subdiretório específico foi declarado pela página da Vercel. [2] [3] [4]

A página individual de `Next.js Contentlayer Blog Starter` expõe o repositório `https://github.com/shadcn/next-contentlayer`, proprietário `shadcn`, usos `Blog` e `Starter`, e a descrição do stack Next.js, Contentlayer e Tailwind. A API pública confirma o repositório público e a branch `main`, cujo commit observado é `5b32397c2034a97a077cd695f3421a2e76af05c5`. A API não retornou licença SPDX para esse repositório; licença foi, portanto, deixada como não verificada. O caminho relativo verificado é a raiz (`/`). [5] [6] [7]

A página individual de `Precedent – Next.js Starter` expõe o repositório `https://github.com/steven-tey/precedent`, demo público e stack descrito como Next.js, TypeScript, Tailwind, Radix, Framer Motion, Prisma e PostgreSQL. A API pública confirma que o repositório é público, informa MIT e fixa a branch `main` no commit `3be40205d7cdf56082cd284f07f12251b9208f79`. O caminho relativo verificado é a raiz (`/`). A página menciona variáveis de ambiente e um dashboard de terceiro no link de configuração; esse destino não foi acessado nem armazenado. [8] [9]

Como fonte oficial complementar, o repositório `vercel/examples` é público, tem licença MIT e branch padrão `main`; seu README descreve `starter/` como aplicações funcionais que podem servir de ponto de partida e explica que exemplos com front matter podem ser publicados como templates. O commit atual observado para `main` foi `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`. A listagem pública de `starter/` retornou nove diretórios: `cms-payload`, `cms-sanity-graphql-fragments`, `express-ai-sdk`, `fastify`, `hono-ai-sdk`, `hono-mcp`, `mcp-api-wrapper`, `personalization-builder-io` e `turborepo-with-hono`. A API de contents forneceu SHAs de árvore para cada diretório, mas isso é uma lista do diretório oficial e não uma prova de que todos esses diretórios aparecem na categoria pública `/templates/starter`. [10] [11] [12]

Na mesma linha, `internal/fields.json` define campos usados no fluxo de publicação de templates, incluindo `slug`, `framework`, `type`, `githubUrl`, `demoUrl` e `deployUrl`; os valores permitidos para `type` incluem `Starter`. Isso explica uma relação de publicação entre exemplos e templates, mas não constitui inventário completo da galeria nem prova de funcionamento dos candidatos. [13]

## Registros verificados

1. **Next.js App Router Playground** — URL da galeria: `https://vercel.com/templates/next.js/app-directory`; repositório: `vercel/next-app-router-playground` (link apresentado pela página como `vercel/app-playground`); caminho relativo: `/`; commit verificado: `b5c0f7eaf1ed070d20aa29f435ce22a48b987684`; licença observada na API: MIT. Evidência: página individual com repository/demo/deploy e API pública de repositório/ref. [2] [3] [4]
2. **Next.js Contentlayer Blog Starter** — URL da galeria: `https://vercel.com/templates/next.js/nextjs-contentlayer`; repositório: `shadcn/next-contentlayer`; caminho relativo: `/`; commit verificado: `5b32397c2034a97a077cd695f3421a2e76af05c5`; licença: não retornada pela API, não verificada. Evidência: página individual com repository/owner/use cases/stack e API pública de repositório/ref. [5] [6] [7]
3. **Precedent – Next.js Starter** — URL da galeria: `https://vercel.com/templates/next.js/precedent`; repositório: `steven-tey/precedent`; caminho relativo: `/`; commit verificado: `3be40205d7cdf56082cd284f07f12251b9208f79`; licença observada na API: MIT. Evidência: página individual com repository/stack/deploy e API pública de repositório/ref. [8] [9]
4. **Entradas oficiais sob `vercel/examples/starter`** — repositório: `vercel/examples`; caminho relativo: `starter/` e os nove diretórios listados acima; commit de `main` verificado: `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`; evidência: API pública de commit e contents. Não foram promovidas automaticamente a registros da categoria, pois a correspondência individual com a rota não foi verificada. [10] [11] [12]

## Limitações e status da evidência

- `coverage` é **partial**: a rota respondeu e revelou entradas, mas a extração contém `[...]`, sem total confiável e sem uma prova independente de que todas as páginas/itens foram percorridos.
- Não foi tratado o HTML renderizado como prova de runtime. Nenhum template foi instalado, executado, compilado ou implantado nesta exploração.
- Não foi encontrada, nesta verificação pública, uma API documentada e garantidamente completa para enumerar a galeria; o sitemap público também foi retornado como parcial/truncado pelo extrator. [14]
- Os links `repository` das páginas individuais provam a origem declarada pela Vercel, mas não provam que o código atualmente no commit observado corresponde byte a byte à implantação/demo da galeria.
- Para os repositórios externos, só foram confirmados o repositório público, a branch/commit observados e, quando retornada pela API, a licença. Não foram inferidos commits de arquivos individuais nem licenças ausentes.
- A listagem de `vercel/examples/starter` não deve ser confundida com a categoria pública: o README do repositório diz que a galeria também contém exemplos e repositórios externos, e a rota pública mostrou vários links que não pertencem a esse diretório. [1] [10]

## References

[1]: https://vercel.com/templates/starter "Vercel Starter Templates category"
[2]: https://vercel.com/templates/next.js/app-directory "Next.js App Router Playground template page"
[3]: https://api.github.com/repos/vercel/app-playground "GitHub API metadata for the App Router Playground repository alias"
[4]: https://api.github.com/repos/vercel/app-playground/git/refs/heads/main "GitHub API main ref for the App Router Playground repository"
[5]: https://vercel.com/templates/next.js/nextjs-contentlayer "Next.js Contentlayer Blog Starter template page"
[6]: https://api.github.com/repos/shadcn/next-contentlayer "GitHub API metadata for next-contentlayer"
[7]: https://api.github.com/repos/shadcn/next-contentlayer/git/refs/heads/main "GitHub API main ref for next-contentlayer"
[8]: https://vercel.com/templates/next.js/precedent "Precedent Next.js Starter template page"
[9]: https://api.github.com/repos/steven-tey/precedent "GitHub API metadata and license for Precedent"
[10]: https://github.com/vercel/examples "Official Vercel examples repository"
[11]: https://api.github.com/repos/vercel/examples/commits/main "GitHub API current main commit for vercel/examples"
[12]: https://api.github.com/repos/vercel/examples/contents/starter?ref=main "GitHub API contents for vercel/examples/starter"
[13]: https://github.com/vercel/examples/blob/main/internal/fields.json "Vercel examples template publication fields"
[14]: https://vercel.com/sitemap.xml "Vercel public sitemap"
