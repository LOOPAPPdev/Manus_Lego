# Scout 33 — Amazon book: *AI Engineering*

## Resultado

**Coverage: partial.** A rota pública indicada da Amazon Brasil foi aberta sem login, mas respondeu com uma página de erro da própria Amazon (“Algo deu errado”), em `/error/500`, sem metadados do livro, preço, estado de estoque ou conteúdo editorial observável [1]. Portanto, os campos específicos da oferta Amazon Brasil não podem ser confirmados.

Como confirmação oficial diretamente relacionada, a página da O’Reilly para o título apresenta um registro editorial de *AI Engineering*, de Chip Huyen, com data “December 2024”, 534 páginas, nível “Intermediate to advanced”, duração indicada de 15h 52m, idioma inglês e editora O’Reilly Media, Inc. [2]. Essa página também exibe “Buy online” e acesso por assinatura, mas isso não prova estoque, preço ou disponibilidade da oferta Amazon Brasil.

## Metadados observados

- **Título:** *AI Engineering*.
- **Subtítulo associado ao produto solicitado:** *Building Applications with Foundation Models*. O subtítulo aparece no título da rota Amazon indicada e no resultado público de busca associado ao ISBN, mas não foi renderizado na página Amazon Brasil durante esta consulta [1].
- **Autoria:** Chip Huyen. A O’Reilly atribui o livro a Chip Huyen [2]. O site oficial da autora também identifica *AI Engineering* como seu livro de 2025 [3].
- **Editora:** O’Reilly Media, Inc., conforme o registro editorial da O’Reilly [2].
- **Data:** a O’Reilly mostra “December 2024” no registro da obra [2]. O site oficial da autora chama o livro de “2025” [3]. A página Amazon Brasil não permitiu resolver essa diferença; ela pode refletir edição, formato ou convenção editorial diferente, mas não deve ser inferida como uma única data confirmada para a oferta Amazon Brasil.
- **Idioma:** English, conforme a O’Reilly [2]. Não foi possível verificar idioma de uma edição Amazon Brasil específica.
- **Extensão:** 534 páginas, conforme a O’Reilly [2].
- **Classificação editorial:** “Intermediate to advanced”, conforme a O’Reilly [2]. Isso é um rótulo editorial, não uma avaliação independente de qualidade pedagógica.
- **ISBN exibido na O’Reilly:** `9781098166298` [2]. A rota Amazon Brasil fornecida pelo solicitante usa o identificador `1098166302`; como a página Amazon Brasil falhou e os identificadores não coincidem literalmente, este relatório não os funde nem afirma equivalência de edição.

## Sumário e descrição editorial observados

A O’Reilly apresenta um sumário que inclui prefácio, dez capítulos, epílogo, índice e seção sobre a autora [2]. Os títulos de capítulos visíveis são:

1. “Introduction to Building AI Applications with Foundation Models”;
2. “Understanding Foundation Models”;
3. “Evaluation Methodology”;
4. “Evaluate AI Systems”;
5. “Prompt Engineering”;
6. “RAG and Agents”;
7. “Finetuning”;
8. “Dataset Engineering”;
9. “Inference Optimization”;
10. “AI Engineering Architecture and User Feedback”.

A descrição editorial da O’Reilly caracteriza o livro como uma discussão sobre engenharia de IA e construção de aplicações sobre modelos fundacionais disponíveis. Também menciona avaliação de modelos abertos, modelos, conjuntos de dados, benchmarks, padrões de aplicação, prompt engineering, RAG, fine-tuning, agentes, engenharia de datasets e otimização de latência e custo [2]. Esses pontos são transcrições/paráfrases da descrição editorial observada; não constituem prova de execução de exemplos, completude técnica, qualidade pedagógica ou desempenho de qualquer sistema.

O sumário acima é o sumário público exibido pela O’Reilly, não uma prova de que a página Amazon Brasil contenha todos esses itens. Como a página Amazon Brasil foi inacessível, a cobertura do sumário na fonte de entrada permanece parcial.

## Disponibilidade e recursos relacionados

O repositório público `chiphuyen/aie-book` declara ser um repositório de recursos para engenheiros de IA e materiais de apoio para o livro *AI Engineering* (Chip Huyen, 2025) [4]. Sua página lista links públicos para Amazon, O’Reilly, Kindle e Audible, além de arquivos como `ToC.md`, `chapter-summaries.md`, `study-notes.md` e `resources.md` [4]. A presença desses links e arquivos é evidência de publicação pública do repositório e de materiais relacionados; não prova que a oferta Amazon Brasil esteja disponível, em estoque, gratuita, licenciada para redistribuição ou acessível sem compra.

O site oficial de Chip Huyen identifica a autora como escritora e cientista da computação e afirma que seu livro *AI Engineering* é de 2025, com link para uma página Amazon abreviada e para a O’Reilly [3]. Isso confirma a relação pública entre autora, título e editor/plataforma, mas não substitui a ficha do produto Amazon Brasil.

## Limitações e não verificações

- A rota solicitada `https://www.amazon.com.br/AI-Engineering-Building-Applications-Foundation/dp/1098166302/` retornou a página pública de erro da Amazon (`https://www.amazon.com.br/error/500`), sem ficha do produto [1].
- Não foi possível confirmar na Amazon Brasil: preço, moeda, vendedor, estoque, formatos disponíveis, data de entrega, avaliações, idioma da edição, edição, ISBN-13, descrição integral ou sumário.
- Uma tentativa de abrir a página equivalente na Amazon.com foi bloqueada por restrição de acesso do navegador; não foi usada como confirmação adicional.
- A página O’Reilly foi entregue com bloqueio de CAPTCHA, embora seu conteúdo textual público tenha exposto o registro editorial e o sumário [2]. Isso reduz a verificabilidade direta da página e mantém a classificação como `partial`.
- A O’Reilly exibe `9781098166298`, enquanto a rota de entrada contém `1098166302`. Não há base suficiente neste scout para declarar que representam a mesma edição ou formato.
- Nenhuma compra, login, matrícula, download protegido, execução de código ou ação externa foi realizada.
- Não foram inferidos preço, licença do livro, completude dos materiais, qualidade pedagógica, resultados de runtime ou cobertura completa do conteúdo.

## Referências

[1]: https://www.amazon.com.br/AI-Engineering-Building-Applications-Foundation/dp/1098166302/ "Amazon Brasil — AI Engineering (rota indicada)"

[2]: https://www.oreilly.com/library/view/ai-engineering/9781098166298/ "O’Reilly — AI Engineering"

[3]: https://huyenchip.com/ "Chip Huyen — site oficial"

[4]: https://github.com/chiphuyen/aie-book "GitHub — chiphuyen/aie-book"
