# Scout — Vercel AI templates

**Rota:** `https://vercel.com/templates/ai`  
**Tipo:** public Vercel category route  
**Observado em:** 2026-11-20 06:53–06:54 (UTC−03:00)  
**Coverage:** `partial`

## Resultado

A rota pública abriu e exibiu o título “AI app templates and examples”, o texto “Discover templates to jumpstart your AI application”, campo de busca, filtro e uma galeria renderizada no cliente. A primeira renderização mostrou 12 cartões e um botão `Load More`. Dois acionamentos sucessivos do botão acrescentaram mais 12 cartões cada, totalizando **36 cartões observados nesta sessão**. O botão continuou presente depois do segundo carregamento, portanto a observação não representa uma lista final nem uma enumeração exaustiva da categoria. A classificação é `partial`, não `complete`.

A página não expõe na URL um número de página ou cursor. A interação é incremental e mantém a mesma rota. O conteúdo extraído pelo navegador foi truncado depois de parte da galeria quando a lista cresceu, embora os cartões adicionais tenham sido visíveis no DOM/renderização. Isso impede afirmar, apenas com esta rota pública, quantas entradas existem no total ou que os 36 itens são todos os itens disponíveis.

## Entradas públicas observadas

Os 12 itens da carga inicial foram:

- eve Coding Agent — `/templates/eve/eve-coding-agent-template`
- eve Company Brain — `/templates/eve/eve-company-brain-template`
- Jev x AI SDK Form Router — `/templates/next.js/jev-and-ai-sdk`
- eve Web Chat — `/templates/eve/eve-chat-template`
- Hume AI - Empathic Voice Interface Starter — `/templates/next.js/empathic-voice-interface-starter`
- Lead Agent — `/templates/next.js/lead-processing-agent`
- Customer Reviews AI Summary — `/templates/next.js/customer-reviews-ai-summary-nextjs-vercel`
- Morphic: AI-powered answer engine — `/templates/next.js/morphic-ai-answer-engine-generative-ui`
- eve Mem0 Agent — `/templates/eve/eve-mem0-agent`
- Durable iMessage AI Agent — `/templates/nitro/durable-imessage-ai-agent`
- eve BELL Stack — `/templates/eve/bell-stack`
- eve Discord Community Agent — `/templates/eve/eve-discord-agent`

A primeira ação `Load More` acrescentou, entre outros cartões, Alt Text Generator, Paint by Text, qrGPT – AI QR Code Generator, Next.js OpenAI Doc Search Starter, Sourcery with Vercel, Liftoff – AI Mock Interview Simulator, Swift – AI Voice Assistant, Nuxt AI-powered Notion-like WYSIWYG editor, AI SDK Computer Use, Vercel x xAI Chatbot, Vibe Coding Platform e AI Research Agent. A segunda ação acrescentou JigsawStack Starter, Fal Video Generator, Forefront AI Dataset Filtering Tool, Kernel Browser Automation Starter, ChatHN – Chat with Hacker News, Stagehand + Next.js Quickstart, Open Source AI Artifacts and Code Execution, Azure AI RAG Chatbot Sample, Vercel x Groq Chatbot, Demo Banking Web App to Test with Autonoma AI, AI SDK Image Generator e Drama Engine Template.

Esses nomes e caminhos são **descoberta de galeria**, não verificação de código, runtime, licença ou repositório. A página de categoria por si só não fornece SHA de commit.

## Registros com origem pública verificada

### 1. Chatbot

- **Vercel detail URL:** `https://vercel.com/templates/next.js/chatbot`
- **Owner/repository exibidos no detalhe:** `vercel/chatbot`
- **Repository URL:** `https://github.com/vercel/chatbot`
- **Path relativo verificado:** `/` para o template; `README.md`, `LICENSE`, `package.json` e `.env.example` existem na árvore do commit consultado.
- **Branch/commit verificável:** `main` → `a8989b522fa3672a2ae52f053105e40993b36ca1`
- **License evidence:** o detalhe público fornece `https://github.com/vercel/chatbot/blob/main/LICENSE`; a API do repositório retornou `NOASSERTION` para o campo SPDX, portanto não foi convertido em uma licença SPDX afirmada.
- **Natureza da evidência:** o detalhe Vercel confirma owner e nome do repositório; a API pública GitHub confirma o repositório, branch, SHA e árvore não truncada. Não houve execução, instalação ou teste de runtime.

### 2. Morphic: AI-powered answer engine

- **Vercel detail URL:** `https://vercel.com/templates/next.js/morphic-ai-answer-engine-generative-ui`
- **Owner/repository exibidos no detalhe:** `miurla/morphic`
- **Repository URL:** `https://github.com/miurla/morphic`
- **Path relativo verificado:** `/` para o template; `README.md`, `LICENSE`, `package.json`, `evals/README.md` e `scripts/README.md` existem na árvore do commit consultado.
- **Branch/commit verificável:** `main` → `889d6254347657660491f56033cce497add99c69`
- **License evidence:** o detalhe público fornece `https://github.com/miurla/morphic/blob/main/LICENSE`; a API do repositório retornou SPDX `Apache-2.0` no momento da consulta.
- **Natureza da evidência:** o detalhe Vercel confirma owner e nome do repositório; a API pública GitHub confirma o repositório, branch, SHA e árvore não truncada. Não houve execução, instalação ou teste de runtime.

Os SHAs acima são o estado observável da branch `main` no momento da consulta, não uma afirmação de que a página Vercel tenha fixado esses commits. Para integração, o SHA deve ser preservado e o conteúdo/licença deve ser rechecado antes de qualquer reutilização.

## Limitações e status de evidência

- A cobertura é `partial`: foram observados 36 cartões após dois carregamentos, mas `Load More` continuou disponível e não existe prova pública de uma enumeração completa.
- A galeria é dinâmica e renderizada na página; o texto extraído ficou truncado quando a lista cresceu. Não foi usado endpoint interno ou API não documentada.
- A categoria não mostrou SHA, árvore de arquivos ou licença nos cartões. Essas propriedades foram verificadas separadamente apenas para Chatbot e Morphic, por meio das páginas de detalhe e da API pública do GitHub.
- O relatório não afirma que os templates funcionam em runtime. Nenhum candidato foi clonado, instalado, executado, implantado ou submetido a testes.
- Entradas cujo detalhe ou repositório não foi aberto permanecem apenas `discovered_unverified`; não foram inventados repositórios, caminhos, commits ou licenças.
- A galeria pode conter repositórios de terceiros fora de `vercel/examples`; por isso o monorepo oficial não é tratado como inventário completo da categoria.

## References

[1]: https://vercel.com/templates/ai "Vercel AI app templates and examples category"
[2]: https://vercel.com/templates/next.js/chatbot "Vercel Chatbot template detail"
[3]: https://github.com/vercel/chatbot "GitHub vercel/chatbot repository"
[4]: https://api.github.com/repos/vercel/chatbot "GitHub public repository API for vercel/chatbot"
[5]: https://api.github.com/repos/vercel/chatbot/git/ref/heads/main "GitHub main ref for vercel/chatbot"
[6]: https://api.github.com/repos/vercel/chatbot/git/trees/a8989b522fa3672a2ae52f053105e40993b36ca1?recursive=1 "GitHub tree at verified Chatbot commit"
[7]: https://vercel.com/templates/next.js/morphic-ai-answer-engine-generative-ui "Vercel Morphic template detail"
[8]: https://github.com/miurla/morphic "GitHub miurla/morphic repository"
[9]: https://api.github.com/repos/miurla/morphic "GitHub public repository API for miurla/morphic"
[10]: https://api.github.com/repos/miurla/morphic/git/ref/heads/main "GitHub main ref for miurla/morphic"
[11]: https://api.github.com/repos/miurla/morphic/git/trees/889d6254347657660491f56033cce497add99c69?recursive=1 "GitHub tree at verified Morphic commit"
[12]: https://github.com/vercel/examples "Vercel official examples repository; not a complete gallery inventory"
