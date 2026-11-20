# Scout 07 — Vercel SaaS

- **Rota:** https://vercel.com/templates/saas
- **Tipo:** public Vercel category route
- **Data/hora da observação:** 2026-11-20 (UTC−03:00)
- **Coverage:** `partial`
- **Status da evidência:** a rota pública renderizou e expôs entradas navegáveis; a cobertura não é exaustiva porque a própria página usa carregamento incremental e não oferece, nesta observação, um total final ou uma lista pública garantidamente completa.

## O que foi observado na rota

A página abriu publicamente com o título “SaaS website templates and starters”, descrição da categoria, campo de busca, botão de filtros e uma galeria. Na primeira renderização foram observados 12 cards e o controle `Load More`. Os 12 primeiros cards foram: Onelink, Next.js Enterprise Boilerplate, Syntro, Platforms Starter Kit, EnvShare, Astroship, Odyssey, Xata: Typo-Tolerant Full-Text Search, VisActor Next.js Template, Minimal Next.js SaaS Website Starter, Finwise: SaaS Landing Page e Replicache Starter. A evidência é a página renderizada e seu conteúdo extraído [1].

O controle `Load More` foi acionado uma vez. A galeria passou a mostrar mais 12 entradas, totalizando 24 cards observados nesta sessão, e o controle continuou presente. As entradas adicionais observadas foram: Evervault: Encryption Starter Kit for Next.js, Saasfly, Paddle Billing Subscription Starter, Update Starter: Subscriptions and Auth for SaaS, Stark Industries HQ - Agentic Email Assistants, Novel – AI-powered Notion-style editor, Next.js SaaS Starter, Liveblocks Starter Kit, Stripe Subscription Starter, LaunchPad: Next.js × Strapi Starter, Waitly e SaaStart: Auth0 + Next.js SaaS Starter Kit [2]. Isso comprova uma segunda página/lote renderizado, mas não comprova que não existam outros lotes.

Não foi usado endpoint interno ou dashboard privado. O sitemap público foi consultado como fonte auxiliar, mas a resposta foi truncada no retorno e não constituiu inventário exaustivo da categoria. O README do projeto local também registra que a galeria Vercel é dinamicamente paginada e que não há garantia de descoberta completa [3].

## Registros com origem pública verificável

Os registros abaixo são os que tiveram página de detalhes Vercel com link de repositório e SHA público do repositório verificado via API GitHub. A verificação é de descoberta/metadados e proveniência; não é teste de runtime.

### 1. Next.js SaaS Starter

- **Título na categoria:** Next.js SaaS Starter
- **URL da página Vercel:** https://vercel.com/templates/next.js/next-js-saas-starter
- **Repositório:** https://github.com/nextjs/saas-starter
- **Commit verificado:** `6e33e58b1e553a41fe22e6b941a7229a002de361` (branch `main` no momento da consulta) [5]
- **Caminhos relativos verificáveis no commit:** `README.md`, `LICENSE`, `.env.example`, `package.json`, `pnpm-lock.yaml`, `app/`, `components/ui/`, `lib/`, `middleware.ts`, `drizzle.config.ts`, `next.config.ts`, `tsconfig.json` [4]
- **Evidência de licença:** a página pública do repositório informa “MIT license” e lista `LICENSE`; isso é evidência de metadado público, não uma revisão jurídica de compatibilidade [4].
- **Metadados declarados pela página de template:** Next.js, Postgres, Drizzle, Stripe e shadcn/ui; a página também fornece demo público e link de deploy [4].
- **Natureza da evidência:** página pública Vercel + página pública GitHub + API pública de commit/tree. O README descreve comandos e recursos, mas nenhum comando foi executado e nenhuma implantação foi testada.

### 2. Platforms Starter Kit

- **Título na categoria:** Platforms Starter Kit
- **URL da página Vercel:** https://vercel.com/templates/next.js/platforms-starter-kit
- **Repositório:** https://github.com/vercel/platforms
- **Commit verificado:** `ec12e65709c8263dd3462c4d33261851b8a3157d` (branch `main` no momento da consulta) [7]
- **Caminho relativo explicitamente verificável no diff do commit:** `README.md`; o commit também referencia a árvore `ab5db3f8b4fb77c7c2f1609e3148afcbcef24450` [7].
- **Metadados declarados pela página de template:** Next.js com App Router, Redis/Upstash, Tailwind e shadcn/ui, além de exemplo de aplicação multi-tenant [6].
- **Natureza da evidência:** página pública Vercel + API pública de commit GitHub. A existência de um commit e o conteúdo do README/diff não comprovam funcionamento em runtime, configuração válida de Redis ou implantação bem-sucedida.

Como referência de escopo, a própria página de detalhes de `Saasfly` expõe outro repositório público (`https://github.com/saasfly/saasfly`) e diretório de build `apps/nextjs`, mas esse repositório não foi incluído como registro verificado porque não foi obtido um SHA via API nesta exploração [8].

## Relação com o repositório oficial `vercel/examples`

A página pública de `vercel/examples` informa que o repositório é uma coleção curada de exemplos e que templates da galeria podem incluir repositórios externos [9]. A API pública retornou o commit atual observado do branch `main` como `a4b4827297bec79b81ddb2ff22a53089ebe88cd8` e uma árvore sem `truncated: true`, mas isso é a árvore do repositório oficial, não uma enumeração da categoria SaaS nem prova de que todos os cards da galeria estejam nesse monorepo [10]. O README do repositório lista explicitamente a galeria Vercel como local de filtragem adicional e explica que metadados de front matter podem gerar templates [9].

## Limitações e classificação

- `partial` é a classificação apropriada: 24 cards foram observados após uma renderização inicial e um `Load More`, porém o botão permaneceu disponível e não foi estabelecido um total final.
- A página é dinâmica. O conteúdo e a ordenação podem mudar entre consultas; os nomes acima são uma fotografia da sessão, não um snapshot versionado da galeria.
- Não há prova, nesta rota, de que os 24 cards observados sejam todos os registros da categoria, nem de que o sitemap público forneça cobertura completa dessa categoria.
- Para a maioria dos cards não foi seguido o link de detalhes nem verificado o repositório. Eles permanecem descobertos, não enriquecidos.
- Nenhuma execução de código, instalação de dependências, build, deploy, teste de demo, teste de autenticação, banco, Stripe, Redis ou webhook foi realizada.
- README, descrições e metadados de template foram tratados como evidência de referência, não como prova de funcionamento em runtime.
- Licença foi confirmada apenas como metadado público para `nextjs/saas-starter`; não foi inferida licença para os demais registros.

## Referências

[1]: https://vercel.com/templates/saas "Vercel SaaS templates category"
[2]: https://vercel.com/templates/saas "Vercel SaaS category after one Load More interaction"
[3]: https://github.com/LOOPAPPdev/Manus_Lego/blob/main/docs/pipeline.md "Manus LEGO pipeline limitations"
[4]: https://vercel.com/templates/next.js/next-js-saas-starter "Vercel Next.js SaaS Starter template"
[5]: https://api.github.com/repos/nextjs/saas-starter/commits/main "GitHub API commit for nextjs/saas-starter"
[6]: https://vercel.com/templates/next.js/platforms-starter-kit "Vercel Platforms Starter Kit template"
[7]: https://api.github.com/repos/vercel/platforms/commits/main "GitHub API commit for vercel/platforms"
[8]: https://vercel.com/templates/next.js/saasfly "Vercel Saasfly template"
[9]: https://github.com/vercel/examples "Vercel examples repository"
[10]: https://api.github.com/repos/vercel/examples/commits/main "GitHub API commit for vercel/examples"
