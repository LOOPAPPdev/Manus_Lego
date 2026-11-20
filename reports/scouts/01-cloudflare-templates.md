# Scout: `cloudflare/templates`

- **Rota:** https://github.com/cloudflare/templates
- **Tipo:** repositório oficial do GitHub
- **Data da verificação:** 2026-11-20
- **Coverage:** `complete` somente para o escopo verificável definido abaixo: o manifesto público `templates.json` na branch `main` e a correspondência das suas entradas com diretórios de template de primeiro nível na árvore completa do commit verificado. Isso não significa cobertura histórica, cobertura de outros canais Cloudflare, nem validação de runtime.

## Conclusão

A rota é pública, acessível e identificada como `cloudflare/templates`. A API pública do GitHub informa que o repositório é público, não é fork, não está arquivado, usa `main` como branch padrão e descreve o projeto como “Templates for Cloudflare Workers” [1]. A mesma resposta declara licença MIT/SPDX `MIT` no nível do repositório; o arquivo `LICENSE` está presente em `main` com SHA `93df5004e18e1c130ae042306137618603863bff` [1] [5].

A referência `refs/heads/main` apontava, no momento da consulta, para o commit `9674298a122ac464f8d4d8d2b38c3491d6b35d18` [2]. Nesse commit, `templates.json` foi verificado pelo endpoint de contents no caminho relativo `templates.json`, com blob SHA `654c18ece56fd0125376b41e90a6653030f8861b`, tamanho 4.586 bytes e URL pública de conteúdo [4]. O JSON contém 41 chaves sob `templates`; cada chave possui um `package_json_hash` [3] [4].

A árvore recursiva da API para o mesmo commit retornou `sha` `9674298a122ac464f8d4d8d2b38c3491d6b35d18` e `truncated: false` [6]. A comparação determinística entre o JSON decodificado e essa árvore encontrou 41 diretórios de primeiro nível terminados em `-template`, exatamente os mesmos 41 IDs do manifesto: nenhum ID do manifesto sem diretório correspondente e nenhum diretório desse padrão ausente do manifesto. Essa é a base para classificar a cobertura como completa para esse escopo restrito.

## Proveniência e metadados verificáveis

- **Provider/repositório:** GitHub, `cloudflare/templates`.
- **Repositório:** `https://github.com/cloudflare/templates`.
- **Branch observada:** `main`.
- **Commit observado:** `9674298a122ac464f8d4d8d2b38c3491d6b35d18`.
- **Manifesto:** `templates.json` no commit acima; blob SHA `654c18ece56fd0125376b41e90a6653030f8861b`.
- **Licença declarada pelo GitHub:** MIT; arquivo relativo `LICENSE`; blob SHA `93df5004e18e1c130ae042306137618603863bff`.
- **Árvore:** endpoint recursivo do commit acima; `truncated: false`.
- **Natureza da evidência:** metadados da API, conteúdo público do manifesto, SHA de blob e inventário de caminhos da árvore Git. README e metadados foram tratados como contexto de proveniência, não como prova de execução.

O README público diz que o repositório reúne templates iniciais para aplicações full-stack em Workers e documenta comandos de início e testes E2E [7]. Essa descrição é evidência documental de escopo e de existência de uma infraestrutura de testes no repositório, mas não constitui execução independente neste scout.

## Registros realmente verificados

Cada registro abaixo foi verificado como: (1) chave presente em `templates.json` no commit `9674298a122ac464f8d4d8d2b38c3491d6b35d18`; (2) diretório de primeiro nível com o mesmo caminho relativo na árvore completa do mesmo commit; (3) entrada contendo `package_json_hash` no manifesto. O caminho relativo é o ID seguido de `/` para indicar a raiz do template.

1. `agent-visibility-template` — `agent-visibility-template/`
2. `astro-blog-starter-template` — `astro-blog-starter-template/`
3. `chanfana-openapi-template` — `chanfana-openapi-template/`
4. `d1-template` — `d1-template/`
5. `durable-chat-template` — `durable-chat-template/`
6. `llm-chat-app-template` — `llm-chat-app-template/`
7. `multiplayer-globe-template` — `multiplayer-globe-template/`
8. `next-starter-template` — `next-starter-template/`
9. `openauth-template` — `openauth-template/`
10. `r2-explorer-template` — `r2-explorer-template/`
11. `react-postgres-fullstack-template` — `react-postgres-fullstack-template/`
12. `react-router-hono-fullstack-template` — `react-router-hono-fullstack-template/`
13. `react-router-starter-template` — `react-router-starter-template/`
14. `remix-starter-template` — `remix-starter-template/`
15. `saas-admin-template` — `saas-admin-template/`
16. `text-to-image-template` — `text-to-image-template/`
17. `to-do-list-kv-template` — `to-do-list-kv-template/`
18. `vite-react-template` — `vite-react-template/`
19. `worker-publisher-template` — `worker-publisher-template/`
20. `containers-template` — `containers-template/`
21. `d1-starter-sessions-api-template` — `d1-starter-sessions-api-template/`
22. `hello-world-do-template` — `hello-world-do-template/`
23. `mysql-hyperdrive-template` — `mysql-hyperdrive-template/`
24. `nlweb-template` — `nlweb-template/`
25. `nodejs-http-server-template` — `nodejs-http-server-template/`
26. `postgres-hyperdrive-template` — `postgres-hyperdrive-template/`
27. `react-router-postgres-ssr-template` — `react-router-postgres-ssr-template/`
28. `x402-proxy-template` — `x402-proxy-template/`
29. `workflows-starter-template` — `workflows-starter-template/`
30. `workers-for-platforms-template` — `workers-for-platforms-template/`
31. `microfrontend-template` — `microfrontend-template/`
32. `workers-builds-notifications-template` — `workers-builds-notifications-template/`
33. `ai-brand-visibility-template` — `ai-brand-visibility-template/`
34. `commerce-llms-txt-template` — `commerce-llms-txt-template/`
35. `agent-commerce-analytics-template` — `agent-commerce-analytics-template/`
36. `react-starter-template` — `react-starter-template/`
37. `internal-sites-template` — `internal-sites-template/`
38. `voice-agent-template` — `voice-agent-template/`
39. `email-routing-template` — `email-routing-template/`
40. `email-sending-template` — `email-sending-template/`
41. `grpc-container-template` — `grpc-container-template/`

O manifesto fornece `package_json_hash` para cada um desses IDs, mas esse campo não foi reinterpretado como SHA de commit nem como prova de conteúdo executável. Para os registros acima, o commit de proveniência é o commit do repositório (`9674298a122ac464f8d4d8d2b38c3491d6b35d18`), e a evidência de caminho é a árvore Git desse commit [3] [4] [6].

## Limitações e segurança da conclusão

- A verificação é um snapshot da branch `main` no instante da consulta. A branch pode avançar; o commit acima deve ser usado para reproduzir o resultado.
- “Completa” aplica-se apenas à relação `templates.json` ↔ diretórios de primeiro nível `*-template` dentro da árvore não truncada daquele commit. Não sustenta que o repositório contenha todos os templates já publicados pela Cloudflare, todos os templates históricos, todos os templates exibidos por dashboards, ou templates fora deste repositório.
- A árvore Git é um inventário de caminhos e objetos. Não é um grafo completo de dependências e não prova que qualquer template inicia, compila, faz deploy ou passa em testes em runtime.
- Não foram executados scripts, instalações, comandos `npm`/`pnpm`, servidores, deploys, testes E2E ou chamadas autenticadas. O README descreve testes E2E, mas essa descrição não foi usada como resultado de teste [7].
- Os `package_json_hash` do manifesto foram registrados como metadados do manifesto. Não foi feita inferência adicional sobre seu algoritmo, nem foram tratados como commits.
- A licença MIT foi observada no nível do repositório. Isso não substitui uma revisão de licenças de dependências, subdiretórios ou conteúdo de terceiros antes de reutilização.
- Nenhum dashboard privado, identificador de conta, credencial, token ou segredo foi acessado ou armazenado.

## References

[1]: https://api.github.com/repos/cloudflare/templates "GitHub repository metadata for cloudflare/templates"
[2]: https://api.github.com/repos/cloudflare/templates/git/ref/heads/main "GitHub reference for the main branch"
[3]: https://raw.githubusercontent.com/cloudflare/templates/main/templates.json "Public templates.json manifest"
[4]: https://api.github.com/repos/cloudflare/templates/contents/templates.json?ref=main "GitHub contents metadata for templates.json"
[5]: https://api.github.com/repos/cloudflare/templates/contents/LICENSE?ref=main "GitHub contents metadata for the repository LICENSE"
[6]: https://api.github.com/repos/cloudflare/templates/git/trees/main?recursive=1 "Recursive Git tree for cloudflare/templates"
[7]: https://raw.githubusercontent.com/cloudflare/templates/main/README.md "Public README for cloudflare/templates"
