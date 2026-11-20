# Scout 12 — Vercel CMS

**Rota pesquisada:** https://vercel.com/templates/cms  
**Provider:** Vercel  
**Data da observação:** 2026-11-20  
**Coverage:** `partial`

A página pública da categoria CMS respondeu com uma página intitulada “CMS Templates” e expôs 25 entradas observáveis, cada uma com título, URL de template e descrição curta. A resposta não apresentou um mecanismo público de paginação, contador total independente ou manifesto exportável que permita demonstrar enumeração completa da categoria. Por isso, a cobertura é `partial`, não `complete`. A listagem da galeria é evidência de descoberta e metadado; não é evidência de execução em runtime.[1]

## Entradas observadas na categoria

As seguintes entradas foram observadas diretamente na rota CMS:[1]

1. **ISR Blog with Next.js and WordPress** — https://vercel.com/templates/next.js/isr-blog-nextjs-wordpress
2. **Sanity + Next.js Personal Website** — https://vercel.com/templates/next.js/sanity-next-js-personal-website
3. **Wix CMS: Next.js CMS starter** — https://vercel.com/templates/next.js/wix-cms
4. **Update Redirects in Realtime** — https://vercel.com/templates/next.js/update-redirects-in-realtime
5. **Next.js Starter for WordPress Headless CMS** — https://vercel.com/templates/next.js/nextjs-wordpress-headless-cms
6. **Optimizely SaaS CMS + Next.js 15** — https://vercel.com/templates/next.js/optimizely-saas-cms-next-js-15
7. **CMS-Kit: Sanity + Next.js 15 Visual Site Builder** — https://vercel.com/templates/next.js/cms-kit-sanity
8. **Ecommerce Template with Crystallize and Remix** — https://vercel.com/templates/remix/ecommerce-crystalize-remix
9. **Builder.io Shopify Commerce** — https://vercel.com/templates/next.js/builderio-shopify-commerce-headless
10. **Next.js Blog with Draft Mode** — https://vercel.com/templates/next.js/nextjs-blog-draft-mode
11. **Builder.io Personalization Starter** — https://vercel.com/templates/next.js/personalization-builder-io
12. **Notion-backed Next.js Blog** — https://vercel.com/templates/next.js/notion-blog
13. **Stablo – Minimal Blog Template** — https://vercel.com/templates/next.js/stablo-blog
14. **Next.JS ButterCMS Starter Project** — https://vercel.com/templates/next.js/NextJS-starter-buttercms
15. **eve Marketing Team** — https://vercel.com/templates/eve/eve-marketing-team
16. **Clean Next.js + Sanity App** — https://vercel.com/templates/next.js/sanity-template-nextjs-clean
17. **eve Contentful Agent** — https://vercel.com/templates/eve/eve-contentful-agent
18. **Glide Publishing Platform - Next.js Starter** — https://vercel.com/templates/next.js/gpp-starter
19. **eve Sanity Copilot** — https://vercel.com/templates/eve/eve-sanity-copilot
20. **LaunchPad: Next.js × Strapi Starter** — https://vercel.com/templates/next.js/strapi
21. **ServerlessWP** — https://vercel.com/templates/other/serverless-wordpress
22. **BaseHub Marketing Website** — https://vercel.com/templates/next.js/basehub-marketing-website
23. **Bulk Redirects via a CMS** — https://vercel.com/templates/next.js/bulk-redirects-via-a-cms
24. **Next.js Waitlist with Notion CMS** — https://vercel.com/templates/next.js/next-js-waitlist-with-notion-cms
25. **Payload Website Starter** — https://vercel.com/templates/next.js/payload-website-starter

## Registros aprofundados com origem pública e pinagem

Os registros abaixo têm, na página pública individual, um link explícito para o repositório de origem. O SHA é o commit observado na referência pública correspondente via API GitHub. A licença só é informada quando o campo público do repositório confirmou um SPDX/licença; `license: null` foi preservado como licença não confirmada, sem inferência pelo README.[2][3][4][5][6][7][8][9]

### 1. ISR Blog with Next.js and WordPress

- **Página Vercel:** https://vercel.com/templates/next.js/isr-blog-nextjs-wordpress
- **Repositório:** https://github.com/vercel/next.js
- **Caminho relativo:** `examples/cms-wordpress`
- **Referência observada na galeria:** `canary`
- **Commit/SHA observado:** `bb63c72077ad7b81b2319f74a7ef3b00c1751483`
- **Licença do repositório:** MIT, confirmada pelo endpoint público do repositório
- **Proveniência:** a página Vercel aponta explicitamente para `vercel/next.js/tree/canary/examples/cms-wordpress`.[2][3]
- **Status:** `discovered_unverified`; não foi executado build, teste ou deploy neste scout.

### 2. Next.js Blog with Draft Mode

- **Página Vercel:** https://vercel.com/templates/next.js/nextjs-blog-draft-mode
- **Repositório:** https://github.com/vercel/next.js
- **Caminho relativo:** `examples/cms-contentful`
- **Referência observada na galeria:** `canary`
- **Commit/SHA observado:** `bb63c72077ad7b81b2319f74a7ef3b00c1751483`
- **Licença do repositório:** MIT, confirmada pelo endpoint público do repositório
- **Proveniência:** a página Vercel aponta explicitamente para `vercel/next.js/tree/canary/examples/cms-contentful`.[4][3]
- **Status:** `discovered_unverified`; a descrição e o demo não foram tratados como prova de funcionamento.

### 3. Sanity + Next.js Personal Website

- **Página Vercel:** https://vercel.com/templates/next.js/sanity-next-js-personal-website
- **Repositório:** https://github.com/sanity-io/template-nextjs-personal-website
- **Caminho relativo:** `.` (a página aponta para a raiz do repositório)
- **Referência observada na galeria:** `main`
- **Commit/SHA observado:** `fec0fe5683e54715adb9cd35b09e93144a73046c`
- **Licença:** não confirmada; o endpoint público do repositório retornou `license: null`
- **Proveniência:** o front matter público da página contém o link de repositório para `sanity-io/template-nextjs-personal-website`.[5][6]
- **Status:** `discovered_unverified`; a documentação da página menciona recursos, mas não foi considerada teste de runtime.

### 4. Clean Next.js + Sanity App

- **Página Vercel:** https://vercel.com/templates/next.js/sanity-template-nextjs-clean
- **Repositório:** https://github.com/sanity-io/sanity-template-nextjs-clean
- **Caminho relativo:** `.` (a página aponta para a raiz do repositório)
- **Referência observada na galeria:** `main`
- **Commit/SHA observado:** `d082fad65cdfa85547789d2a7dc51086fec898b2`
- **Licença:** não confirmada; o endpoint público do repositório retornou `license: null`
- **Proveniência:** o front matter público da página contém o link de repositório para `sanity-io/sanity-template-nextjs-clean`.[7][8]
- **Status:** `discovered_unverified`.

### 5. Next.js Starter for WordPress Headless CMS

- **Página Vercel:** https://vercel.com/templates/next.js/nextjs-wordpress-headless-cms
- **Repositório:** https://github.com/9d8dev/next-wp
- **Caminho relativo:** `.` (a página aponta para a raiz do repositório)
- **Referência observada na galeria:** `main`
- **Commit/SHA observado:** `4a2caeb1e14191fe58113b94326c2ad92106ff8b`
- **Licença do repositório:** MIT, confirmada pelo endpoint público do repositório
- **Proveniência:** o front matter público da página contém o link de repositório para `9d8dev/next-wp`.[9][10]
- **Status:** `discovered_unverified`; comandos, testes descritos no README e demo não são prova de execução aqui.

### 6. Notion-backed Next.js Blog

- **Página Vercel:** https://vercel.com/templates/next.js/notion-blog
- **Repositório:** https://github.com/ijjk/notion-blog
- **Caminho relativo:** `.` (a página aponta para a raiz do repositório)
- **Referência observada na galeria:** `main`
- **Commit/SHA observado:** `362af9e5457cdc8c11fa4d0adac6e81dcb902975`
- **Licença do repositório:** MIT, confirmada pelo endpoint público do repositório
- **Proveniência:** o front matter público da página contém o link de repositório para `ijjk/notion-blog`.[11][12]
- **Status:** `discovered_unverified`; a própria página menciona dependência de token e índice Notion, mas nenhum segredo foi acessado.

### 7. LaunchPad: Next.js × Strapi Starter

- **Página Vercel:** https://vercel.com/templates/next.js/strapi
- **Repositório:** https://github.com/strapi/LaunchPad
- **Caminho relativo:** `.` (a página aponta para a raiz do repositório)
- **Referência observada na galeria:** `main`
- **Commit/SHA observado:** `c54b5c2e665b8e8589d7ea360d6261b64f6399a1`
- **Licença:** não confirmada; o endpoint público do repositório retornou `license: null`
- **Proveniência:** o front matter público da página contém o link de repositório para `strapi/LaunchPad`.[13][14]
- **Status:** `discovered_unverified`.

### 8. Payload Website Starter

- **Página Vercel:** https://vercel.com/templates/next.js/payload-website-starter
- **Repositório:** https://github.com/payloadcms/payload
- **Caminho relativo:** `templates/with-vercel-website`
- **Referência observada na galeria:** `3.x` no link de repositório da página
- **Commit/SHA observado:** `e083b4a2c4b5af0844b83b4a8bf651cd3b772349`
- **Licença do repositório:** MIT, confirmada pelo endpoint público do repositório
- **Proveniência:** o front matter aponta para `payloadcms/payload/tree/3.x/templates/with-vercel-website`; o corpo também descreve o template como oficial do Payload.[15][16]
- **Status:** `discovered_unverified`; a afirmação editorial “production-ready” não foi usada como prova de runtime.

## Entradas com descoberta observada, mas sem registro aprofundado

Foram observadas na categoria, mas não receberam registro aprofundado com SHA e licença confirmados neste scout: **Wix CMS: Next.js CMS starter**, **Update Redirects in Realtime**, **Optimizely SaaS CMS + Next.js 15**, **CMS-Kit: Sanity + Next.js 15 Visual Site Builder**, **Ecommerce Template with Crystallize and Remix**, **Builder.io Shopify Commerce**, **Builder.io Personalization Starter**, **Stablo – Minimal Blog Template**, **Next.JS ButterCMS Starter Project**, **eve Marketing Team**, **eve Contentful Agent**, **Glide Publishing Platform - Next.js Starter**, **eve Sanity Copilot**, **ServerlessWP**, **BaseHub Marketing Website**, **Bulk Redirects via a CMS** e **Next.js Waitlist with Notion CMS**. A presença na página CMS não foi convertida em origem, caminho, commit ou licença por analogia.

## Limitações e decisões de evidência

- A página CMS é pública e observável, mas não demonstrou que os 25 cards constituem a enumeração completa da categoria. O sitemap público foi consultado, porém a resposta foi truncada pela ferramenta e não constitui uma enumeração independente e completa dos templates CMS; portanto não altera `coverage: partial`.[17]
- A galeria fornece links de repositório, mas não prova que o código funciona em runtime. Nenhum candidato foi clonado, executado, instalado ou implantado.
- Branches como `canary`, `main` e `3.x` são referências mutáveis. Os SHAs acima são os heads observados no momento da consulta e devem ser tratados como pinagens da observação, não como garantia de imutabilidade futura.
- Quando a API GitHub informou `license: null`, a licença foi deixada como não confirmada. Não foi inferida a partir de nomes, demos, README ou licença de outro repositório.
- Não foram acessados dashboards privados, credenciais, tokens ou segredos. A menção pública a variáveis de ambiente na documentação não foi tratada como autorização para obtê-las.
- Nenhum manifesto central do projeto foi alterado.

## References

[1]: https://vercel.com/templates/cms "Vercel CMS Templates"
[2]: https://vercel.com/templates/next.js/isr-blog-nextjs-wordpress "ISR Blog with Next.js and WordPress"
[3]: https://api.github.com/repos/vercel/next.js/git/ref/heads/canary "GitHub API canary reference for vercel/next.js"
[4]: https://vercel.com/templates/next.js/nextjs-blog-draft-mode "Next.js Blog with Draft Mode"
[5]: https://vercel.com/templates/next.js/sanity-next-js-personal-website "Sanity + Next.js Personal Website"
[6]: https://api.github.com/repos/sanity-io/template-nextjs-personal-website/git/ref/heads/main "GitHub API main reference for Sanity personal website template"
[7]: https://vercel.com/templates/next.js/sanity-template-nextjs-clean "Clean Next.js + Sanity App"
[8]: https://api.github.com/repos/sanity-io/sanity-template-nextjs-clean/git/ref/heads/main "GitHub API main reference for Sanity clean template"
[9]: https://vercel.com/templates/next.js/nextjs-wordpress-headless-cms "Next.js Starter for WordPress Headless CMS"
[10]: https://api.github.com/repos/9d8dev/next-wp/git/ref/heads/main "GitHub API main reference for next-wp"
[11]: https://vercel.com/templates/next.js/notion-blog "Notion-backed Next.js Blog"
[12]: https://api.github.com/repos/ijjk/notion-blog/git/ref/heads/main "GitHub API main reference for notion-blog"
[13]: https://vercel.com/templates/next.js/strapi "LaunchPad: Next.js × Strapi Starter"
[14]: https://api.github.com/repos/strapi/LaunchPad/git/ref/heads/main "GitHub API main reference for Strapi LaunchPad"
[15]: https://vercel.com/templates/next.js/payload-website-starter "Payload Website Starter"
[16]: https://api.github.com/repos/payloadcms/payload/git/ref/heads/3.x "GitHub API 3.x reference for Payload"
[17]: https://vercel.com/sitemap.xml "Vercel public sitemap"
