# Services Module - GenAI Email & Report Drafting System

This directory contains the AI service layer for generating professional emails and reports using Google Gemini.

## Modules

### `prompt_engine.py`

Structured prompt builder for AI content generation.

**Key Features:**

- Email generation prompts with customizable tone and format
- Report generation prompts with structure guidance
- Input validation and safe defaults
- Zero-copy policy - all prompts are project-specific

**Usage:**

```python
from services import PromptEngine

# Generate email prompt
email_prompt = PromptEngine.build_email_prompt(
    context="Request a meeting to discuss Q1 project milestones",
    recipient="Engineering Team",
    subject="Q1 Milestone Review Meeting",
    tone="professional"  # professional, casual, formal, friendly
)

# Generate report prompt
report_prompt = PromptEngine.build_report_prompt(
    topic="Security Vulnerability Assessment",
    key_points="Focus on web application vulnerabilities and API authentication",
    tone="formal",  # professional, casual, formal, friendly
    structure="detailed"  # executive_summary, detailed, bullet_points
)
```

**Available Tones:**

- `professional` - Professional and respectful tone
- `casual` - Casual and friendly while maintaining professionalism
- `formal` - Formal and reserved with proper business etiquette
- `friendly` - Warm and friendly while remaining professional

**Available Report Structures:**

- `executive_summary` - Concise high-level overview (500-800 words)
- `detailed` - Comprehensive analysis with sections (1000-1500 words)
- `bullet_points` - Organized bullet point format for scannability

### `gemini_service.py`

Production-grade wrapper for Google Gemini API integration.

**Key Features:**

- API key management via environment variable
- Timeout and error handling (network, rate limits, authentication)
- Diagnostic logging with correlation IDs (no secrets logged)
- Output normalization for consistent storage
- Health check functionality

**Usage:**

```python
from services import GeminiService

# Initialize service (reads GEMINI_API_KEY from environment)
service = GeminiService()

# Generate content
result = service.generate_content(
    prompt="Your prompt here",
    temperature=0.7,  # Optional: 0.0 to 1.0
    correlation_id="request-123"  # Optional: for tracking
)

print(result["content"])  # Generated text
print(result["latency_ms"])  # Request latency
print(result["correlation_id"])  # Tracking ID

# Health check
health = service.health_check()
print(health["status"])  # "healthy" or "unhealthy"
```

**Error Handling:**

The service provides specific exception types for different error scenarios:

```python
from services.gemini_service import (
    GeminiError,          # Base exception
    GeminiAPIError,       # API errors (auth, network, etc.)
    GeminiRateLimitError, # Rate limit exceeded
    GeminiTimeoutError    # Request timeout
)

try:
    result = service.generate_content(prompt="Test")
except GeminiRateLimitError:
    # Handle rate limiting
    print("Rate limit exceeded, please retry later")
except GeminiTimeoutError:
    # Handle timeout
    print("Request timed out")
except GeminiAPIError:
    # Handle other API errors
    print("API error occurred")
```

## Configuration

Set the following environment variables:

```bash
# Required
GEMINI_API_KEY=your-gemini-api-key-here

# Optional (with defaults)
GEMINI_MODEL=gemini-3-flash-preview
GEMINI_TIMEOUT=30
GEMINI_TEMPERATURE=0.7
```

## Testing

Run the test suite:

```bash
# Test prompt engine
pytest tests/test_prompt_engine.py -v

# Test Gemini service
pytest tests/test_gemini_service.py -v

# Run all tests
pytest -v
```

## Demo

Run the demonstration script to see the modules in action:

```bash
python demo_gemini_integration.py
```

## Integration Example

Complete workflow for generating a document:

```python
from services import PromptEngine, GeminiService

# Step 1: Build the prompt
prompt = PromptEngine.build_email_prompt(
    context="Request feedback on the new feature",
    recipient="Product Manager",
    tone="professional"
)

# Step 2: Initialize Gemini service
service = GeminiService()

# Step 3: Generate content
result = service.generate_content(
    prompt=prompt,
    correlation_id="doc-gen-001"
)

# Step 4: Use the generated content
email_content = result["content"]
print(f"Generated in {result['latency_ms']}ms")
print(email_content)
```

## Security Considerations

✅ **DO:**

- Store API keys in environment variables only
- Use correlation IDs for request tracking
- Monitor logs for errors and performance
- Implement retry logic for transient failures

❌ **DON'T:**

- Commit API keys to source control
- Log sensitive user data or API keys
- Skip input validation
- Ignore rate limit errors

## Architecture

```text
┌─────────────────┐
│  Route Handler  │  (Phase 05)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Prompt Engine   │  ← Builds structured prompts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gemini Service  │  ← Calls Google Gemini API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Google Gemini   │  ← AI Model
└─────────────────┘
```

## Next Steps (Phase 05)

The AI service layer is complete. Phase 05 will:

- Create REST API endpoints for document generation
- Integrate these services into the application layer
- Add document history retrieval
- Implement audit logging for AI requests

## License

See LICENSE file in the project root.
