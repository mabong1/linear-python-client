"""CLI for the Linear Python client."""

import functools
import json
import os
import sys

import click
import httpx
from rich.console import Console
from rich.table import Table
from rich.text import Text

from linear_python_client.client import LinearClient
from linear_python_client.models import CommentCreateInput, IssueCreateInput, IssueUpdateInput

console = Console()


def get_client() -> LinearClient:
    """Create a LinearClient from the LINEAR_API_KEY env var."""
    key = os.environ.get("LINEAR_API_KEY")
    if not key:
        click.echo("Error: LINEAR_API_KEY environment variable is not set.", err=True)
        sys.exit(1)
    return LinearClient(api_key=key)


def handle_api_errors(func):
    """Decorator to catch HTTP errors and print a user-friendly message."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            click.echo(f"API error {e.response.status_code}: {e.response.text}", err=True)
            sys.exit(1)

    return wrapper


def pretty_option(func):
    """Add --pretty flag to a command."""
    return click.option("--pretty", is_flag=True, default=False, help="Output as a rich table instead of JSON.")(func)


def output_json(data):
    """Print data as formatted JSON. Accepts a pydantic model or list of models."""
    if isinstance(data, list):
        click.echo(json.dumps([item.model_dump(mode="json") for item in data], default=str, indent=2))
    else:
        click.echo(data.model_dump_json(indent=2))


def _str(value) -> str:
    if value is None:
        return ""
    return str(value)


def _color_cell(hex_color: str | None) -> Text:
    """Render a color swatch followed by the hex code using rich Text."""
    if not hex_color:
        return Text("")
    text = Text()
    text.append("\u2588\u2588 ", style=hex_color)
    text.append(hex_color)
    return text


def _priority_label(priority: float | None) -> str:
    labels = {0: "No priority", 1: "Urgent", 2: "High", 3: "Medium", 4: "Low"}
    if priority is None:
        return ""
    return labels.get(int(priority), str(priority))


# --- Root group ---


@click.group()
def cli():
    """Linear CLI - interact with your Linear workspace from the terminal."""


# --- me ---


@cli.command()
@pretty_option
@handle_api_errors
def me(pretty):
    """Show current user info."""
    client = get_client()
    user = client.viewer()
    if not pretty:
        output_json(user)
        return
    table = Table(title="Current User")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("ID", user.id)
    table.add_row("Name", user.name)
    table.add_row("Display Name", user.display_name)
    table.add_row("Email", user.email)
    table.add_row("Active", _str(user.active))
    table.add_row("Admin", _str(user.admin))
    console.print(table)


# --- search ---


@cli.command()
@click.argument("query")
@pretty_option
@handle_api_errors
def search(query, pretty):
    """Search issues by query string."""
    client = get_client()
    results = client.search_issues(query=query)
    if not pretty:
        output_json(results.nodes)
        return
    table = Table(title="Search Results")
    table.add_column("ID", style="bold")
    table.add_column("Title")
    table.add_column("State")
    table.add_column("Priority")
    table.add_column("Assignee")
    for issue in results.nodes:
        state_name = issue.state.name if issue.state else ""
        assignee_name = issue.assignee.display_name if issue.assignee else ""
        table.add_row(issue.identifier, issue.title, state_name, _priority_label(issue.priority), assignee_name)
    console.print(table)


# --- issues ---


@cli.group()
def issues():
    """Manage issues."""


@issues.command("list")
@click.option("--first", type=int, default=50, help="Number of issues to fetch.")
@pretty_option
@handle_api_errors
def issues_list(first, pretty):
    """List issues."""
    client = get_client()
    result = client.list_issues(first=first)
    if not pretty:
        output_json(result.nodes)
        return
    table = Table(title="Issues")
    table.add_column("ID", style="bold")
    table.add_column("Title")
    table.add_column("State")
    table.add_column("Priority")
    table.add_column("Assignee")
    table.add_column("Team")
    for issue in result.nodes:
        state_name = issue.state.name if issue.state else ""
        assignee_name = issue.assignee.display_name if issue.assignee else ""
        team_key = issue.team.key if issue.team else ""
        table.add_row(
            issue.identifier,
            issue.title,
            state_name,
            _priority_label(issue.priority),
            assignee_name,
            team_key,
        )
    console.print(table)


@issues.command("get")
@click.argument("issue_id")
@pretty_option
@handle_api_errors
def issues_get(issue_id, pretty):
    """Get an issue by ID."""
    client = get_client()
    issue = client.get_issue(issue_id)
    if not pretty:
        output_json(issue)
        return
    table = Table(title=f"Issue {issue.identifier}")
    table.add_column("Field", style="bold")
    table.add_column("Value")
    table.add_row("ID", issue.identifier)
    table.add_row("Title", issue.title)
    table.add_row("URL", issue.url)
    table.add_row("State", issue.state.name if issue.state else "")
    table.add_row("Priority", _priority_label(issue.priority))
    table.add_row("Estimate", _str(issue.estimate))
    table.add_row("Assignee", issue.assignee.display_name if issue.assignee else "")
    table.add_row("Team", issue.team.key if issue.team else "")
    table.add_row("Project", issue.project.name if issue.project else "")
    table.add_row("Cycle", issue.cycle.name if issue.cycle else "")
    table.add_row("Due Date", _str(issue.due_date))
    table.add_row("Created", _str(issue.created_at))
    table.add_row("Description", (issue.description or "")[:200])
    console.print(table)


@issues.command("create")
@click.option("--title", required=True, help="Issue title.")
@click.option("--team-id", required=True, help="Team ID.")
@click.option("--description", default=None, help="Issue description.")
@click.option("--assignee-id", default=None, help="Assignee user ID.")
@click.option("--priority", type=int, default=None, help="Priority (0=none, 1=urgent, 2=high, 3=medium, 4=low).")
@click.option("--estimate", type=int, default=None, help="Point estimate.")
@click.option("--state-id", default=None, help="Workflow state ID.")
@click.option("--project-id", default=None, help="Project ID.")
@click.option("--cycle-id", default=None, help="Cycle ID.")
@click.option("--label-id", "label_ids", multiple=True, help="Label ID (repeatable).")
@click.option("--parent-id", default=None, help="Parent issue ID.")
@pretty_option
@handle_api_errors
def issues_create(
    title,
    team_id,
    description,
    assignee_id,
    priority,
    estimate,
    state_id,
    project_id,
    cycle_id,
    label_ids,
    parent_id,
    pretty,
):
    """Create a new issue."""
    client = get_client()
    data = IssueCreateInput(
        title=title,
        team_id=team_id,
        description=description,
        assignee_id=assignee_id,
        priority=priority,
        estimate=estimate,
        state_id=state_id,
        project_id=project_id,
        cycle_id=cycle_id,
        label_ids=list(label_ids) if label_ids else None,
        parent_id=parent_id,
    )
    result = client.create_issue(data)
    if not pretty:
        output_json(result.issue)
        return
    click.echo(f"Created issue {result.issue.identifier}: {result.issue.title}")
    click.echo(f"URL: {result.issue.url}")


@issues.command("update")
@click.argument("issue_id")
@click.option("--title", default=None, help="Issue title.")
@click.option("--description", default=None, help="Issue description.")
@click.option("--assignee-id", default=None, help="Assignee user ID.")
@click.option("--priority", type=int, default=None, help="Priority (0=none, 1=urgent, 2=high, 3=medium, 4=low).")
@click.option("--estimate", type=int, default=None, help="Point estimate.")
@click.option("--state-id", default=None, help="Workflow state ID.")
@click.option("--project-id", default=None, help="Project ID.")
@click.option("--cycle-id", default=None, help="Cycle ID.")
@pretty_option
@handle_api_errors
def issues_update(
    issue_id,
    title,
    description,
    assignee_id,
    priority,
    estimate,
    state_id,
    project_id,
    cycle_id,
    pretty,
):
    """Update an existing issue."""
    client = get_client()
    data = IssueUpdateInput(
        title=title,
        description=description,
        assignee_id=assignee_id,
        priority=priority,
        estimate=estimate,
        state_id=state_id,
        project_id=project_id,
        cycle_id=cycle_id,
    )
    result = client.update_issue(issue_id, data)
    if not pretty:
        output_json(result.issue)
        return
    click.echo(f"Updated issue {result.issue.identifier}: {result.issue.title}")
    click.echo(f"URL: {result.issue.url}")


# --- teams ---


@cli.group()
def teams():
    """Manage teams."""


@teams.command("list")
@pretty_option
@handle_api_errors
def teams_list(pretty):
    """List all teams."""
    client = get_client()
    result = client.list_teams()
    if not pretty:
        output_json(result.nodes)
        return
    table = Table(title="Teams")
    table.add_column("ID", style="bold")
    table.add_column("Key")
    table.add_column("Name")
    table.add_column("Private")
    for team in result.nodes:
        table.add_row(team.id, team.key, team.name, _str(team.private))
    console.print(table)


# --- projects ---


@cli.group()
def projects():
    """Manage projects."""


@projects.command("list")
@pretty_option
@handle_api_errors
def projects_list(pretty):
    """List all projects."""
    client = get_client()
    result = client.list_projects()
    if not pretty:
        output_json(result.nodes)
        return
    table = Table(title="Projects")
    table.add_column("ID", style="bold")
    table.add_column("Name")
    table.add_column("Status")
    table.add_column("Progress")
    table.add_column("Lead")
    table.add_column("Target Date")
    for p in result.nodes:
        status_name = p.status.name if p.status else _str(p.state)
        lead_name = p.lead.display_name if p.lead else ""
        table.add_row(p.id, p.name, status_name, f"{(p.progress or 0) * 100:.0f}%", lead_name, _str(p.target_date))
    console.print(table)


# --- cycles ---


@cli.group()
def cycles():
    """Manage cycles."""


@cycles.command("list")
@pretty_option
@handle_api_errors
def cycles_list(pretty):
    """List all cycles."""
    client = get_client()
    result = client.list_cycles()
    if not pretty:
        output_json(result.nodes)
        return
    table = Table(title="Cycles")
    table.add_column("ID", style="bold")
    table.add_column("Name")
    table.add_column("Number")
    table.add_column("Active")
    table.add_column("Progress")
    table.add_column("Starts")
    table.add_column("Ends")
    for c in result.nodes:
        table.add_row(
            c.id,
            _str(c.name),
            _str(c.number),
            _str(c.is_active),
            f"{(c.progress or 0) * 100:.0f}%",
            _str(c.starts_at),
            _str(c.ends_at),
        )
    console.print(table)


# --- labels ---


@cli.group()
def labels():
    """Manage labels."""


@labels.command("list")
@click.option("--name", "name_filter", default=None, help="Filter labels by name (case-insensitive substring match).")
@pretty_option
@handle_api_errors
def labels_list(name_filter, pretty):
    """List all labels."""
    client = get_client()
    result = client.list_labels()
    items = result.nodes
    if name_filter:
        name_lower = name_filter.lower()
        items = [label for label in items if name_lower in label.name.lower()]
    if not pretty:
        output_json(items)
        return
    table = Table(title="Labels")
    table.add_column("ID", style="bold")
    table.add_column("Name")
    table.add_column("Color")
    for label in items:
        table.add_row(label.id, label.name, _color_cell(label.color))
    console.print(table)


# --- users ---


@cli.group()
def users():
    """Manage users."""


@users.command("list")
@pretty_option
@handle_api_errors
def users_list(pretty):
    """List all users."""
    client = get_client()
    result = client.list_users()
    if not pretty:
        output_json(result.nodes)
        return
    table = Table(title="Users")
    table.add_column("ID", style="bold")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Active")
    table.add_column("Admin")
    for u in result.nodes:
        table.add_row(u.id, u.display_name, u.email, _str(u.active), _str(u.admin))
    console.print(table)


# --- workflows ---


@cli.group()
def workflows():
    """Manage workflow states."""


@workflows.command("list")
@pretty_option
@handle_api_errors
def workflows_list(pretty):
    """List all workflow states."""
    client = get_client()
    result = client.list_workflow_states()
    if not pretty:
        output_json(result.nodes)
        return
    table = Table(title="Workflow States")
    table.add_column("ID", style="bold")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Color")
    table.add_column("Position")
    for s in result.nodes:
        table.add_row(s.id, s.name, s.type, _color_cell(s.color), _str(s.position))
    console.print(table)


# --- comments ---


@cli.group()
def comments():
    """Manage comments."""


@comments.command("create")
@click.argument("issue_id")
@click.argument("body")
@pretty_option
@handle_api_errors
def comments_create(issue_id, body, pretty):
    """Add a comment to an issue."""
    client = get_client()
    data = CommentCreateInput(issue_id=issue_id, body=body)
    result = client.create_comment(data)
    if not pretty:
        output_json(result.comment)
        return
    click.echo(f"Comment added: {result.comment.url}")
