# Anotação

Essa seção contém o [**processo de anotação dos dados**]{Anotação dos dados é o processo de rotulagem de dados. É usada para treinar diferentes modelos em computadores.} e as [diretrizes para anotadores](#diretrizes-para-anotadores) do dataset.

## Processo de anotação

Nós usamos anotadores qualificados para anotar os dados. Os anotadores foram treinados pelo autor do dataset.

### Concordância entre os anotadores

Cada comentário é avaliado por dois anotadores, caso haja discordância entre os anotadores, um terceiro anotador é usado para avaliar o comentário.

## Quem é um anotador qualificado?

Um anotador qualificado precisa ter as seguintes características:

- **Inglês básico**, já que a ferramenta de anotação é feita em Inglês.
- **Português nativo**, já que os textos do dataset são em Português do Brasil.
- Bom conhecimento sobre linguagem ofensiva (em Português) e como identificá-la. Os conceitos serão explicados em X.

## Diretrizes para anotadores

Os anotadores devem seguir as seguintes diretrizes:

---

Olá! Seja bem-vindo ao projeto de anotação de comentários ofensivos em português do Brasil.

Alerta! Você verá neste projeto várias frases ofensivas, tenha consciência de que elas não são direcionadas para você. Evite ficar muitas horas consecutivas fazendo este trabalho, sua saúde em primeiro lugar, combinado? ❤

Antes de começar, vamos alinhar alguns conceitos importantes.

### Qual a tarefa que você está fazendo?

Você deverá anotar/rotular comentários ofensivos. As informações que você fornecerá serão utilizadas para ajudar a identificar comentários ofensivos e/ou entender melhor o comportamento dos *haters*.

### Quais perguntas você deverá responder?

Para cada comentário, você deve responder as seguintes perguntas:

#### Is this text toxic? (Yes/No)

O comentário é ofensivo? Por padrão, o sistema pré-selecionará como "Yes" (Sim), caso o comentário não seja ofensivo, marque como "No" (Não).

#### Which kind of toxicity it has?

Qual o tipo de toxicidade o comentário possui? Responda com uma das opções abaixo:

##### Identity Attack

O comentário possui ataque a orientação sexual ou a identidade de gênero.

> Cuidado para não confundir com [sexismo](#sexism).

##### Insult

O comentário possui um insulto, injúria, xingamento, etc. com o propósito de humilhar ou atingir um ponto fraco da vítima.

##### Profanity/Obscene

O comentário possui palavras obscenas, vulgar, pornográficas, etc. 

##### Racism

O comentário é preconceituoso ou discriminatório com base na raça, cor ou etnia de uma pessoa ou grupo de pessoas.

##### Religious intolerance

O comentário é preconceituoso ou discriminatório com base na religião, culto ou prática religiosa de uma pessoa ou grupo de pessoas.

##### Sexism

O comentário é preconceituoso ou discriminatório com base no gênero de uma pessoa ou grupo de pessoas.

##### Xenophobia

O comentário é preconceituoso ou discriminatório com pessoas que são estrangeiras ou de outras culturas.

#### There's a specific target? (Individual/Group/Other)

Essa pergunta procura identificar se o comentário tóxico é direcionado a um indivíduo, um grupo ou a outros.

Marque apenas se existir um alvo claro do comentário tóxico.

#### Quais palavras são ofensivas/tóxicas?

Quais palavras são ofensivas ou tóxicas? Marque as palavras no texto que são profanas, insultantes ou tóxicas.

As *curse words* são palavras ou conjunto de palavras que serão profanas/insultantes.

Exemplo:

- Vai tomar no c@, seu arr0mb@d0

Na frase acima, temos duas *curse words* que devem ser marcadas: `vai tomar no c@` e `arr0mb@d0`.

Um outro exemplo:

"Que exemplo idiota! Você é burro demais."

Na frase acima, a palavra `idiota` e `burro` são exemplos de *curse words*.

Também são consideradas *curse words* conjunto de palavras, por exemplo: `vai a merda`.

Não selecione palavras como "seu", "sua", "é", etc.

### Perguntas frequentes

#### Diferença entre uma opinião negativa e um comentário tóxico

É importante entender a diferença entre uma opinião negativa e um comentário tóxico.

Uma **opinião negativa** é um texto que expõem uma opinião ou fato desagradável com duras palavras, normalmente criticam o trabalho ou ação de alguém, mas sem ferir a dignidade ou a honra de uma pessoa ou grupo.

Exemplos:

- USER Agora é " estupro" mesmo com a mulher dizendo que quis e gostou. Eu avisei que esse dia ia chegar.
- Moro conseguiu o que queria: eleger Bolsonaro em troca de um ministério. O que aconteceu depois foi "briga de quadrilha", na opinião do advogado Kakay. Por tudo isso, ele considera o ex-juiz "a própria fake news". Veja na última HASHTAG do ano! HASHTAG URL
- USER Crime é invadir a casa dos outros.

Um **comentário tóxico** extrapola a liberdade de expressão, normalmente contém palavras ofensivas ou insultantes. Procura denegrir a dignidade ou a honra de uma pessoa ou grupo.

Exemplos:

- O presidente da empresa USER é um idiota e não entende o que é importante para a empresa.
- Esse retardado não sabe jogar pqp

#### Erros ortográficos e formas de evitar a detecção de toxicidade

Os usuários podem digitar palavras errôneamente ou substituindo caracteres para evitar a detecção de toxicidade. Neste caso, você deve interpretar como palavras normais. 

Você deve seguir com as marcações da mesma forma, capturando as palavras como se estivessem corretas.

#### O texto é ilegível, o que fazer?

Se o texto for ilegível ou os processos de anonimização de dados removeram parte importante do texto, você pode clicar no botão "Skip" para pular o comentário.

Exemplo:

- USER HASHTAG
- USER f

#### É possível voltar em um comentário tóxico já anotado?

Não é possível.

---

Em caso de dúvidas, pode entrar em contato com Douglas Trajano.