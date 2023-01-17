# ToChiquinho

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DougTrajano_ToChiquinho&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DougTrajano_ToChiquinho)

ToChiquinho is a toxicity detection system for Brazilian Portuguese texts based on the [OLID-BR](https://github.com/DougTrajano/olid-br/) dataset.

## Modeling features

- Early stopping policy (patience).
- Imbalanced dataset handling.
- Hyperparameter optimization (Bayesian optimization).

## Usage

ToChiquinho is available as a Docker image. To run it, you need to have Docker installed on your machine.

Then, you can run the following command:

```bash
docker run -p 5000:5000 dougtrajano/tochiquinho
```

### Defining the task

ToChiquinho is a toxicity detection system with multiple tasks. You can parameterize the task that will be served by the API by setting the `API_TASK` environment variable. The available tasks are:

- `all`: serves all tasks (default) - Warning: this task is not recommended for production environments.
- `route`: serves the route task. This task is recommended for production environments.
- `toxic_spans`: serves the toxic spans detection task.
- `toxicity_target_type`: serves the toxicity target type identification task.
- `toxicity_target`: serves the toxicity target classification task.
- `toxicity_type`: serves the toxicity type detection task.
- `toxicity`: serves the toxicity classification task.

See more in the [Environment variables](#environment-variables) section.

## Environment variables


| Variable | Description | Default |
|----------|-------------|---------|


## Changelog

See the [GitHub Releases](https://github.com/DougTrajano/ToChiquinho/releases) page for a history of notable changes to this project.

## License

The project is licensed under the [Apache 2.0 License](LICENSE).