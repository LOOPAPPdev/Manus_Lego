# Scout da rota pública Vercel — ecommerce

- **Rota:** https://vercel.com/templates/ecommerce
- **Tipo:** public Vercel category route
- **Data/hora da observação:** 2026-11-20 (sessão UTC-03; páginas e APIs públicas consultadas nesta execução)
- **Coverage:** `partial`
- **Status da evidência:** descoberta pública verificável; não constitui teste de runtime, build, deploy ou funcionamento do template.

## Resultado observado

A rota carregou a categoria “Ecommerce website templates and starters” e mostrou uma galeria de cards. Na primeira renderização havia 12 cards e um controle `Load More`. Após um clique nesse controle, a página exibiu 21 entradas no total. O controle inicial e a mudança de conteúdo foram observados diretamente no DOM/renderização da página. Não foi encontrado um contador total, uma lista pública declarada como completa, nem uma garantia de que a galeria paginada/filtrada contenha todos os itens disponíveis.

Entradas públicas observadas na rota, na ordem exibida após o carregamento incremental:

1. Vercel Shop — https://vercel.com/templates/next.js/vercel-shop
2. Medusa Next.js Ecommerce Store Starter — https://vercel.com/templates/next.js/medusa
3. SvelteKit Commerce — https://vercel.com/templates/svelte/sveltekit-commerce
4. Next.js + Salesforce Commerce Cloud — https://vercel.com/templates/next.js/next-js-salesforce-commerce-cloud
5. Nuxt Commerce — https://vercel.com/templates/nuxt/nuxt-commerce
6. Shirt Shop — Feature Flags using Next.js — https://vercel.com/templates/next.js/shirt-shop-feature-flags
7. Next.js + BigCommerce Starter — https://vercel.com/templates/next.js/bigcommerce-starter-nextjs
8. Your Next Store — Commerce with Next.js and Stripe — https://vercel.com/templates/next.js/yournextstore
9. Next.js Saleor Commerce — https://vercel.com/templates/next.js/nextjs-saleor-commerce
10. Shopware Ecommerce Store with Nuxt — https://vercel.com/templates/nuxt/shopware-nuxt-ecommerce
11. Wix Events and eCommerce Next.js starter — https://vercel.com/templates/next.js/wix-commerce-ticketing
12. Blazity Enterprise Ecommerce Starter — https://vercel.com/templates/next.js/blazity-enterprise-ecommerce-starter
13. Next.js Shopware Starter — https://vercel.com/templates/next.js/nextjs-shopware-starter
14. TiDB Cloud Starter — https://vercel.com/templates/next.js/tidb-cloud-starter
15. Paddle Mobile Web Payments Starter — https://vercel.com/templates/next.js/paddle-mobile-web-payments-starter
16. Paddle In-App Checkout Starter — https://vercel.com/templates/next.js/paddle-in-app-checkout-starter
17. Ecommerce Template with Crystallize and Remix — https://vercel.com/templates/remix/ecommerce-crystalize-remix
18. Builder.io Shopify Commerce — https://vercel.com/templates/next.js/builderio-shopify-commerce-headless
19. Catalyst by BigCommerce — https://vercel.com/templates/next.js/catalyst-by-bigcommerce
20. Stripe Subscription Starter — https://vercel.com/templates/next.js/subscription-starter
21. Whop SaaS Template — https://vercel.com/templates/next.js/whop-template

Os nomes, descrições resumidas e URLs acima são evidência de descoberta na página da categoria. Eles não provam que os repositórios estejam no monorepo `vercel/examples`, não provam compatibilidade entre templates e não provam funcionamento em runtime.

## Registros com origem aprofundada

Somente os dois registros abaixo foram verificados além do card da categoria. Para ambos, a página pública de detalhe expôs um repositório GitHub; a API pública do GitHub confirmou que o repositório é público e permitiu fixar o SHA mais recente do branch `main` observado na consulta. O caminho relativo informado é o caminho-raiz do repositório (`/`), porque a página de detalhe não apontou para um subdiretório específico.

### 1. Vercel Shop

- **Título na categoria:** Vercel Shop
- **URL de catálogo:** https://vercel.com/templates/next.js/vercel-shop
- **Descrição observada:** “Production-ready Shopify storefront on Next.js”.
- **Repository:** https://github.com/vercel/shop
- **Caminho relativo:** `/`
- **Branch consultado:** `main`
- **Commit/SHA observado:** `52b3b87d78b724f8b0b49c3be37fe44f03a493a2`
- **Commit URL:** https://github.com/vercel/shop/commit/52b3b87d78b724f8b0b49c3be37fe44f03a493a2
- **Licença observada na API pública do GitHub:** MIT (`spdx_id: MIT`)
- **Natureza da evidência:** detalhe público da Vercel aponta para `vercel/shop`; API pública do GitHub confirma repositório público, branch padrão `main`, licença e SHA do commit mais recente. Isso é evidência de proveniência e metadados, não de execução.

### 2. Medusa Next.js Ecommerce Store Starter

- **Título na categoria:** Medusa Next.js Ecommerce Store Starter
- **URL de catálogo:** https://vercel.com/templates/next.js/medusa
- **Descrição observada:** template ecommerce com Next.js App Router, Medusa, TailwindCSS, busca Algolia e checkout Stripe.
- **Repository:** https://github.com/medusajs/nextjs-starter-medusa
- **Caminho relativo:** `/`
- **Branch consultado:** `main`
- **Commit/SHA observado:** `9818886f06e493cb2249733d114d339aa216ef00`
- **Commit URL:** https://github.com/medusajs/nextjs-starter-medusa/commit/9818886f06e493cb2249733d114d339aa216ef00
- **Licença observada na API pública do GitHub:** MIT (`spdx_id: MIT`)
- **Estado relevante observado:** a API pública marca o repositório como `archived: true`; a página de detalhe informa que o repositório está deprecated e recomenda `dtc-starter`.
- **Natureza da evidência:** detalhe público da Vercel aponta para o repositório e para a licença; API pública do GitHub confirma repositório, SHA, licença e arquivamento. O aviso de depreciação é uma limitação material para reuso e não é evidência de runtime.

## Paginação, renderização e cobertura

A categoria é renderizada publicamente com cards e carregamento incremental. A primeira resposta/renderização apresentou 12 cards e `Load More`; uma interação pública carregou mais nove cards. A observação não estabeleceu se o segundo conjunto é a última página, se existem itens ocultos por filtros, se a ordenação é estável ou se conteúdo adicional depende de JavaScript, região, cache ou mudanças posteriores da Vercel.

O sitemap público `https://vercel.com/sitemap.xml` foi consultado, mas sua resposta foi truncada pelo tamanho da extração e não constituiu uma lista independente e completa da categoria ecommerce. Portanto, ele não pode ser usado para afirmar cobertura exaustiva. Também não foi encontrado um endpoint público documentado e garantidamente completo para a galeria. A cobertura desta exploração é, assim, `partial`: há uma lista observada e reprodutível de 21 links públicos na sessão, mas não uma enumeração completa comprovada.

## Limitações e salvaguardas

- A rota e os detalhes públicos são páginas de marketplace/catálogo; não foram executados `npm`, `pip`, scripts de candidatos, builds, deploys, testes de integração ou verificações de checkout.
- Para 19 das 21 entradas, a exploração confirmou o card e a URL pública da Vercel, mas não confirmou repositório, caminho relativo, commit/SHA ou licença. Esses itens permanecem descobertos, não enriquecidos.
- Não houve clone ou espelhamento de código-fonte. Nenhum dashboard privado, credencial, token, identificador de conta ou segredo foi acessado ou armazenado.
- A presença na categoria não implica que a implementação ainda esteja mantida, seja licenciada de forma compatível ou funcione sem serviços/segredos externos.
- O template Medusa é uma exceção importante: a fonte pública vinculada está arquivada e marcada como deprecated; qualquer reutilização exigiria revisão específica e consulta ao substituto recomendado.
- SHAs registrados são os commits mais recentes retornados pela API pública no momento da consulta, não uma afirmação de que a página da Vercel esteja fixada exatamente nesses commits.

## Referências

[1]: https://vercel.com/templates/ecommerce "Vercel Ecommerce Website Templates and Starters"
[2]: https://vercel.com/templates/next.js/vercel-shop "Vercel Shop template detail"
[3]: https://github.com/vercel/shop "Vercel Shop public repository"
[4]: https://api.github.com/repos/vercel/shop "GitHub API metadata for vercel/shop"
[5]: https://api.github.com/repos/vercel/shop/commits?per_page=1 "Latest public commit for vercel/shop"
[6]: https://vercel.com/templates/next.js/medusa "Medusa Next.js Ecommerce Store Starter template detail"
[7]: https://github.com/medusajs/nextjs-starter-medusa "Medusa Next.js starter public repository"
[8]: https://api.github.com/repos/medusajs/nextjs-starter-medusa "GitHub API metadata for nextjs-starter-medusa"
[9]: https://api.github.com/repos/medusajs/nextjs-starter-medusa/commits?per_page=1 "Latest public commit for nextjs-starter-medusa"
[10]: https://vercel.com/sitemap.xml "Vercel public sitemap"
