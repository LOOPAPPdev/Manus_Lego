# Scout Vercel — categoria pública Cron

## Conclusão

A rota pública `https://vercel.com/templates/cron` foi acessível e exibiu três entradas observáveis: **Vercel + DBOS Integration**, **Vercel Cron Job Example** e **Cron OG Cards** [1]. A página não forneceu evidência pública suficiente para afirmar que esses três cards são a enumeração completa da categoria; por isso, a cobertura deste scout é **partial**. A consulta ao sitemap público foi truncada pelo próprio extrator e não constituiu uma lista exaustiva independente [2].

A presença de descrição, demo ou link de deploy na galeria foi tratada somente como metadado de descoberta. Não foi feita alegação de funcionamento em runtime, pois nenhum candidato foi executado ou validado por implantação.

## Registros verificados

### 1. Vercel + DBOS Integration

- Página pública da galeria: `https://vercel.com/templates/next.js/vercel-dbos-integration` [3]
- Título observado: `Vercel + DBOS Integration`.
- Descrição observada: `Run durable background workflows from your Vercel app.`
- Origem pública indicada pela própria página: `https://github.com/dbos-inc/dbos-vercel-integration` [3]
- Repositório: `dbos-inc/dbos-vercel-integration`.
- Caminho relativo: `.` (a página aponta para a raiz do repositório; a árvore do commit contém os arquivos do template na raiz).
- Commit/SHA verificado no branch `main`: `8cb15fb7534a2e7ca92cac0e814fcdcaa99ce484` [4]
- Evidência de árvore: a árvore recursiva desse commit retornou `truncated: false` e listou, entre outros, `README.md`, `LICENSE`, `package.json`, `vercel.json`, `app/api/dbos/route.ts` e `app/page.tsx` [5].
- Licença: **MIT**, confirmada pelo metadado público do repositório e pelo arquivo `LICENSE` no commit consultado [6].
- Escopo da evidência: a página descreve workflows em background acionados por Vercel Cron, mas isso é descrição da galeria; não é prova de execução em runtime [3].

### 2. Vercel Cron Job Example

- Página pública da galeria: `https://vercel.com/templates/next.js/vercel-cron` [7]
- Título observado: `Vercel Cron Job Example`.
- Descrição observada: `A Next.js app that uses Vercel Cron Jobs to update data at different intervals.`
- Origem pública indicada pela própria página: `https://github.com/vercel/examples/tree/main/solutions/cron` [7]
- Repositório: `vercel/examples`.
- Caminho relativo: `solutions/cron`.
- Commit/SHA verificado no branch `main`: `a4b4827297bec79b81ddb2ff22a53089ebe88cd8` [8]
- Evidência de conteúdo no caminho: a API pública de contents listou `solutions/cron/README.md` (SHA `90f53bd476ff1d1070beba3ef94a7a99efb0ceb2`), `package.json` (SHA `f782b58be7dba6464f54c574c36164bd6b33ac62`), `vercel.json` e outros arquivos do diretório [9].
- Licença: **MIT**, confirmada no arquivo público `license.md` do repositório oficial [10]. Esta confirmação é do repositório; o registro não presume licenças diferentes para dependências ou conteúdo externo.
- Escopo da evidência: a galeria e o README descrevem o uso de Vercel Cron Jobs, mas nenhum runtime foi executado neste scout [7].

### 3. Cron OG Cards

- Página pública da galeria: `https://vercel.com/templates/next.js/cron-og` [11]
- Título observado: `Cron OG Cards`.
- Descrição observada: `A template for scheduled updates to your OG social cards using Vercel Cron Jobs and Upstash Redis.`
- Origem pública indicada pela própria página: `https://github.com/gt-codes/og-cron` [11]
- Repositório: `gt-codes/og-cron`.
- Caminho relativo: `.` (a página aponta para a raiz do repositório).
- Commit/SHA verificado no branch `main`: `84b736881e452724e2af4eb7e05f0d027ac6f0cd` [12]
- Evidência de árvore: a árvore recursiva do commit retornou `truncated: false` e listou `README.md`, `package.json`, `vercel.json`, `src/app/api/cron/route.ts` e `src/app/api/og/route.tsx` [13].
- Licença: **não confirmada**. O metadado público do repositório informa `license: null` e a listagem da raiz consultada não mostrou arquivo `LICENSE` [14] [15].
- Escopo da evidência: a página afirma atualizações periódicas de dados e geração de imagens OG, mas isso permanece metadado/documentação pública, não validação de runtime [11].

## Evidências de descoberta e cobertura

1. A página renderizada da categoria mostra o título “Find your cron template”, o texto sobre Vercel Cron Jobs e exatamente os três cards acima; também mostra um campo de busca e um botão `Filters` [1].
2. A extração textual da mesma rota expõe os links relativos `/templates/next.js/vercel-dbos-integration`, `/templates/next.js/vercel-cron` e `/templates/next.js/cron-og` [1].
3. O sitemap público `https://vercel.com/sitemap.xml` foi acessível, porém o resultado recebido foi explicitamente `partial`/truncated pelo extrator. Assim, ele não prova enumeração completa da categoria [2].
4. A documentação do projeto determina que a galeria Vercel pode ser dinamicamente paginada e que a cobertura deve permanecer não exaustiva sem lista independente completa [16].

## Limitações

- A categoria foi observada em uma página pública, mas não houve evidência independente de que a lista de três cards seja completa.
- O sitemap retornado foi truncado e não foi usado para inferir completude.
- Não foram usados dashboards privados, credenciais, tokens ou URLs privadas.
- Não foram executados scripts, instalações, builds, deploys ou aplicações dos candidatos.
- Demos e links de deploy foram preservados apenas como metadados observados nas páginas; não foram tratados como prova de funcionamento.
- A licença de `gt-codes/og-cron` permanece desconhecida; nenhum SPDX foi inferido por analogia.
- Para os repositórios externos, os SHAs são os commits públicos atuais observados nos branches `main` durante esta consulta; a galeria não forneceu um SHA próprio.

## References

[1]: https://vercel.com/templates/cron "Vercel Cron Templates category"
[2]: https://vercel.com/sitemap.xml "Vercel public sitemap"
[3]: https://vercel.com/templates/next.js/vercel-dbos-integration "Vercel + DBOS Integration template"
[4]: https://api.github.com/repos/dbos-inc/dbos-vercel-integration/git/ref/heads/main "DBOS integration main branch reference"
[5]: https://api.github.com/repos/dbos-inc/dbos-vercel-integration/git/trees/8cb15fb7534a2e7ca92cac0e814fcdcaa99ce484?recursive=1 "DBOS integration commit tree"
[6]: https://api.github.com/repos/dbos-inc/dbos-vercel-integration/license "DBOS integration license metadata"
[7]: https://vercel.com/templates/next.js/vercel-cron "Vercel Cron Job Example template"
[8]: https://api.github.com/repos/vercel/examples/git/ref/heads/main "Vercel examples main branch reference"
[9]: https://api.github.com/repos/vercel/examples/contents/solutions/cron "Vercel examples cron directory contents"
[10]: https://api.github.com/repos/vercel/examples/license "Vercel examples license metadata"
[11]: https://vercel.com/templates/next.js/cron-og "Cron OG Cards template"
[12]: https://api.github.com/repos/gt-codes/og-cron/git/ref/heads/main "Cron OG repository main branch reference"
[13]: https://api.github.com/repos/gt-codes/og-cron/git/trees/84b736881e452724e2af4eb7e05f0d027ac6f0cd?recursive=1 "Cron OG commit tree"
[14]: https://api.github.com/repos/gt-codes/og-cron "Cron OG repository metadata"
[15]: https://api.github.com/repos/gt-codes/og-cron/contents/?ref=84b736881e452724e2af4eb7e05f0d027ac6f0cd "Cron OG repository root contents"
[16]: https://github.com/LOOPAPPdev/Manus_Lego/blob/main/docs/pipeline.md "Manus LEGO pipeline and coverage policy"
