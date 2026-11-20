# Scout 25 — Cloudflare VibeSDK

## Identificação e cobertura

- **source_id:** `25-cloudflare-vibesdk`
- **label:** Cloudflare VibeSDK
- **rota de entrada:** https://github.com/cloudflare/vibesdk
- **repositório:** `cloudflare/vibesdk`
- **provedor:** GitHub público / Cloudflare
- **branch observado:** `main`
- **commit/SHA observado:** `32c9e429cd2712ea5959a89f65ae434162b89229`
- **data do commit observada:** 2026-10-22T01:15:27Z
- **coverage:** `partial`

A cobertura é `partial` porque a API pública forneceu uma árvore recursiva completa para o commit observado (`truncated: false`) e foram lidos o README, a licença, o guia de setup, `package.json` e `wrangler.jsonc`, mas não foi feita auditoria exaustiva de todos os arquivos, dependências transitivas, histórico, branches, releases, vulnerabilidades, build ou execução. A inspeção foi somente documental e de metadados; nenhum código foi clonado, instalado ou executado.

## Proveniência, branch e árvore

A API pública do GitHub identifica o repositório como público, não-fork, com branch padrão `main`, e aponta o commit atual de `main` para `32c9e429cd2712ea5959a89f65ae434162b89229`. A resposta do branch informa que o commit é uma fusão assinada e verificada pelo GitHub, com mensagem `Merge pull request #460 from cloudflare/staging / Staging -> Main`. Essa é uma propriedade do commit publicado, não uma validação do comportamento do software.

A consulta pública da árvore recursiva em `main` retornou a raiz com SHA `32c9e429cd2712ea5959a89f65ae434162b89229` e `truncated: false`. Os caminhos observados incluem, entre outros, `docs/`, `migrations/`, `packages/artifacts-viewer/`, `scripts/`, `sdk/`, `shared/`, `space/`, `src/`, `test/`, `worker/`, `README.md`, `LICENSE`, `package.json`, `wrangler.jsonc`, `SandboxDockerfile` e arquivos de configuração TypeScript/Vite/Vitest. Isso sustenta um inventário de caminhos para esse commit; não sustenta que cada arquivo tenha sido semanticamente revisado.

## README e capacidades declaradas

No caminho `README.md` do SHA observado, o projeto se descreve como uma plataforma open source e agentic para construir e implantar aplicações full-stack sobre a plataforma Cloudflare. O README declara um fluxo com agente de código, esclarecimentos humanos, workspace ao vivo, previews dinâmicos, inspeção do console do navegador, armazenamento SQLite por aplicação em Durable Object Facet, histórico em Cloudflare Artifacts, roteamento de provedores via AI Gateway, progresso em tempo real e exportação de projetos.

A arquitetura documentada no README nomeia `ThinkAgent`, `SpaceDO`, Cloudflare Artifacts, Worker Loader, uma aplicação gerada e AI Gateway. O workflow descrito é entender, construir, salvar restore points, implantar preview, verificar, reparar e transmitir progresso. O README também declara que o acesso Bash do workspace é desabilitado e descreve isolamento por projeto, autorização de previews assinados e restore points reversíveis.

Esses itens são declarações da documentação do repositório no commit fixado. Não foram tratados como prova de que o fluxo funciona, de que os controles são eficazes, nem de que uma implantação foi realizada.

## Setup, requisitos e limites operacionais declarados

O `docs/setup.md` observado declara Node.js 22 ou posterior, conta Cloudflare com acesso por API e token Cloudflare como requisitos. Para recursos remotos e produção, documenta Workers Paid, Workers for Platforms e, quando aplicável, Advanced Certificate Manager. O setup interativo é descrito como capaz de coletar credenciais, configurar domínio, AI Gateway, provedores de modelo, OAuth, KV, D1, R2, migrações e arquivos `.dev.vars`/`.prod.vars`.

O README lista comandos para desenvolvimento, build, typecheck, lint, testes e deploy; `package.json` confirma esses scripts no commit observado, além de indicar `engines.node` como `>=22`, workspace `space`, versão do pacote `1.5.0` e dependências diretas de React, Vite, Wrangler, Vitest, pacotes Cloudflare, Hono, Drizzle e outras bibliotecas. A presença desses scripts e dependências é metadado de configuração, não evidência de que tenham sido executados com sucesso.

O guia de setup documenta que previews atuais usam `SPACE_DO`, `LOADER` e Dynamic Workers; Artifacts é opcional atrás de `ENABLE_ARTIFACTS` para o filesystem padrão baseado em SQLite. Também declara que Docker não é necessário para o caminho atual de preview Think/SpaceDO, embora `SandboxDockerfile` e configuração de container permaneçam no repositório para tooling legado ou outros usos documentados.

O mesmo guia explicita limitações do botão de deploy dentro da interface de chat: exige domínio customizado, ao menos uma implantação inicial, dispatch bindings remotos e um dispatch worker em execução; o modo somente local ainda não é suportado para esse recurso. Também registra que falhas de build devem ser investigadas no bundler e falhas de runtime da aplicação no console do navegador. Essas são instruções e limitações declaradas pela documentação, não resultados de teste deste scout.

## Configuração observada

No caminho `wrangler.jsonc`, o commit observado declara o worker principal em `worker/index.ts`, assets em `dist/client`, compatibilidade Node, observabilidade, dispatch namespace, bindings `AI` e `BROWSER`, Artifacts, containers, D1, Durable Objects, Worker Loader, R2, KV, migrações e rotas documentadas. O arquivo contém identificadores públicos de configuração do repositório, como nomes de namespace, IDs de banco/KV e domínio de produção. Eles foram registrados aqui apenas como existência de configuração no artefato público; não são prova de que esses recursos estejam acessíveis, provisionados ou funcionais neste scout.

O arquivo também declara `keep_vars: true` e variáveis de feature gerenciadas no dashboard. Isso reforça que a configuração efetiva pode depender de ambiente e credenciais externas, portanto o repositório sozinho não fornece uma reprodução completa do runtime.

## Licença

O caminho `LICENSE` no SHA observado contém a licença MIT, com copyright `2025 Cloudflare`. O texto concede uso, cópia, modificação, publicação, distribuição, sublicenciamento e venda, sujeito à preservação dos avisos de copyright e licença, e inclui a cláusula de ausência de garantia e responsabilidade. A API de metadados do repositório também identifica `MIT License` e SPDX `MIT`.

A identificação MIT se aplica ao repositório conforme observado. Isso não substitui a revisão de licenças de dependências diretas/transitivas, arquivos vendorizados, templates externos ou ativos obtidos durante o uso.

## O que não foi verificado

Não foi verificado build, instalação de dependências, execução de scripts, testes unitários ou de integração, deploy, disponibilidade de `build.cloudflare.dev`, funcionamento de previews, isolamento efetivo, segurança de bindings, permissões de tokens, configuração de domínio, migrações, desempenho, custos, advisories ou vulnerabilidades. Também não foi acessado dashboard privado, conta Cloudflare, token, segredo ou endpoint autenticado.

O README e o setup contêm comandos e instruções que poderiam alterar ambientes ou coletar credenciais. Eles foram apenas lidos como evidência documental. O conteúdo de `package.json` e `wrangler.jsonc` foi usado apenas para inventário; nenhuma dependência ou script foi executado.

## Registros verificados

1. Repositório público `cloudflare/vibesdk`, URL de entrada e descrição pública observados.
2. Branch `main` e SHA `32c9e429cd2712ea5959a89f65ae434162b89229` observados na API de branches.
3. Commit de `main` associado à árvore `df6fcfe7b96638865588be0e3fbd80a1eb8e58f8` e assinatura marcada como verificada pelo GitHub, conforme resposta pública do branch.
4. Árvore recursiva do commit retornada com `truncated: false`; caminhos de topo e arquivos principais observados.
5. `README.md` lido no SHA fixado, incluindo descrição, arquitetura, workflow, comandos e limites documentados.
6. `docs/setup.md` lido no SHA fixado, incluindo pré-requisitos, recursos, credenciais, toggles e limitações de implantação.
7. `package.json` lido no SHA fixado, incluindo versão, requisito Node, scripts, workspace e dependências declaradas.
8. `wrangler.jsonc` lido no SHA fixado, incluindo worker principal, bindings, recursos, migrações e configuração de deploy.
9. `LICENSE` lido no SHA fixado e classificado como MIT; SPDX `MIT` confirmado pela API do repositório.

## References

[1]: https://github.com/cloudflare/vibesdk "Cloudflare VibeSDK repository"
[2]: https://api.github.com/repos/cloudflare/vibesdk "GitHub public repository metadata"
[3]: https://api.github.com/repos/cloudflare/vibesdk/branches/main "GitHub main branch metadata and commit SHA"
[4]: https://api.github.com/repos/cloudflare/vibesdk/git/trees/main?recursive=1 "GitHub recursive tree for main"
[5]: https://raw.githubusercontent.com/cloudflare/vibesdk/32c9e429cd2712ea5959a89f65ae434162b89229/README.md "README.md at pinned commit"
[6]: https://raw.githubusercontent.com/cloudflare/vibesdk/32c9e429cd2712ea5959a89f65ae434162b89229/docs/setup.md "docs/setup.md at pinned commit"
[7]: https://raw.githubusercontent.com/cloudflare/vibesdk/32c9e429cd2712ea5959a89f65ae434162b89229/package.json "package.json at pinned commit"
[8]: https://raw.githubusercontent.com/cloudflare/vibesdk/32c9e429cd2712ea5959a89f65ae434162b89229/wrangler.jsonc "wrangler.jsonc at pinned commit"
[9]: https://raw.githubusercontent.com/cloudflare/vibesdk/32c9e429cd2712ea5959a89f65ae434162b89229/LICENSE "LICENSE at pinned commit"
