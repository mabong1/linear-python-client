"""Auto-generated Pydantic models from Linear GraphQL schema."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorkflowState(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    color: str | None = Field(default=None, description="The state's UI color as a HEX string.")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    description: str | None = Field(default=None, description="Description of the state.")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    name: str | None = Field(default=None, description="The state's name.")
    position: float | None = Field(default=None, description="The position of the state in the team flow.")
    team: Team | None = Field(default=None, description="The team to which this state belongs to.")
    type: str | None = Field(default=None, description='The type of the state. One of "triage", "backlog", "un...')
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")


class IssueLabel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    color: str | None = Field(default=None, description="The label's color as a HEX string.")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    creator: User | None = Field(default=None, description="The user who created the label.")
    description: str | None = Field(default=None, description="The label's description.")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    is_group: bool | None = Field(default=None, alias="isGroup", description="Whether the label is a group.")
    last_applied_at: datetime | None = Field(default=None, alias="lastAppliedAt", description="The date when the la...")
    name: str | None = Field(default=None, description="The label's name.")
    retired_at: datetime | None = Field(default=None, alias="retiredAt", description="[Internal] When the label was...")
    team: Team | None = Field(default=None, description="The team that the label is associated with. If null, the...")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")


class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    active: bool | None = Field(default=None, description="Whether the user account is active or disabled (suspended).")
    admin: bool | None = Field(default=None, description="Whether the user is an organization administrator.")
    app: bool | None = Field(default=None, description="Whether the user is an app.")
    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    avatar_background_color: str | None = Field(default=None, alias="avatarBackgroundColor")
    avatar_url: str | None = Field(default=None, alias="avatarUrl", description="An URL to the user's avatar image.")
    calendar_hash: str | None = Field(default=None, alias="calendarHash", description="[DEPRECATED] Hash for the us...")
    can_access_any_public_team: bool | None = Field(default=None, alias="canAccessAnyPublicTeam")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    created_issue_count: int | None = Field(default=None, alias="createdIssueCount")
    description: str | None = Field(default=None, description="A short description of the user, either its title or...")
    disable_reason: str | None = Field(default=None, alias="disableReason", description="Reason why is the account ...")
    display_name: str | None = Field(default=None, alias="displayName", description="The user's display (nick) name...")
    email: str | None = Field(default=None, description="The user's email address.")
    git_hub_user_id: str | None = Field(default=None, alias="gitHubUserId", description="The user's GitHub user ID.")
    guest: bool | None = Field(default=None, description="Whether the user is a guest in the workspace and limited ...")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    initials: str | None = Field(default=None, description="The initials of the user.")
    is_assignable: bool | None = Field(default=None, alias="isAssignable", description="Whether the user is assigna...")
    is_me: bool | None = Field(default=None, alias="isMe", description="Whether the user is the currently authentic...")
    is_mentionable: bool | None = Field(default=None, alias="isMentionable", description="Whether the user is menti...")
    last_seen: datetime | None = Field(default=None, alias="lastSeen", description="The last time the user was seen...")
    name: str | None = Field(default=None, description="The user's full name.")
    organization: Organization | None = Field(default=None, description="Organization the user belongs to.")
    owner: bool | None = Field(default=None, description="Whether the user is an organization owner.")
    status_emoji: str | None = Field(default=None, alias="statusEmoji", description="The emoji to represent the use...")
    status_label: str | None = Field(default=None, alias="statusLabel", description="The label of the user current ...")
    status_until_at: datetime | None = Field(default=None, alias="statusUntilAt", description="A date at which the ...")
    supports_agent_sessions: bool | None = Field(default=None, alias="supportsAgentSessions")
    timezone: str | None = Field(default=None, description="The local timezone of the user.")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")
    url: str | None = Field(default=None, description="User's profile URL.")


class Team(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    ai_discussion_summaries_enabled: bool | None = Field(default=None, alias="aiDiscussionSummariesEnabled")
    ai_thread_summaries_enabled: bool | None = Field(default=None, alias="aiThreadSummariesEnabled")
    all_members_can_join: bool | None = Field(default=None, alias="allMembersCanJoin")
    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    auto_archive_period: float | None = Field(default=None, alias="autoArchivePeriod")
    auto_close_child_issues: bool | None = Field(default=None, alias="autoCloseChildIssues")
    auto_close_parent_issues: bool | None = Field(default=None, alias="autoCloseParentIssues")
    auto_close_period: float | None = Field(default=None, alias="autoClosePeriod", description="Period after which ...")
    auto_close_state_id: str | None = Field(default=None, alias="autoCloseStateId", description="The canceled workf...")
    color: str | None = Field(default=None, description="The team's color.")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    cycle_calender_url: str | None = Field(default=None, alias="cycleCalenderUrl", description="Calendar feed URL (...")
    cycle_cooldown_time: float | None = Field(default=None, alias="cycleCooldownTime")
    cycle_duration: float | None = Field(default=None, alias="cycleDuration", description="The duration of a cycle ...")
    cycle_issue_auto_assign_completed: bool | None = Field(default=None, alias="cycleIssueAutoAssignCompleted")
    cycle_issue_auto_assign_started: bool | None = Field(default=None, alias="cycleIssueAutoAssignStarted")
    cycle_lock_to_active: bool | None = Field(default=None, alias="cycleLockToActive")
    cycle_start_day: float | None = Field(default=None, alias="cycleStartDay", description="The day of the week tha...")
    cycles_enabled: bool | None = Field(default=None, alias="cyclesEnabled", description="Whether the team uses cyc...")
    default_issue_estimate: float | None = Field(default=None, alias="defaultIssueEstimate")
    description: str | None = Field(default=None, description="The team's description.")
    display_name: str | None = Field(default=None, alias="displayName", description="The name of the team including...")
    group_issue_history: bool | None = Field(default=None, alias="groupIssueHistory")
    icon: str | None = Field(default=None, description="The icon of the team.")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    inherit_issue_estimation: bool | None = Field(default=None, alias="inheritIssueEstimation")
    inherit_workflow_statuses: bool | None = Field(default=None, alias="inheritWorkflowStatuses")
    issue_estimation_allow_zero: bool | None = Field(default=None, alias="issueEstimationAllowZero")
    issue_estimation_extended: bool | None = Field(default=None, alias="issueEstimationExtended")
    issue_estimation_type: str | None = Field(default=None, alias="issueEstimationType")
    join_by_default: bool | None = Field(default=None, alias="joinByDefault", description="[Internal] Whether new u...")
    key: str | None = Field(default=None, description="The team's unique key. The key is used in URLs.")
    name: str | None = Field(default=None, description="The team's name.")
    organization: Organization | None = Field(default=None, description="The organization that the team is associ...")
    private: bool | None = Field(default=None, description="Whether the team is private or not.")
    require_priority_to_leave_triage: bool | None = Field(default=None, alias="requirePriorityToLeaveTriage")
    retired_at: datetime | None = Field(default=None, alias="retiredAt", description="The time at which the team wa...")
    scim_group_name: str | None = Field(default=None, alias="scimGroupName", description="The SCIM group name for t...")
    scim_managed: bool | None = Field(default=None, alias="scimManaged", description="Whether the team is managed b...")
    set_issue_sort_order_on_state_change: str | None = Field(default=None, alias="setIssueSortOrderOnStateChange")
    timezone: str | None = Field(default=None, description='The timezone of the team. Defaults to "America/Los_Ang...')
    triage_enabled: bool | None = Field(default=None, alias="triageEnabled", description="Whether triage mode is en...")
    upcoming_cycle_count: float | None = Field(default=None, alias="upcomingCycleCount")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")


class Cycle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    auto_archived_at: datetime | None = Field(default=None, alias="autoArchivedAt", description="The time at which ...")
    completed_at: datetime | None = Field(default=None, alias="completedAt", description="The completion time of th...")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    description: str | None = Field(default=None, description="The cycle's description.")
    ends_at: datetime | None = Field(default=None, alias="endsAt", description="The end time of the cycle.")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    is_active: bool | None = Field(default=None, alias="isActive", description="Whether the cycle is currently active.")
    is_future: bool | None = Field(default=None, alias="isFuture", description="Whether the cycle is in the future.")
    is_next: bool | None = Field(default=None, alias="isNext", description="Whether the cycle is the next cycle for...")
    is_past: bool | None = Field(default=None, alias="isPast", description="Whether the cycle is in the past.")
    is_previous: bool | None = Field(default=None, alias="isPrevious", description="Whether the cycle is the previo...")
    name: str | None = Field(default=None, description="The custom name of the cycle.")
    number: float | None = Field(default=None, description="The number of the cycle.")
    progress: float | None = Field(default=None, description="The overall progress of the cycle. This is the (compl...")
    starts_at: datetime | None = Field(default=None, alias="startsAt", description="The start time of the cycle.")
    team: Team | None = Field(default=None, description="The team that the cycle is associated with.")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")


class Project(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    auto_archived_at: datetime | None = Field(default=None, alias="autoArchivedAt", description="The time at which ...")
    canceled_at: datetime | None = Field(default=None, alias="canceledAt", description="The time at which the proje...")
    color: str | None = Field(default=None, description="The project's color.")
    completed_at: datetime | None = Field(default=None, alias="completedAt", description="The time at which the pro...")
    content: str | None = Field(default=None, description="The project's content in markdown format.")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    creator: User | None = Field(default=None, description="The user who created the project.")
    description: str | None = Field(default=None, description="The project's description.")
    frequency_resolution: str | None = Field(default=None, alias="frequencyResolution")
    health: str | None = Field(default=None, description="The health of the project.")
    health_updated_at: datetime | None = Field(default=None, alias="healthUpdatedAt")
    icon: str | None = Field(default=None, description="The icon of the project.")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    label_ids: list[str] | None = Field(default=None, alias="labelIds", description="Id of the labels associated wi...")
    lead: User | None = Field(default=None, description="The project lead.")
    name: str | None = Field(default=None, description="The project's name.")
    priority: int | None = Field(default=None, description="The priority of the project. 0 = No priority, 1 = Urgen...")
    priority_label: str | None = Field(default=None, alias="priorityLabel", description="The priority of the projec...")
    priority_sort_order: float | None = Field(default=None, alias="prioritySortOrder")
    progress: float | None = Field(default=None, description="The overall progress of the project. This is the (com...")
    scope: float | None = Field(default=None, description="The overall scope (total estimate points) of the project.")
    slug_id: str | None = Field(default=None, alias="slugId", description="The project's unique URL slug.")
    sort_order: float | None = Field(default=None, alias="sortOrder", description="The sort order for the project w...")
    start_date: str | None = Field(default=None, alias="startDate", description="The estimated start date of the pr...")
    start_date_resolution: str | None = Field(default=None, alias="startDateResolution")
    started_at: datetime | None = Field(default=None, alias="startedAt", description="The time at which the project...")
    status: ProjectStatus | None = Field(default=None, description="The status that the project is associated with.")
    target_date: str | None = Field(default=None, alias="targetDate", description="The estimated completion date of...")
    target_date_resolution: str | None = Field(default=None, alias="targetDateResolution")
    trashed: bool | None = Field(default=None, description="A flag that indicates whether the project is in the tra...")
    update_reminder_frequency: float | None = Field(default=None, alias="updateReminderFrequency")
    update_reminder_frequency_in_weeks: float | None = Field(default=None, alias="updateReminderFrequencyInWeeks")
    update_reminders_day: str | None = Field(default=None, alias="updateRemindersDay")
    update_reminders_hour: float | None = Field(default=None, alias="updateRemindersHour")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")
    url: str | None = Field(default=None, description="Project URL.")


class ProjectStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    color: str | None = Field(default=None, description="The UI color of the status as a HEX string.")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    description: str | None = Field(default=None, description="Description of the status.")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    indefinite: bool | None = Field(default=None, description="Whether or not a project can be in this status indef...")
    name: str | None = Field(default=None, description="The name of the status.")
    position: float | None = Field(default=None, description="The position of the status in the workspace's project...")
    type: str | None = Field(default=None, description="The type of the project status.")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")


class Comment(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    body: str | None = Field(default=None, description="The comment content in markdown format.")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    edited_at: datetime | None = Field(default=None, alias="editedAt", description="The time user edited the comment.")
    hide_in_linear: bool | None = Field(default=None, alias="hideInLinear", description="[Internal] Whether the com...")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    initiative_id: str | None = Field(default=None, alias="initiativeId", description="[Internal] The ID of the ini...")
    initiative_update_id: str | None = Field(default=None, alias="initiativeUpdateId")
    is_artificial_agent_session_root: bool | None = Field(default=None, alias="isArtificialAgentSessionRoot")
    issue: Issue | None = Field(default=None, description="The issue that the comment is associated with.")
    issue_id: str | None = Field(default=None, alias="issueId", description="The ID of the issue that the comment i...")
    parent_id: str | None = Field(default=None, alias="parentId", description="The ID of the parent comment under w...")
    post: Any | None = Field(default=None, description="The post that the comment is associated with.")
    project: Project | None = Field(default=None, description="[Internal] The project that the comment is associa...")
    project_id: str | None = Field(default=None, alias="projectId", description="[Internal] The ID of the project t...")
    project_update_id: str | None = Field(default=None, alias="projectUpdateId", description="The ID of the project...")
    quoted_text: str | None = Field(default=None, alias="quotedText", description="The text that this comment refer...")
    resolved_at: datetime | None = Field(default=None, alias="resolvedAt", description="The time the resolvingUser ...")
    resolving_comment_id: str | None = Field(default=None, alias="resolvingCommentId")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")
    url: str | None = Field(default=None, description="Comment's URL.")
    user: User | None = Field(default=None, description="The user who wrote the comment.")


class Issue(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    added_to_cycle_at: datetime | None = Field(default=None, alias="addedToCycleAt")
    added_to_project_at: datetime | None = Field(default=None, alias="addedToProjectAt")
    added_to_team_at: datetime | None = Field(default=None, alias="addedToTeamAt", description="The time at which t...")
    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    assignee: User | None = Field(default=None, description="The user to whom the issue is assigned to.")
    auto_archived_at: datetime | None = Field(default=None, alias="autoArchivedAt", description="The time at which ...")
    auto_closed_at: datetime | None = Field(default=None, alias="autoClosedAt", description="The time at which the ...")
    branch_name: str | None = Field(default=None, alias="branchName", description="Suggested branch name for the is...")
    canceled_at: datetime | None = Field(default=None, alias="canceledAt", description="The time at which the issue...")
    completed_at: datetime | None = Field(default=None, alias="completedAt", description="The time at which the iss...")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    creator: User | None = Field(default=None, description="The user who created the issue.")
    customer_ticket_count: int | None = Field(default=None, alias="customerTicketCount")
    cycle: Cycle | None = Field(default=None, description="The cycle that the issue is associated with.")
    description: str | None = Field(default=None, description="The issue's description in markdown format.")
    due_date: str | None = Field(default=None, alias="dueDate", description="The date at which the issue is due.")
    estimate: float | None = Field(default=None, description="The estimate of the complexity of the issue..")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    identifier: str | None = Field(default=None, description="Issue's human readable identifier (e.g. ENG-123).")
    integration_source_type: str | None = Field(default=None, alias="integrationSourceType")
    label_ids: list[str] | None = Field(default=None, alias="labelIds", description="Id of the labels associated wi...")
    number: float | None = Field(default=None, description="The issue's unique number.")
    previous_identifiers: list[str] | None = Field(default=None, alias="previousIdentifiers")
    priority: float | None = Field(default=None, description="The priority of the issue. 0 = No priority, 1 = Urgen...")
    priority_label: str | None = Field(default=None, alias="priorityLabel", description="Label for the priority.")
    priority_sort_order: float | None = Field(default=None, alias="prioritySortOrder")
    project: Project | None = Field(default=None, description="The project that the issue is associated with.")
    sla_breaches_at: datetime | None = Field(default=None, alias="slaBreachesAt", description="The time at which th...")
    sla_high_risk_at: datetime | None = Field(default=None, alias="slaHighRiskAt", description="The time at which t...")
    sla_medium_risk_at: datetime | None = Field(default=None, alias="slaMediumRiskAt")
    sla_started_at: datetime | None = Field(default=None, alias="slaStartedAt", description="The time at which the ...")
    sla_type: str | None = Field(default=None, alias="slaType", description="The type of SLA set on the issue. Cale...")
    snoozed_until_at: datetime | None = Field(default=None, alias="snoozedUntilAt", description="The time until an ...")
    sort_order: float | None = Field(default=None, alias="sortOrder", description="The order of the item in relatio...")
    started_at: datetime | None = Field(default=None, alias="startedAt", description="The time at which the issue w...")
    started_triage_at: datetime | None = Field(default=None, alias="startedTriageAt")
    state: WorkflowState | None = Field(default=None, description="The workflow state that the issue is associate...")
    sub_issue_sort_order: float | None = Field(default=None, alias="subIssueSortOrder")
    suggestions_generated_at: datetime | None = Field(default=None, alias="suggestionsGeneratedAt")
    team: Team | None = Field(default=None, description="The team that the issue is associated with.")
    title: str | None = Field(default=None, description="The issue's title.")
    trashed: bool | None = Field(default=None, description="A flag that indicates whether the issue is in the trash...")
    triaged_at: datetime | None = Field(default=None, alias="triagedAt", description="The time at which the issue l...")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")
    url: str | None = Field(default=None, description="Issue URL.")
    labels: IssueLabelNodes | None = Field(default=None, description="Labels for this issue.")


class Organization(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    agent_automation_enabled: bool | None = Field(default=None, alias="agentAutomationEnabled")
    ai_addon_enabled: bool | None = Field(default=None, alias="aiAddonEnabled", description="[INTERNAL] Whether the...")
    ai_discussion_summaries_enabled: bool | None = Field(default=None, alias="aiDiscussionSummariesEnabled")
    ai_thread_summaries_enabled: bool | None = Field(default=None, alias="aiThreadSummariesEnabled")
    allowed_file_upload_content_types: list[str] | None = Field(default=None, alias="allowedFileUploadContentTypes")
    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    code_intelligence_enabled: bool | None = Field(default=None, alias="codeIntelligenceEnabled")
    code_intelligence_repository: str | None = Field(default=None, alias="codeIntelligenceRepository")
    coding_agent_enabled: bool | None = Field(default=None, alias="codingAgentEnabled")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    created_issue_count: int | None = Field(default=None, alias="createdIssueCount")
    customer_count: int | None = Field(default=None, alias="customerCount", description="Number of customers in the...")
    customers_enabled: bool | None = Field(default=None, alias="customersEnabled", description="Whether the organiz...")
    default_feed_summary_schedule: str | None = Field(default=None, alias="defaultFeedSummarySchedule")
    deletion_requested_at: datetime | None = Field(default=None, alias="deletionRequestedAt")
    feed_enabled: bool | None = Field(default=None, alias="feedEnabled", description="Whether the organization has ...")
    fiscal_year_start_month: float | None = Field(default=None, alias="fiscalYearStartMonth")
    generated_updates_enabled: bool | None = Field(default=None, alias="generatedUpdatesEnabled")
    git_branch_format: str | None = Field(default=None, alias="gitBranchFormat", description="How git branches are ...")
    git_linkback_descriptions_enabled: bool | None = Field(default=None, alias="gitLinkbackDescriptionsEnabled")
    git_linkback_messages_enabled: bool | None = Field(default=None, alias="gitLinkbackMessagesEnabled")
    git_public_linkback_messages_enabled: bool | None = Field(default=None, alias="gitPublicLinkbackMessagesEnabled")
    hipaa_compliance_enabled: bool | None = Field(default=None, alias="hipaaComplianceEnabled")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    initiative_update_reminders_day: str | None = Field(default=None, alias="initiativeUpdateRemindersDay")
    initiative_update_reminders_hour: float | None = Field(default=None, alias="initiativeUpdateRemindersHour")
    linear_agent_enabled: bool | None = Field(default=None, alias="linearAgentEnabled")
    logo_url: str | None = Field(default=None, alias="logoUrl", description="The organization's logo URL.")
    name: str | None = Field(default=None, description="The organization's name.")
    period_upload_volume: float | None = Field(default=None, alias="periodUploadVolume")
    previous_url_keys: list[str] | None = Field(default=None, alias="previousUrlKeys")
    project_update_reminders_day: str | None = Field(default=None, alias="projectUpdateRemindersDay")
    project_update_reminders_hour: float | None = Field(default=None, alias="projectUpdateRemindersHour")
    release_channel: str | None = Field(default=None, alias="releaseChannel", description="The feature release chan...")
    restrict_agent_invocation_to_members: bool | None = Field(default=None, alias="restrictAgentInvocationToMembers")
    roadmap_enabled: bool | None = Field(default=None, alias="roadmapEnabled", description="Whether the organizatio...")
    saml_enabled: bool | None = Field(default=None, alias="samlEnabled", description="Whether SAML authentication i...")
    scim_enabled: bool | None = Field(default=None, alias="scimEnabled", description="Whether SCIM provisioning is ...")
    slack_project_channel_prefix: str | None = Field(default=None, alias="slackProjectChannelPrefix")
    trial_ends_at: datetime | None = Field(default=None, alias="trialEndsAt", description="The time at which the tr...")
    trial_starts_at: datetime | None = Field(default=None, alias="trialStartsAt", description="The time at which th...")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")
    url_key: str | None = Field(default=None, alias="urlKey", description="The organization's unique URL key.")
    user_count: int | None = Field(default=None, alias="userCount", description="Number of active users in the orga...")
    working_days: list[float] | None = Field(default=None, alias="workingDays", description="[Internal] The list of...")


class IssueConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[IssueEdge] | None = Field(default=None)
    nodes: list[Issue] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class IssueEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: Issue | None = Field(default=None)


class ProjectConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[ProjectEdge] | None = Field(default=None)
    nodes: list[Project] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class ProjectEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: Project | None = Field(default=None)


class TeamConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[TeamEdge] | None = Field(default=None)
    nodes: list[Team] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class TeamEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: Team | None = Field(default=None)


class CycleConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[CycleEdge] | None = Field(default=None)
    nodes: list[Cycle] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class CycleEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: Cycle | None = Field(default=None)


class IssueLabelConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[IssueLabelEdge] | None = Field(default=None)
    nodes: list[IssueLabel] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class IssueLabelEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: IssueLabel | None = Field(default=None)


class UserConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[UserEdge] | None = Field(default=None)
    nodes: list[User] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class UserEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: User | None = Field(default=None)


class WorkflowStateConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[WorkflowStateEdge] | None = Field(default=None)
    nodes: list[WorkflowState] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class WorkflowStateEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: WorkflowState | None = Field(default=None)


class CommentConnection(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    edges: list[CommentEdge] | None = Field(default=None)
    nodes: list[Comment] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")


class CommentEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: Comment | None = Field(default=None)


class PageInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    end_cursor: str | None = Field(default=None, alias="endCursor", description="Cursor representing the last resul...")
    has_next_page: bool | None = Field(default=None, alias="hasNextPage", description="Indicates if there are more ...")
    has_previous_page: bool | None = Field(default=None, alias="hasPreviousPage", description="Indicates if there a...")
    start_cursor: str | None = Field(default=None, alias="startCursor", description="Cursor representing the first ...")


class IssuePayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    issue: Issue | None = Field(default=None, description="The issue that was created or updated.")
    last_sync_id: float | None = Field(default=None, alias="lastSyncId", description="The identifier of the last sy...")
    success: bool | None = Field(default=None, description="Whether the operation was successful.")


class IssueSearchResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    added_to_cycle_at: datetime | None = Field(default=None, alias="addedToCycleAt")
    added_to_project_at: datetime | None = Field(default=None, alias="addedToProjectAt")
    added_to_team_at: datetime | None = Field(default=None, alias="addedToTeamAt", description="The time at which t...")
    archived_at: datetime | None = Field(default=None, alias="archivedAt", description="The time at which the entit...")
    assignee: User | None = Field(default=None, description="The user to whom the issue is assigned to.")
    auto_archived_at: datetime | None = Field(default=None, alias="autoArchivedAt", description="The time at which ...")
    auto_closed_at: datetime | None = Field(default=None, alias="autoClosedAt", description="The time at which the ...")
    branch_name: str | None = Field(default=None, alias="branchName", description="Suggested branch name for the is...")
    canceled_at: datetime | None = Field(default=None, alias="canceledAt", description="The time at which the issue...")
    completed_at: datetime | None = Field(default=None, alias="completedAt", description="The time at which the iss...")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The time at which the entity ...")
    creator: User | None = Field(default=None, description="The user who created the issue.")
    customer_ticket_count: int | None = Field(default=None, alias="customerTicketCount")
    cycle: Cycle | None = Field(default=None, description="The cycle that the issue is associated with.")
    description: str | None = Field(default=None, description="The issue's description in markdown format.")
    due_date: str | None = Field(default=None, alias="dueDate", description="The date at which the issue is due.")
    estimate: float | None = Field(default=None, description="The estimate of the complexity of the issue..")
    id: str | None = Field(default=None, description="The unique identifier of the entity.")
    identifier: str | None = Field(default=None, description="Issue's human readable identifier (e.g. ENG-123).")
    integration_source_type: str | None = Field(default=None, alias="integrationSourceType")
    label_ids: list[str] | None = Field(default=None, alias="labelIds", description="Id of the labels associated wi...")
    metadata: Any | None = Field(default=None, description="Metadata related to search result.")
    number: float | None = Field(default=None, description="The issue's unique number.")
    previous_identifiers: list[str] | None = Field(default=None, alias="previousIdentifiers")
    priority: float | None = Field(default=None, description="The priority of the issue. 0 = No priority, 1 = Urgen...")
    priority_label: str | None = Field(default=None, alias="priorityLabel", description="Label for the priority.")
    priority_sort_order: float | None = Field(default=None, alias="prioritySortOrder")
    project: Project | None = Field(default=None, description="The project that the issue is associated with.")
    sla_breaches_at: datetime | None = Field(default=None, alias="slaBreachesAt", description="The time at which th...")
    sla_high_risk_at: datetime | None = Field(default=None, alias="slaHighRiskAt", description="The time at which t...")
    sla_medium_risk_at: datetime | None = Field(default=None, alias="slaMediumRiskAt")
    sla_started_at: datetime | None = Field(default=None, alias="slaStartedAt", description="The time at which the ...")
    sla_type: str | None = Field(default=None, alias="slaType", description="The type of SLA set on the issue. Cale...")
    snoozed_until_at: datetime | None = Field(default=None, alias="snoozedUntilAt", description="The time until an ...")
    sort_order: float | None = Field(default=None, alias="sortOrder", description="The order of the item in relatio...")
    started_at: datetime | None = Field(default=None, alias="startedAt", description="The time at which the issue w...")
    started_triage_at: datetime | None = Field(default=None, alias="startedTriageAt")
    state: WorkflowState | None = Field(default=None, description="The workflow state that the issue is associate...")
    sub_issue_sort_order: float | None = Field(default=None, alias="subIssueSortOrder")
    suggestions_generated_at: datetime | None = Field(default=None, alias="suggestionsGeneratedAt")
    team: Team | None = Field(default=None, description="The team that the issue is associated with.")
    title: str | None = Field(default=None, description="The issue's title.")
    trashed: bool | None = Field(default=None, description="A flag that indicates whether the issue is in the trash...")
    triaged_at: datetime | None = Field(default=None, alias="triagedAt", description="The time at which the issue l...")
    updated_at: datetime | None = Field(default=None, alias="updatedAt", description="The last time at which the en...")
    url: str | None = Field(default=None, description="Issue URL.")


class IssueSearchResultEdge(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    cursor: str | None = Field(default=None, description="Used in `before` and `after` args")
    node: IssueSearchResult | None = Field(default=None)


class IssueSearchPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    archive_payload: Any | None = Field(default=None, alias="archivePayload", description="Archived entities matchi...")
    edges: list[IssueSearchResultEdge] | None = Field(default=None)
    nodes: list[IssueSearchResult] | None = Field(default=None)
    page_info: PageInfo | None = Field(default=None, alias="pageInfo")
    total_count: float | None = Field(default=None, alias="totalCount", description="Total number of results for qu...")


class CommentPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    comment: Comment | None = Field(default=None, description="The comment that was created or updated.")
    last_sync_id: float | None = Field(default=None, alias="lastSyncId", description="The identifier of the last sy...")
    success: bool | None = Field(default=None, description="Whether the operation was successful.")


class IssueCreateInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    assignee_id: str | None = Field(default=None, alias="assigneeId", description="The identifier of the user to as...")
    completed_at: datetime | None = Field(default=None, alias="completedAt", description="The date when the issue w...")
    create_as_user: str | None = Field(default=None, alias="createAsUser", description="Create issue as a user with...")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The date when the issue was c...")
    cycle_id: str | None = Field(default=None, alias="cycleId", description="The cycle associated with the issue.")
    delegate_id: str | None = Field(default=None, alias="delegateId", description="The identifier of the agent user...")
    description: str | None = Field(default=None, description="The issue description in markdown format.")
    description_data: Any | None = Field(default=None, alias="descriptionData", description="[Internal] The issue d...")
    display_icon_url: str | None = Field(default=None, alias="displayIconUrl", description="Provide an external use...")
    due_date: str | None = Field(default=None, alias="dueDate", description="The date at which the issue is due.")
    estimate: int | None = Field(default=None, description="The estimated complexity of the issue.")
    id: str | None = Field(default=None, description="The identifier in UUID v4 format. If none is provided, the ba...")
    label_ids: list[str] | None = Field(default=None, alias="labelIds", description="The identifiers of the issue l...")
    last_applied_template_id: str | None = Field(default=None, alias="lastAppliedTemplateId")
    parent_id: str | None = Field(default=None, alias="parentId", description="The identifier of the parent issue. ...")
    preserve_sort_order_on_create: bool | None = Field(default=None, alias="preserveSortOrderOnCreate")
    priority: int | None = Field(default=None, description="The priority of the issue. 0 = No priority, 1 = Urgent,...")
    priority_sort_order: float | None = Field(default=None, alias="prioritySortOrder")
    project_id: str | None = Field(default=None, alias="projectId", description="The project associated with the is...")
    project_milestone_id: str | None = Field(default=None, alias="projectMilestoneId")
    reference_comment_id: str | None = Field(default=None, alias="referenceCommentId")
    sla_breaches_at: datetime | None = Field(default=None, alias="slaBreachesAt", description="[Internal] The times...")
    sla_started_at: datetime | None = Field(default=None, alias="slaStartedAt", description="[Internal] The timesta...")
    sla_type: str | None = Field(default=None, alias="slaType", description="The SLA day count type for the issue. ...")
    sort_order: float | None = Field(default=None, alias="sortOrder", description="The position of the issue relate...")
    source_comment_id: str | None = Field(default=None, alias="sourceCommentId", description="The comment the issue...")
    source_pull_request_comment_id: str | None = Field(default=None, alias="sourcePullRequestCommentId")
    state_id: str | None = Field(default=None, alias="stateId", description="The team state of the issue.")
    sub_issue_sort_order: float | None = Field(default=None, alias="subIssueSortOrder")
    subscriber_ids: list[str] | None = Field(default=None, alias="subscriberIds", description="The identifiers of t...")
    team_id: str = Field(alias="teamId", description="The identifier of the team associated with the issue.")
    template_id: str | None = Field(default=None, alias="templateId", description="The identifier of a template the...")
    title: str | None = Field(default=None, description="The title of the issue.")
    use_default_template: bool | None = Field(default=None, alias="useDefaultTemplate")


class IssueUpdateInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    added_label_ids: list[str] | None = Field(default=None, alias="addedLabelIds", description="The identifiers of ...")
    assignee_id: str | None = Field(default=None, alias="assigneeId", description="The identifier of the user to as...")
    auto_closed_by_parent_closing: bool | None = Field(default=None, alias="autoClosedByParentClosing")
    cycle_id: str | None = Field(default=None, alias="cycleId", description="The cycle associated with the issue.")
    delegate_id: str | None = Field(default=None, alias="delegateId", description="The identifier of the agent user...")
    description: str | None = Field(default=None, description="The issue description in markdown format.")
    description_data: Any | None = Field(default=None, alias="descriptionData", description="[Internal] The issue d...")
    due_date: str | None = Field(default=None, alias="dueDate", description="The date at which the issue is due.")
    estimate: int | None = Field(default=None, description="The estimated complexity of the issue.")
    label_ids: list[str] | None = Field(default=None, alias="labelIds", description="The identifiers of the issue l...")
    last_applied_template_id: str | None = Field(default=None, alias="lastAppliedTemplateId")
    parent_id: str | None = Field(default=None, alias="parentId", description="The identifier of the parent issue. ...")
    priority: int | None = Field(default=None, description="The priority of the issue. 0 = No priority, 1 = Urgent,...")
    priority_sort_order: float | None = Field(default=None, alias="prioritySortOrder")
    project_id: str | None = Field(default=None, alias="projectId", description="The project associated with the is...")
    project_milestone_id: str | None = Field(default=None, alias="projectMilestoneId")
    removed_label_ids: list[str] | None = Field(default=None, alias="removedLabelIds")
    sla_breaches_at: datetime | None = Field(default=None, alias="slaBreachesAt", description="[Internal] The times...")
    sla_started_at: datetime | None = Field(default=None, alias="slaStartedAt", description="[Internal] The timesta...")
    sla_type: str | None = Field(default=None, alias="slaType", description="The SLA day count type for the issue. ...")
    snoozed_by_id: str | None = Field(default=None, alias="snoozedById", description="The identifier of the user wh...")
    snoozed_until_at: datetime | None = Field(default=None, alias="snoozedUntilAt", description="The time until an ...")
    sort_order: float | None = Field(default=None, alias="sortOrder", description="The position of the issue relate...")
    state_id: str | None = Field(default=None, alias="stateId", description="The team state of the issue.")
    sub_issue_sort_order: float | None = Field(default=None, alias="subIssueSortOrder")
    subscriber_ids: list[str] | None = Field(default=None, alias="subscriberIds", description="The identifiers of t...")
    team_id: str | None = Field(default=None, alias="teamId", description="The identifier of the team associated wi...")
    title: str | None = Field(default=None, description="The issue title.")
    trashed: bool | None = Field(default=None, description="Whether the issue has been trashed.")


class CommentCreateInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    body: str | None = Field(default=None, description="The comment content in markdown format.")
    create_as_user: str | None = Field(default=None, alias="createAsUser", description="Create comment as a user wi...")
    create_on_synced_slack_thread: bool | None = Field(default=None, alias="createOnSyncedSlackThread")
    created_at: datetime | None = Field(default=None, alias="createdAt", description="The date when the comment was...")
    display_icon_url: str | None = Field(default=None, alias="displayIconUrl", description="Provide an external use...")
    do_not_subscribe_to_issue: bool | None = Field(default=None, alias="doNotSubscribeToIssue")
    id: str | None = Field(default=None, description="The identifier in UUID v4 format. If none is provided, the ba...")
    initiative_id: str | None = Field(default=None, alias="initiativeId", description="[Internal] The initiative to...")
    initiative_update_id: str | None = Field(default=None, alias="initiativeUpdateId")
    issue_id: str | None = Field(default=None, alias="issueId", description="The issue to associate the comment wit...")
    parent_id: str | None = Field(default=None, alias="parentId", description="The parent comment under which to ne...")
    post_id: str | None = Field(default=None, alias="postId", description="The post to associate the comment with.")
    project_id: str | None = Field(default=None, alias="projectId", description="[Internal] The project to associat...")
    project_update_id: str | None = Field(default=None, alias="projectUpdateId", description="The project update to...")
    quoted_text: str | None = Field(default=None, alias="quotedText", description="The text that this comment refer...")
    subscriber_ids: list[str] | None = Field(default=None, alias="subscriberIds", description="[INTERNAL] The ident...")


class CommentUpdateInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    body: str | None = Field(default=None, description="The comment content.")
    do_not_subscribe_to_issue: bool | None = Field(default=None, alias="doNotSubscribeToIssue")
    quoted_text: str | None = Field(default=None, alias="quotedText", description="The text that this comment refer...")
    resolving_comment_id: str | None = Field(default=None, alias="resolvingCommentId")
    resolving_user_id: str | None = Field(default=None, alias="resolvingUserId", description="[INTERNAL] The user w...")
    subscriber_ids: list[str] | None = Field(default=None, alias="subscriberIds", description="[INTERNAL] The ident...")


class IssueLabelNodes(BaseModel):
    """Helper model for nested label responses (labels { nodes { ... } })."""

    model_config = ConfigDict(populate_by_name=True)

    nodes: list[IssueLabel] | None = Field(default=None)


# Rebuild all models to resolve forward references
WorkflowState.model_rebuild()
IssueLabel.model_rebuild()
User.model_rebuild()
Team.model_rebuild()
Cycle.model_rebuild()
Project.model_rebuild()
ProjectStatus.model_rebuild()
Comment.model_rebuild()
Issue.model_rebuild()
Organization.model_rebuild()
IssueConnection.model_rebuild()
IssueEdge.model_rebuild()
ProjectConnection.model_rebuild()
ProjectEdge.model_rebuild()
TeamConnection.model_rebuild()
TeamEdge.model_rebuild()
CycleConnection.model_rebuild()
CycleEdge.model_rebuild()
IssueLabelConnection.model_rebuild()
IssueLabelEdge.model_rebuild()
UserConnection.model_rebuild()
UserEdge.model_rebuild()
WorkflowStateConnection.model_rebuild()
WorkflowStateEdge.model_rebuild()
CommentConnection.model_rebuild()
CommentEdge.model_rebuild()
PageInfo.model_rebuild()
IssuePayload.model_rebuild()
IssueSearchResult.model_rebuild()
IssueSearchResultEdge.model_rebuild()
IssueSearchPayload.model_rebuild()
CommentPayload.model_rebuild()
IssueCreateInput.model_rebuild()
IssueUpdateInput.model_rebuild()
CommentCreateInput.model_rebuild()
CommentUpdateInput.model_rebuild()
