## Common Bug Patterns to Always Test
- SQL injection in all search and input fields
- XSS attacks in text input fields
- Session not invalidated after logout
- Race conditions in concurrent form submissions
- Integer overflow in quantity/numeric fields
- Missing authorization checks on API endpoints
- CSRF token missing on state-changing requests
- Sensitive data exposed in API error responses