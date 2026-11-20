# Scout — `vercel/examples`

## Resultado

**Coverage: `partial`** para o escopo do repositório oficial `vercel/examples` no commit `a4b4827297bec79b81ddb2ff22a53089ebe88cd8` (branch padrão `main`). A árvore GitHub recursiva retornou `truncated: false`, portanto a listagem de caminhos daquele commit é verificável como completa para o snapshot consultado [1]. Isso não sustenta cobertura completa de todos os templates publicados no marketplace da Vercel, nem de todos os READMEs com frontmatter, porque a própria documentação diz que apenas exemplos com frontmatter geram drafts de template e que a galeria inclui uma superfície separada [2].

A rota é pública, pertence à organização Vercel, não é fork, tem branch padrão `main` e o metadado da API identifica licença MIT [3]. A verificação foi somente de metadados, conteúdo textual e árvore Git; nenhum exemplo foi instalado, executado, implantado ou testado em runtime.

## Evidência do repositório e do commit

- Repositório: `vercel/examples`; URL pública: <https://github.com/vercel/examples>.
- Commit observado: `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`, com árvore `344b37d2c1a9421f5d8945ae0f25da62f9d1db33`; URL do commit: <https://github.com/vercel/examples/commit/a4b4827297bec79b81ddb2ff22a53089ebe88cd8> [4].
- A API do repositório reporta `full_name: vercel/examples`, `private: false`, `fork: false`, `default_branch: main`, `archived: false`, `license: MIT` e descrição oficial de coleção curada de exemplos e soluções [3].
- A árvore recursiva do commit acima retorna `truncated: false`; nela aparecem, entre outros, `README.md`, `internal/fields.json`, `internal/publishing-templates.md` e os diretórios de exemplos. A árvore é evidência de caminhos e blobs, não de funcionamento [1].
- `README.md` no commit tem SHA `6f73b859c88a7d4880cb3dcaaa84c9b9067ce53e` e está em <https://github.com/vercel/examples/blob/a4b4827297bec79b81ddb2ff22a53089ebe88cd8/README.md> [5].
- `internal/fields.json` no mesmo commit tem SHA `e00be6a3516bb432e245be6cf3cbb59ba471d074` e está em <https://github.com/vercel/examples/blob/a4b4827297bec79b81ddb2ff22a53089ebe88cd8/internal/fields.json> [6].

## README/frontmatter e convenções verificadas

O README raiz afirma que exemplos com frontmatter criam um novo draft de template no Contentful. Para adicionar um template à galeria, orienta colocar o frontmatter no topo do README e consultar `internal/fields.json` para os valores possíveis. Também exige, como convenções de contribuição, `.gitignore`, `package.json`, README, licença `MIT`, URL de demo e, quando necessário, `.env.example` com instruções; isso é documentação de processo, não prova de que cada exemplo atende ou funciona [2].

O README de `edge-middleware/bot-protection-datadome/README.md` é um registro efetivamente verificado no commit, com SHA de blob `1decaf915047b3ba15c77a932df62a54df2d5f59`, e conteúdo observado com frontmatter YAML. Ele contém os campos `name`, `slug`, `description`, `framework`, `useCase`, `css`, `deployUrl`, `demoUrl`, `ignoreE2E` e `relatedTemplates`, seguido de instruções e URL de demo. O caminho fixado é <https://github.com/vercel/examples/blob/a4b4827297bec79b81ddb2ff22a53089ebe88cd8/edge-middleware/bot-protection-datadome/README.md> [7]. A leitura comprova a presença declarada de URLs e metadados no arquivo; não comprova que a demo esteja disponível agora nem que o código execute.

`internal/fields.json` define onze campos obrigatórios: `name`, `slug`, `publisher`, `description`, `framework`, `type`, `css`, `githubUrl`, `demoUrl`, `relatedTemplates` e `deployUrl`. O arquivo especifica tipos, limites e enumerações. Entre as regras observadas estão: `name` até 50 caracteres; `slug` único; `description` até 140; `framework` como array de até dois itens; `type` com um a três itens; `css` com um a dois itens; `relatedTemplates` com um a quatro links para o tipo Contentful `templates`; e `deployUrl` compatível com o prefixo `https://vercel.com/new/clone` [6].

Há uma diferença importante entre a convenção documentada e o registro observado: o exemplo DataDome usa `useCase: Edge Middleware`, enquanto o `fields.json` consultado enumera o campo `type` (incluindo `Edge Middleware`) e não lista `useCase`. Não se deve normalizar ou inferir esse registro como válido para publicação apenas pela leitura; a validação operacional de Contentful e a execução da aplicação não foram realizadas.

## Registros realmente verificados

1. **`edge-middleware/bot-protection-datadome`** — repositório `vercel/examples`; caminho relativo `edge-middleware/bot-protection-datadome/README.md`; ref `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`; frontmatter e corpo do README lidos diretamente da URL raw fixada [7]. Evidência: metadados YAML, `demoUrl`, `deployUrl`, `relatedTemplates`, instruções de variáveis de ambiente e comando de desenvolvimento. Status de runtime: **não verificado**.
2. **Convenção de schema de templates** — repositório `vercel/examples`; caminho relativo `internal/fields.json`; ref `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`; blob SHA `e00be6a3516bb432e245be6cf3cbb59ba471d074` [6]. Evidência: schema textual dos campos obrigatórios, validações, enumerações e regexes. Isso é uma convenção de metadados, não um inventário de registros publicados.
3. **Convenção de publicação** — repositório `vercel/examples`; caminho relativo `internal/publishing-templates.md`; ref `a4b4827297bec79b81ddb2ff22a53089ebe88cd8`; o documento informa que mudanças em READMEs de exemplos criam drafts e descreve atualização/publicação via Contentful [8]. O conteúdo contém instruções para funcionários e referências a variáveis/serviço privado; nenhum segredo ou valor privado foi armazenado neste relatório.

## Limitações e decisão de coverage

- `partial` é a classificação apropriada: há evidência forte para o snapshot do repositório, README, schema e um registro de frontmatter, mas não foi feita enumeração e validação individual de todos os READMEs do monorepo.
- A árvore `truncated: false` permite afirmar completude da árvore GitHub **daquele commit consultado**, não completude do catálogo de templates, da galeria Vercel ou de repositórios de terceiros [1] [2].
- README, frontmatter, URLs de demo e metadados da API não são prova de funcionamento em runtime. Não foram executados `pnpm`, scripts do candidato, builds, testes, deploys ou chamadas a dashboards privados.
- A licença MIT foi observada no metadado do repositório [3], enquanto a convenção do README recomenda MIT para novos exemplos [2]. Isso não constitui revisão de licenças de dependências, compatibilidade jurídica ou autorização para copiar código.
- O endpoint raw do README `solutions/monorepo/README.md` retornou somente um README de índice sem frontmatter; não foi tratado como registro de template individual. Nenhuma conclusão de ausência global foi extraída dessa observação.
- O conteúdo consultado é um snapshot temporal. A rota pode mudar após o commit fixado; qualquer integração futura deve repin a SHA e repetir as verificações.

## References

[1]: https://api.github.com/repos/vercel/examples/git/trees/a4b4827297bec79b81ddb2ff22a53089ebe88cd8?recursive=1 "GitHub recursive tree for vercel/examples at commit a4b4827297bec79b81ddb2ff22a53089ebe88cd8"
[2]: https://raw.githubusercontent.com/vercel/examples/a4b4827297bec79b81ddb2ff22a53089ebe88cd8/README.md "vercel/examples README at pinned commit"
[3]: https://api.github.com/repos/vercel/examples "GitHub repository metadata for vercel/examples"
[4]: https://api.github.com/repos/vercel/examples/commits/main "GitHub main branch commit metadata for vercel/examples"
[5]: https://api.github.com/repos/vercel/examples/contents/README.md?ref=a4b4827297bec79b81ddb2ff22a53089ebe88cd8 "GitHub contents metadata for README.md at pinned commit"
[6]: https://raw.githubusercontent.com/vercel/examples/a4b4827297bec79b81ddb2ff22a53089ebe88cd8/internal/fields.json "Template fields schema at pinned commit"
[7]: https://raw.githubusercontent.com/vercel/examples/a4b4827297bec79b81ddb2ff22a53089ebe88cd8/edge-middleware/bot-protection-datadome/README.md "DataDome example README and frontmatter at pinned commit"
[8]: https://raw.githubusercontent.com/vercel/examples/a4b4827297bec79b81ddb2ff22a53089ebe88cd8/internal/publishing-templates.md "Publishing templates instructions at pinned commit"
