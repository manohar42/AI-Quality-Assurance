## Playwright Test Patterns
- Use Page Object Model for all UI tests
- Use async/await pattern throughout
- Use pytest fixtures for browser setup/teardown
- Assert using: expect(page.locator(...)).to_be_visible()
- Use data-testid attributes for element selection
- Group tests by feature using pytest classes
- Add screenshots on failure using page.screenshot()
