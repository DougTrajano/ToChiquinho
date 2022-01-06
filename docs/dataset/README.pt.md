---
title: OLID-BR
summary: Offensive Language Identification Dataset in Brazilian Portuguese.
---

# OLID-BR

OLID-BR contém uma coleção de frases anotadas em português brasileiro usando um modelo de anotação que abrange os seguintes níveis:

- [[Offensive content detection](#offensive-content-detection)]{Detect offensive content in sentences and categorize it.|top-right}
- [[Offense target identification](#offense-target-identification)]{Detect if an offensive sentence is targeted to a person or group of people.|top-right}
- [[Offensive spans identification](#offensive-spans-identification)]{Detect curse words in sentences.|top-right}

<figure>
  <img src="../images/olid-br-taxonomy.png"/>
  <figcaption>Taxonomia hierárquica para categorizar linguagem ofensiva, proposta pelo autor.</figcaption>
</figure>

## Categorização

### Offensive content detection

Este nível é usado para detectar conteúdo ofensivo em uma frase.

#### Este texto é ofensivo?

We use the [[Perspective API](https://www.perspectiveapi.com/)]{Perspective API is the product of a collaborative research effort by Jigsaw and Google's Counter Abuse Technology team.|top-right} to detect if the sentence contains offensive content with double-check by our [qualified annotators](annotation.md#who-are-qualified-annotators).

- `OFF` Offensive: Inappropriate language, insults, or threats.
- `NOT` Not offensive: No offense or profanity.

#### Qual tipo de ofensa o texto contém?

These categories are tagged by our annotators.

`Identity Attack`, `Insult`, `Profane`, `Racism`, `Religious intolerance`, `Sexism`, and `Xenophobia`.

See the [glossary](../glossary.md) for detailed explanation.

### Offense target identification

This level is used to detect if an offensive sentence is targeted to a person or group of people.

#### Este comentário ofensivo é direcionado a alguém?

- `TIN` Targeted Insult: Targeted insult or threat towards an individual, a group or other.
- `UNT` Untargeted: Non-targeted profanity and swearing.

#### Qual o alvo do comentário ofensivo?

- `IND` The offense targets an individual, often defined as “cyberbullying”.
- `GRP` The offense targets a group of people based on ethnicity, gender, sexual
- `OTH` The target can belong to other categories, such as an organization, an event, an issue, etc.

### Offensive spans identification

As toxic span we define a sequence of words that attribute to the text's toxicity. Consider, for example, the following text:

> "Esse é um exemplo `estúpido`, então obrigado por nada `a!@#!@.`"

The toxic spans are:

```python
["estúpido", "a!@#!@."]
```

[^1]: Zampieri et al. "Predicting the type and target of offensive posts in social media." NAACL 2019.
[^2]: João A. Leite, Diego F. Silva, Kalina Bontcheva, Carolina Scarton (2020): Toxic Language Detection in Social Media for Brazilian Portuguese: New Dataset and Multilingual Analysis. Published at AACL-IJCNLP 2020.
