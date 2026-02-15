"""Concept response serialization."""

from db.models import Concept


def concept_to_response(c: Concept) -> dict:
    """Map a Concept model to the content API response (id, title, body, tags)."""
    return {
        "id": c.id,
        "title": c.title,
        "body": c.body,
        "tags": c.tags or [],
    }


def concept_to_roadmap_item(c: Concept) -> dict:
    """Map a Concept model to a roadmap item (id, title, phase, sort_order, prerequisite_concept_ids, track)."""
    return {
        "id": c.id,
        "title": c.title,
        "phase": c.phase,
        "sort_order": c.sort_order,
        "prerequisite_concept_ids": c.prerequisite_concept_ids or [],
        "track": c.track,
    }
