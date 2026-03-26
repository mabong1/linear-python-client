# linear-python-client

Python client for the [Linear](https://linear.app) GraphQL API.

## Installation

```bash
pip install linear-python-client
```

## Usage

```python
from linear_python_client import LinearClient

client = LinearClient("your-api-key")

# Get current user
viewer = client.viewer()
print(viewer.name, viewer.email)

# List issues
issues = client.list_issues(first=10)
for issue in issues.nodes:
    print(issue.identifier, issue.title)

# Search issues
results = client.search_issues(query="bug fix")
for issue in results.nodes:
    print(issue.title)

# Create an issue
from linear_python_client import IssueCreateInput

result = client.create_issue(IssueCreateInput(
    title="My new issue",
    team_id="your-team-id",
    priority=2,
))
print(result.issue.identifier, result.issue.url)

# Update an issue
from linear_python_client import IssueUpdateInput

result = client.update_issue(issue_id, IssueUpdateInput(title="Renamed issue"))

# Use as context manager
with LinearClient("your-api-key") as client:
    teams = client.list_teams()
```

## CLI

Set the `LINEAR_API_KEY` environment variable and use the `linear` command:

```bash
export LINEAR_API_KEY="your-api-key"

linear me                              # Current user info
linear me --pretty                     # Rich table output
linear search "bug fix"                # Search issues
linear issues list                     # List issues
linear issues get <id>                 # Get issue details
linear issues create --title "Bug" --team-id <id>
linear issues update <id> --title "Renamed"
linear teams list                      # List teams
linear projects list                   # List projects
linear cycles list                     # List cycles
linear labels list                     # List labels
linear users list                      # List users
linear workflows list                  # List workflow states
linear comments create <issue-id> "Comment body"
```

All commands support `--pretty` for rich table output (default is JSON).

## Authentication

Get your API key from **Settings > API > Personal API keys** in your Linear workspace.

## Code generation

The client and models are generated from the [Linear GraphQL schema](https://github.com/linear/linear):

```bash
make generate
```

## Setup

```bash
make install
uv run pre-commit install
```

## Development

```bash
make test            # Run tests
make cov             # Run tests with coverage
make check           # Lint with ruff
make format          # Format code with ruff
make format-check    # Check formatting without modifying
make generate        # Regenerate models and client from schema
```

## Project structure

```
linear_python_client/
    __init__.py        # Package exports
    client.py          # LinearClient with all API methods (generated)
    models.py          # Pydantic models for all types (generated)
    cli.py             # CLI (Click + Rich)
bin/
    generate.py        # Code generator script
tests/                 # Tests
linear.schema.graphql  # Linear GraphQL schema
pyproject.toml         # Project configuration
Makefile               # Development commands
```

---

This project was generated with the help of AI (Claude).
