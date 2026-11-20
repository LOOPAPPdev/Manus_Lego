# Scout — Cloudflare OS

## Identificação e proveniência

A rota pública observada é [cloudflare/cloudflare-os](https://github.com/cloudflare/cloudflare-os), de propriedade da organização `cloudflare`. A API pública informa `private: false`, `visibility: public`, `default_branch: main`, descrição “Agent workspace built on Cloudflare Workers for creating documents, building apps, and running agents with your company’s context and systems.” e licença detectada como Apache License 2.0, SPDX `Apache-2.0`. [1]

A branch `main` foi observada na API pública em 2026-11-20 com o commit completo `7f9f7a8fff57458d87601f3668119a03a8b9f181`. O commit tem mensagem `GitLab: report CI reads by job, not by required role (#1238)`, foi retornado como assinado/verificado pelo GitHub (`verified: true`, razão `valid`) e aponta para a árvore `ee22d137ae072fe7801e6e9939aeb368ed510203`. [2] Os registros abaixo usam esse SHA como ponto de proveniência; a branch continua sendo uma referência mutável.

## Árvore e arquivos observados

A página pública do repositório lista, na raiz, `.agents/skills/`, `.github/`, `docs/`, `packages/`, `plans/`, `scripts/`, `AGENTS.md`, `CONTRIBUTING.md`, `LICENSE`, `README.md`, `package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml`, `tsconfig.json`, `vite.config.ts`, `wrangler.jsonc` e outros arquivos de configuração. [3] A consulta recursiva pública da árvore retornou `truncated: false` e mostrou, entre outros, os caminhos `.agents/skills/frontend-conventions/SKILL.md`, `.agents/skills/write-gatekeeper/SKILL.md`, `.agents/skills/write-gatekeeper/SKELETON.md`, workflows em `.github/workflows/` e os blobs correspondentes. [4]

O endpoint público de conteúdo da raiz confirmou, na referência `main`, que `AGENTS.md` existe com SHA `70b5b6d5d64cb82af4a4c291085a183698545298`, e que a raiz também contém `LICENSE`, `README.md`, `package.json` e `pnpm-workspace.yaml`, entre os demais itens retornados. [3] A API de README confirmou `README.md` com SHA `6bea65e71df1ce1e5f745ad3803303e03f3eb490`. [5]

## README e afirmações sobre workspace

O README descreve Cloudflare OS como um ambiente de produtividade com IA, originalmente desenvolvido para uso interno da Cloudflare, e afirma três capacidades de produto: interface de chat de agentes; desenvolvimento de aplicações “gadgets” em sandbox; e uma estrutura de segurança chamada Gatekeepers. [6] Essas são afirmações documentais do próprio projeto, não prova independente de que cada capacidade esteja funcionando em uma implantação específica.

O README documenta um quick start local com `pnpm run-local`, acesso em `http://localhost:8787` e uso de Wrangler/workerd; também declara explicitamente que o modo local não é destinado à produção. [6] O mesmo README oferece uma rota de deploy em `https://os.cloudflare.app/deploy`, mas essa URL é uma instrução/documentação externa ao repositório, não uma evidência de deploy executado neste scout. [6]

O arquivo `package.json` público, observado na branch `main`, tem SHA `21c8678e3a000718d728e67b67aab08ef1a377e0`. Seu conteúdo codificado pela API declara o pacote raiz `cloudflare-os`, `packageManager: pnpm@11.17.0...` e scripts como `build`, `run-local`, `test`, `dev-client`, `dev-server`, `lint`, `configs:check` e `configs:generate`. [7] Isso verifica a presença declarada dos comandos no manifesto, mas não verifica que tenham sido executados com sucesso.

O arquivo `pnpm-workspace.yaml` público foi observado com SHA `b2772e23e05303ce39e30e1a54b54f23e7618229`. A configuração declara `packages/*` e `scripts` como membros do workspace, além de catálogos e overrides de dependências. [8] Isso é prova de configuração de workspace no repositório, não prova de instalação, resolução completa ou build limpo.

## Gatekeepers e gatekeepers/gatekeepers

O README define Gatekeepers como uma camada de segurança baseada em capacidades. Segundo a documentação, um Gatekeeper gerencia o acesso de um agente ou Gadget a um recurso externo, fornece uma API Cap’n Web, trata autorização como OAuth, restringe acesso ao recurso pretendido, registra ações e pode solicitar aprovação humana para efeitos colaterais. [6] O README também afirma que cada Gatekeeper é implementado como um Worker separado e lista diretórios de configuração para integrações como GitHub, Google, Cloudflare, Supabase, Notion, Confluence, Email Workers, Home Assistant, Slack, Spotify, Microsoft 365, PagerDuty, X e ZoomInfo. [6]

O `AGENTS.md` público do candidato contém regras de engenharia específicas para Gatekeepers. Ele afirma que cada Gatekeeper roda como um Worker separado, salvo pacotes `gatekeeper-*` sem `wrangler.jsonc`, que seriam bibliotecas; descreve descoberta baseada na presença de `wrangler.jsonc`; e orienta carregar `.agents/skills/write-gatekeeper/SKILL.md` ao escrever ou revisar um Gatekeeper. [9] O mesmo documento descreve requisitos de observação para novos Gatekeepers, incluindo `subresources`, `verifyObserverAccess()`, `getHistoricalSubresources()` somente leitura e `addObserver()`/`removeObserver()` sem operação. [9]

O `AGENTS.md` também documenta controles de conexão, como página de handoff, ticket de uso único, nonce por fluxo e commit explícito de reconnect. [9] São requisitos e descrição de desenho no texto de governança do repositório. Não foram tratados como evidência de que OAuth, isolamento, auditoria, aprovação humana, tickets ou nonces tenham sido testados em runtime neste scout.

## Licença

A API pública de licença identifica o arquivo `LICENSE` na referência `main`, com blob SHA `f433b1a53f5b830a205fd2df78e2b34974656c7b`, nome `Apache License 2.0` e SPDX `Apache-2.0`. [10] Este registro é suficiente para catalogar a licença declarada/detectada do repositório no ponto consultado. Não é uma análise de compatibilidade de todas as dependências nem autorização para copiar código.

## Verificação e limites

Não clonei, instalei dependências nem executei código do candidato. Não executei `pnpm run-local`, `pnpm build`, `pnpm test`, `pnpm lint`, Wrangler, workerd, Workers ou qualquer fluxo de deploy. Portanto, não há prova de execução, build, runtime, segurança, isolamento, cobertura de testes ou funcionamento de Gatekeepers.

A evidência é suficiente para proveniência pública, branch/commit, existência de arquivos e diretórios observados, README, manifesto de workspace, scripts declarados e licença. A consulta de árvore pública foi usada para descoberta, mas este relatório não afirma uma enumeração independente e exaustiva de todos os arquivos, integrações ou dependências. A lista de Gatekeepers acima é a lista documentada no README, não uma auditoria completa da árvore nem uma confirmação de que cada integração esteja configurada ou operacional.

Também não foram acessados dashboards privados, contas Cloudflare, tokens, segredos ou endpoints autenticados. A URL de deploy foi apenas lida como referência documental. A cobertura permanece `partial`: completa para os fatos pontuais explicitamente observados nas APIs/páginas citadas; não completa para execução, segurança, runtime, dependências, inventário operacional total ou validação de todas as alegações do README.

## Registros verificados

- Provider: `cloudflare`; repository: `cloudflare/cloudflare-os`; route: `https://github.com/cloudflare/cloudflare-os`; visibility: public; default branch: `main`. [1]
- Branch: `main`; observed commit/SHA: `7f9f7a8fff57458d87601f3668119a03a8b9f181`; commit tree SHA: `ee22d137ae072fe7801e6e9939aeb368ed510203`. [2]
- README: `README.md`; repository-relative path: `README.md`; branch: `main`; observed blob SHA: `6bea65e71df1ce1e5f745ad3803303e03f3eb490`. [5]
- Workspace manifest: `pnpm-workspace.yaml`; branch: `main`; observed blob SHA: `b2772e23e05303ce39e30e1a54b54f23e7618229`; declares `packages/*` and `scripts`. [8]
- Root manifest: `package.json`; branch: `main`; observed blob SHA: `21c8678e3a000718d728e67b67aab08ef1a377e0`; declares pnpm and build/run/test-related scripts. [7]
- Governance: `AGENTS.md`; branch: `main`; observed blob SHA: `70b5b6d5d64cb82af4a4c291085a183698545298`; contains Gatekeepers and development-check guidance. [3] [9]
- License: `LICENSE`; branch: `main`; observed blob SHA: `f433b1a53f5b830a205fd2df78e2b34974656c7b`; detected license `Apache-2.0`. [10]
- Gatekeeper skill path observed in recursive tree: `.agents/skills/write-gatekeeper/SKILL.md`; the tree response reported a blob at that relative path. [4]

## References

[1]: https://api.github.com/repos/cloudflare/cloudflare-os "GitHub public repository metadata"
[2]: https://api.github.com/repos/cloudflare/cloudflare-os/branches/main "GitHub public main branch and commit"
[3]: https://api.github.com/repos/cloudflare/cloudflare-os/contents/?ref=main "GitHub public root contents"
[4]: https://api.github.com/repos/cloudflare/cloudflare-os/git/trees/main?recursive=1 "GitHub public recursive tree"
[5]: https://api.github.com/repos/cloudflare/cloudflare-os/readme "GitHub public README metadata"
[6]: https://raw.githubusercontent.com/cloudflare/cloudflare-os/main/README.md "Cloudflare OS README"
[7]: https://api.github.com/repos/cloudflare/cloudflare-os/contents/package.json?ref=main "Cloudflare OS package manifest"
[8]: https://api.github.com/repos/cloudflare/cloudflare-os/contents/pnpm-workspace.yaml?ref=main "Cloudflare OS pnpm workspace manifest"
[9]: https://raw.githubusercontent.com/cloudflare/cloudflare-os/main/AGENTS.md "Cloudflare OS repository governance and Gatekeepers guidance"
[10]: https://api.github.com/repos/cloudflare/cloudflare-os/license "GitHub public license metadata"
