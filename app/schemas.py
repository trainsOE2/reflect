from enum import StrEnum;
from pydantic import BaseModel, ConfigDict, StrictInt, Field

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



