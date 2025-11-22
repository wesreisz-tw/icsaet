# Task 01: Project Setup and Structure

## Story Reference
- **Parent Story:** SCRUM-5 - Cursor MCP Server for ICAET Query Access
- **Task Sequence:** 1 of 8

## Task Objective
Create the foundational Python project structure for the ICAET MCP server with proper package configuration, dependencies, and basic project scaffolding.

## Scope
- Initialize Python project structure following src-layout pattern
- Configure pyproject.toml with all dependencies
- Set up basic .gitignore and development tooling
- Create placeholder module files
- Configure development environment requirements

## Acceptance Criteria
1. Project structure matches specification:
   ```
   icsaet-mcp/
   ├── pyproject.toml
   ├── README.md (stub)
   ├── .gitignore
   ├── src/
   │   └── icsaet_mcp/
   │       ├── __init__.py
   │       ├── __main__.py (stub)
   │       ├── server.py (stub)
   │       ├── tools.py (stub)
   │       ├── prompts.py (stub)
   │       ├── logging_config.py (stub)
   │       └── utils.py (stub)
   └── tests/
       ├── __init__.py
       ├── conftest.py (stub)
       ├── mock_server.py (stub)
       ├── test_server.py (stub)
       ├── test_tools.py (stub)
       └── test_integration.py (stub)
   ```

2. pyproject.toml includes:
   - Python 3.12+ requirement
   - Core dependencies: fastmcp>=0.1.0, httpx>=0.24.0
   - Dev dependencies: pytest, pytest-asyncio, pytest-httpx, flask, black, ruff
   - Package metadata and entry points
   - Build system configuration

3. All stub files contain valid Python (imports, docstrings, pass statements)

4. Package can be installed in editable mode: `pip install -e ".[dev]"`

5. Basic smoke test passes: `python -c "import icsaet_mcp"`

## Dependencies
- None (first task)

## Required Inputs
- SCRUM-5 specification document
- Architecture section defining structure
- Packaging section defining pyproject.toml configuration

## Expected Outputs and Handoff Criteria

### Outputs
1. Complete project structure with all directories and stub files
2. Valid pyproject.toml ready for package installation
3. .gitignore configured for Python projects
4. All dependencies installable via pip

### Handoff Criteria
- `pip install -e ".[dev]"` succeeds without errors
- `python -m icsaet_mcp` runs without import errors (may exit immediately, but no ImportError)
- All test files are importable: `pytest --collect-only` succeeds
- Project structure matches specification exactly

### Handoff to Task 02
- Task 02 will implement the core MCP server in server.py and __main__.py
- Task 02 requires: working package structure, stub files in place, dependencies installed

## Task-Specific Constraints
1. Use exact dependency versions from SCRUM-5 specification
2. Follow src-layout pattern (not flat layout)
3. All stub files must be valid Python (no syntax errors)
4. Package must be installable locally before handoff
5. Do not implement any business logic - stubs only
6. README.md should only contain project title and "Work in Progress" note

## Validation Checklist
- [ ] Project structure created
- [ ] pyproject.toml valid and complete
- [ ] Package installs with dev dependencies
- [ ] All stub files importable
- [ ] No import errors when running module
- [ ] pytest can collect (even if no tests yet)

