"""Shared relative-timestamp formatting — used by every "Recent Activity"/
"Posted N days ago"-style display across both portals so the wording stays
consistent (Student Dashboard, Jobs page, Recruiter Dashboard)."""

from datetime import UTC, datetime


def relative_time(moment: datetime) -> str:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    delta = datetime.now(UTC) - moment
    seconds = delta.total_seconds()
    if seconds < 3600:
        return "Just now"
    if seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = int(seconds // 86400)
    if days < 7:
        return f"{days} day{'s' if days != 1 else ''} ago"
    weeks = days // 7
    return f"{weeks} week{'s' if weeks != 1 else ''} ago"


def relative_posted(moment: datetime) -> str:
    """Day-granularity phrasing for job postings — spec.md's Jobs page
    example is "Posted 2 days ago", coarser than `relative_time`'s
    hour-level "Just now"/"N hours ago" (which reads oddly for a listing
    that's naturally day-scale)."""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    days = (datetime.now(UTC) - moment).days
    if days <= 0:
        return "Posted today"
    if days == 1:
        return "Posted 1 day ago"
    if days < 14:
        return f"Posted {days} days ago"
    weeks = days // 7
    return f"Posted {weeks} week{'s' if weeks != 1 else ''} ago"
