# FastAPI Advanced Tutorials

This repository contains a collection of advanced FastAPI tutorials covering various aspects of modern API development.

## Tutorials

1. **API Versioning** (`22apiversioning/`)
   - Version-specific routers and models
   - Prometheus metrics integration
   - Request/response logging
   - Health check endpoints

2. **GraphQL Integration** (`23graphql/`)
   - Strawberry GraphQL integration
   - Queries and mutations
   - GraphQL types and schemas
   - CRUD operations through GraphQL

3. **WebSocket Security** (`24websocketsecurity/`)
   - Secure WebSocket connections with JWT
   - User management and password hashing
   - SQLAlchemy integration
   - Real-time message broadcasting

4. **Microservices and API Gateway** (`25microservices/`)
   - Service discovery and routing
   - Circuit breaker pattern
   - Load balancing
   - Health checks and CORS

5. **Event-Driven Architecture** (`26eventdriven/`)
   - RabbitMQ integration
   - Event publishing and consuming
   - Message persistence
   - Background tasks

6. **Distributed Tracing** (`27distributedtracing/`)
   - OpenTelemetry integration
   - Jaeger tracing
   - Prometheus metrics
   - Analytics endpoints

7. **CI/CD and Testing** (`28cicdtesting/`)
   - Unit and integration tests
   - GitHub Actions workflow
   - Docker configurations
   - Code coverage reporting

8. **API Gateway Security and Load Testing** (`29securityloadtesting/`)
   - Rate limiting
   - IP whitelisting/blacklisting
   - Security middleware
   - Load testing with Locust

## Requirements

- Python 3.9+
- FastAPI 0.68.0+
- Additional dependencies in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-tutorials
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Examples

Each tutorial is contained in its own directory with a dedicated Python file. To run any example:

1. Navigate to the tutorial directory:
```bash
cd <tutorial-directory>
```

2. Run the FastAPI application:
```bash
uvicorn <filename>:app --reload
```

For example, to run the API versioning example:
```bash
cd 22apiversioning
uvicorn 22apiversioning:app --reload
```

## Testing

To run the tests:

```bash
pytest
```

For coverage report:
```bash
pytest --cov=app --cov-report=html
```

## Load Testing

To run load tests with Locust:

```bash
cd 29securityloadtesting
locust -f 29securityloadtesting.py
```

Then open http://localhost:8089 in your browser.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 