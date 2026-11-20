# Scout 30 — scikit-learn User Guide

## Identificação e escopo observado

- **Fonte principal:** scikit-learn User Guide.
- **Rota de entrada:** https://scikit-learn.org/stable/user_guide.html
- **Organização/autoria observável:** documentação oficial do projeto scikit-learn; a página pública aponta para o repositório `scikit-learn/scikit-learn` no GitHub. Não foi observada uma assinatura nominal de autor na página do User Guide.
- **Versão exibida:** a página estável de entrada do site identificou a documentação como `scikit-learn 1.9.1 documentation`; a home oficial informa que 1.9.1 ficou disponível em setembro de 2026 e 1.9.0 em junho de 2026. [1]
- **Repositório relacionado observado:** `https://github.com/scikit-learn/scikit-learn`, branch padrão `main`, licença exibida `BSD-3-Clause license`. O repositório lista, entre outros caminhos, `doc/`, `examples/` e `sklearn/`. [5]
- **Commit observado, sem tratá-lo como pin da documentação estável:** na página pública de commits da branch `main`, o commit mais recente exibido durante a pesquisa foi `e4b91c579c75e592ae202d5b8b1d230101d8203c` (`FEA Add array API support to coverage_error`, 17 nov. 2026). A página estável não informa que seu conteúdo esteja fixado nesse SHA; portanto, ele é apenas um registro do estado observado da branch principal. [6]

## Estrutura do User Guide

O índice oficial é hierárquico e organiza a documentação por tarefa, técnica e operação de ciclo de vida. A página de entrada expõe 15 áreas numeradas:

1. **Supervised learning**, com 17 subseções principais, incluindo modelos lineares, LDA/QDA, kernel ridge, SVM, SGD, vizinhos, processos Gaussianos, decomposição cruzada, Naive Bayes, árvores, ensembles, multiclass/multioutput, seleção de atributos, aprendizado semissupervisionado, regressão isotônica, calibração de probabilidade e redes neurais supervisionadas.
2. **Unsupervised learning**, com mistura Gaussiana, manifold learning, clustering, biclustering, decomposição/fatoração de matrizes, estimação de covariância, detecção de novidade/outliers, estimação de densidade e redes neurais não supervisionadas.
3. **Model selection and evaluation**, cobrindo validação cruzada, ajuste de hiperparâmetros, ajuste de limiar de decisão, métricas/scoring e curvas de validação.
4. **Metadata Routing**, incluindo exemplos de uso, interface da API e um “Metadata Routing Support Status”.
5. **Inspection**, com partial dependence/ICE e permutation feature importance.
6. **Visualizations**, com utilitários de plotagem e objetos de visualização.
7. **Callbacks**, incluindo registro, invocação, uso com meta-estimators, callbacks embutidos e “Callback Support Status”.
8. **Dataset transformations**, incluindo pipelines/estimadores compostos, extração de atributos, pré-processamento, imputação, redução dimensionalidade não supervisionada, projeções aleatórias, aproximações de kernel, métricas/afinidades/kernels e transformação do alvo `y`.
9. **Dataset loading utilities**, separando datasets toy, datasets do mundo real, datasets gerados e carregamento de outras fontes.
10. **Computing with scikit-learn**, com estratégias de escala, desempenho computacional e paralelismo/gestão de recursos.
11. **Model persistence**, incluindo visão geral, ONNX, `skops.io`, `pickle`/`joblib`/`cloudpickle`, limitações de segurança e manutenção e pontos-chave.
12. **Common pitfalls and recommended practices**, com pré-processamento inconsistente, data leakage e controle de aleatoriedade.
13. **Data Interoperability**, com saída Pandas/Polars via `set_output` e suporte experimental à Array API.
14. **Choosing the right estimator**, apresentado como um mapa separado de seleção de estimador.
15. **External Resources, Videos and Talks**, com MOOC, vídeos e tutoriais externos.

Essa enumeração é a estrutura editorial exposta no índice oficial, não uma afirmação de que cada subseção foi testada, executada ou avaliada pedagogicamente. O conteúdo do índice foi observado diretamente no HTML/Markdown extraído da rota de entrada. [2]

## Módulos, algoritmos e conceitos documentados

A estrutura combina módulos de alto nível e páginas técnicas. Entre os algoritmos explicitamente listados no índice estão Ordinary Least Squares, Ridge, Lasso, Elastic-Net, LARS, OMP, regressão Bayesiana, regressão logística, GLMs, SVM, SGD, vizinhos, Gaussian Processes, Naive Bayes, árvores, gradient boosting, random forests, bagging, voting, stacking, AdaBoost, PCA, kPCA, Truncated SVD/LSA, dictionary learning, factor analysis, ICA, NMF, LDA, K-means, Affinity Propagation, Mean Shift, Spectral Clustering, clustering hierárquico, DBSCAN, HDBSCAN, OPTICS, BIRCH, biclustering, estimação de densidade e RBM. [2]

As páginas também documentam mecanismos transversais, não apenas estimadores: validação cruzada, busca em grade e aleatória, successive halving, métricas de classificação/regressão/clustering, pipelines, `ColumnTransformer`, extração de atributos de texto/imagem/dicionários, imputação, projeção aleatória, kernels, persistência de modelos, controle de aleatoriedade, interoperabilidade de arrays e práticas contra vazamento de dados. [2]

A referência de API é apresentada pela própria documentação como referência de classes e funções, e recomenda o User Guide para detalhes e orientações de uso. Na amostra retornada, ela expõe objetos de configuração (`config_context`, `get_config`, `set_config`), a hierarquia de estimadores/mixins em `sklearn.base` e funções como `clone`, `is_classifier`, `is_clusterer` e `is_regressor`. Isso confirma uma separação editorial entre especificação de API e explicação conceitual do User Guide. [4]

## Exemplos

A galeria oficial de exemplos declara que reúne exemplos que mostram como scikit-learn pode ser usado; alguns ilustram a API em geral e outros tratam aplicações específicas em formato de tutorial. A própria galeria remete ao User Guide para explicações mais detalhadas. [3]

A organização observada inclui, entre outras, categorias de classificação, clustering, decomposição, imputação de valores ausentes, seleção de modelos, SVM e documentos de texto. Na amostra diretamente observada aparecem exemplos de comparação de classificadores, PCA com Iris, K-means em dígitos, imputação, busca aleatória versus grid search, successive halving, curvas ROC/precision-recall, validação cruzada, classificação de textos e clustering de documentos.

Esses registros comprovam a presença editorial de exemplos e seus títulos/rotas, mas não comprovam execução, saída correta, desempenho, reprodutibilidade ou qualidade pedagógica. A página da galeria é extensa e foi consultada por seleção de conteúdo; não foi produzido um inventário item a item de todos os exemplos.

## Status documental e manutenção

A documentação estável apresenta histórico de releases com versões 1.9.1, 1.9.0, 1.8.0 e versões anteriores. A página de histórico informa que os changelogs e release notes de todas as releases estão vinculados ali. [7]

A Developer’s Guide oficial documenta contribuição de código e documentação, construção local com Sphinx e geração da galeria. A instrução distingue uma construção usual do site sem a galeria (`make`) de `make html`, que também gera a galeria e executa os exemplos; a mesma página informa que GitHub Actions constrói automaticamente a documentação alterada em pull requests e disponibiliza o resultado renderizado. [8] Essa descrição é evidência do processo documental declarado, não prova de que este scout tenha executado a construção, os exemplos ou a suíte de testes.

O repositório GitHub observado identifica a licença como BSD-3-Clause e descreve o projeto como um módulo Python de machine learning construído sobre SciPy. A home oficial também declara que o projeto é open source, comercialmente utilizável e distribuído sob licença BSD. [1] [5] Não foi copiado código-fonte.

## Classificação de coverage

**Coverage: `partial`.** Há evidência direta e ampla da estrutura completa exposta no índice do User Guide, incluindo suas 15 áreas numeradas e subseções. Porém, o escopo solicitado também inclui módulos, algoritmos, exemplos e status documental; a API e a galeria são páginas muito extensas, e a consulta realizada foi seletiva, sem inventário exaustivo e sem pin da versão da documentação por SHA. Portanto, não seria correto declarar cobertura completa do conjunto de módulos ou de todos os exemplos.

## Limitações e não-verificações

- Não foi executado código, exemplo, teste, build Sphinx, notebook ou runtime.
- Não foram instaladas dependências nem clonado o repositório.
- A presença de uma seção, classe, função ou exemplo foi tratada como fato editorial/documental; não como prova de implementação funcional, qualidade, completude pedagógica ou desempenho.
- A galeria de exemplos e a API foram consultadas como páginas públicas extensas; a seleção retornada não constitui inventário exaustivo.
- A versão estável foi observada como 1.9.1 em 20 nov. 2026, mas não foi observada uma referência que fixe a publicação estável a um commit SHA específico.
- O SHA da branch `main` registrado acima pertence ao histórico público observado do repositório e não deve ser usado como pin da documentação estável.
- Nenhum caminho de arquivo do repositório foi validado contra um commit específico além dos diretórios de topo exibidos pela página pública do GitHub.

## References

[1]: https://scikit-learn.org/stable/index.html "scikit-learn homepage"
[2]: https://scikit-learn.org/stable/user_guide.html "User Guide — scikit-learn 1.9.1 documentation"
[3]: https://scikit-learn.org/stable/auto_examples/index.html "Examples"
[4]: https://scikit-learn.org/stable/api/index.html "API Reference"
[5]: https://github.com/scikit-learn/scikit-learn "scikit-learn GitHub repository"
[6]: https://github.com/scikit-learn/scikit-learn/commits/main/ "scikit-learn main commit history"
[7]: https://scikit-learn.org/stable/whats_new.html "Release History"
[8]: https://scikit-learn.org/stable/developers/contributing.html "Contributing — documentation and development"
