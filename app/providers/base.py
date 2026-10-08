"""Provider-agnostic LLM interface. No vendor SDK is imported here or in any caller."""

from dataclasses import dataclass
from typing import Any, Protocol

# ---------- Request / response ----------

@dataclass(frozen=True)
class ToolSpec:
  """A 'form' the model must fill in. The filled-in arguments are the answer."""
  name: str
  description: str
  input_schema: dict[str, Any]

@dataclass(frozen=True)
class ProviderRequest:
  system: str
  user: str
  tool: ToolSpec
  max_tokens: int = 1024
  temperatute: float = 0.0
  timeout_s: float = 10.0

@dataclass(frozen=True)
class ProviderResponse:
  tool_input: dict[str, Any] | None
  model: str
  input_tokens: int
  output_tokens: int
  latency_ms: int

