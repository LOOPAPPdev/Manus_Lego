# Scout 23 — Cloudflare GitHub organization

**Fonte única:** organização pública Cloudflare no GitHub  
**Rota de entrada:** https://github.com/cloudflare  
**Data da observação:** 2026-11-20  
**Coverage:** `partial`

## Resultado

A página pública da organização Cloudflare informa 582 repositórios disponíveis e apresenta, entre os repositórios visíveis, `cloudflare/workers-sdk`, `cloudflare/workerd`, `cloudflare/cloudflare-docs`, `cloudflare/mcp` e outros projetos relacionados a Workers, runtime, documentação e ferramentas.[1] A API pública de repositórios foi consultada nas páginas 1 e 2, ordenadas por `full_name`; essas respostas confirmam metadados públicos de repositórios, mas não constituem um inventário completo dos 582 repositórios.[2] [3]

Os registros abaixo são referências públicas de proveniência e metadados. Não houve clone, instalação, execução de código candidato, deploy, acesso a dashboard privado ou uso de credenciais. A presença de README, scripts, configuração ou descrição não é tratada como prova de funcionamento, build, segurança ou runtime.

## Registros verificados

### 1. `cloudflare/templates`

- **Proveniência:** https://github.com/cloudflare/templates
- **Descrição observada:** “Templates for Cloudflare Workers”. O repositório é público, não é fork, declara licença MIT e usa a branch padrão `main`.[4]
- **Branch e commit observados:** `main` → `9674298a122ac464f8d4d8d2b38c3491d6b35d18`.[5]
- **Caminho relativo verificado:** `templates.json`, branch `main`, blob SHA `654c18ece56fd0125376b41e90a6653030f8861b`; URL observada: https://github.com/cloudflare/templates/blob/main/templates.json.[6]
- **Conteúdo/metadado observado:** o manifesto contém nomes de templates como `astro-blog-starter-template`, `durable-chat-template`, `llm-chat-app-template`, `react-postgres-fullstack-template`, `saas-admin-template`, `vite-react-template` e `workflows-starter-template`, entre outros.[6]
- **README observado:** `README.md` na branch `main`, com instruções de uso via dashboard ou C3 e uma seção que descreve testes E2E Playwright local/live. Isso é documentação declarada no repositório; não foi executada nesta exploração e não prova que todos os templates passam hoje.[7]
- **Classificação:** `reference_only`; o manifesto é evidência de catálogo/metadados, não de execução.

### 2. `cloudflare/workers-sdk`

- **Proveniência:** https://github.com/cloudflare/workers-sdk
- **Descrição observada:** “Home to Wrangler, the CLI for Cloudflare Workers”. O repositório é público, não é fork, declara Apache-2.0, usa TypeScript e tem branch padrão `main`.[8]
- **Branch e commit observados:** `main` → `f3f7bbc1fe609e14ea9a7be78a25551d270f1fce`.[9]
- **Caminho relativo verificado:** `README.md`, branch `main`, blob SHA `feb90d4d6a28e25dcc1ba517e33f6499597078c6`; URL observada: https://github.com/cloudflare/workers-sdk/blob/main/README.md.[10]
- **Conteúdo/metadado observado:** o README apresenta o SDK Workers, o comando `create-cloudflare`, links para documentação e um diretório de pacotes que inclui `wrangler`, `create-cloudflare` e `miniflare`.[10]
- **Classificação:** `reference_only`; descrição, licença e README foram observados, mas nenhuma instalação, build ou execução do CLI foi realizada.

### 3. `cloudflare/workerd`

- **Proveniência:** https://github.com/cloudflare/workerd
- **Descrição observada:** “The JavaScript / Wasm runtime that powers Cloudflare Workers”. O repositório é público, não é fork, declara Apache-2.0, usa C++ e tem branch padrão `main`.[11]
- **Branch e commit observados:** a consulta ao endpoint da branch solicitada `master` retornou objeto com `name: main`; o commit observado é `b5f552cf014f3dd658972220a6ce17cf02c8288e`.[12]
- **Caminho relativo verificado:** `README.md`, branch `main`, blob SHA `db5edb598582a31a3d19a6e036c7150d8dc0b85d`; URL observada: https://github.com/cloudflare/workerd/blob/main/README.md.[13]
- **Classificação:** `reference_only`; a descrição identifica o projeto como runtime, mas não é prova de compilação, execução, compatibilidade ou segurança.

### 4. `cloudflare/cloudflare-docs`

- **Proveniência:** https://github.com/cloudflare/cloudflare-docs
- **Descrição observada:** “Cloudflare’s documentation”. O repositório é público, não é fork, declara CC-BY-4.0 para a documentação e informa branch padrão `production`.[14]
- **Branch e commit observados:** `production` → `8d8d6854a33e7a3ea7571b0740986c0c126cd3b5`.[15]
- **Caminho relativo verificado:** `README.md`, branch `production`; URL observada: https://github.com/cloudflare/cloudflare-docs/blob/production/README.md. A página do repositório expõe o README e os arquivos `LICENSE` e `LICENSE-CODE`; ela informa CC-BY-4.0 para conteúdo e MIT para código, salvo exceções indicadas.[16]
- **Conteúdo/metadado observado:** o README descreve o repositório como fonte aberta da documentação de desenvolvedores Cloudflare e remete ao guia de contribuição.[16]
- **Classificação:** `reference_only`; documentação e licenças declaradas foram observadas, sem validação de build do site ou de conteúdo publicado.

### 5. `cloudflare/mcp`

- **Proveniência:** https://github.com/cloudflare/mcp
- **Descrição observada:** “MCP server for the Cloudflare API”. O repositório é público, não é fork, declara Apache-2.0, usa TypeScript e tem branch padrão `main`.[17]
- **Branch e commit observados:** `main` → `b8602d6d5ce543ef5933ea3d98f06be8e20759fa`.[18]
- **Caminho relativo verificado:** `README.md`, branch `main`, blob SHA `02c2c3ac5ca38ea5510c7460be26ac46ec985236`; URL observada: https://github.com/cloudflare/mcp/blob/main/README.md.[19]
- **Conteúdo/metadado observado:** o README documenta um endpoint MCP público, opções OAuth/API token e o modo Code Mode, além de listar produtos suportados. Essas são afirmações e instruções do README; não foram testadas e não constituem prova de endpoint disponível, autenticação bem-sucedida, cobertura da API ou segurança.[19]
- **Classificação:** `reference_only`; não foram enviados tokens nem feitas chamadas autenticadas.

## Proveniência adicional observada

A organização também expõe `cloudflare/agents-starter` como repositório público descrito como starter kit para agentes de IA. O endpoint de metadados informa licença MIT, branch `main` e linguagem TypeScript; a branch `main` aponta para `4ea6a72cbabe2b62a66294214361ac106b4a247e`, e o caminho `README.md` tem blob SHA `75c12d013d12e6a4f263fe9aa6f5d7f88e824fe6`.[20] [21] [22] O registro é mantido como referência contextual, não como candidato enriquecido, porque a amostra principal já estava limitada e não houve execução.

## Limitações e decisões de cobertura

- **Coverage `partial`:** a própria página da organização informa 582 repositórios, enquanto esta exploração aprofundou cinco repositórios e registrou um sexto apenas como contexto. As páginas 1 e 2 da API pública foram consultadas, mas não foram tratadas como inventário completo.[1] [2] [3]
- A listagem de repositórios e o README são metadados/documentação. Não foram usados para afirmar que um template, CLI, runtime, servidor MCP ou documentação compila, executa, está implantado ou é seguro.
- Não foram consultados dashboards privados, contas, tokens, segredos, endpoints autenticados ou ambientes Cloudflare.
- Não houve clone, download de árvore completa, instalação de dependências, execução de scripts, build, teste E2E, análise de dependências, auditoria de segurança ou verificação de licença além do campo/README público observado.
- O catálogo local exige SHA e caminho relativo para integração futura. Os registros acima têm branch e commit observados quando a API forneceu ambos; para `cloudflare/cloudflare-docs`, o `README.md` foi observado na página pública na branch `production`, e o commit da branch foi verificado separadamente.
- A data, contagens, descrições e SHAs são observações pontuais da API/páginas públicas; podem mudar após a coleta.

## References

[1]: https://github.com/cloudflare "Cloudflare GitHub organization"
[2]: https://api.github.com/orgs/cloudflare/repos?per_page=100&page=1&sort=full_name&direction=asc "Cloudflare public repositories API, page 1"
[3]: https://api.github.com/orgs/cloudflare/repos?per_page=100&page=2&sort=full_name&direction=asc "Cloudflare public repositories API, page 2"
[4]: https://api.github.com/repos/cloudflare/templates "cloudflare/templates repository metadata"
[5]: https://api.github.com/repos/cloudflare/templates/branches/main "cloudflare/templates main branch commit"
[6]: https://api.github.com/repos/cloudflare/templates/contents/templates.json?ref=main "cloudflare/templates templates.json"
[7]: https://github.com/cloudflare/templates "cloudflare/templates repository README"
[8]: https://api.github.com/repos/cloudflare/workers-sdk "cloudflare/workers-sdk repository metadata"
[9]: https://api.github.com/repos/cloudflare/workers-sdk/branches/main "cloudflare/workers-sdk main branch commit"
[10]: https://api.github.com/repos/cloudflare/workers-sdk/contents/README.md?ref=main "cloudflare/workers-sdk README"
[11]: https://api.github.com/repos/cloudflare/workerd "cloudflare/workerd repository metadata"
[12]: https://api.github.com/repos/cloudflare/workerd/branches/master "cloudflare/workerd branch endpoint response"
[13]: https://api.github.com/repos/cloudflare/workerd/contents/README.md?ref=main "cloudflare/workerd README"
[14]: https://api.github.com/repos/cloudflare/cloudflare-docs "cloudflare/cloudflare-docs repository metadata"
[15]: https://api.github.com/repos/cloudflare/cloudflare-docs/branches/production "cloudflare/cloudflare-docs production branch commit"
[16]: https://github.com/cloudflare/cloudflare-docs "cloudflare/cloudflare-docs repository README"
[17]: https://api.github.com/repos/cloudflare/mcp "cloudflare/mcp repository metadata"
[18]: https://api.github.com/repos/cloudflare/mcp/branches/main "cloudflare/mcp main branch commit"
[19]: https://github.com/cloudflare/mcp/blob/main/README.md "cloudflare/mcp README"
[20]: https://api.github.com/repos/cloudflare/agents-starter "cloudflare/agents-starter repository metadata"
[21]: https://api.github.com/repos/cloudflare/agents-starter/branches/main "cloudflare/agents-starter main branch commit"
[22]: https://api.github.com/repos/cloudflare/agents-starter/contents/README.md?ref=main "cloudflare/agents-starter README"
