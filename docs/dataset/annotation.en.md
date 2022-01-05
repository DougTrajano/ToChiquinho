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