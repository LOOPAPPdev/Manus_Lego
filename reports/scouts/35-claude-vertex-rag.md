# Claude Academy — Multi-index RAG pipeline com Claude no Google Cloud

**Fonte principal:** Claude Academy, organização Anthropic, curso público “Claude on Google Cloud”, aula “A Multi-index RAG pipeline”.  
**Rota de entrada:** https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai/a-multi-index-rag-pipeline  
**Data da consulta:** 2026-11-20.  
**Coverage:** `partial`.

A rota pública foi acessível sem login. A página identifica a aula como **Lesson 40 of 66**, com duração editorial de **8 min**, dentro do curso “Claude on Google Cloud”. O conteúdo observado é documental/educacional: descreve uma arquitetura híbrida e apresenta pseudocódigo/trechos de implementação. Não foi feito login, matrícula, chamada a API, execução de notebook, execução de pipeline ou validação de resultados em runtime.

## O que a aula pública cobre

A aula parte do pressuposto de que existem duas buscas independentes: busca semântica baseada em embeddings vetoriais e busca lexical BM25. O fluxo descrito envia a pergunta do usuário para os dois índices em paralelo e combina os resultados em uma lista ranqueada única. O texto apresenta uma classe `Retriever` como coordenadora, com uma interface comum de `add_document()` e `search()` para `VectorIndex` e `BM25Index`. [1]

A motivação para não somar diretamente os scores é que os índices usam escalas diferentes: a busca vetorial retorna similaridade de cosseno, enquanto BM25 retorna pontuação de relevância. A solução pedagógica apresentada é **Reciprocal Rank Fusion (RRF)**, que combina a posição dos documentos nos rankings, em vez de combinar scores brutos. A fórmula exibida é `RRF_score(d) = Σ(1 / (k + rank_i(d)))`; a aula diz que `k` costuma ser 60, mas usa 1 no exemplo para facilitar a leitura. [1]

O exemplo editorial usa três seções e dois rankings. A seção 2 aparece em primeiro no vetor e em segundo no BM25; a seção 7 aparece em segundo e terceiro; a seção 6 aparece em terceiro e primeiro. A aula calcula, respectivamente, scores RRF de 0,833, 0,583 e 0,75 e conclui com a ordem seção 2, seção 6, seção 7. Esses números são os resultados do exemplo didático da página, não uma medição independente deste scout. [1]

O trecho de implementação mostrado define `Retriever.__init__(*indexes)` e `search(query_text, k=1, k_rrf=60)`. A descrição informa que a lógica completa, parcialmente omitida no trecho visível, rastreia ranks por documento, calcula os scores RRF, descarta scores não positivos e retorna os documentos de maior score ordenados. A página também menciona validações para ausência de índices, query que não seja string, `k` não positivo e `k_rrf` negativo. Isso documenta a intenção da implementação, mas não comprova que o código foi executado ou que todas as validações funcionam. [1]

Na seção “Testing the Hybrid Approach”, a página afirma que, para a pergunta `what happened with INC-2023-Q4-011?`, a busca híbrida prioriza “Section 10: Cybersecurity Analysis”, seguida por “Section 2: Software Engineering” e “Section 5: Legal Developments”. A mesma seção contrasta uma saída de busca vetorial isolada e exibe scores aproximados para a saída híbrida. A evidência é uma descrição/saída apresentada pela própria aula; não há, nesta pesquisa, reprodução do notebook ou confirmação externa da qualidade, da base de documentos, do conjunto de avaliação ou da métrica. [1]

Por fim, a aula lista como benefícios uma arquitetura modular, extensibilidade por uma interface comum, combinação de compreensão semântica com correspondência lexical e possibilidade de adicionar outros índices. O diagrama textual menciona um possível terceiro índice, mas não define um índice concreto, um repositório, uma implementação ou um benchmark para ele. [1]

## Objetivos, pré-requisitos e posição no curso

A página do curso declara que “Claude on Google Cloud” ensina a trabalhar com modelos Anthropic através do Google Cloud Agent Platform, incluindo configuração, prompting, uso de ferramentas, RAG, agentes e padrões de implantação em produção. O curso lista 66 aulas, 9 quizzes, cerca de 8,5 horas e um badge de conclusão. [2]

Entre os resultados de aprendizagem publicados estão configurar modelos Claude no Agent Platform; construir pipelines RAG com chunking, embeddings, BM25 e contextual retrieval; usar recursos avançados do Claude; implementar MCP; e desenhar fluxos com agentes. A seção específica de RAG é descrita como um guia de implementação que cobre chunking, embeddings, busca híbrida com BM25, arquiteturas multi-index, reranking e contextual retrieval. A aula pesquisada é, portanto, uma parte do módulo RAG, não uma especificação completa de todo o curso. [2]

O curso informa como público “devs que querem adicionar recursos de IA aos seus apps”. Os pré-requisitos editoriais publicados são: proficiência em Python; conhecimento básico de manipulação de JSON; uma conta Google Cloud com acesso ao Agent Platform; e uma chave de API Claude além da conta Google Cloud, porque o projeto da seção de MCP chama diretamente a API Claude. A página não afirma que todos esses pré-requisitos são necessários para ler a aula 40, nem apresenta requisitos técnicos específicos adicionais para o algoritmo RRF. [2]

A aula anterior de configuração do Vertex AI orienta habilitar modelos Anthropic no Model Garden, instalar e autenticar o `gcloud`, selecionar o projeto e configurar Application Default Credentials. A própria página instrui `gcloud init`, `gcloud auth login`, `gcloud config set project YOUR_PROJECT_ID` e `gcloud auth application-default login`; essas são instruções editoriais para um aluno, não ações executadas nesta pesquisa. [3]

## Relação Claude–Vertex AI / Agent Platform

O curso enquadra Claude como modelo Anthropic acessado através do Google Cloud Agent Platform. A documentação atual do Google confirma que os modelos Anthropic Claude no Agent Platform são modelos serverless e totalmente gerenciados, acessados por API diretamente no endpoint do Agent Platform, sem necessidade de provisionar ou administrar infraestrutura. O Google também distingue essa oferta da plataforma de desenvolvimento Claude operada na infraestrutura da Anthropic. [4]

A documentação da Anthropic confirma que a oferta “Claude Models on Google Cloud (Google managed)” requer um projeto Google Cloud com acesso ao Agent Platform, a identidade chamadora com permissão `aiplatform.endpoints.predict` (por exemplo, o papel `roles/aiplatform.user`) e credenciais Google Cloud. Para a oferta gerenciada pelo Google, a documentação descreve endpoints que terminam em `:rawPredict` e `:streamRawPredict` para streaming, e clientes SDK como `AnthropicVertex`. Esses detalhes confirmam a relação de integração, mas não significam que a aula multi-index use necessariamente um modelo ou endpoint específico; a página da aula focaliza a recuperação e a fusão dos índices, não uma chamada concreta ao modelo. [5]

O Google documenta ainda que a habilitação de modelos parceiros é específica por projeto e administrada por entitlements do Google Cloud Marketplace. O estado deve ser verificado no model card do Model Garden; a documentação diz que listar modelos parceiros habilitados por projeto via CLI/API não é suportado. [4] Isso reforça que “Claude no Vertex AI” não equivale a uma capacidade local ou automaticamente disponível sem configuração e autorização do projeto.

A documentação do Google consultada registra que os modelos Anthropic não são um produto Google e estão sujeitos aos termos aplicáveis a ofertas separadas; ela também informa que a página foi atualizada em 2026-11-19. A página da Academia e a aula não exibem autor individual, data de publicação, versão de modelo, commit, branch ou licença de código/repositório. Não foi observado repositório público vinculado à aula, caminho de arquivos, SHA ou licença do material da aula. [4]

## Registros verificados

- **Organização/fonte editorial:** Claude Academy / Anthropic; curso público “Claude on Google Cloud”. [2]
- **Rota exata da aula:** `https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai/a-multi-index-rag-pipeline`. [1]
- **Título e posição:** “A Multi-index RAG pipeline”, Lesson 40 of 66, duração editorial 8 min. [1]
- **Tópicos observados:** interface unificada; `VectorIndex`; `BM25Index`; classe `Retriever`; Reciprocal Rank Fusion; implementação; teste narrado; benefícios da arquitetura híbrida. [1]
- **Fórmula observada:** `RRF_score(d) = Σ(1 / (k + rank_i(d)))`; a aula usa `k=1` no exemplo e menciona 60 como valor típico. [1]
- **Contexto do curso:** 66 aulas, 9 quizzes, aproximadamente 8,5 horas; RAG inclui chunking, embeddings, BM25, multi-index, reranking e contextual retrieval. [2]
- **Pré-requisitos editoriais do curso:** Python, JSON básico, conta Google Cloud com acesso ao Agent Platform e chave Claude para a parte de MCP. [2]
- **Relação de plataforma confirmada:** Claude é modelo Anthropic acessado via Agent Platform/Vertex AI; a oferta Google-managed é serverless e usa API gerenciada. [4] [5]
- **Requisitos de acesso documentados:** projeto Google Cloud, permissão `aiplatform.endpoints.predict`/papel compatível e credenciais Google Cloud para a oferta Google-managed. [5]
- **Caminhos/repositórios/branches/commits:** não observados na página da aula, na página do curso ou nas fontes oficiais consultadas; não foram inventados.
- **Licenças:** nenhuma licença foi observada para o material da Claude Academy ou para um repositório da aula. A página oficial do Google consultada declara CC BY 4.0 para o conteúdo, salvo indicação contrária, e Apache 2.0 para exemplos de código da documentação Google; isso se aplica à documentação Google indicada, não é atribuído à aula da Academia. [4]

## Limitações e classificação

A classificação é **partial**, não `complete`. A rota e as páginas relacionadas são públicas, mas o conteúdo é uma página de curso dinâmica e editorial; a consulta cobre a aula solicitada e o contexto diretamente relacionado, não um inventário exaustivo de todos os materiais, notebooks, avaliações, dependências ou fontes do curso. A listagem de 66 aulas foi observada na página do curso/aula, mas não foi tratada como prova de completude do conteúdo interno de cada aula. [1] [2]

Não foi feito login, matrícula, compra, execução de pipeline, execução de código, chamada a Vertex AI, acesso ao Model Garden, validação de permissões, medição de latência, comparação estatística, teste de qualidade, auditoria de segurança ou confirmação de resultados do exemplo INC-2023-Q4-011. Portanto, o relatório não afirma runtime, reprodutibilidade, qualidade pedagógica, completude da implementação, atualidade de modelos ou desempenho da arquitetura.

A fonte da aula não informa data de publicação, versão de modelo, versão de dependência, repositório, branch, commit/SHA, caminho de arquivo ou licença própria. Também não há evidência observada de um dataset completo, de uma suíte de testes independente, de uma métrica de recuperação, de uma implementação efetiva de embeddings/BM25 ou de uma implantação em produção. Esses campos permanecem não verificados.

## Referências

[1]: https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai/a-multi-index-rag-pipeline "A Multi-index RAG pipeline — Claude Academy"
[2]: https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai "Claude on Google Cloud — Claude Academy"
[3]: https://academy.claude.com/courses/claude-with-google-cloud-s-vertex-ai/vertex-ai-setup "Vertex AI Setup — Claude Academy"
[4]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude "Anthropic's Claude on Google Cloud models — Google Cloud Documentation"
[5]: https://docs.anthropic.com/en/api/claude-on-vertex-ai "Claude Models on Google Cloud (Google managed) — Anthropic Documentation"
