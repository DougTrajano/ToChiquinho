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
    
    Pending

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
