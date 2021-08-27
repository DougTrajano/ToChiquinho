# Annotation

This section describes the [**data annotation process**]{Data annotation is the categorization and labeling of data for AI applications,.} and the respective [guidelines](#annotators-guidelines) for the dataset.

## Annotation process

We use [qualified annotators](#who-are-qualified-annotators) to annotate and labeling the dataset. The annotators are trained by the authors of the dataset.

The majority vote strategy is used to aggregate the annotations and provide a higher-level annotation.

Each sentence is tagged by at least three qualified annotators.

## Who are qualified annotators?

A qualified annotators has the following requirements:

- **Basic English** as it has the language used in the annotation tool.
- **Native Portuguese** as the texts presented in the dataset are in Brazilian Portuguese.
- A good understanding about offensive language (in portuguese) and how to detect it.

## Annotators guidelines

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

    Olá! Seja bem-vindo ao projeto de rotulação de textos ofensivos em português do Brasil.

    Alerta! Você verá neste projeto várias frases ofensivas, tenha consciência de que elas não são direcionadas para você. Evite ficar muitas horas consecutivas fazendo este trabalho, sua saúde em primeiro lugar, combinado? ❤

    Antes de começar, vamos alinhar alguns conceitos que podem ser úteis em momentos de dúvidas, ok?

    **O que é um texto negativo?**

    Um texto negativo é algo que expõem uma opinião ou fato desagradável, mas sem ferir a imagem ou honra de uma pessoa ou grupo.

    Exemplo:

    - Eu acredito que o presidente da empresa USER não faz um bom trabalho.
    - Perdemos, pois o jogador USER não fez nenhum gol.

    **O que é um texto ofensivo?**

    Um texto ofensivo é algo que extrapola a liberdade de expressão e fere a imagem ou honra de uma pessoa ou grupo. 

    Exemplos:

    - O presidente da empresa USER é um idiota e não entende o que é importante para a empresa.
    - Esse retardado não sabe jogar pqp

    **O que é uma *bad sentence*?**

    Uma *bad sentence* é uma palavra ou conjunto de palavras que em si é ofensivo, por exemplo:

    "Que exemplo idiota! Você é burro demais."

    Na frase acima, a palavra `idiota` e `burro` são exemplos de *bad sentences*. Também podem ser usadas conjunto de palavras, por exemplo: `vai a merda`.

    **Erros ortográficos e maneiras de evitar detecção de toxicidade**

    Palavras com erros ortográficos devem ser interpretadas como palavras normais, mas não serão corrigidas.

    Muitas vezes, usuários mudam a ortografia de uma palavra para tentar evitar que o texto seja detectado como ofensivo. Por exemplo:

    - Vai tomar no c@, seu arr0mb@d0

    Você deve seguir com as marcações da mesma forma, capturando as palavras como se estivessem corretas.
    
    ---

    Em caso de dúvidas, pode entrar em contato com Douglas Trajano.
