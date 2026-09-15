"""Minimal agent used to verify sandbox return-value capture."""


def run() -> str:
    """Return a deterministic value without network or model calls."""
    return "KNOWN_OUTPUT_123"
