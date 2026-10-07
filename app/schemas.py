from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, StrictInt, Field, model_validator

class StrictModel(BaseModel):
  """Base for request models: Unknown fields are a 422, not silently ignored."""
  model_config = ConfigDict(extra="forbid")


# ---------- Vocabulary ----------
class Label(StrEnum):
  CLEAN = "clean"
  VIOLATION = "violation"
  UNCERTAIN = "uncertain"

class Decision(StrEnum):
  ALLOW = "allow"
  BLOCK = "block"
  REVIEW = "review"

class ClassifierStatus(StrEnum):
  OK = "ok"
  ERROR = "error"

class ErrorCode(StrEnum):
  TIMEOUT = "timeout" 
  PROVIDER_ERROR = "provider_error"
  MALFORMED_OUTPUT = "malformed_output"

class ConfidenceBasis(StrEnum):
  SELF_REPORTED = "self_reported"
  VOTE_FRACTION = "vote_fraction"

# ---------- Request ----------

class Price(StrictModel):
  amount_minor: StrictInt = Field(ge=0)
  currency: str = Field(pattern=r"^[A-Z]{3}$")

class Listing(StrictModel):
  id: str = Field(min_length=1)
  title: str = Field(min_length=1, max_length=200)
  description: str = Field(max_length=5000)
  price: Price
  category: str = Field(min_length=1)

class ModerationRequest(StrictModel):
  tenant_id: str = Field(min_length=1)
  listing: Listing


# ---------- Response ----------

class TokenUsage(BaseModel):
  input: StrictInt = Field(ge=0)
  output: StrictInt = Field(ge=0)

class ClassifierResult(BaseModel):
  name: str
  status: ClassifierStatus
  label: Label | None = None
  categories: list[str] = Field(default_factory=list)
  confidence: float | None = Field(default = None, ge=0.0, le=1.0)
  confidence_basis: ConfidenceBasis | None = None
  rationale: str | None = Field(default=None, min_length=1)
  injection_suspected: bool
  error_code: ErrorCode | None = None
  latency_ms: StrictInt = Field(ge=0)
  model: str
  tokens: TokenUsage | None = None

  @model_validator(mode="after")
  def check_status_consistency(self) -> Self:
    if self.status is ClassifierStatus.OK:
      if self.label is None or self.confidence is None or self.rationale is None:
        raise ValueError("ClassifierStatus \"OK\" requires label, confidence and rationale")
      if self.error_code is not None:
        raise ValueError("ClassifierStatus \"OK\" requires error_code to be \"None\"")
    else:
      if self.error_code is None:
        raise ValueError("ClassifierStatus \"ERROR\" requires an error_code")
      if self.label is not None or self.confidence is not None or self.rationale is not None:
        raise ValueError("ClassifierStatus \"ERROR\" cannot have label, confidence and rationale")
    return self

class Integrity(BaseModel):
  injection_suspected: bool

class ModerationResponse(BaseModel):
  listing_id: str = Field(min_length=1)
  tenant_id: str = Field(min_length=1)
  decision: Decision
  policy_version: str
  classifiers: list[ClassifierResult]
  integrity: Integrity
  trace_id: str


