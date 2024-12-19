# Fondeadora Serverless Template Service

This project is a template for creating new Fondeadora Serverless services. It uses modern Python development tools and practices:

- [uv](https://docs.astral.sh/uv/) for dependency management and task automation
- [ruff](https://github.com/astral-sh/ruff) for formatting and linting
- [pytest](https://docs.pytest.org/) for testing
- [pyright](https://github.com/microsoft/pyright) for static type checking
- [pydantic](https://docs.pydantic.dev/) for data validation
- [AWS Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/latest/) for structured logging, tracing and error handling

## Project Structure

- [`src/`](./src/): Source code
- [`tests/`](./tests/): Unit tests
- [`serverless.yml`](./serverless.yml): Serverless service definition

Within the `src/` directory, you will find the following structure:

- `cash_deposits/`: An example module
  - `adapters/`: Adapters for external services infrastructure (implement ports defined in `domain/ports/`)
  - `domain/`: Domain logic
    - `ports/`: Ports for external services
    - `model.py`: Business model
  - `entrypoints/`: Lambda handlers
  - `services/`: Application services (expose use cases to entrypoints)

The main concepts behind this architecture are:

- **Ports and Adapters**: This architecture is based on the [Ports and Adapters](https://en.wikipedia.org/wiki/Ports_and_adapters_architecture) pattern. It allows the domain layer to be implemented independently of the infrastructure layer.
- **Domain-Driven Design**: The domain layer is the core of the application and contains the business logic. The application services layer is responsible for exposing use cases to the outside world (entrypoints). The adapters layer is responsible for integrating with the infrastructure layer (e.g. databases, message queues, etc.).

Usually the flow will go like this:

1. A Lambda function is invoked.
2. The request is processed by the entrypoint. We use AWS Lambda Powertools event parsers to extract the event data from the Lambda event to a Pydantic DTO.
3. The entrypoint calls an application service with the use case implementation, passing the DTO as an argument and any required dependencies.
4. The application service orchestrates the dependencies to gather required data.
5. The application service calls the domain logic to perform the necessary operations.
6. The domain logic returns the result, which is returned to the entrypoint.
7. The entrypoint returns the result to the caller.

## Development

Initialize virtual environment

```sh
uv venv
```
Activate with: source .venv/bin/activate


Install dependencies

```sh
uv sync -p 3.13
```

Run tasks

```sh
uv run poe format
uv run poe lint
uv run poe test
uv run poe ci
```

## Testing

We use [pytest](https://docs.pytest.org/) for testing. The tests are located in the `tests/` directory and are automatically discovered by pytest.

The directory structure of the tests should match the source code structure. For example, if you have a `cash_deposits/` module, you should have a `tests/cash_deposits/` directory with the tests inside.

## Deployment

This project is configured to be deployed using GitHub Actions. The deployment workflow is defined in [`.github/workflows/deploy.yaml`](./.github/workflows/deploy.yaml).
