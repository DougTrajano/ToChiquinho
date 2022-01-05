# Annotation

This section describes the [**data annotation process**]{Data annotation is the categorization and labeling of data for AI applications,.} and the respective [guidelines](#annotators-guidelines) for the dataset.

## Annotation Process

We use [qualified annotators](#who-are-qualified-annotators) to annotate the dataset. The annotators are trained by the authors of the dataset.

Each sentence is tagged by at least three qualified annotators.

### Annotation Agreement

Pending

## Who are qualified annotators?

A qualified annotator must have the following attributes:
 
- **Basic English** as it has the language used in the annotation tool.
- **Native Portuguese** as the texts presented in the dataset are in Brazilian Portuguese.
- A good understanding of offensive language (in Portuguese) and how to detect it. The concepts will be explained below.

## Annotation Guidelines

The annotators are required to follow the following guidelines:

=== "English"
    Hi! Welcome to the Offensive Language Identification Dataset in Brazilian Portuguese.

    Warning! You will see several offensive phrases, be aware that they are not targeted for you. Avoid spending too many hours doing this work, your health first, ok? ❤

    Before starting, let's define some concepts and see some examples.

    **What is negative text?**

    A negative text is something that exposes an uncomfortable opinion or a negative sentiment, but it is not a threat.
    
    Example:

    - @USER @USER Obama wanted liberals & illegals to move into red states
    - @USER @USER @USER It’s not my fault you support gun control
    
    **What is offensive text?**

    An offensive text is something that exposes a threat or insult a person or a group of people.

    Examples:

    - @USER @USER Go home you’re drunk!!! @USER #MAGA #Trump2020 👊🇺🇸👊 URL
    - @USER Someone should'veTaken"" this piece of shit to a volcano. 😂

    **What is a bad sentence?**

    A bad sentence contains curse words, for example:

    - What a idiot example! You're Dork!

    In the above phrase, the words `idiot` and `Dork` are examples of bad sentences. Sets of words can also be used, for example: `piece of shit`.

    **Spelling errors and ways to avoid detection of toxicity**

    Misspellings should be interpreted as its own word, but it will not be fixed.

    Sometimes, users try to spell the curse words wrong to avoid detection of toxicity. For example:

    - M@therfucker! You're a piece of sh1t!
    
    You should follow the annotation in the same way as if the user wrote the sentence correctly.

=== "Portuguese"

    Olá! Seja bem-vindo ao projeto de anotação de comentários ofensivos em português do Brasil.

    Alerta! Você verá neste projeto várias frases ofensivas, tenha consciência de que elas não são direcionadas para você. Evite ficar muitas horas consecutivas fazendo este trabalho, sua saúde em primeiro lugar, combinado? ❤

    Antes de começar, vamos alinhar alguns conceitos importantes.

    ### What's the task to do?

    Você deverá anotar/rotular comentários ofensivos. As informações que você fornecerá serão utilizadas para ajudar a identificar comentários ofensivos e/ou entender melhor o comportamento dos *haters*.

    ### Which questions should I answer?

    Para cada comentário, você deve responder as seguintes perguntas:

    #### Is this text toxic? (Yes/No)
    
    O comentário é ofensivo? Por padrão, o sistema pré-selecionará como "Yes" (Sim), caso o comentário não seja ofensivo, marque como "No" (Não).

    #### Which kind of toxicity it has?

    Qual o tipo de toxicidade o comentário possui? Responda com uma das opções abaixo:

    ##### Identity Attack
    
    O comentário possui ataque a orientação sexual, identidade de gênero, ou gênero.
    
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
    
    ##### Xanophobia
    
    O comentário é preconceituoso ou discriminatório com pessoas que são estrangeiras ou de outras culturas.
    
    #### There's a specific target? (Individual/Group/Other)
    
    Essa pergunta procura identificar se o comentário tóxico é direcionado a um indivíduo, um grupo ou a outros.

    Marque apenas se existir um alvo claro do comentário tóxico.

    #### What words are toxic/offensive?

    Quais palavras são ofensivas ou tóxicas? Marque as palavras no texto que são profanas, insultantes ou tóxicas.

    As *curse words* são palavras ou conjunto de palavras que serão profanas/insultantes.

    Exemplo:

    - Vai tomar no c@, seu arr0mb@d0

    Na frase acima, temos duas *curse words* que devem ser marcadas: `vai tomar no c@` e `arr0mb@d0`.

    Um outro exemplo:

    "Que exemplo idiota! Você é burro demais."

    Na frase acima, a palavra `idiota` e `burro` são exemplos de *curse words*.
    
    Também são consideradas *curse words* conjunto de palavras, por exemplo: `vai a merda`.

    ### Diferença entre uma opinião negativa e um comentário tóxico

    É importante entender a diferença entre uma opinião negativa e um comentário tóxico.
    
    Uma **opinião negativa** é um texto que expõem uma opinião ou fato desagradável com duras palavras, normalmente criticam o trabalho ou ação de alguém, mas sem ferir a dignidade ou a honra de uma pessoa ou grupo.

    Exemplos:

    - Eu acredito que o presidente da empresa USER não faz um bom trabalho.
    - Perdemos, pois o jogador USER não fez nenhum gol.

    Um **comentário tóxico** extrapola a liberdade de expressão, normalmente contém palavras ofensivas ou insultantes. Procura denegrir a dignidade ou a honra de uma pessoa ou grupo.
    
    Exemplos:

    - O presidente da empresa USER é um idiota e não entende o que é importante para a empresa.
    - Esse retardado não sabe jogar pqp

    ### Erros ortográficos e formas de evitar a detecção de toxicidade

    Os usuários podem digitar palavras errôneamente ou substituindo caracteres para evitar a detecção de toxicidade. Neste caso, você deve interpretar como palavras normais, mas não serão corrigidas. 
    
    Você deve seguir com as marcações da mesma forma, capturando as palavras como se estivessem corretas.
    
    ---

    Em caso de dúvidas, pode entrar em contato com Douglas Trajano.