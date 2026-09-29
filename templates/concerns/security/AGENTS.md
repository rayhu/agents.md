## Security

### Secrets

- Never write secrets, tokens, or credentials into source, tests, fixtures, logs, or docs. Read them from the environment or secret manager.
- Do not commit `.env` files. Do not print secrets when debugging.

### Input and output

- Validate all external input at the boundary; reject rather than sanitize when possible.
- Use parameterized queries only. No string-built SQL, shell commands, or file paths from untrusted input.
- Encode output for its context. Do not render untrusted HTML; do not use `dangerouslySetInnerHTML` / `innerHTML` with untrusted data.
- Never `eval` or dynamically execute strings.

### Authn / authz

- Authorization is enforced server-side in deterministic code on every request, not inferred from client state.
- Default deny. Check ownership of every resource by ID.

### Crypto

- Use vetted libraries. Do not implement your own hashing, encryption, or token schemes.
- Password hashing with a dedicated algorithm (argon2 / bcrypt / scrypt). Constant-time comparison for secrets.

### Agent permissions

- Do not run destructive or irreversible commands (delete, force-push, drop, deploy) without explicit instruction.
- Do not disable security checks, linters, or CI to make a change pass.
- Do not exfiltrate repository content to external services.
