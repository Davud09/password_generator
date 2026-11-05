# Security Policy

## Reporting a vulnerability

Please do not report security vulnerabilities in public issues or discussions.
Contact [add a private security contact or reporting URL] with a description
and steps to reproduce the issue. Avoid including real passwords or other
secrets in your report.

This project does not yet have a confirmed private reporting channel. Configure
one before publishing this policy.

## Security expectations

The implementation should be reviewed to confirm that it:

- Uses a cryptographically secure random source for generated passwords.
- Does not log, transmit, or persist generated passwords unless that behavior is
  an intentional, clearly disclosed feature.
- Handles clipboard contents and generated-password display appropriately for
  its platform.
- Does not include generated passwords in telemetry, crash reports, or test output.

These are review requirements, not claims about the current implementation.
