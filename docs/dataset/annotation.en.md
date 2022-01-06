# Annotation

This section describes the [**data annotation process**]{Data annotation is the categorization and labeling of data for AI applications,.} and the [annotators guidelines](#annotators-guidelines) for the dataset.

## Annotation Process

We use [qualified annotators](#who-are-qualified-annotators) to annotate the dataset. The annotators are trained by the authors of the dataset.

### Annotation Agreement

Each comment is tagged by two juddges, if they disagree, a third judge will be asked to decide the annotation.

## Who are qualified annotators?

A qualified annotator must have the following attributes:
 
- **Basic English** as it has the language used in the annotation tool.
- **Native Portuguese** as the texts presented in the dataset are in Brazilian Portuguese.
- A good understanding of offensive language (in Portuguese) and how to detect it. The concepts will be explained below.

## Annotation Guidelines

Annotators must follow the following guidelines:

---

Hi! Welcome to the Offensive Language Annotation Project in Brazilian Portuguese.

Warning! You will see several offensive comments, be aware that they are not directed to you. Avoid spending too many consecutive hours doing this work, your health first, okay? ❤

Before starting, let's align some concepts.

### What's the task you are doing?

You must annotate/labeling offensive comments. The information you provide will be used to help identify offensive comments and/or better understand *haters* behavior.

### What questions should you answer?

For each comment, you must answer the following questions:

#### Is this text toxic? (Yes/No)

Is the comment offensive? By default the system will pre-select it as "Yes", if the comment is not offensive, mark it as "No".

#### Which kind of toxicity it has?

What kind of toxicity does the comment have? Respond with one of the options below:

##### Identity Attack

The comment has an attack on sexual orientation, gender identity, or gender.

##### Insult

The comment has an insult, insult, name calling, etc. for the purpose of humiliating or hitting a victim's weak point.

##### Profanity/Obscene

The comment has obscene, vulgar, pornographic, etc. words.

##### Racism

The comment is prejudiced or discriminatory based on the race, color or ethnicity of a person or group of people.

##### Religious intolerance

The comment is prejudiced or discriminatory based on the religion, cult or religious practice of a person or group of people.

##### Sexism

The comment is prejudiced or discriminatory based on the gender of a person or group of people.

##### Xanophobia

The comment is prejudiced or discriminatory towards people who are foreigners or from other cultures.

#### Is there a specific target? (Individual/Group/Other)

This question seeks to identify whether the toxic comment is directed at an individual, a group, or others.

Check only if there is a clear target for the toxic comment.

#### What words are offensive/toxic?

What words are offensive or toxic? Mark words in the text that are profane, insulting, or toxic.

*curse words* are words or set of words that will be profane/insulting.

Example:

- Will take it in c@, your arr0mb@d0

In the sentence above, we have two *curse words* that must be marked: `will take no c@` and `arr0mb@d0`.

Another example:

"What a silly example! You are too dumb."

In the sentence above, the word `idiot` and `dumb` are examples of *curse words*.

*curse words* are also considered a set of words, for example: `go to shit`.

### Difference between a negative opinion and a toxic comment

It's important to understand the difference between a negative opinion and a toxic comment.

A **negative opinion** is a text that exposes an unpleasant opinion or fact in harsh words, usually criticizing someone's work or action, but without hurting the dignity or honor of a person or group.

Examples:

- I believe that the president of the USER company does not do a good job.
- We lost because the USER player didn't score any goals.

A **toxic comment** goes beyond freedom of expression, usually contains offensive or insulting words. It seeks to denigrate the dignity or honor of a person or group.

Examples:

- The president of the USER company is an idiot and doesn't understand what is important to the company.
- This retard doesn't know how to play pqp

### Misspellings and ways to avoid detection of toxicity

Users may mistype words or substitute characters to avoid detection of toxicity. In this case, you should interpret them as normal words, but they won't be corrected.

You should follow through with the tags in the same way, capturing the words as if they were correct.

---

If you have any questions, you can contact Douglas Trajano.