# Backend code style

## Docstrings

This project uses **Google-style** docstrings.

### Module docstrings

- One-line summary of the module purpose.
- Optional "Usage" or "Notes" section if helpful.

Example:

```python
"""Curriculum generation: LightRAG context + Gemini structured output.

Uses Google Gemini only. See services/curriculum.py for the main entry point.
"""
```

### Function and method docstrings

- One-line summary.
- `Args:` (or `Arguments:`) for each parameter with type and description.
- `Returns:` with type and description.
- `Raises:` for documented exceptions, when relevant.

Example:

```python
def get_concept_by_id(concept_id: str, db: Session) -> Concept | None:
    """Fetch a concept by its primary key.

    Args:
        concept_id: The concept identifier (slug).
        db: SQLAlchemy session.

    Returns:
        The Concept instance, or None if not found.
    """
```

For simple functions, a one-line summary is enough when Args/Returns are obvious from the signature.

### Config and constants

- Module-level constants can have a one-line comment for each logical group (e.g. DB, LightRAG, CORS).
