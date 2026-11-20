# Scout público — Vercel Marketing Sites

**Rota pesquisada:** <https://vercel.com/templates/marketing-sites>  
**Data da observação:** 2026-11-20  
**Coverage:** `partial`

A página pública da categoria exibiu nove cartões observáveis: Drupal Marketing Site, Astroship, Odyssey, eve Marketing Team, eve Contentful Agent, eve Sanity Copilot, BaseHub Marketing Website, Bulk Redirects via a CMS e Router.so - Headless Forms and Lead Routing [1]. Não foi encontrada evidência pública de enumeração completa da categoria. A página não apresentou um total fechado, manifesto completo ou mecanismo de paginação verificável. O sitemap público contém a própria categoria e apenas quatro das páginas individuais entre os cartões observados: Bulk Redirects via a CMS, BaseHub Marketing Website, Headless Forms, Odyssey, Drupal Marketing Site e Astroship [2]. Portanto, o resultado é deliberadamente parcial e não afirma que os nove cartões sejam o inventário total.

Os SHAs abaixo são os commits atuais da branch padrão retornados pela API pública do GitHub durante a coleta. Eles fixam o estado do repositório consultado, mas não constituem prova de runtime. Nenhum código foi clonado, instalado ou executado.

## Registros observados e origem pública

1. **Drupal Marketing Site** — Página pública: <https://vercel.com/templates/next.js/drupal-nextjs-marketing-site> [3]. Repositório: <https://github.com/chapter-three/next-drupal> [3]. Caminho relativo: `examples/example-marketing` (o link público da página aponta para esse diretório). Commit observado na branch `main`: `80a89f1466bcdc980b4de529241b42de296b2a7d` [4]. Licença confirmada pela página pública e pelo metadado público do repositório: MIT [3][4]. A página lista Next.js e Tailwind, mas isso é metadado da galeria e não verificação de funcionamento.

2. **Astroship** — Página pública: <https://vercel.com/templates/astro/astroship> [5]. Repositório: <https://github.com/surjithctly/astroship> [5]. Caminho relativo: `.` (a página aponta para a raiz do repositório). Commit observado na branch `main`: `da1272bb141abf42a3435d81774df92f0427ad57` [4]. Licença confirmada: GPL-3.0 [4] e link público de licença na página [5].

3. **Odyssey** — Página pública: <https://vercel.com/templates/astro/odyssey> [6]. Repositório: <https://github.com/treefarmstudio/odyssey-theme> [6]. Caminho relativo: `.`. Commit observado na branch `main`: `d191e5715a2519e25be4629b933189c421b30a1a` [4]. Licença confirmada: MIT [4] e link público de licença na página [6].

4. **eve Marketing Team** — Página pública: <https://vercel.com/templates/eve/eve-marketing-team> [7]. Repositório: <https://github.com/vercel-labs/marketing-team-eve-template> [7]. Caminho relativo: `.`. Commit observado na branch `main`: `a23bd76fb2c8f690a734c09b2b9aef1924a1c999` [4]. Licença confirmada: MIT [4] e link público de licença na página [7].

5. **eve Contentful Agent** — Página pública: <https://vercel.com/templates/eve/eve-contentful-agent> [8]. Repositório: <https://github.com/vercel-labs/eve-contentful-agent-template> [8]. Caminho relativo: `.`. Commit observado na branch `main`: `a05976e63a47653f7832db81a63ecc2bb12cbfc7` [4]. Licença confirmada: MIT [4] e link público de licença na página [8].

6. **eve Sanity Copilot** — Página pública: <https://vercel.com/templates/eve/eve-sanity-copilot> [9]. Repositório: <https://github.com/vercel-labs/sanity-copilot-eve-template> [9]. Caminho relativo: `.`. Commit observado na branch `main`: `e0f4d11858a25a641e6e5054e3cd64ee940fe4c6` [4]. Licença confirmada: MIT [4] e link público de licença na página [9]. A página também menciona `sanity-io/agent-toolkit`; isso é uma dependência/referência pública adicional, não o repositório principal do cartão.

7. **BaseHub Marketing Website** — Página pública: <https://vercel.com/templates/next.js/basehub-marketing-website> [10]. Repositório: <https://github.com/basehub-ai/marketing-website-template> [10]. Caminho relativo: `.`. Commit observado na branch `main`: `7cfc4038b591fbc9206d453636db3b1fb3e676c6` [4]. Licença: **não confirmada** no metadado público consultado; não atribuo uma licença por analogia ou pelo título da página.

8. **Bulk Redirects via a CMS** — Página pública: <https://vercel.com/templates/next.js/bulk-redirects-via-a-cms> [11]. Repositório: <https://github.com/vercel/examples> [11]. Caminho relativo: `cdn/cms-bulk-redirects`. Commit observado na branch `main`: `a4b4827297bec79b81ddb2ff22a53089ebe88cd8` [4]. Licença confirmada: MIT no metadado público do repositório e link `license.md` na página [4][11]. A página também contém referências a `vercel/next.js` usadas no texto de instrução; não as trato como origem principal do cartão.

9. **Router.so — Headless Forms and Lead Routing** — Página pública: <https://vercel.com/templates/next.js/headless-forms> [12]. Repositório: <https://github.com/routerso/router> [12]. Caminho relativo: `.` para o template, com documentação pública relacionada em `docs/forms/README.md` e `docs/forms/release-runbook.md` [12]. Commit observado na branch `main`: `3f6528897e549d80315a335654e9bea65f5bdd4b` [4]. Licença confirmada: AGPL-3.0 no metadado público do repositório e link público de licença associado ao proprietário `9d8dev` [4][12].

## Limitações e classificação

- A página da categoria é dinâmica e não expõe, na evidência observada, um total ou uma enumeração fechada. O sitemap público não demonstrou todas as páginas da categoria. Coverage é, portanto, `partial`, não `complete`.
- A presença de um cartão, README, descrição, demo, link de deploy, stack ou metadado de galeria não foi usada como prova de funcionamento em runtime.
- Os SHAs registram o HEAD público da branch padrão consultada no momento da coleta. Eles não provam que a Vercel tenha usado exatamente aquele commit para o deploy ou para a renderização da galeria.
- Para BaseHub, a licença não foi confirmada e permanece omitida como licença verificável.
- Não foram acessados dashboards privados, credenciais, tokens ou segredos. Não foram executados scripts, instalações ou código dos candidatos.

## Referências

[1]: https://vercel.com/templates/marketing-sites "Vercel — Marketing Site Templates & Starters"
[2]: https://vercel.com/crawled-sitemap.xml "Vercel — sitemap público crawled-sitemap.xml"
[3]: https://vercel.com/templates/next.js/drupal-nextjs-marketing-site "Vercel — Drupal Marketing Site"
[4]: https://api.github.com/repos/{owner}/{repo} "GitHub REST API — metadados públicos de repositórios e commits consultados"
[5]: https://vercel.com/templates/astro/astroship "Vercel — Astroship"
[6]: https://vercel.com/templates/astro/odyssey "Vercel — Odyssey"
[7]: https://vercel.com/templates/eve/eve-marketing-team "Vercel — eve Marketing Team"
[8]: https://vercel.com/templates/eve/eve-contentful-agent "Vercel — eve Contentful Agent"
[9]: https://vercel.com/templates/eve/eve-sanity-copilot "Vercel — eve Sanity Copilot"
[10]: https://vercel.com/templates/next.js/basehub-marketing-website "Vercel — BaseHub Marketing Website"
[11]: https://vercel.com/templates/next.js/bulk-redirects-via-a-cms "Vercel — Bulk Redirects via a CMS"
[12]: https://vercel.com/templates/next.js/headless-forms "Vercel — Router.so Headless Forms and Lead Routing"
