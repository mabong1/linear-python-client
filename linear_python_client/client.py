"""Auto-generated Linear API client."""

from typing import Any

import httpx

from linear_python_client.models import (
    CommentConnection,
    CommentCreateInput,
    CommentPayload,
    CycleConnection,
    Issue,
    IssueConnection,
    IssueCreateInput,
    IssueLabelConnection,
    IssuePayload,
    IssueSearchPayload,
    IssueUpdateInput,
    ProjectConnection,
    TeamConnection,
    User,
    UserConnection,
    WorkflowStateConnection,
)

BASE_URL = "https://api.linear.app/graphql"


_FRAGMENT_COMMENT = """fragment CommentFragment on Comment {
  id
  body
  url
  createdAt
  updatedAt
  editedAt
  archivedAt
  resolvedAt
  user { id name displayName email }
}"""

_FRAGMENT_CYCLE = """fragment CycleFragment on Cycle {
  id
  name
  number
  description
  startsAt
  endsAt
  completedAt
  progress
  isActive
  isFuture
  isNext
  isPast
  isPrevious
  createdAt
  updatedAt
  archivedAt
}"""

_FRAGMENT_ISSUE = """fragment IssueFragment on Issue {
  id
  identifier
  title
  description
  priority
  priorityLabel
  estimate
  dueDate
  url
  branchName
  number
  completedAt
  canceledAt
  startedAt
  createdAt
  updatedAt
  archivedAt
  trashed
  labelIds
  previousIdentifiers
  sortOrder
  state { id name color type }
  assignee { id name displayName email }
  team { id name key }
  project { id name }
  cycle { id name number }
  labels { nodes { id name color } }
}"""

_FRAGMENT_ISSUE_LABEL = """fragment IssueLabelFragment on IssueLabel {
  id
  name
  color
  description
  isGroup
  createdAt
  updatedAt
  archivedAt
}"""

_FRAGMENT_PAGE_INFO = """fragment PageInfoFragment on PageInfo {
  hasNextPage
  hasPreviousPage
  startCursor
  endCursor
}"""

_FRAGMENT_PROJECT = """fragment ProjectFragment on Project {
  id
  name
  description
  icon
  color
  state
  slugId
  url
  progress
  scope
  priority
  priorityLabel
  startDate
  targetDate
  startedAt
  completedAt
  canceledAt
  sortOrder
  createdAt
  updatedAt
  archivedAt
  status { id name color type position indefinite }
  lead { id name displayName email }
}"""

_FRAGMENT_TEAM = """fragment TeamFragment on Team {
  id
  name
  key
  description
  color
  icon
  private
  timezone
  cyclesEnabled
  cycleDuration
  cycleCooldownTime
  triageEnabled
  createdAt
  updatedAt
  archivedAt
}"""

_FRAGMENT_USER = """fragment UserFragment on User {
  id
  name
  displayName
  email
  avatarUrl
  active
  admin
  createdAt
  updatedAt
  archivedAt
}"""

_FRAGMENT_WORKFLOW_STATE = """fragment WorkflowStateFragment on WorkflowState {
  id
  name
  color
  type
  position
  description
  createdAt
  updatedAt
  archivedAt
}"""


class LinearClient:
    """Python client for the Linear GraphQL API."""

    def __init__(self, api_key: str, *, base_url: str = BASE_URL, timeout: float = 30.0) -> None:
        """Initialize the client.

        Args:
            api_key: Your Linear API key.
            base_url: GraphQL endpoint URL.
            timeout: Request timeout in seconds.
        """
        self._client = httpx.Client(
            headers={"Authorization": api_key, "Content-Type": "application/json"},
            timeout=timeout,
        )
        self._base_url = base_url

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "LinearClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def _request(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a GraphQL request."""
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables
        response = self._client.post(self._base_url, json=payload)
        response.raise_for_status()
        result = response.json()
        if "errors" in result:
            errors = result["errors"]
            msg = errors[0].get("message", str(errors)) if errors else str(result)
            raise httpx.HTTPStatusError(msg, request=response.request, response=response)
        return result["data"]

    def viewer(self) -> User:
        """Viewer."""
        query = (
            _FRAGMENT_USER
            + """
query Viewer {
  viewer {
    ...UserFragment
    organization {
      id
      name
      urlKey
      logoUrl
      createdAt
      updatedAt
    }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        data = self._request(query, variables)
        return User.model_validate(data["viewer"])

    def get_issue(self, id: str) -> Issue:
        """Get issue."""
        query = (
            _FRAGMENT_ISSUE
            + """
query GetIssue($id: String!) {
  issue(id: $id) {
    ...IssueFragment
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["id"] = id
        data = self._request(query, variables)
        return Issue.model_validate(data["issue"])

    def list_issues(
        self,
        first: int | None = 50,
        after: str | None = None,
        include_archived: bool | None = None,
    ) -> IssueConnection:
        """List issues."""
        query = (
            _FRAGMENT_ISSUE
            + _FRAGMENT_PAGE_INFO
            + """
query ListIssues($first: Int, $after: String, $includeArchived: Boolean) {
  issues(first: $first, after: $after, includeArchived: $includeArchived) {
    nodes { ...IssueFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        if include_archived is not None:
            variables["includeArchived"] = include_archived
        data = self._request(query, variables)
        return IssueConnection.model_validate(data["issues"])

    def search_issues(
        self,
        query: str,
        first: int | None = 50,
        after: str | None = None,
        include_archived: bool | None = None,
    ) -> IssueSearchPayload:
        """Search issues."""
        query = (
            _FRAGMENT_ISSUE
            + _FRAGMENT_PAGE_INFO
            + """
query SearchIssues($query: String!, $first: Int, $after: String, $includeArchived: Boolean) {
  issueSearch(query: $query, first: $first, after: $after, includeArchived: $includeArchived) {
    nodes { ...IssueFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["query"] = query
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        if include_archived is not None:
            variables["includeArchived"] = include_archived
        data = self._request(query, variables)
        return IssueSearchPayload.model_validate(data["issueSearch"])

    def create_issue(self, input_data: IssueCreateInput) -> IssuePayload:
        """Create issue."""
        query = (
            _FRAGMENT_ISSUE
            + """
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { ...IssueFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["input"] = input_data.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
        )
        data = self._request(query, variables)
        return IssuePayload.model_validate(data["issueCreate"])

    def update_issue(self, id: str, input_data: IssueUpdateInput) -> IssuePayload:
        """Update issue."""
        query = (
            _FRAGMENT_ISSUE
            + """
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue { ...IssueFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["id"] = id
        variables["input"] = input_data.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
        )
        data = self._request(query, variables)
        return IssuePayload.model_validate(data["issueUpdate"])

    def list_teams(self, first: int | None = 50, after: str | None = None) -> TeamConnection:
        """List teams."""
        query = (
            _FRAGMENT_TEAM
            + _FRAGMENT_PAGE_INFO
            + """
query ListTeams($first: Int, $after: String) {
  teams(first: $first, after: $after) {
    nodes { ...TeamFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        data = self._request(query, variables)
        return TeamConnection.model_validate(data["teams"])

    def list_projects(self, first: int | None = 50, after: str | None = None) -> ProjectConnection:
        """List projects."""
        query = (
            _FRAGMENT_PROJECT
            + _FRAGMENT_PAGE_INFO
            + """
query ListProjects($first: Int, $after: String) {
  projects(first: $first, after: $after) {
    nodes { ...ProjectFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        data = self._request(query, variables)
        return ProjectConnection.model_validate(data["projects"])

    def list_cycles(self, first: int | None = 50, after: str | None = None) -> CycleConnection:
        """List cycles."""
        query = (
            _FRAGMENT_CYCLE
            + _FRAGMENT_PAGE_INFO
            + """
query ListCycles($first: Int, $after: String) {
  cycles(first: $first, after: $after) {
    nodes { ...CycleFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        data = self._request(query, variables)
        return CycleConnection.model_validate(data["cycles"])

    def list_labels(self, first: int | None = 50, after: str | None = None) -> IssueLabelConnection:
        """List labels."""
        query = (
            _FRAGMENT_ISSUE_LABEL
            + _FRAGMENT_PAGE_INFO
            + """
query ListLabels($first: Int, $after: String) {
  issueLabels(first: $first, after: $after) {
    nodes { ...IssueLabelFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        data = self._request(query, variables)
        return IssueLabelConnection.model_validate(data["issueLabels"])

    def list_users(self, first: int | None = 50, after: str | None = None) -> UserConnection:
        """List users."""
        query = (
            _FRAGMENT_USER
            + _FRAGMENT_PAGE_INFO
            + """
query ListUsers($first: Int, $after: String) {
  users(first: $first, after: $after) {
    nodes { ...UserFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        data = self._request(query, variables)
        return UserConnection.model_validate(data["users"])

    def list_workflow_states(self, first: int | None = 50, after: str | None = None) -> WorkflowStateConnection:
        """List workflow states."""
        query = (
            _FRAGMENT_WORKFLOW_STATE
            + _FRAGMENT_PAGE_INFO
            + """
query ListWorkflowStates($first: Int, $after: String) {
  workflowStates(first: $first, after: $after) {
    nodes { ...WorkflowStateFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        data = self._request(query, variables)
        return WorkflowStateConnection.model_validate(data["workflowStates"])

    def create_comment(self, input_data: CommentCreateInput) -> CommentPayload:
        """Create comment."""
        query = (
            _FRAGMENT_COMMENT
            + """
mutation CreateComment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    success
    comment { ...CommentFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["input"] = input_data.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
        )
        data = self._request(query, variables)
        return CommentPayload.model_validate(data["commentCreate"])

    def list_comments(self, first: int | None = 50, after: str | None = None) -> CommentConnection:
        """List comments."""
        query = (
            _FRAGMENT_COMMENT
            + _FRAGMENT_PAGE_INFO
            + """
query ListComments($first: Int, $after: String) {
  comments(first: $first, after: $after) {
    nodes { ...CommentFragment }
    pageInfo { ...PageInfoFragment }
  }
}
"""
        )
        variables: dict[str, Any] = {}
        variables["first"] = first
        if after is not None:
            variables["after"] = after
        data = self._request(query, variables)
        return CommentConnection.model_validate(data["comments"])
