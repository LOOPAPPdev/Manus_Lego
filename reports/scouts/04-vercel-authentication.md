# Scout — Vercel authentication

**Rota:** https://vercel.com/templates/authentication  
**Tipo:** public Vercel category route  
**Data da observação:** 2026-11-20  
**Coverage:** `partial`

## Conclusão

A rota pública respondeu e renderizou uma listagem estática extraível de **28 entradas** nesta captura. A página apresenta título, descrição e links individuais para os templates, mas não informa um total de resultados, não expõe um controle de paginação na resposta extraída e não fornece uma garantia de completude. Portanto, a cobertura é `partial`, não `complete`. A própria documentação do projeto já alerta que a galeria Vercel é dinâmica/paginada e não tem descoberta exaustiva garantida [1].

A página individual de cada template contém frontmatter público com `links.repository`; isso é evidência de associação publicada entre o card Vercel e uma origem GitHub, não evidência de execução em runtime. Em oito entradas foi possível confirmar, adicionalmente, repositório público, branch/commit atual pela API pública do GitHub e caminho relativo indicado pela URL da página Vercel ou pelo próprio conteúdo da página. Nenhum template foi clonado, instalado, executado ou submetido a teste de build/runtime.

## Evidência da categoria

A extração pública da rota em [2] retornou estes 28 cards, na ordem observada:

1. eve Web Chat — https://vercel.com/templates/eve/eve-chat-template
2. Kinde Next.js Starter — https://vercel.com/templates/next.js/kinde-next-js-starter
3. MCP with Next.js and Descope — https://vercel.com/templates/next.js/mcp-with-next-js-and-descope
4. SvelteKit Authentication — https://vercel.com/templates/svelte/sveltekit-authentication
5. Gemini AI Chatbot — https://vercel.com/templates/next.js/gemini-ai-chatbot
6. Auth0 React Starter — https://vercel.com/templates/react/auth0-react
7. Clerk Authentication Starter — https://vercel.com/templates/next.js/clerk-authentication-starter
8. Auth0 Next.js Starter — https://vercel.com/templates/next.js/auth0-next-js-starter
9. Plasmic NextAuth Starter — https://vercel.com/templates/next.js/plasmic-nextauth-starter
10. Nuxt AI Chatbot — https://vercel.com/templates/nuxt/nuxt-ai-chatbot
11. eve Personal Agent — https://vercel.com/templates/nuxt/eve-personal-agent
12. Auth for subdomains — https://vercel.com/templates/next.js/subdomains-auth
13. Next.js SaaS Starter — https://vercel.com/templates/next.js/next-js-saas-starter
14. AI Headshot Generator — https://vercel.com/templates/next.js/headshot-ai
15. Liveblocks Starter Kit — https://vercel.com/templates/next.js/liveblocks-starter-kit
16. Stripe Subscription Starter — https://vercel.com/templates/next.js/subscription-starter
17. Supabase Starter — https://vercel.com/templates/next.js/supabase
18. Blog (with comments) — https://vercel.com/templates/next.js/blog-with-comments
19. SaaStart: Auth0 + Next.js SaaS Starter Kit — https://vercel.com/templates/next.js/auth0-nextjs-saas-starter
20. Chat SDK Community Agent — https://vercel.com/templates/next.js/chat-sdk-community-agent
21. Fullstack Blog with Next.js + Prisma — https://vercel.com/templates/next.js/fullstack-prisma-nextjs-blog
22. Partner Gallery — https://vercel.com/templates/next.js/supabase-partner-gallery
23. AgentGPT - AI Agents with Langchain & OpenAI — https://vercel.com/templates/next.js/agent-gpt
24. Whop SaaS Template — https://vercel.com/templates/next.js/whop-template
25. Coding Agent Template — https://vercel.com/templates/next.js/coding-agent-template
26. Taxonomy — https://vercel.com/templates/next.js/taxonomy
27. Chatbot — https://vercel.com/templates/next.js/chatbot
28. Precedent – Next.js Starter — https://vercel.com/templates/next.js/precedent

A resposta também inclui documentação adicional da Vercel, mas não há, na extração, um contador de resultados, uma indicação de “última página” ou uma declaração de inventário completo [2].

## Registros aprofundados e verificáveis

Os registros abaixo são **descoberta/referência**, não validação de funcionamento. O SHA é o commit resolvido no branch público consultado em 2026-11-20. O caminho é relativo ao repositório GitHub.

- **SvelteKit Authentication** — página Vercel [3]; repository `nextauthjs/sveltekit-auth-example`; caminho `apps/examples/sveltekit` (a página informa que o exemplo é mantido no monorepo `nextauthjs/next-auth`, enquanto o repositório público apontado é o espelho/exemplo); commit `879b182f6cf044d14727b69777d7e757423bcd28` no branch `main`; licença SPDX `ISC` observada no endpoint público do repositório [11] e SHA no endpoint de commits [19]. Natureza da evidência: frontmatter/link de origem + metadados GitHub + commit; runtime não verificado.

- **Clerk Authentication Starter** — página Vercel [4]; repository `clerk/nextjs-auth-starter-template`; caminho `.`; commit `9e5619c2a22d2db2adf76271fe32f65e8d3c0183` no branch `main`; o endpoint do repositório indica licença `null`, portanto nenhuma licença foi inferida [12]; SHA e árvore do commit foram confirmados publicamente [20]. Natureza da evidência: frontmatter/link de origem + metadados GitHub + commit; runtime não verificado.

- **Auth0 React Starter** — página Vercel [5]; repository `auth0-developer-hub/spa_react_javascript_hello-world`; caminho `vercel` (a própria URL do repositório publicada no frontmatter termina em `/tree/vercel`); commit `d0eefc6924f9335927478395730bbb42b2c3e92c` no branch `main`; licença SPDX `Apache-2.0` observada no endpoint público [13]; SHA confirmado no endpoint de commits [21]. Natureza da evidência: frontmatter/link de origem + metadados GitHub + commit; runtime não verificado.

- **Auth0 Next.js Starter** — página Vercel [6]; repository `auth0-samples/auth0-nextjs-samples`; caminho `Sample-01`; commit `99f4866f3358fa3e9fa1904f969da3ecbe26f6ad` no branch `main`; licença SPDX `MIT` observada no endpoint público [14]; o commit público contém arquivos sob `Sample-01`, incluindo `Sample-01/package.json` [22]. Natureza da evidência: frontmatter/link de origem + caminho no commit + metadados GitHub; runtime não verificado.

- **Supabase Starter** — página Vercel [7]; repository `vercel/next.js`; caminho `examples/with-supabase`; commit `6d5078c51e505f2387f644c39cbee0371cb3d1e1` no branch `canary`; licença SPDX `MIT` observada no endpoint público [15]; SHA confirmado no endpoint de commits [23]. Natureza da evidência: frontmatter/link de origem + metadados GitHub + commit; runtime não verificado. Como a página aponta para `canary`, o registro é sensível a mudanças do branch e não representa necessariamente o estado usado por uma implantação histórica.

- **Next.js SaaS Starter** — página Vercel [8]; repository `nextjs/saas-starter`; caminho `.`; commit `6e33e58b1e553a41fe22e6b941a7229a002de361` no branch `main`; licença SPDX `MIT` observada no endpoint público [16]; SHA e arquivos modificados foram confirmados [24]. Natureza da evidência: frontmatter/link de origem + metadados GitHub + commit; runtime não verificado.

- **Auth for subdomains** — página Vercel [9]; repository `vercel/examples`; caminho `solutions/subdomain-auth`; commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8` no branch `main`; licença SPDX `MIT` observada no endpoint público [17]; SHA confirmado no endpoint de commits [25]. Natureza da evidência: frontmatter/link de origem + metadados GitHub + commit; runtime não verificado.

- **Plasmic NextAuth Starter** — página Vercel [10]; repository `plasmicapp/plasmic-next-auth-example`; caminho `.`; commit `fa4599329096323df0f88c7467cb265d5c50f2b5` no branch `master`; o endpoint público indica licença `null`, logo a licença permanece desconhecida [18]; o commit contém `app/plasmic-host/page.tsx`, confirmando a árvore do repositório [26]. Natureza da evidência: frontmatter/link de origem + metadados GitHub + commit; runtime não verificado.

## Evidência de sitemap e limites de descoberta

O sitemap público `https://vercel.com/sitemap.xml` foi acessível, mas a resposta retornada pelo extrator estava marcada como `partial`/truncated: o documento original tinha aproximadamente 809 mil caracteres e apenas uma parte foi retornada [27]. Assim, o sitemap não foi usado para declarar uma lista completa da categoria. Também não foi usado nenhum endpoint interno ou não documentado da Vercel.

## Limitações explícitas

- Os 28 cards são o conjunto observável na resposta pública desta captura, não um inventário completo da categoria.
- A página não expõe, na resposta extraída, total, cursor, paginação ou critério de ordenação; a ausência de tais campos não prova que não existam na interface visual/dinâmica.
- Apenas oito páginas individuais foram aprofundadas até o link de origem e o commit; os demais 20 cards permanecem descobertos, mas não verificados neste scouting.
- Um link `repository` é evidência de proveniência publicada, não prova de que o código esteja íntegro, licenciado para qualquer uso, seguro, compilável ou funcionando em produção.
- Nenhum build, teste automatizado, deploy, login OAuth, integração de provedor ou demo foi executado. Descrições, READMEs e demos hospedadas não foram tratados como prova de runtime.
- Licença `null` nos metadados GitHub de Clerk e Plasmic foi preservada como desconhecida; não foi inventada licença a partir de README ou do fato de o código ser público.
- Não foram coletados segredos, dashboards privados, tokens, identificadores privados ou credenciais.

## References

[1]: https://github.com/LOOPAPPdev/Manus_Lego/blob/main/docs/pipeline.md "Manus LEGO pipeline and Vercel gallery limitations"
[2]: https://vercel.com/templates/authentication "Vercel authentication templates category"
[3]: https://vercel.com/templates/svelte/sveltekit-authentication "SvelteKit Authentication template"
[4]: https://vercel.com/templates/next.js/clerk-authentication-starter "Clerk Authentication Starter template"
[5]: https://vercel.com/templates/react/auth0-react "Auth0 React Starter template"
[6]: https://vercel.com/templates/next.js/auth0-next-js-starter "Auth0 Next.js Starter template"
[7]: https://vercel.com/templates/next.js/supabase "Supabase Starter template"
[8]: https://vercel.com/templates/next.js/next-js-saas-starter "Next.js SaaS Starter template"
[9]: https://vercel.com/templates/next.js/subdomains-auth "Auth for subdomains template"
[10]: https://vercel.com/templates/next.js/plasmic-nextauth-starter "Plasmic NextAuth Starter template"
[11]: https://api.github.com/repos/nextauthjs/sveltekit-auth-example "GitHub metadata for sveltekit-auth-example"
[12]: https://api.github.com/repos/clerk/nextjs-auth-starter-template "GitHub metadata for nextjs-auth-starter-template"
[13]: https://api.github.com/repos/auth0-developer-hub/spa_react_javascript_hello-world "GitHub metadata for Auth0 React sample"
[14]: https://api.github.com/repos/auth0-samples/auth0-nextjs-samples "GitHub metadata for Auth0 Next.js samples"
[15]: https://api.github.com/repos/vercel/next.js "GitHub metadata for Next.js"
[16]: https://api.github.com/repos/nextjs/saas-starter "GitHub metadata for saas-starter"
[17]: https://api.github.com/repos/vercel/examples "GitHub metadata for Vercel examples"
[18]: https://api.github.com/repos/plasmicapp/plasmic-next-auth-example "GitHub metadata for Plasmic NextAuth example"
[19]: https://api.github.com/repos/nextauthjs/sveltekit-auth-example/commits/main "Current main commit for sveltekit-auth-example"
[20]: https://api.github.com/repos/clerk/nextjs-auth-starter-template/commits/main "Current main commit for Clerk starter"
[21]: https://api.github.com/repos/auth0-developer-hub/spa_react_javascript_hello-world/commits/main "Current main commit for Auth0 React sample"
[22]: https://api.github.com/repos/auth0-samples/auth0-nextjs-samples/commits/main "Current main commit for Auth0 Next.js samples"
[23]: https://api.github.com/repos/vercel/next.js/commits/canary "Current canary commit for Next.js"
[24]: https://api.github.com/repos/nextjs/saas-starter/commits/main "Current main commit for saas-starter"
[25]: https://api.github.com/repos/vercel/examples/commits/main "Current main commit for Vercel examples"
[26]: https://api.github.com/repos/plasmicapp/plasmic-next-auth-example/commits/master "Current master commit for Plasmic NextAuth example"
[27]: https://vercel.com/sitemap.xml "Vercel public sitemap"
