# Data Pipeline

Nessa página, nós vamos descrever a [**pipeline de dados**]{A data pipeline é uma série de processos de processamento de dados.} usados para gerar o dataset.

## Fonte de dados

Nós queremos coletar comentários de várias fontes, como:

- Instagram
- Facebook
- Twitter
- Twitch

Para cada fonte, definimos um conjunto de perfis públicos que queremos coletar comentários.

## Arquitetura

O seguinte diagrama mostra a arquitetura da [**pipeline de dados**]{A data pipeline é uma série de processos de processamento de dados.}.

<figure>
  <img src="../images/ingestion-pipeline.png"/>
  <figcaption>Arquitetura - Fonte: Elaborada pelo autor.</figcaption>
</figure>

## Filtragem

Nós queremos filtrar comentários que não sejam relevantes para o escopo do dataset. Para isso, definimos alguns critérios que cada comentário deve possuir.

- Comentários devem ser em português.
- Comentários devem ter um nível de toxicidade (medido pela Perspective API) maior que 0.5.

## Privacidade

Para garantir a privacidade dos usuários, nós aplicaremos algumas regras de anonimização dos dados diretamente na pipeline de dados.

- Usuários mencionados foram substituídos pelo texto "@USER".
- URLs foram substituídos pelo texto "URL".