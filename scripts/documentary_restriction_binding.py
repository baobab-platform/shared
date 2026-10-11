"""PEO-02T executable contract semantics beyond JSON Schema 2020-12.

JSON Schema validates individual objects; matching a CP response to the exact
originating request and comparing timestamps are inherently pair/temporal
rules. Every downstream PEP must enforce equivalents in its own runtime.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Mapping

POLICY = "ADR-BCP-026/PEO-02T:negative-only"
MAX_LEASE = timedelta(seconds=2)
MAX_AGE = timedelta(seconds=3)
CLOCK_SKEW = timedelta(seconds=1)


class RestrictionDecisionRejected(ValueError):
    """A request/response pair cannot be consumed as current CP evidence."""


def _utc(value: object) -> datetime:
    if not isinstance(value, str):
        raise RestrictionDecisionRejected("missing decision timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RestrictionDecisionRejected("invalid decision timestamp") from exc
    if parsed.tzinfo is None:
        raise RestrictionDecisionRejected("decision timestamp must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def verify_current_restriction_pair(
    request: Mapping[str, str],
    response: Mapping[str, object],
    *,
    organisation_id: str,
    now: datetime,
) -> bool:
    """Return whether a negative hold is ACTIVE; never return 'authorised'.

    Both objects must already conform to their individual canonical JSON
    schemas. Consumers must independently redeem workload-owned Context,
    active tenant PRIMARY Organisation and other provider/legal authorities.
    """
    if not isinstance(request, Mapping) or not isinstance(response, Mapping):
        raise RestrictionDecisionRejected("missing bounded assessment pair")
    if now.tzinfo is None:
        raise RestrictionDecisionRejected("reference time must be timezone-aware")
    for name in ("context_id", "operation_reference", "market", "capability"):
        if not isinstance(request.get(name), str) or response.get(name) != request[name]:
            raise RestrictionDecisionRejected("CP decision does not match originating scope")
    if (
        not isinstance(organisation_id, str) or not organisation_id
        or response.get("organisation_id") != organisation_id
        or response.get("authority_granted") is not False
        or response.get("policy_reference") != POLICY
        or type(response.get("blocked")) is not bool
    ):
        raise RestrictionDecisionRejected("decision has unauthorised or alien authority")
    evaluated = _utc(response.get("evaluated_at"))
    expires = _utc(response.get("expires_at"))
    now_utc = now.astimezone(timezone.utc)
    if (
        expires <= evaluated or expires - evaluated > MAX_LEASE
        or expires <= now_utc
        or evaluated > now_utc + CLOCK_SKEW
        or now_utc - evaluated > MAX_AGE
    ):
        raise RestrictionDecisionRejected("CP decision is stale, inverted or over-leased")
    return response["blocked"]
