# Cloudflare Workers platform services — scout 22

**source_id:** `22-cloudflare-services`  
**route:** `https://developers.cloudflare.com/workers/`  
**label:** Cloudflare Workers platform services  
**coverage:** `partial`  
**data da observação:** 2026-11-20

A rota pública de entrada descreve Cloudflare Workers como uma plataforma serverless para construir, implantar e escalar aplicações na rede global da Cloudflare. A mesma página lista integrações de armazenamento, computação, mídia, jobs em segundo plano e observabilidade. Entre as integrações explicitamente relacionadas estão Durable Objects, D1, KV, R2, Workers AI e Browser Run. [1]

## Registros verificados

### Workers e bindings

- **Produto:** Cloudflare Workers.
- **Referência pública:** `https://developers.cloudflare.com/workers/`.
- **Observação:** a página de entrada apresenta Workers como ambiente serverless de construção, implantação e escala; cita frameworks React, Vue, Svelte, Next, Astro e React Router, além de JavaScript, TypeScript, Python e Rust. Isso é documentação de produto, não prova de que um candidato específico foi compilado, implantado ou executado. [1]
- **Integração observada:** a documentação de Bindings afirma que bindings permitem ao Worker interagir com recursos da plataforma e lista AI, Browser Run, D1, Durable Objects, KV e R2, entre outros. A página também descreve binding como uma capacidade/permissão e uma API associadas ao Worker. [10]
- **Registro de execução:** nenhum Worker foi criado, implantado ou executado nesta exploração.

### D1

- **Produto:** Cloudflare D1.
- **Referência pública:** `https://developers.cloudflare.com/d1/`.
- **Observações verificadas:** D1 é documentado como banco de dados gerenciado serverless com semântica SQL de SQLite, acesso por Worker e API HTTP, recuperação de desastre e suporte a Time Travel. A página também documenta réplicas de leitura globais e uso a partir de Workers ou Pages. [2]
- **Classificação da evidência:** documentação e metadados de capacidade; não é prova de criação de banco, consulta bem-sucedida, recuperação ou desempenho.
- **Repositório, caminho, branch e SHA:** não observados nas páginas consultadas; nenhum valor foi inferido.

### R2

- **Produto:** Cloudflare R2 Storage.
- **Referência pública:** `https://developers.cloudflare.com/r2/`.
- **Observações verificadas:** R2 é documentado como armazenamento de objetos para dados não estruturados, incluindo aplicações cloud-native, conteúdo web, data lakes e artefatos ou datasets de processos de machine learning. A página menciona Location Hints, CORS, buckets públicos e tokens com escopo de bucket. [3]
- **Classificação da evidência:** documentação de produto e recursos; não é prova de bucket criado, upload, leitura, política CORS ou ausência de cobrança em uma execução real.
- **Repositório, caminho, branch e SHA:** não observados.

### KV

- **Produto:** Cloudflare Workers KV.
- **Referência pública:** `https://developers.cloudflare.com/kv/`.
- **Observações verificadas:** Workers KV é documentado como armazenamento global de chave-valor e baixa latência para APIs e sites dinâmicos. A documentação mostra acesso por bindings e REST API, e exemplifica operações put, get, list e delete. Também informa que KV pode armazenar configurações, preferências e detalhes de autenticação. [4]
- **Classificação da evidência:** exemplos e documentação de API; os trechos não constituem execução observada de nenhuma operação nem validação de consistência, latência ou limites.
- **Repositório, caminho, branch e SHA:** não observados.

### Durable Objects

- **Produto:** Cloudflare Durable Objects.
- **Referência pública:** `https://developers.cloudflare.com/durable-objects/`.
- **Observações verificadas:** Durable Objects são descritos como blocos para aplicações stateful e sistemas distribuídos. Cada objeto tem nome globalmente único e armazenamento durável associado, com consistência forte; a documentação cita coordenação entre clientes, chat, edição colaborativa, jogos multiplayer, WebSocket Hibernation, Storage API e alarms. [5]
- **Classificação da evidência:** documentação de arquitetura e APIs; não é prova de instância criada, coordenação entre clientes, transação ou execução de WebSocket.
- **Limitação específica:** a documentação de desenvolvimento local informa que bindings de Durable Objects não podem ser conectados remotamente com `remote: true` no fluxo local descrito; eles rodam localmente, embora possam interagir com outros recursos remotos por padrões documentados. [12]
- **Repositório, caminho, branch e SHA:** não observados.

### Containers

- **Produto:** Cloudflare Containers.
- **Referência pública:** `https://developers.cloudflare.com/containers/`.
- **Observações verificadas:** Containers são documentados como containers serverless executados ao lado de Workers, para cargas intensivas em CPU/memória/disco, runtimes específicos, sistemas de arquivos completos e imagens existentes. A página informa que instâncias são iniciadas sob demanda e controladas pelo código do Worker; também descreve integração com Durable Objects e implantação via Wrangler. [6]
- **Classificação da evidência:** documentação de produto e exemplos de configuração; o material não demonstra build de uma imagem, disponibilidade de uma instância ou deploy concluído.
- **Repositório, caminho, branch e SHA:** não observados.

### Workers AI

- **Produto:** Cloudflare Workers AI.
- **Referência pública:** `https://developers.cloudflare.com/workers-ai/`.
- **Observações verificadas:** Workers AI é documentado como execução de modelos de machine learning em GPUs serverless na rede Cloudflare, invocável a partir de Workers, Pages ou API Cloudflare. A página afirma haver catálogo de mais de 50 modelos open source, modelo de cobrança pay-for-what-you-use e integração relacionada com AI Gateway, Vectorize, R2, D1, Durable Objects e KV. [7]
- **Classificação da evidência:** documentação e catálogo declarativo de produto; não é prova de inferência, modelo específico carregado, latência, quota ou resultado de API.
- **Limitação específica:** a documentação de desenvolvimento local informa que modelos AI rodam remotamente; um binding Workers AI com `remote: false` produz erro, e a omissão de `remote` usa o recurso remoto com aviso. [12]
- **Repositório, caminho, branch e SHA:** não observados.

### Browser Rendering / Browser Run

- **Produto observado:** a página consultada em `https://developers.cloudflare.com/browser-rendering/` redireciona semanticamente para a documentação intitulada **Browser Run** em `https://developers.cloudflare.com/browser-run/`; o texto diz que Browser Run era anteriormente conhecido como Browser Rendering. [8]
- **Observações verificadas:** Browser Run é documentado como Chrome headless na rede global, com automação, scraping, testes, geração de conteúdo, screenshots, PDFs, snapshots, links, elementos HTML, dados estruturados e crawling. A documentação separa Quick Actions stateless de sessões controladas por Puppeteer, Playwright, CDP ou Stagehand, e relaciona integração com Workers e Durable Objects. [8]
- **Classificação da evidência:** documentação de produto e métodos de integração; não é prova de sessão de navegador iniciada, screenshot, PDF, crawl ou teste concluído.
- **Limitação específica:** a documentação de bindings lista Browser Run; a documentação de desenvolvimento local avisa que, sem `remote: true`, Browser Run gera um aviso para considerar uma experiência mais próxima da produção. [10] [12]
- **Repositório, caminho, branch e SHA:** não observados.

### Zero Trust / Cloudflare One

- **Produto:** Cloudflare One, incluindo o modelo Zero Trust e produtos relacionados.
- **Referência pública:** `https://developers.cloudflare.com/cloudflare-one/`.
- **Observações verificadas:** Cloudflare One é documentado como plataforma SASE que unifica rede e segurança. A descrição de Zero Trust afirma que cada requisição é autenticada e autorizada com base em identidade e contexto antes do acesso. A página lista Access, Tunnel, Secure Web Gateway, Browser Isolation, CASB, DLP, segurança de e-mail, DEX e outros produtos. [9]
- **Classificação da evidência:** documentação conceitual e catálogo de produtos; não é prova de política criada, usuário autenticado, túnel estabelecido, tráfego inspecionado ou evento de segurança.
- **Relação com Workers:** a documentação de Workers local menciona Cloudflare Access como consideração quando um Worker protegido por Access conecta-se a bindings remotos. Isso apenas documenta um caminho de integração e não demonstra uma conta ou configuração privada. [12]
- **Repositório, caminho, branch e SHA:** não observados.

## Relações de armazenamento e cobertura da entrada

A página pública “Choose a data or storage product” mapeia KV para armazenamento chave-valor, R2 para objetos, Durable Objects para coordenação e estado, e D1 para banco SQL leve. Ela também descreve cenários combinando vários produtos. [11] Essa página reforça a relação entre os produtos, mas não transforma a amostra em inventário completo da plataforma.

O índice público `https://developers.cloudflare.com/workers/llms.txt` expõe seções de overview, getting started, examples, languages e platform, além de links para templates, bindings, storage options e vários outros recursos. O índice é evidência de que a documentação é mais ampla que o foco deste scout, não uma enumeração exaustiva dos serviços Cloudflare existentes. [13]

## Proveniência e decisão de coverage

A fonte primária observada foi exclusivamente a documentação pública `developers.cloudflare.com`, entrando pela rota Workers e seguindo links oficiais para D1, R2, KV, Durable Objects, Containers, Workers AI, Browser Run, Cloudflare One, Bindings, storage options, local development e o índice `llms.txt`. Não foram acessados dashboards, contas, tokens, segredos ou APIs autenticadas. Não foi clonado, instalado ou executado código de candidato.

A cobertura é **partial**. Todos os oito focos pedidos têm pelo menos uma página pública oficial observada, mas a investigação é uma seleção orientada pelo escopo, não uma enumeração completa de todos os serviços, páginas, exemplos, repositórios ou capacidades da plataforma. Não há prova de execução, build, implantação, runtime, segurança operacional ou desempenho. Nenhum repositório, caminho relativo, branch ou commit/SHA foi observado nas páginas consultadas; portanto esses campos não são afirmados.

## References

[1]: https://developers.cloudflare.com/workers/ "Cloudflare Workers overview"
[2]: https://developers.cloudflare.com/d1/ "Cloudflare D1"
[3]: https://developers.cloudflare.com/r2/ "Cloudflare R2"
[4]: https://developers.cloudflare.com/kv/ "Cloudflare Workers KV"
[5]: https://developers.cloudflare.com/durable-objects/ "Cloudflare Durable Objects"
[6]: https://developers.cloudflare.com/containers/ "Cloudflare Containers"
[7]: https://developers.cloudflare.com/workers-ai/ "Cloudflare Workers AI"
[8]: https://developers.cloudflare.com/browser-run/ "Cloudflare Browser Run, formerly Browser Rendering"
[9]: https://developers.cloudflare.com/cloudflare-one/ "Cloudflare One and Zero Trust"
[10]: https://developers.cloudflare.com/workers/runtime-apis/bindings/ "Workers Bindings"
[11]: https://developers.cloudflare.com/workers/platform/storage-options/ "Choose a data or storage product"
[12]: https://developers.cloudflare.com/workers/local-development/ "Workers local development"
[13]: https://developers.cloudflare.com/workers/llms.txt "Workers documentation index"
