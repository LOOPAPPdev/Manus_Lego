# Scout 18 — Cloudflare API documentation

**Fonte única:** Cloudflare API documentation

**Rota de entrada:** https://developers.cloudflare.com/api/

**Data da observação:** 2026-11-20

**Cobertura:** `partial`

## Conclusão

A documentação pública da Cloudflare descreve uma API REST e também referencia a API GraphQL. A referência REST usa endpoints sob a base estável `https://api.cloudflare.com/client/v4/`; a própria documentação afirma que a versão mais recente é a Version 4. A autenticação preferida é por API token enviado como `Authorization: Bearer <API_TOKEN>`. Chaves globais de API continuam documentadas como mecanismo legado, com permissões amplas e limitações de segurança.

A referência pública apresenta recursos e operações organizados por produto, com método HTTP, caminho, seção de segurança, parâmetros, modelos de retorno e exemplos. Foram confirmados, entre outros, endpoints de contas, tokens de conta e verificação de token do usuário. A página de referência também exibe versões observadas de bibliotecas TypeScript, Python, Go e Terraform. Essas versões são metadados da documentação; não foram tratadas como prova de instalação, build, execução, compatibilidade ou runtime.

A classificação é `partial`: a referência é ampla, mas esta coleta verificou uma amostra representativa de páginas e não gerou uma enumeração independente e exaustiva de todos os produtos, operações, modelos, permissões ou depreciações.

## Evidências observadas

1. A rota de entrada é uma página intitulada “API Reference”. Ela apresenta a referência por grupos de recursos e operações, incluindo exemplos visíveis como `GET /accounts`, `GET /accounts/{account_id}`, `POST /accounts` e operações de tokens de conta. A navegação renderizada também lista numerosas áreas de produto, mas a presença na navegação não foi interpretada como prova de funcionamento do endpoint. [1]

2. A página geral da API informa que a documentação cobre a REST API e a GraphQL API e encaminha para “Get started”, “How to”, “Reference” e “Troubleshooting”. [2]

3. A documentação de chamadas afirma que cada elemento da API Cloudflare é fixado a uma versão, que a versão mais recente é a Version 4 e que a base HTTPS estável para endpoints Version 4 é `https://api.cloudflare.com/client/v4/`. O mesmo texto recomenda o cabeçalho Bearer e mostra um exemplo com `/zones/$ZONE_ID`. [3]

4. A documentação de início informa que chamadas da API exigem autenticação. Recomenda API tokens sempre que possível e também documenta API keys, incluindo a Global API key legada, Origin CA keys e Account API tokens. [4]

5. A página de criação de token documenta tokens de usuário e de conta, políticas com escopo de conta, usuário ou zona, permissões de leitura/edição, expiração opcional e filtragem por IP. Ela registra que o segredo do token é mostrado uma única vez e não deve ser armazenado em texto puro. Também fornece o endpoint público `GET https://api.cloudflare.com/client/v4/user/tokens/verify` com `Authorization: Bearer <API_TOKEN>` como exemplo de verificação. [5]

6. A página específica “Verify Token” confirma `GET /user/tokens/verify`, a segurança por API Token e um envelope de resposta documentado com `success`, `errors`, `messages` e `result`. O resultado documentado contém `id`, `status`, `expires_on` e `not_before`, com status possíveis `active`, `disabled` e `expired`. O exemplo de curl usa a mesma base Version 4 e uma variável de ambiente para o token. [6]

7. A página “List Accounts” confirma `GET /accounts`, descreve paginação por `page` e `per_page`, ordenação por `direction`, e documenta um envelope com `errors`, `messages`, `success`, `result` e `result_info`. A página mostra API Token como esquema preferido e API Email + API Key como esquema anterior. Essa observação é documental e não foi validada contra uma conta. [7]

8. A página de formatos de credenciais documenta os prefixos escaneáveis `cfk_` para Global API Key, `cfut_` para User API Token e `cfat_` para Account API Token, além de informar que tokens antigos continuam funcionando. Também repete a rota de verificação de token e o cabeçalho Bearer. Nenhum segredo foi coletado ou usado. [8]

9. A página de Global API key classifica esse mecanismo como anterior/legado, afirma que ele tem acesso a todos os recursos do usuário e as mesmas permissões do usuário, e recomenda API tokens para novos clientes. [9]

10. A página de SDKs informa que a Cloudflare oferece SDKs para Go, TypeScript e Python, além de exemplos curl. Ela ilustra `GET https://api.cloudflare.com/client/v4/zones` com Bearer token e recomenda selecionar curl ou SDK conforme o caso de uso. [10]

11. A rota principal da referência exibiu, no momento da observação, as seguintes versões de bibliotecas: TypeScript `7.3.0`, Python `5.10.0`, Go `v7.15.0` e Terraform `5.29.0` com restrição declarada `~> 5.0`. Essas são versões mostradas na documentação; não foram instaladas nem executadas. [1]

12. A página de depreciações fornece evidência de que a documentação acompanha mudanças de API, datas de depreciação, datas de fim de vida e endpoints substitutos. Entre os registros visíveis estão endpoints de Radar, Zone Settings Batch API, a configuração `foundation_dns`, Account Roles API e rotas legadas de Workers KV. A lista é um mecanismo documental de mudança, não uma prova de que cada migração foi testada. [11]

## Registros realmente verificados

- `GET /accounts` — método e caminho observados na referência; parâmetros de paginação e ordenação observados; segurança documentada como API Token preferido e API Email + API Key anterior. [7]
- `GET /user/tokens/verify` — método, caminho, esquema Bearer, formato de resposta e estados de token observados na página específica. [6]
- `GET /zones` — exemplo de chamada com a base Version 4 e Bearer token observado na página de SDKs. [10]
- `GET /zones/$ZONE_ID` — exemplo de chamada com a base Version 4 e Bearer token observado na página “Make API calls”. [3]
- `POST /accounts/{account_id}/tokens`, `GET /accounts/{account_id}/tokens`, `GET /accounts/{account_id}/tokens/verify` e operações relacionadas de token de conta — caminhos observados na listagem da referência principal; não foram executados. [1]
- Base pública documentada: `https://api.cloudflare.com/client/v4/`. [3]
- Esquema de autenticação preferido documentado: `Authorization: Bearer <API_TOKEN>`. [3] [5] [6]
- Versões de bibliotecas observadas na referência: TypeScript `7.3.0`, Python `5.10.0`, Go `v7.15.0`, Terraform `5.29.0`/`~> 5.0`. [1]
- Nenhum repositório, branch ou commit/SHA foi usado como evidência primária nesta exploração. Os links para SDKs exibidos na documentação não foram clonados, instalados ou executados.

## O que não foi provado

- Não foi feita qualquer chamada autenticada à API. Não há prova de que um token funcione, de que uma conta exista, de que uma permissão seja suficiente ou de que uma operação altere estado.
- Não foram usados tokens, API keys, IDs de conta, IDs de zona, dashboards privados ou credenciais.
- Exemplos de resposta, exemplos de curl e nomes de SDK são documentação e metadados, não evidência de execução, build, segurança, disponibilidade, SLA ou runtime.
- A listagem da referência principal não foi convertida em um inventário completo e independente de todos os endpoints, parâmetros, permissões ou modelos.
- Não foi avaliada compatibilidade entre SDKs, Terraform, versões de runtime, dependências ou projetos candidatos.
- Não foram feitas conclusões sobre licenças ou sobre o conteúdo de repositórios públicos. Nenhum código de candidato foi clonado, instalado ou executado.

## Limitações e segurança

A extração textual da rota principal é extensa e foi parcialmente truncada por algumas interfaces, embora a navegação pública tenha mostrado a árvore de recursos e exemplos iniciais. Páginas específicas de endpoint foram consultadas para reduzir esse risco, mas isso não elimina a limitação de cobertura.

A documentação inclui exemplos com valores que têm aparência de identificadores ou segredos. Eles foram tratados somente como exemplos textuais; nenhum valor foi reutilizado. Este relatório não armazena credenciais, identificadores privados, URLs de dashboard ou dados de conta.

## Referências

[1]: https://developers.cloudflare.com/api/ "Cloudflare API Reference"

[2]: https://developers.cloudflare.com/fundamentals/api/ "Cloudflare's API"

[3]: https://developers.cloudflare.com/fundamentals/api/how-to/make-api-calls/ "Make API calls"

[4]: https://developers.cloudflare.com/fundamentals/api/get-started/ "Get started"

[5]: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/ "Create API token"

[6]: https://developers.cloudflare.com/api/resources/user/subresources/tokens/methods/verify/ "Verify Token"

[7]: https://developers.cloudflare.com/api/resources/accounts/methods/list/ "List Accounts"

[8]: https://developers.cloudflare.com/fundamentals/api/get-started/token-formats/ "Token formats"

[9]: https://developers.cloudflare.com/fundamentals/api/get-started/keys/ "Get Global API key (legacy)"

[10]: https://developers.cloudflare.com/fundamentals/api/reference/sdks/ "SDKs"

[11]: https://developers.cloudflare.com/fundamentals/api/reference/deprecations/ "API deprecations"
