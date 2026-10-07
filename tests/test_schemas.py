import pytest
from pydantic import ValidationError

from app.schemas import ClassifierResult, ModerationRequest

def valid_request() -> dict:
  """A fresh valid request each call, so tests can mutate their own copy."""
  return {
    "tenant_id": "demo-marketplace",
    "listing": {
        "id": "lst_123",
        "title": "iPhone 15 Pro",
        "description": "Brand new, sealed in box.",
        "price": {"amount_minor": 5000, "currency": "USD"},
        "category": "electronics",
    },
  }


def test_valid_request_parses():
    req = ModerationRequest.model_validate(valid_request())
    assert req.listing.price.amount_minor == 5000


def test_float_amount_rejected():
    data = valid_request()
    data["listing"]["price"]["amount_minor"] = 4999.0
    with pytest.raises(ValidationError):
        ModerationRequest.model_validate(data)