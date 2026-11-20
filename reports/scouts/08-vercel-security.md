# Scout — Vercel Security

**Rota:** https://vercel.com/templates/security  
**Tipo:** public Vercel category route  
**Data da observação:** 2026-11-20 07:01–07:02 (UTC−03:00)  
**Coverage:** `partial`

## Resultado observado

A rota pública respondeu com o título “Find your Security Templates” e exibiu quatro entradas no conteúdo renderizado: **Advanced AI Bot Protection**, **Arcjet Next.js Example App**, **Evervault: Encryption Starter Kit for Next.js** e **ChatGPT app with Next.js** [1]. A extração pública não mostrou controles de paginação nem uma contagem total; isso é apenas uma observação do conteúdo retornado, não prova de que a categoria tenha somente quatro registros.

O sitemap público da Vercel foi acessível, mas a resposta foi marcada como parcial/truncada pelo extrator: o documento tinha 809.136 caracteres originais e apenas 12.014 retornados [2]. Portanto ele não sustenta uma enumeração completa dos templates da categoria. O repositório oficial `vercel/examples` também declara que a galeria inclui exemplos além do monorepo oficial, e que a publicação depende de metadados de template no README [3]. Esses fatos reforçam a classificação `partial`, e não `complete`.

## Registros públicos verificáveis

Os quatro registros abaixo foram realmente descobertos na rota e tiveram o link de origem exposto na página individual. A verificação de SHA foi feita via API pública do GitHub; a consulta de conteúdo no SHA fixado confirmou a existência do caminho ou dos arquivos do repositório. Isso comprova proveniência e inventário de arquivos, não funcionamento em runtime.

1. **Advanced AI Bot Protection** — página Vercel [4]. Repositório `vercel/ai`; caminho relativo `examples/next-openai-kasada-bot-protection`; commit/SHA `2613bb45d43f7548b12b4e8d74d200656fe9584d`. A consulta de commits filtrada pelo caminho retornou esse SHA [5]. A consulta de conteúdo no mesmo SHA confirmou, entre outros, `README.md`, `.env.local.example`, `app/` e `kasada/` [6]. A página descreve integração com Kasada e exige configuração de endpoint/chaves; nenhum teste de build, deploy ou endpoint foi executado neste scout.

2. **Arcjet Next.js Example App** — página Vercel [7]. Repositório `arcjet/example-nextjs`; caminho relativo `.` (a página aponta para a raiz do repositório); commit/SHA `2ecb602b2f34c0bc1b02764f9c28a45e700da3a3`. A API pública de commits retornou esse SHA [8], e a consulta de conteúdo nesse SHA confirmou arquivos da raiz, incluindo `.env.local.example` e `tsconfig.json` [9]. A página expõe o demo `https://example.arcjet.com/` e descreve áreas de proteção contra bots, rate limiting e ataques, mas essas afirmações da documentação não foram tratadas como teste de runtime.

3. **Evervault: Encryption Starter Kit for Next.js** — página Vercel [10]. Repositório `evervault/evervault-starter-kit`; caminho relativo `.`; commit/SHA `f0025bd115dd212551bb3c11bf483611e26b2dda`. A API pública de commits retornou esse SHA [11], e a consulta de conteúdo confirmou `README.md`, `package.json`, `.env.example`, `app/`, `components/` e `public/` no mesmo SHA [12]. A página também expõe o demo `https://demo.evervault.com/`. Não foi feita implantação, execução, validação de integração Evervault ou auditoria de licença neste scout.

4. **ChatGPT app with Next.js** — página Vercel [13]. Repositório `vercel-labs/chatgpt-apps-sdk-nextjs-starter`; caminho relativo `.`; commit/SHA `b911c88f93c0a0a9b39d650743fb1085db39a147`. A API pública de commits retornou esse SHA [14], e a consulta de conteúdo confirmou `README.md`, `app/`, `middleware.ts`, `next.config.ts` e `baseUrl.ts` [15]. A página expõe o demo `https://chatgpt-apps-sdk-nextjs-starter.labs.vercel.dev/`. A própria mensagem do commit descreve uma atualização de Next.js relacionada a advisory, mas isso é histórico de commit e não uma garantia atual de segurança ou runtime; nenhuma execução foi realizada.

## Fonte relacionada verificada, não contada como entrada da rota

O README do repositório oficial `vercel/examples` referencia o exemplo **Bot Protection with DataDome** e o caminho `edge-middleware/bot-protection-datadome` [3]. A página do diretório confirmou esse caminho, seus arquivos e metadados de template [16]. A API pública de commits retornou o SHA `cb2643e806ee6189c28554afdc65f8587411f116` para esse caminho [17], e a consulta de conteúdo nesse SHA confirmou `README.md`, `.env.example`, `middleware.ts`, `package.json` e demais arquivos do exemplo [18]. Contudo, esse registro não apareceu no conteúdo extraído da rota `/templates/security` nesta observação, portanto não foi contado entre os quatro registros da rota.

## Limitações e status de evidência

- A cobertura é `partial`: quatro entradas foram observadas diretamente na resposta pública da rota, mas não há evidência independente de que esse conjunto seja exaustivo.
- A página é conteúdo de galeria e seus READMEs/metadados são evidência de descoberta e descrição, não prova de funcionamento em runtime. Não foram executados código, scripts de candidatos, instalação de dependências, builds, deploys ou testes de integração.
- O sitemap público foi acessível, mas o retorno foi truncado pelo extrator e não pode ser usado para contar ou fechar a categoria.
- Não foi possível verificar, apenas com a resposta pública observada, se existe paginação adicional, carregamento por interação ou filtros que alterem o conjunto renderizado.
- Links de origem foram registrados somente em hosts públicos HTTPS. Nenhum dashboard privado, credencial, segredo ou identificador de conta foi acessado ou armazenado.
- Licenças dos quatro repositórios de terceiros não foram inferidas a partir da página Vercel; devem ser revisadas antes de qualquer reutilização. O repositório oficial `vercel/examples` informa MIT no nível do repositório [3], mas isso não transfere licença para os demais registros.
- O campo de commit representa o SHA consultado no GitHub para o repositório/caminho público observado. Ele não é uma garantia de que a galeria Vercel esteja materializando exatamente a mesma revisão em todos os momentos.

## References

[1]: https://vercel.com/templates/security "Vercel Security Templates category"
[2]: https://vercel.com/sitemap.xml "Vercel public sitemap"
[3]: https://github.com/vercel/examples "vercel/examples repository and template publishing guidance"
[4]: https://vercel.com/templates/next.js/advanced-ai-bot-protection "Advanced AI Bot Protection template"
[5]: https://api.github.com/repos/vercel/ai/commits?path=examples/next-openai-kasada-bot-protection&per_page=1 "GitHub commits for Kasada example path"
[6]: https://api.github.com/repos/vercel/ai/contents/examples/next-openai-kasada-bot-protection?ref=2613bb45d43f7548b12b4e8d74d200656fe9584d "GitHub contents for Kasada example at pinned SHA"
[7]: https://vercel.com/templates/next.js/arcjet-next-js-example-app "Arcjet Next.js Example App template"
[8]: https://api.github.com/repos/arcjet/example-nextjs/commits?per_page=1 "GitHub latest commit for Arcjet example repository"
[9]: https://api.github.com/repos/arcjet/example-nextjs/contents?ref=2ecb602b2f34c0bc1b02764f9c28a45e700da3a3 "GitHub root contents for Arcjet example at pinned SHA"
[10]: https://vercel.com/templates/next.js/evervault-starter-kit "Evervault Encryption Starter Kit template"
[11]: https://api.github.com/repos/evervault/evervault-starter-kit/commits?per_page=1 "GitHub latest commit for Evervault starter repository"
[12]: https://api.github.com/repos/evervault/evervault-starter-kit/contents?ref=f0025bd115dd212551bb3c11bf483611e26b2dda "GitHub root contents for Evervault starter at pinned SHA"
[13]: https://vercel.com/templates/next.js/chatgpt-app-with-next-js "ChatGPT app with Next.js template"
[14]: https://api.github.com/repos/vercel-labs/chatgpt-apps-sdk-nextjs-starter/commits?per_page=1 "GitHub latest commit for ChatGPT Apps SDK starter"
[15]: https://api.github.com/repos/vercel-labs/chatgpt-apps-sdk-nextjs-starter/contents?ref=b911c88f93c0a0a9b39d650743fb1085db39a147 "GitHub root contents for ChatGPT starter at pinned SHA"
[16]: https://github.com/vercel/examples/tree/main/edge-middleware/bot-protection-datadome "DataDome example directory in vercel/examples"
[17]: https://api.github.com/repos/vercel/examples/commits?path=edge-middleware/bot-protection-datadome&per_page=1 "GitHub commits for DataDome example path"
[18]: https://api.github.com/repos/vercel/examples/contents/edge-middleware/bot-protection-datadome?ref=cb2643e806ee6189c28554afdc65f8587411f116 "GitHub contents for DataDome example at pinned SHA"
