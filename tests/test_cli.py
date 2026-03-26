import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from linear_python_client.cli import cli
from linear_python_client.models import (
    Comment,
    CommentPayload,
    Cycle,
    CycleConnection,
    Issue,
    IssueConnection,
    IssueLabel,
    IssueLabelConnection,
    IssueLabelNodes,
    IssuePayload,
    IssueSearchPayload,
    IssueSearchResult,
    PageInfo,
    Project,
    ProjectConnection,
    ProjectStatus,
    Team,
    TeamConnection,
    User,
    UserConnection,
    WorkflowState,
    WorkflowStateConnection,
)


def make_runner():
    return CliRunner(env={"LINEAR_API_KEY": "test-key"})


def make_page_info():
    return PageInfo(has_next_page=False, has_previous_page=False, start_cursor=None, end_cursor=None)


def make_user(**overrides):
    defaults = dict(
        id="user-1",
        name="Alice",
        display_name="Alice A.",
        email="alice@example.com",
        active=True,
        admin=False,
    )
    defaults.update(overrides)
    return User(**defaults)


def make_workflow_state(**overrides):
    defaults = dict(
        id="state-1",
        name="In Progress",
        color="#f2c94c",
        type="started",
    )
    defaults.update(overrides)
    return WorkflowState(**defaults)


def make_team(**overrides):
    defaults = dict(
        id="team-1",
        name="Engineering",
        key="ENG",
        private=False,
    )
    defaults.update(overrides)
    return Team(**defaults)


def make_project(**overrides):
    defaults = dict(
        id="project-1",
        name="Backend Rewrite",
        state="started",
        url="https://linear.app/project/1",
        progress=0.5,
        status=ProjectStatus(id="status-1", name="In Progress", color="#f2c94c", type="started"),
    )
    defaults.update(overrides)
    return Project(**defaults)


def make_cycle(**overrides):
    defaults = dict(
        id="cycle-1",
        name="Sprint 1",
        number=1,
        is_active=True,
        progress=0.3,
        starts_at="2024-01-01T00:00:00Z",
        ends_at="2024-01-14T00:00:00Z",
    )
    defaults.update(overrides)
    return Cycle(**defaults)


def make_label(**overrides):
    defaults = dict(
        id="label-1",
        name="bug",
        color="#ff0000",
    )
    defaults.update(overrides)
    return IssueLabel(**defaults)


def _issue_defaults(**overrides):
    defaults = dict(
        id="issue-1",
        identifier="ENG-1",
        title="Fix the bug",
        url="https://linear.app/issue/ENG-1",
        priority=2,
        priority_label="High",
        branch_name="fix-the-bug",
        number=1,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        state=make_workflow_state(),
        assignee=make_user(),
        team=make_team(),
        labels=IssueLabelNodes(nodes=[make_label()]),
    )
    defaults.update(overrides)
    return defaults


def make_issue(**overrides):
    return Issue(**_issue_defaults(**overrides))


def make_search_result(**overrides):
    return IssueSearchResult(**_issue_defaults(**overrides))


def make_comment(**overrides):
    defaults = dict(
        id="comment-1",
        body="This is a comment.",
        url="https://linear.app/comment/1",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
        user=make_user(),
    )
    defaults.update(overrides)
    return Comment(**defaults)


# --- me ---


@patch("linear_python_client.cli.get_client")
def test_me_json(mock_get_client):
    client = MagicMock()
    client.viewer.return_value = make_user()
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["me"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


@patch("linear_python_client.cli.get_client")
def test_me_pretty(mock_get_client):
    client = MagicMock()
    client.viewer.return_value = make_user()
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["me", "--pretty"])
    assert result.exit_code == 0
    assert "Alice" in result.output
    assert "alice@example.com" in result.output


# --- search ---


@patch("linear_python_client.cli.get_client")
def test_search(mock_get_client):
    client = MagicMock()
    client.search_issues.return_value = IssueSearchPayload(nodes=[make_search_result()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["search", "bug"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 1
    assert data[0]["title"] == "Fix the bug"


@patch("linear_python_client.cli.get_client")
def test_search_pretty(mock_get_client):
    client = MagicMock()
    client.search_issues.return_value = IssueSearchPayload(nodes=[make_search_result()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["search", "bug", "--pretty"])
    assert result.exit_code == 0
    assert "Fix the bug" in result.output
    assert "ENG-1" in result.output


# --- issues list ---


@patch("linear_python_client.cli.get_client")
def test_issues_list(mock_get_client):
    client = MagicMock()
    client.list_issues.return_value = IssueConnection(nodes=[make_issue()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["issues", "list"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 1
    assert data[0]["identifier"] == "ENG-1"


@patch("linear_python_client.cli.get_client")
def test_issues_list_pretty(mock_get_client):
    client = MagicMock()
    client.list_issues.return_value = IssueConnection(nodes=[make_issue()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["issues", "list", "--pretty"])
    assert result.exit_code == 0
    assert "Fix the bug" in result.output
    assert "ENG" in result.output


# --- issues get ---


@patch("linear_python_client.cli.get_client")
def test_issues_get(mock_get_client):
    client = MagicMock()
    client.get_issue.return_value = make_issue()
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["issues", "get", "issue-1"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["title"] == "Fix the bug"


@patch("linear_python_client.cli.get_client")
def test_issues_get_pretty(mock_get_client):
    client = MagicMock()
    client.get_issue.return_value = make_issue()
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["issues", "get", "issue-1", "--pretty"])
    assert result.exit_code == 0
    assert "Fix the bug" in result.output
    assert "ENG-1" in result.output
    assert "High" in result.output


# --- issues create ---


@patch("linear_python_client.cli.get_client")
def test_issues_create(mock_get_client):
    client = MagicMock()
    client.create_issue.return_value = IssuePayload(success=True, issue=make_issue())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["issues", "create", "--title", "New bug", "--team-id", "team-1"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["title"] == "Fix the bug"


# --- issues update ---


@patch("linear_python_client.cli.get_client")
def test_issues_update(mock_get_client):
    client = MagicMock()
    client.update_issue.return_value = IssuePayload(success=True, issue=make_issue(title="Updated"))
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["issues", "update", "issue-1", "--title", "Updated"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["title"] == "Updated"


# --- teams ---


@patch("linear_python_client.cli.get_client")
def test_teams_list(mock_get_client):
    client = MagicMock()
    client.list_teams.return_value = TeamConnection(nodes=[make_team()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["teams", "list"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data[0]["name"] == "Engineering"


@patch("linear_python_client.cli.get_client")
def test_teams_list_pretty(mock_get_client):
    client = MagicMock()
    client.list_teams.return_value = TeamConnection(nodes=[make_team()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["teams", "list", "--pretty"])
    assert result.exit_code == 0
    assert "Engineering" in result.output
    assert "ENG" in result.output


# --- projects ---


@patch("linear_python_client.cli.get_client")
def test_projects_list(mock_get_client):
    client = MagicMock()
    client.list_projects.return_value = ProjectConnection(nodes=[make_project()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["projects", "list"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data[0]["name"] == "Backend Rewrite"


@patch("linear_python_client.cli.get_client")
def test_projects_list_pretty(mock_get_client):
    client = MagicMock()
    client.list_projects.return_value = ProjectConnection(nodes=[make_project()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["projects", "list", "--pretty"])
    assert result.exit_code == 0
    assert "Backend Rewrite" in result.output
    assert "50%" in result.output


# --- cycles ---


@patch("linear_python_client.cli.get_client")
def test_cycles_list_pretty(mock_get_client):
    client = MagicMock()
    client.list_cycles.return_value = CycleConnection(nodes=[make_cycle()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["cycles", "list", "--pretty"])
    assert result.exit_code == 0
    assert "Sprint 1" in result.output


# --- labels ---


@patch("linear_python_client.cli.get_client")
def test_labels_list(mock_get_client):
    client = MagicMock()
    client.list_labels.return_value = IssueLabelConnection(nodes=[make_label()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["labels", "list"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data[0]["name"] == "bug"


@patch("linear_python_client.cli.get_client")
def test_labels_list_filter_by_name(mock_get_client):
    client = MagicMock()
    client.list_labels.return_value = IssueLabelConnection(
        nodes=[
            make_label(id="l1", name="bug"),
            make_label(id="l2", name="feature"),
            make_label(id="l3", name="bugfix"),
        ],
        page_info=make_page_info(),
    )
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["labels", "list", "--name", "bug"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data) == 2
    names = {item["name"] for item in data}
    assert names == {"bug", "bugfix"}


@patch("linear_python_client.cli.get_client")
def test_labels_list_pretty_shows_color_swatch(mock_get_client):
    client = MagicMock()
    client.list_labels.return_value = IssueLabelConnection(
        nodes=[make_label(color="#ff0000")], page_info=make_page_info()
    )
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["labels", "list", "--pretty"])
    assert result.exit_code == 0
    assert "#ff0000" in result.output
    assert "\u2588\u2588" in result.output


# --- users ---


@patch("linear_python_client.cli.get_client")
def test_users_list_pretty(mock_get_client):
    client = MagicMock()
    client.list_users.return_value = UserConnection(nodes=[make_user()], page_info=make_page_info())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["users", "list", "--pretty"])
    assert result.exit_code == 0
    assert "Alice" in result.output
    assert "alice@example.com" in result.output


# --- workflows ---


@patch("linear_python_client.cli.get_client")
def test_workflows_list_pretty(mock_get_client):
    client = MagicMock()
    client.list_workflow_states.return_value = WorkflowStateConnection(
        nodes=[make_workflow_state()], page_info=make_page_info()
    )
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["workflows", "list", "--pretty"])
    assert result.exit_code == 0
    assert "In Progress" in result.output
    assert "started" in result.output


# --- comments ---


@patch("linear_python_client.cli.get_client")
def test_comments_create(mock_get_client):
    client = MagicMock()
    client.create_comment.return_value = CommentPayload(success=True, comment=make_comment())
    mock_get_client.return_value = client

    runner = make_runner()
    result = runner.invoke(cli, ["comments", "create", "issue-1", "This is a comment."])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["body"] == "This is a comment."


# --- missing token ---


def test_missing_token():
    runner = CliRunner(env={"LINEAR_API_KEY": ""})
    result = runner.invoke(cli, ["me"])
    assert result.exit_code != 0
    assert "LINEAR_API_KEY" in result.output
