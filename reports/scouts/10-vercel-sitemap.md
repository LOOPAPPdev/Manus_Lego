# Scout 10 — Vercel sitemap público

- **Rota:** `https://vercel.com/sitemap.xml`
- **Tipo:** public Vercel sitemap route
- **Data/hora da coleta:** 2026-11-20, aproximadamente 07:04–07:05 (fuso da sessão `-03:00`)
- **Coverage:** `partial`

## Conclusão

A rota respondeu publicamente com XML válido (`application/xml; charset=utf-8`) e foi analisada integralmente fora da ferramenta de visualização. O XML continha 9.569 elementos `loc`; 630 URLs continham `/templates/`, distribuídas em 109 grupos de primeiro nível. Na mesma amostra foram observadas 106 URLs de grupo/categoria e 524 URLs de template mais específicas, pela estrutura de caminho observada.

Isso demonstra **descobribilidade pública** de categorias e templates, mas não demonstra cobertura completa do marketplace Vercel. A classificação permanece `partial`: o sitemap é uma fotografia da publicação observada no momento da coleta, não uma lista independente e garantidamente exaustiva, e a própria documentação local determina que sitemaps/paginação da Vercel sejam tratados como potencialmente incompletos [1].

## Evidências verificáveis

1. A rota principal [sitemap público da Vercel](https://vercel.com/sitemap.xml) respondeu com XML e URLs públicas. A análise local do corpo completo contou 9.569 `loc` e 630 URLs contendo `/templates/`. A ferramenta de leitura web marcou a resposta como parcial por truncamento de apresentação, mas o download HTTP independente recebeu 1.333.063 bytes e o XML foi parseado com sucesso; portanto, a contagem acima não foi inferida do trecho truncado da ferramenta.
2. A categoria [AI app templates and examples](https://vercel.com/templates/ai) respondeu publicamente e listou URLs como `https://vercel.com/templates/next.js/ai-alt-text-generator` e `https://vercel.com/templates/next.js/morphic-ai-answer-engine-generative-ui`. A página também foi marcada como parcial pela ferramenta por tamanho de retorno, então seus itens não devem ser tratados como lista completa.
3. A categoria [Find your Starter Templates](https://vercel.com/templates/starter) respondeu publicamente e listou, entre outros, `https://vercel.com/templates/next.js/app-directory`, `https://vercel.com/templates/astro/welcome-to-astro` e `https://vercel.com/templates/python/python-hello-world`. A listagem foi truncada pela ferramenta de leitura e não sustenta exaustividade.
4. A categoria [Find your authentication template](https://vercel.com/templates/authentication) respondeu com status público e listou exemplos, incluindo `https://vercel.com/templates/next.js/kinde-next-js-starter`, `https://vercel.com/templates/svelte/sveltekit-authentication` e `https://vercel.com/templates/next.js/clerk-authentication-starter`.
5. A página individual [Next.js App Router Playground](https://vercel.com/templates/next.js/app-directory) expôs no frontmatter público o repositório `https://github.com/vercel/app-playground`, além do título e descrição do template. A API pública do GitHub identificou o repositório canônico como `vercel/next-app-router-playground`, branch padrão `main`, com SHA observado `b5c0f7eaf1ed070d20aa29f435ce22a48b987684` em [API de commit](https://api.github.com/repos/vercel/app-playground/commits/HEAD). O caminho relativo do template dentro do repositório não foi indicado pela página; não foi inventado.
6. A página individual [Welcome to Astro](https://vercel.com/templates/astro/welcome-to-astro) expôs no frontmatter público o repositório e caminho `https://github.com/withastro/astro/tree/main/examples/basics`. A API pública do GitHub confirmou o repositório `withastro/astro`, branch `main`, com SHA observado `d2b3c9656279d451b5cd831fdb1ca08fff171d72` em [API de commit](https://api.github.com/repos/withastro/astro/commits/main). O caminho relativo verificável é `examples/basics`.

## Registros realmente verificados

- **Registro de descoberta do sitemap:** URL `https://vercel.com/sitemap.xml`; repositório, caminho relativo e commit/SHA **não se aplicam/não são expostos pelo sitemap**. Evidência: XML público parseável e contagem acima.
- **Registro de categoria:** URL `https://vercel.com/templates/ai`; repositório, caminho relativo e commit/SHA **não foram expostos pela página de categoria**. Evidência: título, lista de links e descrições públicas; não é evidência de funcionamento em runtime.
- **Registro de categoria:** URL `https://vercel.com/templates/starter`; repositório, caminho relativo e commit/SHA **não foram expostos pela página de categoria**. Evidência: título e links públicos observados.
- **Registro de categoria:** URL `https://vercel.com/templates/authentication`; repositório, caminho relativo e commit/SHA **não foram expostos pela página de categoria**. Evidência: título e links públicos observados.
- **Registro de template:** título `Next.js App Router Playground`; URL `https://vercel.com/templates/next.js/app-directory`; repositório declarado pela página `vercel/app-playground` (URL pública `https://github.com/vercel/app-playground`); caminho relativo **não indicado**; SHA observado `b5c0f7eaf1ed070d20aa29f435ce22a48b987684` via API pública. A página também declara o demo `https://app-dir.vercel.app/`, mas nenhum demo foi usado como prova de runtime.
- **Registro de template:** título `Welcome to Astro`; URL `https://vercel.com/templates/astro/welcome-to-astro`; repositório `withastro/astro`; caminho relativo `examples/basics`; SHA observado `d2b3c9656279d451b5cd831fdb1ca08fff171d72` via API pública. A página declara ainda o demo `https://astro-template.vercel.app/`, que não foi usado como prova de runtime.

## Limitações explícitas

- O sitemap prova que URLs eram publicamente descobríveis na coleta; não prova que os templates estão funcionando, compilam, são seguros, têm dependências compatíveis ou são licenciados para reutilização.
- A contagem de 9.569 `loc` e 630 URLs de template é observada no XML baixado naquele momento, não uma garantia de cobertura histórica, futura ou completa do marketplace.
- As respostas das páginas `/templates/ai` e `/templates/starter` foram truncadas pela ferramenta de leitura; os exemplos citados são apenas amostras.
- A página de autenticação foi lida integralmente, mas a quantidade de itens exibida na página ainda não é tratada como inventário exaustivo independente.
- O sitemap mistura templates, documentação, blog, changelog e outras áreas; somente URLs contendo `/templates/` foram contadas para o escopo deste scout.
- Nenhuma fonte pública consultada nesta rota forneceu, para todos os 630 registros observados, um repositório, caminho relativo e SHA. Os dois vínculos de repositório e SHAs acima são apenas os dois registros individuais efetivamente verificados.
- Não foram clonados repositórios, executados scripts de candidatos, instaladas dependências, acessados dashboards privados ou armazenados segredos.
- Os SHAs são pontos observados na API pública no momento da coleta; não foram usados para afirmar que o conteúdo do template foi executado ou que a página Vercel permanece sincronizada com esse commit.

## References

[1]: https://vercel.com/sitemap.xml "Vercel public sitemap"
[2]: https://vercel.com/templates/ai "Vercel AI templates category"
[3]: https://vercel.com/templates/starter "Vercel starter templates category"
[4]: https://vercel.com/templates/authentication "Vercel authentication templates category"
[5]: https://vercel.com/templates/next.js/app-directory "Vercel Next.js App Router Playground template"
[6]: https://github.com/vercel/app-playground "Public GitHub repository link exposed by the Vercel template"
[7]: https://api.github.com/repos/vercel/app-playground/commits/HEAD "GitHub public commit API for app-playground"
[8]: https://vercel.com/templates/astro/welcome-to-astro "Vercel Welcome to Astro template"
[9]: https://github.com/withastro/astro/tree/main/examples/basics "Public GitHub source path exposed by the Vercel template"
[10]: https://api.github.com/repos/withastro/astro/commits/main "GitHub public commit API for Astro main"
