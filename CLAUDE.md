# Linear Python Client

Fully typed Python SDK for the Linear GraphQL API. Provides both a programmatic client and a CLI.

## Quick Reference

- **Python**: 3.13+ (`.python-version`)
- **Package manager**: UV (`uv.lock`)
- **Build backend**: Hatchling
- **License**: MIT
- **Entry point**: `linear` CLI command

## Commands

```bash
make install          # uv sync
make test             # pytest
make cov              # pytest with coverage
make check            # ruff lint
make format           # ruff format + fix
make format-check     # format validation
make generate         # Regenerate models/client from schema
```

## Architecture

### Code generation pipeline

`linear.schema.graphql` (42K lines) → `bin/generate.py` → generates two files:

- `linear_python_client/models.py` — Pydantic v2 models (29+ entity types, connections, payloads, inputs)
- `linear_python_client/client.py` — HTTP client with 13 typed methods wrapping GraphQL queries/mutations

**Do not edit `models.py` or `client.py` by hand** — run `make generate` after modifying `bin/generate.py` or the schema.

### Hand-written files

- `linear_python_client/cli.py` — Click CLI with Rich table output, reads `LINEAR_API_KEY` env var
- `linear_python_client/__init__.py` — re-exports `LinearClient` and all models
- `bin/generate.py` — regex-based GraphQL schema parser and code generator

### Key patterns

- **Field naming**: GraphQL `camelCase` ↔ Python `snake_case` via Pydantic `Field(alias=...)` with `populate_by_name=True`
- **All response fields optional** (`Type | None = None`) because GraphQL returns only requested fields
- **Pagination**: Connection/Edge/PageInfo pattern with cursor-based pagination
- **Error handling**: `httpx.HTTPStatusError` raised on HTTP or GraphQL errors
- **Client**: uses `httpx` synchronous client, supports context manager protocol

### Dependencies

| Runtime | Dev |
|---------|-----|
| httpx >= 0.27 | pytest >= 8.0 |
| pydantic >= 2.0 | pytest-cov >= 6.0 |
| click >= 8.0 | ruff >= 0.11 |
| rich >= 13.0 | pre-commit >= 4.0 |

## Linting

Ruff with `line-length = 120`, rules: `E, F, I, N, W, UP, B, SIM, RUF`.

## Testing

- `tests/test_main.py` — client initialization (2 tests)
- `tests/test_cli.py` — CLI commands with mocked client (40+ tests), covers JSON and `--pretty` output modes
- Uses `unittest.mock.patch` and Click's `CliRunner`

## CLI commands

```
linear me                                    # Current user info
linear search <query>                        # Search issues
linear issues {list,get,create,update}       # Issue CRUD
linear teams list
linear projects list
linear cycles list
linear labels list
linear users list
linear workflows list
linear comments create <issue-id> <body>
```

Global flag: `--pretty` for Rich table output (default is JSON).
