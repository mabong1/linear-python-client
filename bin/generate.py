#!/usr/bin/env python3
"""Generate Python client code from Linear GraphQL schema.

Reads linear.schema.graphql and produces:
- linear_python_client/models.py  (Pydantic models for core types)
- linear_python_client/client.py  (LinearClient with typed methods)
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "linear.schema.graphql"
OUTPUT_DIR = ROOT / "linear_python_client"

# ---------------------------------------------------------------------------
# Schema parsing
# ---------------------------------------------------------------------------

GRAPHQL_TO_PYTHON = {
    "String": "str",
    "Int": "int",
    "Float": "float",
    "Boolean": "bool",
    "ID": "str",
    "DateTime": "datetime",
    "TimelessDate": "str",
    "JSON": "Any",
    "JSONObject": "Any",
}

# Types we generate Pydantic models for
CORE_TYPES = [
    "WorkflowState",
    "IssueLabel",
    "User",
    "Team",
    "Cycle",
    "Project",
    "ProjectStatus",
    "Comment",
    "Issue",
    "Organization",
    "IssueConnection",
    "IssueEdge",
    "ProjectConnection",
    "ProjectEdge",
    "TeamConnection",
    "TeamEdge",
    "CycleConnection",
    "CycleEdge",
    "IssueLabelConnection",
    "IssueLabelEdge",
    "UserConnection",
    "UserEdge",
    "WorkflowStateConnection",
    "WorkflowStateEdge",
    "CommentConnection",
    "CommentEdge",
    "PageInfo",
    "IssuePayload",
    "IssueSearchResult",
    "IssueSearchResultEdge",
    "IssueSearchPayload",
    "CommentPayload",
    "IssueCreateInput",
    "IssueUpdateInput",
    "CommentCreateInput",
    "CommentUpdateInput",
    # Note: IssueLabelNodes is generated separately after the main types
]

# Extra types referenced by injected fields (for type resolution)
EXTRA_TYPES = {"IssueLabelNodes"}

# Fields to skip (internal, connections with args, or too complex)
SKIP_FIELDS = {
    "descriptionState",
    "contentState",
    "documentContent",
    "documentContentId",
    "activitySummary",
    "boardOrder",
    "favorite",
    "lastAppliedTemplate",
    "recurringIssueTemplate",
    "sharedAccess",
    "summary",
    "syncedWith",
    "currentProgress",
    "progressHistory",
    "completedIssueCountHistory",
    "completedScopeHistory",
    "inProgressScopeHistory",
    "issueCountHistory",
    "scopeHistory",
    "facets",
    "integrationsSettings",
    "securitySettings",
    "reactionData",
    "reactions",
    "defaultIssueState",
    "defaultProjectTemplate",
    "defaultTemplateForMembers",
    "defaultTemplateForNonMembers",
    "draftWorkflowState",
    "markedAsDuplicateWorkflowState",
    "mergeWorkflowState",
    "mergeableWorkflowState",
    "reviewWorkflowState",
    "startWorkflowState",
    "triageIssueState",
    "triageResponsibility",
    "activeCycle",
    "children",
    "posts",
    "authSettings",
    "aiProviderConfiguration",
    "themeSettings",
    "samlSettings",
    "scimSettings",
    "bodyData",
    "agentSession",
    "externalThread",
    "externalUser",
    "initiative",
    "initiativeUpdate",
    "projectUpdate",
    "resolvingComment",
    "threadSummary",
    "convertedFromIssue",
    "lastUpdate",
    "inheritedFrom",
    "identityProvider",
    "subscription",
    "ipRestrictions",
    "projectStatuses",
    "asksExternalUserRequester",
    "asksRequester",
    "externalUserCreator",
    "delegate",
    "sourceComment",
    "snoozedBy",
    "projectMilestone",
    "botActor",
    "parent",
    "onBehalfOf",
    "resolvingUser",
    "retiredBy",
    "linearAgentSettings",
    "customersConfiguration",
    "slackProjectChannelIntegration",
    "projectUpdateRemindersPausedUntilAt",
    "initiativeUpdateReminderFrequencyInWeeks",
    "projectUpdateReminderFrequencyInWeeks",
    "projectUpdatesReminderFrequency",
}


def load_schema() -> str:
    return SCHEMA_PATH.read_text()


def extract_type_block(name: str, content: str, keyword: str = "type") -> str | None:
    """Extract a type/input block from the schema."""
    pattern = rf"^{keyword} {name}\b[^\n]*\{{"
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return None
    start = match.start()
    brace_count = 0
    for j in range(match.end() - 1, len(content)):
        if content[j] == "{":
            brace_count += 1
        elif content[j] == "}":
            brace_count -= 1
            if brace_count == 0:
                return content[start : j + 1]
    return None


def parse_fields(block: str) -> list[dict]:
    """Parse fields from a type block, skipping fields with arguments (connections)."""
    fields = []
    seen_names: set[str] = set()
    lines = block.split("\n")
    i = 0
    doc_buffer = []

    while i < len(lines):
        line = lines[i].strip()

        # Collect doc comments
        if line == '"""':
            doc_buffer = []
            i += 1
            while i < len(lines) and lines[i].strip() != '"""':
                doc_buffer.append(lines[i].strip())
                i += 1
            i += 1
            continue

        # Single-line doc
        if line.startswith('"') and line.endswith('"') and ":" not in line:
            doc_buffer = [line.strip('"')]
            i += 1
            continue

        # Skip fields with arguments (sub-queries / connections)
        # Case 1: field(arg: Type): ReturnType  (all on one or more lines)
        # Case 2: field(\n  arg: Type\n): ReturnType
        if "(" in line:
            paren_count = line.count("(") - line.count(")")
            if paren_count > 0:
                # Opening paren without matching close - skip until balanced
                while paren_count > 0:
                    i += 1
                    if i >= len(lines):
                        break
                    paren_count += lines[i].count("(") - lines[i].count(")")
                # Also skip the line with ): ReturnType
                i += 1
                doc_buffer = []
                continue
            # Paren balanced on same line - this is a field with inline args, skip it
            if ":" in line and line.index("(") < line.rindex(":"):
                i += 1
                doc_buffer = []
                continue

        # Regular field line
        if ":" in line and not line.startswith("{") and not line.startswith("}") and not line.startswith("#"):
            # Remove @deprecated annotations
            field_line = re.sub(r"\s*@deprecated\([^)]*\)", "", line)
            match = re.match(r"(\w+)\s*:\s*(.+)", field_line)
            if match:
                fname = match.group(1)
                ftype_raw = match.group(2).strip()
                if fname not in SKIP_FIELDS and fname not in seen_names:
                    seen_names.add(fname)
                    fields.append(
                        {
                            "name": fname,
                            "graphql_type": ftype_raw,
                            "description": " ".join(doc_buffer).strip() if doc_buffer else "",
                        }
                    )
            doc_buffer = []
        else:
            doc_buffer = []

        i += 1

    return fields


def graphql_type_to_python(gql_type: str, for_model: bool = True, quote_refs: bool = False) -> tuple[str, bool]:
    """Convert a GraphQL type string to Python type annotation.

    Returns (type_string, is_required).
    """
    is_required = gql_type.endswith("!")
    gql_type = gql_type.rstrip("!")

    # List type
    list_match = re.match(r"\[(.+)\]", gql_type)
    if list_match:
        inner = list_match.group(1).rstrip("!")
        inner_py, _ = graphql_type_to_python(inner, for_model, quote_refs)
        return f"list[{inner_py}]", is_required

    # Scalar or known type
    if gql_type in GRAPHQL_TO_PYTHON:
        return GRAPHQL_TO_PYTHON[gql_type], is_required

    # Enum - we'll use str for now
    if gql_type.endswith("Type") or gql_type in (
        "Day",
        "PaginationOrderBy",
        "IntegrationService",
        "ReleaseChannel",
        "SLADayCountType",
        "FeedSummarySchedule",
        "DateResolutionType",
        "FrequencyResolutionType",
        "ProjectUpdateReminderFrequency",
        "ProjectUpdateHealthType",
        "TriageResponsibility",
    ):
        return "str", is_required

    # Reference to another model we generate - always quote for forward refs
    if gql_type in CORE_TYPES or gql_type in EXTRA_TYPES:
        if quote_refs:
            return f'"{gql_type}"', is_required
        return gql_type, is_required

    # Unknown type - use Any
    return "Any", is_required


# ---------------------------------------------------------------------------
# Model generation
# ---------------------------------------------------------------------------


def generate_models(schema: str) -> str:
    lines: list[str] = []
    lines.append('"""Auto-generated Pydantic models from Linear GraphQL schema."""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from datetime import datetime  # noqa: F401")
    lines.append("from typing import Any")
    lines.append("")
    lines.append("from pydantic import BaseModel, ConfigDict, Field")
    lines.append("")
    lines.append("")

    for type_name in CORE_TYPES:
        kw = "input" if type_name.endswith("Input") else "type"
        block = extract_type_block(type_name, schema, keyword=kw)
        if not block:
            print(f"  WARNING: {type_name} not found in schema")
            continue

        fields = parse_fields(block)
        # Inject extra fields for specific models
        if type_name == "Issue":
            fields.append(
                {
                    "name": "labels",
                    "graphql_type": "IssueLabelNodes",
                    "description": "Labels for this issue.",
                }
            )
        lines.extend(generate_model_class(type_name, fields, is_input=kw == "input"))
        lines.append("")
        lines.append("")

    # Add IssueLabelNodes helper for nested label responses
    lines.append("class IssueLabelNodes(BaseModel):")
    lines.append('    """Helper model for nested label responses (labels { nodes { ... } })."""')
    lines.append("")
    lines.append("    model_config = ConfigDict(populate_by_name=True)")
    lines.append("")
    lines.append("    nodes: list[IssueLabel] | None = Field(default=None)")
    lines.append("")
    lines.append("")

    # Rebuild models to resolve forward references
    lines.append("# Rebuild all models to resolve forward references")
    for type_name in CORE_TYPES:
        lines.append(f"{type_name}.model_rebuild()")
    lines.append("")

    return "\n".join(lines)


def camel_to_snake(name: str) -> str:
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def generate_model_class(name: str, fields: list[dict], is_input: bool = False) -> list[str]:
    lines: list[str] = []
    lines.append(f"class {name}(BaseModel):")
    lines.append("    model_config = ConfigDict(populate_by_name=True)")
    lines.append("")

    if not fields:
        lines.append("    pass")
        return lines

    for field in fields:
        fname = field["name"]
        python_name = camel_to_snake(fname)
        py_type, is_required = graphql_type_to_python(field["graphql_type"], quote_refs=True)

        field_kwargs: list[str] = []

        # Alias if name differs
        if python_name != fname:
            field_kwargs.append(f"alias={fname!r}")

        # GraphQL only returns requested fields, so make all fields optional
        # except for input types where required fields are meaningful
        if not is_required or not is_input:
            if "| None" not in py_type:
                py_type = f"{py_type} | None"
            field_kwargs.insert(0, "default=None")

        # Add description if it fits
        desc = field.get("description", "")
        escaped_desc = ""
        if desc:
            escaped_desc = desc.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

        def _emit_field(python_name: str, py_type: str, field_kwargs: list[str], escaped_desc: str) -> str:
            """Build a field line that fits within 120 chars."""
            # Try with full description
            if escaped_desc:
                all_kwargs = [*field_kwargs, f'description="{escaped_desc}"']
                candidate = f"    {python_name}: {py_type} = Field({', '.join(all_kwargs)})"
                # Use repr-aware length: escaped chars like \" take 2 chars in source
                source_len = len(candidate) + candidate.count('\\"') + candidate.count("\\\\")
                if source_len <= 120:
                    return candidate
                # Truncate description to fit
                if field_kwargs:
                    prefix = f'    {python_name}: {py_type} = Field({", ".join(field_kwargs)}, description="'
                else:
                    prefix = f'    {python_name}: {py_type} = Field(description="'
                max_desc = 120 - len(prefix) - len('")')
                if max_desc > 20:
                    truncated = escaped_desc[: max_desc - 3]
                    # Don't end with a backslash (creates invalid escape)
                    truncated = truncated.rstrip("\\")
                    truncated += "..."
                    result = f'{prefix}{truncated}")'
                    if len(result) <= 120:
                        return result
                    # Still too long, shrink more
                    while len(result) > 120 and max_desc > 20:
                        max_desc -= 5
                        truncated = escaped_desc[: max_desc - 3].rstrip("\\") + "..."
                        result = f'{prefix}{truncated}")'
                    if len(result) <= 120:
                        return result

            # No description or no room
            if field_kwargs:
                return f"    {python_name}: {py_type} = Field({', '.join(field_kwargs)})"
            return f"    {python_name}: {py_type}"

        line = _emit_field(python_name, py_type, field_kwargs, escaped_desc)
        # Final safety: if still too long, drop description entirely
        if len(line) > 120:
            line = _emit_field(python_name, py_type, field_kwargs, "")
        lines.append(line)

    return lines


# ---------------------------------------------------------------------------
# Client generation
# ---------------------------------------------------------------------------

# GraphQL query fragments for each core type
FRAGMENTS = {
    "PageInfo": """fragment PageInfoFragment on PageInfo {
  hasNextPage
  hasPreviousPage
  startCursor
  endCursor
}""",
    "WorkflowState": """fragment WorkflowStateFragment on WorkflowState {
  id
  name
  color
  type
  position
  description
  createdAt
  updatedAt
  archivedAt
}""",
    "IssueLabel": """fragment IssueLabelFragment on IssueLabel {
  id
  name
  color
  description
  isGroup
  createdAt
  updatedAt
  archivedAt
}""",
    "User": """fragment UserFragment on User {
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
}""",
    "Team": """fragment TeamFragment on Team {
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
}""",
    "Cycle": """fragment CycleFragment on Cycle {
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
}""",
    "Project": """fragment ProjectFragment on Project {
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
}""",
    "Issue": """fragment IssueFragment on Issue {
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
}""",
    "Comment": """fragment CommentFragment on Comment {
  id
  body
  url
  createdAt
  updatedAt
  editedAt
  archivedAt
  resolvedAt
  user { id name displayName email }
}""",
}

# Query/mutation definitions used to generate client methods
OPERATIONS = [
    {
        "name": "viewer",
        "type": "query",
        "query": """query Viewer {
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
}""",
        "return_type": "User",
        "return_path": "viewer",
        "args": [],
        "fragments": ["User"],
    },
    {
        "name": "get_issue",
        "type": "query",
        "query": """query GetIssue($id: String!) {
  issue(id: $id) {
    ...IssueFragment
  }
}""",
        "return_type": "Issue",
        "return_path": "issue",
        "args": [("id", "str")],
        "fragments": ["Issue"],
    },
    {
        "name": "list_issues",
        "type": "query",
        "query": """query ListIssues($first: Int, $after: String, $includeArchived: Boolean) {
  issues(first: $first, after: $after, includeArchived: $includeArchived) {
    nodes { ...IssueFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "IssueConnection",
        "return_path": "issues",
        "args": [
            ("first", "int | None", "50"),
            ("after", "str | None", "None"),
            ("include_archived", "bool | None", "None"),
        ],
        "fragments": ["Issue", "PageInfo"],
    },
    {
        "name": "search_issues",
        "type": "query",
        "query": """query SearchIssues($query: String!, $first: Int, $after: String, $includeArchived: Boolean) {
  issueSearch(query: $query, first: $first, after: $after, includeArchived: $includeArchived) {
    nodes { ...IssueFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "IssueSearchPayload",
        "return_path": "issueSearch",
        "args": [
            ("query", "str"),
            ("first", "int | None", "50"),
            ("after", "str | None", "None"),
            ("include_archived", "bool | None", "None"),
        ],
        "fragments": ["Issue", "PageInfo"],
    },
    {
        "name": "create_issue",
        "type": "mutation",
        "query": """mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    success
    issue { ...IssueFragment }
  }
}""",
        "return_type": "IssuePayload",
        "return_path": "issueCreate",
        "args": [("input_data", "IssueCreateInput")],
        "input_var": "input",
        "fragments": ["Issue"],
    },
    {
        "name": "update_issue",
        "type": "mutation",
        "query": """mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    success
    issue { ...IssueFragment }
  }
}""",
        "return_type": "IssuePayload",
        "return_path": "issueUpdate",
        "args": [("id", "str"), ("input_data", "IssueUpdateInput")],
        "input_var": "input",
        "fragments": ["Issue"],
    },
    {
        "name": "list_teams",
        "type": "query",
        "query": """query ListTeams($first: Int, $after: String) {
  teams(first: $first, after: $after) {
    nodes { ...TeamFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "TeamConnection",
        "return_path": "teams",
        "args": [("first", "int | None", "50"), ("after", "str | None", "None")],
        "fragments": ["Team", "PageInfo"],
    },
    {
        "name": "list_projects",
        "type": "query",
        "query": """query ListProjects($first: Int, $after: String) {
  projects(first: $first, after: $after) {
    nodes { ...ProjectFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "ProjectConnection",
        "return_path": "projects",
        "args": [("first", "int | None", "50"), ("after", "str | None", "None")],
        "fragments": ["Project", "PageInfo"],
    },
    {
        "name": "list_cycles",
        "type": "query",
        "query": """query ListCycles($first: Int, $after: String) {
  cycles(first: $first, after: $after) {
    nodes { ...CycleFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "CycleConnection",
        "return_path": "cycles",
        "args": [("first", "int | None", "50"), ("after", "str | None", "None")],
        "fragments": ["Cycle", "PageInfo"],
    },
    {
        "name": "list_labels",
        "type": "query",
        "query": """query ListLabels($first: Int, $after: String) {
  issueLabels(first: $first, after: $after) {
    nodes { ...IssueLabelFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "IssueLabelConnection",
        "return_path": "issueLabels",
        "args": [("first", "int | None", "50"), ("after", "str | None", "None")],
        "fragments": ["IssueLabel", "PageInfo"],
    },
    {
        "name": "list_users",
        "type": "query",
        "query": """query ListUsers($first: Int, $after: String) {
  users(first: $first, after: $after) {
    nodes { ...UserFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "UserConnection",
        "return_path": "users",
        "args": [("first", "int | None", "50"), ("after", "str | None", "None")],
        "fragments": ["User", "PageInfo"],
    },
    {
        "name": "list_workflow_states",
        "type": "query",
        "query": """query ListWorkflowStates($first: Int, $after: String) {
  workflowStates(first: $first, after: $after) {
    nodes { ...WorkflowStateFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "WorkflowStateConnection",
        "return_path": "workflowStates",
        "args": [("first", "int | None", "50"), ("after", "str | None", "None")],
        "fragments": ["WorkflowState", "PageInfo"],
    },
    {
        "name": "create_comment",
        "type": "mutation",
        "query": """mutation CreateComment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    success
    comment { ...CommentFragment }
  }
}""",
        "return_type": "CommentPayload",
        "return_path": "commentCreate",
        "args": [("input_data", "CommentCreateInput")],
        "input_var": "input",
        "fragments": ["Comment"],
    },
    {
        "name": "list_comments",
        "type": "query",
        "query": """query ListComments($first: Int, $after: String) {
  comments(first: $first, after: $after) {
    nodes { ...CommentFragment }
    pageInfo { ...PageInfoFragment }
  }
}""",
        "return_type": "CommentConnection",
        "return_path": "comments",
        "args": [("first", "int | None", "50"), ("after", "str | None", "None")],
        "fragments": ["Comment", "PageInfo"],
    },
]


def generate_client(schema: str) -> str:
    lines: list[str] = []

    lines.append('"""Auto-generated Linear API client."""')
    lines.append("")
    lines.append("from typing import Any")
    lines.append("")
    lines.append("import httpx")
    lines.append("")
    lines.append("from linear_python_client.models import (")

    # Collect all model names used
    model_names: set[str] = set()
    for op in OPERATIONS:
        model_names.add(op["return_type"])
        for arg in op["args"]:
            arg_type = arg[1].replace(" | None", "").strip()
            if arg_type[0].isupper():
                model_names.add(arg_type)
    for name in sorted(model_names):
        lines.append(f"    {name},")
    lines.append(")")
    lines.append("")
    lines.append("")
    lines.append('BASE_URL = "https://api.linear.app/graphql"')
    lines.append("")
    lines.append("")

    # Emit fragment constants
    used_fragments: set[str] = set()
    for op in OPERATIONS:
        for frag in op.get("fragments", []):
            used_fragments.add(frag)

    for frag_name in sorted(used_fragments):
        if frag_name in FRAGMENTS:
            var_name = f"_FRAGMENT_{camel_to_snake(frag_name).upper()}"
            frag_text = FRAGMENTS[frag_name]
            lines.append(f'{var_name} = """{frag_text}"""')
            lines.append("")

    lines.append("")
    lines.append("class LinearClient:")
    lines.append('    """Python client for the Linear GraphQL API."""')
    lines.append("")
    lines.append("    def __init__(self, api_key: str, *, base_url: str = BASE_URL, timeout: float = 30.0) -> None:")
    lines.append('        """Initialize the client.')
    lines.append("")
    lines.append("        Args:")
    lines.append("            api_key: Your Linear API key.")
    lines.append("            base_url: GraphQL endpoint URL.")
    lines.append("            timeout: Request timeout in seconds.")
    lines.append('        """')
    lines.append("        self._client = httpx.Client(")
    lines.append('            headers={"Authorization": api_key, "Content-Type": "application/json"},')
    lines.append("            timeout=timeout,")
    lines.append("        )")
    lines.append("        self._base_url = base_url")
    lines.append("")
    lines.append("    def close(self) -> None:")
    lines.append('        """Close the underlying HTTP client."""')
    lines.append("        self._client.close()")
    lines.append("")
    lines.append('    def __enter__(self) -> "LinearClient":')
    lines.append("        return self")
    lines.append("")
    lines.append("    def __exit__(self, *args: Any) -> None:")
    lines.append("        self.close()")
    lines.append("")
    lines.append("    def _request(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:")
    lines.append('        """Execute a GraphQL request."""')
    lines.append('        payload: dict[str, Any] = {"query": query}')
    lines.append("        if variables:")
    lines.append('            payload["variables"] = variables')
    lines.append("        response = self._client.post(self._base_url, json=payload)")
    lines.append("        response.raise_for_status()")
    lines.append("        result = response.json()")
    lines.append('        if "errors" in result:')
    lines.append('            errors = result["errors"]')
    lines.append('            msg = errors[0].get("message", str(errors)) if errors else str(result)')
    lines.append("            raise httpx.HTTPStatusError(msg, request=response.request, response=response)")
    lines.append('        return result["data"]')
    lines.append("")

    # Generate methods
    for op in OPERATIONS:
        lines.extend(generate_method(op))
        lines.append("")

    return "\n".join(lines)


def generate_method(op: dict) -> list[str]:
    lines: list[str] = []
    name = op["name"]
    return_type = op["return_type"]
    args = op["args"]
    query_str = op["query"]
    return_path = op["return_path"]
    fragments = op.get("fragments", [])
    input_var = op.get("input_var")

    # Build fragment string reference
    frag_vars = []
    for frag in fragments:
        frag_vars.append(f"_FRAGMENT_{camel_to_snake(frag).upper()}")

    # Build method signature
    sig_parts = ["self"]
    for arg in args:
        arg_name = arg[0]
        arg_type = arg[1]
        if len(arg) > 2:
            sig_parts.append(f"{arg_name}: {arg_type} = {arg[2]}")
        else:
            sig_parts.append(f"{arg_name}: {arg_type}")

    sig = ", ".join(sig_parts)
    one_line = f"    def {name}({sig}) -> {return_type}:"
    if len(one_line) <= 120:
        lines.append(one_line)
    else:
        lines.append(f"    def {name}(")
        for part in sig_parts:
            lines.append(f"        {part},")
        lines.append(f"    ) -> {return_type}:")

    # Docstring
    doc = f'        """{name.replace("_", " ").capitalize()}."""'
    lines.append(doc)

    # Build query string with fragments
    if frag_vars:
        frag_concat = " + ".join(frag_vars)
        lines.append(f'        query = {frag_concat} + """')
    else:
        lines.append('        query = """')

    for qline in query_str.split("\n"):
        lines.append(f"{qline}")
    lines.append('"""')

    # Build variables
    lines.append("        variables: dict[str, Any] = {}")
    for arg in args:
        arg_name = arg[0]
        gql_name = arg_name
        # Convert snake_case back to camelCase for GraphQL
        parts = arg_name.split("_")
        gql_name = parts[0] + "".join(p.capitalize() for p in parts[1:])

        if arg_name == "input_data":
            gql_name = input_var or "input"
            lines.append(f'        variables["{gql_name}"] = input_data.model_dump(')
            lines.append('            mode="json", by_alias=True, exclude_none=True,')
            lines.append("        )")
        elif len(arg) > 2 and arg[2] != "None":
            # Has a non-None default
            lines.append(f'        variables["{gql_name}"] = {arg_name}')
        elif len(arg) > 2:
            # Optional with None default
            lines.append(f"        if {arg_name} is not None:")
            lines.append(f'            variables["{gql_name}"] = {arg_name}')
        else:
            lines.append(f'        variables["{gql_name}"] = {arg_name}')

    lines.append("        data = self._request(query, variables)")
    lines.append(f'        return {return_type}.model_validate(data["{return_path}"])')

    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    schema = load_schema()

    # Generate models
    models_code = generate_models(schema)
    models_path = OUTPUT_DIR / "models.py"
    models_path.write_text(models_code)
    print(f"Generated {models_path}")

    # Generate client
    client_code = generate_client(schema)
    client_path = OUTPUT_DIR / "client.py"
    client_path.write_text(client_code)
    print(f"Generated {client_path}")


if __name__ == "__main__":
    main()
