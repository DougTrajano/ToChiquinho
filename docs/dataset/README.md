# OLID-BR Dataset

OLID-BR contains a collection of annotated sentences in Brazilian Portuguese using an annotation model that encompasses the following levels:

- [[Offensive content detection](#offensive-content-detection)]{Detect offensive content in sentences and categorize it.|top-right}
- [[Offensive target identification](#offensive-target-identification)]{Detect if a offensive sentence is targeted to a person or group of people.|top-right}
- [[Offensive spans identification](#offensive-spans-identification)]{Detect curse words in sentences.|top-right}

<figure>
  <img src="../images/olid-br-taxonomy.png"/>
  <figcaption>Hierarchical taxonomy for categorizing offensive language, proposed by author.</figcaption>
</figure>

## Categorization

### Offensive content detection

This level is used to detect offensive content in the sentence.

**Is it an offensive sentence?**

- `OFF` Offensive: Inappropriate language, insults, or threats.
- `NOT` Not offensive: No offense or profanity.

**Which category of offensive content is it?**

`Homophobia`, `Racism`, `Sexism`, `Identity Attack`, `Insult`, `Profanity`, `Sexually Explicit`, and `Xenophobia`.

See the [glossary](../glossary.md) for more information.

### Offensive target identification

**Is the offensive text targeted?**

- `TIN` Targeted Insult: Targeted insult or threat towards an individual, a group or other.
- `UNT` Untargeted: Non-targeted profanity and swearing.

**What is the target?**

- `IND` The offense targets an individual, often defined as “cyberbullying”.
- `GRP` The offense targets a group of people based on ethnicity, gender, sexual
- `OTH` The target can belong to other categories, such as an organization, an event, an issue, etc.

### Offensive spans identification

As toxic span we define a sequence of words that attribute to the text's toxicity. Consider, for example, the following text:

=== "English"
    > "This is a `stupid` example, so thank you for nothing `a!@#!@.`"

    The toxic spans are:

    ```python
    ["stupid", "a!@#!@."]
    ```

=== "Portuguese"
    > "Esse é um exemplo `estúpido`, então obrigado por nada `a!@#!@.`"

    The toxic spans are:

    ```python
    ["estúpido", "a!@#!@."]
    ```

[^1]: Zampieri et al. "Predicting the type and target of offensive posts in social media." NAACL 2019.
[^2]: João A. Leite, Diego F. Silva, Kalina Bontcheva, Carolina Scarton (2020): Toxic Language Detection in Social Media for Brazilian Portuguese: New Dataset and Multilingual Analysis. Published at AACL-IJCNLP 2020.