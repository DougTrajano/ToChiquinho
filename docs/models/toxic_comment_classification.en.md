---
title: Toxic Comment Classification
summary: Detects if the text is toxic or not.
---

Toxic Comment Classification is a method that detects if the text is toxic or not.

## Overview

**Input:** Text in Brazilian Portuguese

**Output:** Binary classification (toxic or not toxic)

**Model architecture:** BERT fine-tuned for binary classification

**Dataset:** [OLID-BR](https://dougtrajano.github.io/olid-br/)

## Usage

PENDING

## Limitations

The following factors may degrade the model’s performance.

**Text Language**:  The model was trained on Brazilian Portuguese texts, so it may not work well on other Portuguese dialects.

**Text Origin**: The model was trained on texts from social media and a few texts from other sources, so it may not work well on other types of texts.

## Trade-offs

Sometimes models exhibit performance issues under particular circumstances. In this section, we'll discuss situations in which you might discover that the model performs less than optimally, and should plan accordingly.

**Text Length**: The model was trained on texts with an average length of 50 words, so it may not work well on longer texts.

## Performance

The model was evaluated on the test set of the [OLID-BR](https://dougtrajano.github.io/olid-br/) dataset.

**Accuracy:** 0.8568

**Precision:** 0.8567

**Recall:** 0.8568

**F1-Score:** 0.8568

| Class | Precision | Recall | F1-Score | Support |
| :---: | :-------: | :----: | :------: | :-----: |
| `NOT` | 0.8679 | 0.8738 | 0.8709 | 1,775 |
| `OFF` | 0.8429 | 0.8359 | 0.8394 | 1,438 |

## Provide Feedback

If you have any feedback on this model, please [open an issue](https://github.com/DougTrajano/ToChiquinho/issues/new) on GitHub.
