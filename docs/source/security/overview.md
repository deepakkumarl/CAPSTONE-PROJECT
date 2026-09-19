# Security Overview

The platform enforces strict security controls and privacy principles to protect host systems and technical data.

## Security Principles

1. **100% Local Privacy**: Zero external API calls or telemetry. All vectors and LLM text generation remain on the local machine.
2. **Defensive Input Sanitization**: Path traversal and malicious uploads are rejected before filesystem writing.
3. **Static Code Analysis**: Automated security linting using **Bandit** in CI/CD pipelines.
4. **No Secrets in Code**: Environment configurations use standard variables; secrets are injected via GitHub Secrets.
