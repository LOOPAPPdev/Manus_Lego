# Scout 24 — Cloudflare templates

## Escopo e resultado

Fonte única observada: repositório público `cloudflare/templates`, rota de entrada `https://github.com/cloudflare/templates`. A referência pública da branch `main` apontou para o commit `9674298a122ac464f8d4d8d2b38c3491d6b35d18`, observado em 2026-11-20. O manifesto `templates.json` está na raiz do repositório, com SHA de blob `654c18ece56fd0125376b41e90a6653030f8861b`.[1] [2] [3]

A cobertura deste relatório é **partial**. A fonte confirmou o manifesto completo retornado pela API, com 42 entradas, e a resposta da árvore Git recursiva informou `truncated:false`. Porém, a captura textual disponibilizada para análise foi limitada ao início da resposta grande; ela permitiu observar 41 diretórios-raiz `*-template` e 43 caminhos `*/package.json`, mas não sustentou uma comparação independente, item a item, de todos os 42 diretórios com todos os `package_json_hash`. Não há base para afirmar cobertura completa da relação manifesto–árvore além do que foi diretamente observado.

## Evidências primárias

1. A API pública de metadados identificou o repositório como `cloudflare/templates`, público, não arquivado, com descrição “Templates for Cloudflare Workers”, branch padrão `main` e licença declarada pelo GitHub como MIT.[1]
2. A API pública da branch `main` retornou o commit `9674298a122ac464f8d4d8d2b38c3491d6b35d18`, cuja árvore Git é `52f8dcb4e12fce581dcf0e28613c0e1d7128ff9e`. A mesma resposta informou assinatura GitHub verificada para o commit e a mensagem “Require passwords for the admin pages in four templates (#1202)”. Isso é metadado de proveniência, não prova de segurança ou de execução.[2]
3. `templates.json` foi observado na raiz, na branch `main`, com blob SHA `654c18ece56fd0125376b41e90a6653030f8861b`, tamanho 4586 bytes e caminho relativo `templates.json`.[3]
4. O conteúdo bruto de `templates.json` tem o objeto superior `templates`. Cada entrada observada contém apenas `package_json_hash`; o manifesto não lista, por si só, uma lista de arquivos, comandos, runtime, licença por template ou resultado de build.[4]
5. A árvore Git recursiva da mesma referência retornou SHA raiz `9674298a122ac464f8d4d8d2b38c3491d6b35d18` e o campo `truncated:false`.[5] A resposta é evidência de inventário Git solicitado, mas a captura textual usada nesta análise foi limitada pelo tamanho da resposta; isso motiva a classificação parcial.
6. Na porção observada da árvore, há diretórios-raiz com os mesmos nomes do padrão do manifesto, incluindo `agent-commerce-analytics-template`, `agent-visibility-template` e `ai-brand-visibility-template`. Também foi observado o caminho `agent-commerce-analytics-template/package.json`, com blob SHA `508f630f91e08799a5969ebec06cc719b54d9690`, e `agent-visibility-template/package.json`, com blob SHA `f661382e62d1236920fa51037e6798d901cbe257`.[5] Esses SHAs de blob observados não foram tratados como equivalentes aos valores `package_json_hash` do manifesto sem uma regra pública adicional que prove tal equivalência.
7. O README público descreve o repositório como uma coleção de templates iniciais para aplicações full-stack em Workers e documenta comandos e uma suíte Playwright E2E. Esse texto é documentação do projeto; não foi executado, portanto não prova build, runtime, implantação, segurança ou funcionamento de qualquer template.[6]

## Registros realmente verificados no manifesto

Todos os 42 registros abaixo foram observados no conteúdo bruto público de `templates.json`, na referência `main` acima. O valor após `package_json_hash` é o valor literal do manifesto; ele não deve ser interpretado como SHA de commit do diretório nem como prova de execução.

- `agent-visibility-template` — `f7a9e81e74e72f8b0d61466264aa3169562c5e9d`
- `astro-blog-starter-template` — `228c8c46924c8c58841070d00d786293bb72af5b`
- `chanfana-openapi-template` — `6b807a1a389907d3f8732d159bc04b98fe6d8b3e`
- `d1-template` — `53956a7184176bfd9cb3fe8d18dd2ca63ef3dcb8`
- `durable-chat-template` — `62173499fbaecb77bebc80718456d376f1c0f7e0`
- `llm-chat-app-template` — `8a4a9ad7b627bb79c4789c439ebff5f5fc5c4577`
- `multiplayer-globe-template` — `f203a89d03ef8a8801bb1e821686b262f8f19adf`
- `next-starter-template` — `22e3356133a3a322930f9669764f877285cbbf44`
- `openauth-template` — `56c2b68ded6225743e0f770a61f100d349d40bd1`
- `r2-explorer-template` — `365e6ebb4d4c9fc91b884b170bebf899174727b0`
- `react-postgres-fullstack-template` — `c391e27e5337819e83ffb2205886006e9d3a7937`
- `react-router-hono-fullstack-template` — `3e90f86adf78f79e927073ef15b911e034a9a6e9`
- `react-router-starter-template` — `5450ccff26ade3bdae21be960c5e29293d65e90c`
- `remix-starter-template` — `42943d0724ed5dc2cab137859daa59b1fd9e1267`
- `saas-admin-template` — `39ce703b1d1615b5404e656423b36529d4697574`
- `text-to-image-template` — `aae2e3a020f503f09a9306a7fdc2b5713bee32e3`
- `to-do-list-kv-template` — `a8ff3dfe801469065841bbd5c84402a1ed329442`
- `vite-react-template` — `29af2e800d534260866c1452c169bf1050663a87`
- `worker-publisher-template` — `27def0cfeab213ea633f1371bef650b4d6be24f0`
- `containers-template` — `e1d267fad54310a8a5feaf8acb87c48505c7904b`
- `d1-starter-sessions-api-template` — `71eb6c2d8b2e14c168140a5c95e265eca2006eb5`
- `hello-world-do-template` — `f52873c561e4ec3d80ceccf307ad56436fe25547`
- `mysql-hyperdrive-template` — `40c92113b00ffc66f05599f9712e99d566b4018e`
- `nlweb-template` — `e070796ba480830ad5ac6d87866898ad25a42b5f`
- `nodejs-http-server-template` — `9276f76915cfc1986703e0341b8f3eef5de61622`
- `postgres-hyperdrive-template` — `30ffdad4cab0d35839984771d2c5eb0cf0efec5d`
- `react-router-postgres-ssr-template` — `a08c3c3ee3dbbfa806f8d350fb64eabc564562f5`
- `x402-proxy-template` — `a3b4fefb68c5e8bf1a591303e05aff7a7d9f7ed8`
- `workflows-starter-template` — `222e9d996b9e78d61566cac3a5e705ce6cfe98ba`
- `workers-for-platforms-template` — `562b92d01c1fad944845bf59de43faa9f6e9df8c`
- `microfrontend-template` — `ceee843aa9324e25aff32f5f42945e9fd4daf7ba`
- `workers-builds-notifications-template` — `0586d36cd40ea67a05d32517b715ca4da6f1cf0e`
- `ai-brand-visibility-template` — `f0caf436890912409a509c4a8929d07a3da1c7e4`
- `commerce-llms-txt-template` — `3dc21b9fe0f3d9707e7dfeba64cc52a2c2962a75`
- `agent-commerce-analytics-template` — `1654efbead1a5f71b54af64e95e98cab1c9ce114`
- `react-starter-template` — `b9f72d919056ce58d57e95260e302f2aad5edbed`
- `internal-sites-template` — `18f977168261adae1afda9f9cc18b0ff7169e72f`
- `voice-agent-template` — `e926996d61e41c2e8e129fe6c1981e6777099c3d`
- `email-routing-template` — `acfc9ca0edaab800b8c718d744821b8506876905`
- `email-sending-template` — `c10ec46edff3e911c2675120d7b9f5787a514fc2`
- `grpc-container-template` — `d010e0a7285da9523c14e1af8f4459ae60a22f9b`

## Relação manifesto–árvore e interpretação

A relação nominal esperada é `templates.json.templates[<id>]` → diretório `<id>/` na raiz do repositório → arquivo `<id>/package.json`. A árvore observada confirma essa forma para os exemplos listados na seção de evidências. O manifesto, contudo, não contém explicitamente os caminhos relativos; os caminhos são derivados do padrão nominal e precisam ser validados contra a árvore da mesma referência antes de qualquer integração.

O campo `package_json_hash` é metadado do manifesto. A evidência coletada não documenta no próprio `templates.json` se ele é um SHA Git blob, hash de conteúdo calculado por outra convenção ou outro identificador. Como os exemplos de SHA de blob observados na árvore (`agent-commerce-analytics-template/package.json` e `agent-visibility-template/package.json`) diferem dos valores correspondentes do manifesto, este relatório não afirma igualdade nem usa esses campos como prova de integridade sem uma verificação adicional da implementação pública que gera o manifesto.

A árvore contém também arquivos e diretórios fora dos candidatos, como `.github/`, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `LICENSE` e `README.md`. Portanto, a árvore pública é mais ampla que o conjunto enumerado no manifesto; `templates.json` deve ser tratado como índice curado, não como uma declaração de que todo caminho do repositório é um template.

## Limitações e não-verificações

- Não clonei o repositório, não instalei dependências e não executei código, scripts, workflows, testes, builds ou servidores de nenhum candidato.
- Não verifiquei runtime, implantação, compatibilidade de bindings, segurança, vulnerabilidades, qualidade dos testes ou funcionamento dos templates.
- Não converti a documentação E2E do README em resultado de teste; a existência de uma suíte descrita não é prova de que ela passou nesta coleta.
- Não confirmei individualmente, para todos os 42 registros, a presença do diretório e a igualdade entre `package_json_hash` e qualquer SHA de blob da árvore. A resposta da API informou `truncated:false`, mas o retorno textual utilizado para inspeção foi limitado por tamanho.
- A licença MIT foi observada como licença declarada do repositório na API do GitHub; isso não substitui a revisão de licença dos arquivos ou dependências de cada template.
- A coleta via shell de uma chamada redundante à API foi bloqueada por `HTTP 403 rate limit exceeded`; o relatório usa as respostas públicas já obtidas pelo leitor web e não trata a falha de taxa como evidência sobre o conteúdo do repositório.
- Não acessei dashboards, contas, tokens, segredos ou URLs privadas.

## References

[1]: https://api.github.com/repos/cloudflare/templates "GitHub API — metadados públicos de cloudflare/templates"
[2]: https://api.github.com/repos/cloudflare/templates/branches/main "GitHub API — branch main e commit observado"
[3]: https://api.github.com/repos/cloudflare/templates/contents/templates.json?ref=main "GitHub API — templates.json na branch main"
[4]: https://raw.githubusercontent.com/cloudflare/templates/main/templates.json "GitHub raw — conteúdo público de templates.json"
[5]: https://api.github.com/repos/cloudflare/templates/git/trees/main?recursive=1 "GitHub API — árvore recursiva pública"
[6]: https://raw.githubusercontent.com/cloudflare/templates/main/README.md "GitHub raw — README público do repositório"
