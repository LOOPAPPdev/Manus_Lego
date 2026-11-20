# Scout 31 — Google Colab

**Fonte principal:** Google Colab, página pública de entrada — consultada em 2026-11-20.

**Coverage:** `partial`

A cobertura é parcial porque a página inicial é dinâmica e apresenta uma seleção de exemplos e novidades, não um inventário exaustivo de notebooks, documentação ou capacidades. A pesquisa ficou restrita a páginas públicas; não houve login, matrícula, compra, execução de notebook de terceiros, instalação ou clonagem de código.

## Produto e entrada pública

A entrada pública observada em [1] é a página inicial do Google Colab (`https://colab.research.google.com/`). Ela mostra um campo **Search notebooks**, uma ação **New notebook**, uma ação **Upload notebook** e uma seção **Example notebooks** com cartões visíveis como “Welcome to Colab”, “Antigravity CLI in Colab”, “Lyria”, “Live translation”, “Markdown Guide”, “Charts in Colab”, “External data: Drive, Sheets, and Cloud Storage”, “Getting started with BigQuery” e “Forms”. A própria página também apresenta um controle **See all**, mas a seleção visível não deve ser tratada como catálogo completo.

Na mesma entrada, a seção “What’s new” expõe links para um exemplo de notebook, referência de MCP, referência de API, anúncio e demonstração. A página também exibe links para VS Code, Colab CLI e produtos pagos do Colab. Esses elementos são evidência de caminhos de entrada e documentação disponibilizados pela interface pública; não são, por si só, prova de que cada recurso foi executado ou validado neste scout.

O cartão público “Welcome to Colab” levou ao endereço `https://colab.research.google.com/notebooks/intro.ipynb` [3]. A URL do notebook foi observada, mas a interface do notebook não carregou conteúdo legível nesta sessão. Não houve execução de células, aceite de permissões, montagem de Drive ou alteração do notebook. Portanto, o resultado prova a existência do link público de exemplo, não a execução, qualidade pedagógica, completude ou funcionamento de suas células.

## Produto documentado e modelo de notebook

A FAQ oficial define o Colab como um serviço de Jupyter Notebook hospedado que não requer configuração para uso e oferece acesso gratuito a recursos computacionais, incluindo GPUs e TPUs; o texto destaca machine learning, ciência de dados e educação como usos adequados [2]. A FAQ também explica que Jupyter é o projeto open source no qual Colab se baseia e que o Colab permite usar e compartilhar notebooks sem baixar, instalar ou executar o Jupyter localmente [2].

Segundo a documentação, notebooks são armazenados no Google Drive ou podem ser carregados do GitHub. O compartilhamento funciona de modo semelhante ao de Google Docs ou Sheets [2]. Ao compartilhar um notebook, são compartilhados seu texto, código, saídas e comentários; a máquina virtual, arquivos personalizados e bibliotecas configuradas não são compartilhados. A documentação recomenda incluir células que instalem e carreguem dependências ou arquivos necessários [2]. A FAQ também registra que notebooks Jupyter/IPython existentes podem ser importados pela opção “Upload notebook” [2].

O formato de saída documentado é o formato aberto Jupyter `.ipynb`; a FAQ informa que notebooks criados no Colab podem ser baixados do Google Drive ou do menu File do próprio Colab [2]. Isso confirma interoperabilidade no nível do formato do arquivo, mas não valida a reprodutibilidade de um notebook específico.

## Execução e runtime

A FAQ afirma que o código é executado em uma máquina virtual privada da conta do usuário. Máquinas virtuais são eliminadas após um período de inatividade e existe uma vida útil máxima imposta pelo serviço [2]. Isso é evidência documental sobre o modelo de execução, não uma medição realizada neste scout.

A documentação descreve runtimes gerenciados e também aponta alternativas públicas como GCP Marketplace, Colab Enterprise e runtime local controlado pelo usuário. Para essas alternativas, a FAQ registra uma limitação material: a montagem do Google Drive no filesystem do runtime não funcionará [2].

A FAQ documenta a ação “Runtime > Disconnect and delete runtime” para devolver máquinas virtuais gerenciadas ao estado original. Ela também informa que o Colab limita a frequência dessa ação para evitar consumo indevido de recursos [2]. Nenhuma dessas operações foi acionada nesta pesquisa.

## Limites e restrições visíveis

A documentação oficial declara que recursos não são garantidos nem ilimitados e que os limites de uso podem variar. Para o nível gratuito, o Colab prioriza usuários que estejam programando ativamente em um notebook [2]. A página de limites informa que limites gerais, timeouts de inatividade, vida máxima da VM, tipos de GPU e outros fatores variam ao longo do tempo e não são publicados pelo Colab [2]. Portanto, não é correto registrar números fixos de GPU, memória, disponibilidade ou duração como garantia geral.

Sobre duração, a FAQ informa que, no nível gratuito, notebooks podem executar por no máximo 12 horas, dependendo da disponibilidade e dos padrões de uso. Ela afirma também que, em geral, notebooks podem executar no máximo 12 horas; Colab Pro, Pro+ e Pay As You Go oferecem maior disponibilidade conforme saldo de unidades computacionais. A documentação menciona execução contínua de até 24 horas no Pro+ quando há unidades suficientes e diz que uma VM dedicada adquirida no GCP Marketplace pode relaxar limites de runtime e de inatividade [2]. Esses são limites e condições documentados pela fonte no momento da consulta, não resultados de teste.

A FAQ lista como proibidos nos runtimes gerenciados: hospedagem de arquivos ou mídia e outros serviços web não relacionados à computação interativa; torrents ou compartilhamento peer-to-peer; proxies remotos; mineração de criptomoedas; ataques de negação de serviço; quebra de senhas; uso de múltiplas contas para contornar restrições; criação de deepfakes; e técnicas de containerização para contornar políticas antiabuso [2]. Em runtimes gratuitos sem saldo positivo de unidades, também podem ser encerradas sem aviso atividades como SSH/desktop remoto, contornar a UI do notebook para interagir principalmente por uma web UI, treinamento de xadrez e workers de computação distribuída [2].

A fonte explica ainda que encerramentos prematuros podem ocorrer quando o usuário tenta contornar a UI do notebook e usa uma web UI para geração de conteúdo em runtime gerenciado gratuito. Não foi realizada tentativa de reproduzir esse comportamento [2].

## IA e recursos recentes documentados

A FAQ inclui uma seção “The New AI-First Colab”. Ela descreve uma experiência conversacional integrada, com geração e transformação de código, um Data Science Agent capaz de analisar dados, gerar um plano, executar código e apresentar resultados, além de transformação de código por linguagem natural [2]. A mesma documentação afirma que usuários elegíveis podem abrir o painel pelo ícone Gemini e que a disponibilidade depende, entre outros requisitos documentados, de idade mínima de 18 anos e localidade suportada [2].

A FAQ afirma que o agente pode criar e executar planos após o usuário revisar e escolher executar, e que pode gerar código que acesse a internet. Também afirma que, por padrão, a IA não acessa arquivos do Drive nem secrets do usuário, embora possa gerar código para acessá-los mediante solicitação explícita [2]. Essas afirmações são documentação de produto. Não constituem prova de que essas capacidades estavam disponíveis nesta sessão ou em toda conta/região.

## Registros verificados

- **Organização/produto:** Google — Google Colab; título observado da página: “Google Colab” [1] [2].
- **Rota pública:** `https://colab.research.google.com/` [1].
- **Notebook público observado:** `https://colab.research.google.com/notebooks/intro.ipynb`, link “Welcome to Colab” [3].
- **Documentação oficial observada:** `https://research.google.com/colaboratory/faq.html`, título “Google Colab”, FAQ pública [2].
- **Formato de notebook documentado:** Jupyter `.ipynb` [2].
- **Estado:** `reference_only` para a documentação e os links; não há evidência de runtime executado neste scout.
- **Commit, branch, repositório e licença:** não observados na fonte pública consultada; não registrados como fatos.
- **Preço:** a página inicial mostra links para planos/produtos pagos, mas este scout não confirmou tabela, valores ou condições comerciais; nenhum preço é registrado.

## Limitações

- A página inicial é dinâmica e a lista visível de exemplos é apenas uma amostra; o controle “See all” não foi usado para alegar inventário completo.
- O notebook público `intro.ipynb` foi apenas aberto por URL; não houve execução de células, instalação de dependências, autenticação, montagem de Drive ou avaliação de resultados.
- A FAQ declara que muitos limites variam e não são publicados. Os valores de duração acima são os únicos números materiais explicitamente encontrados no texto consultado e continuam condicionados à disponibilidade e ao uso.
- Não foi possível confirmar, sem login, elegibilidade regional, disponibilidade de IA, quotas da conta, tipos de hardware ou comportamento de um runtime específico.
- Não foram observados commit/SHA, branch, repositório de implementação ou licença aplicável ao serviço. A referência a Jupyter como projeto base não equivale a uma licença do serviço Colab nem autoriza copiar código.
- A pesquisa não constitui teste de runtime, benchmark, avaliação de segurança, avaliação pedagógica ou prova de completude funcional.

## References

[1]: https://colab.research.google.com/ "Google Colab — página pública de entrada"
[2]: https://research.google.com/colaboratory/faq.html "Google Colab — Frequently Asked Questions"
[3]: https://colab.research.google.com/notebooks/intro.ipynb "Google Colab — Welcome to Colab notebook"
