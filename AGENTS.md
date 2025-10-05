# AGENTS.md

## Coding conventions

- No comments. Code must be self-explanatory through naming and structure.
- Prefer fail-fast validations: validate inputs at the top of the function and
  return or raise early.
- Avoid `else` branches when possible. Use guard clauses, early returns, and
  polymorphism instead of if/else chains.
- Prefer small, single-responsibility functions.
- Handle errors explicitly; never swallow exceptions.

## Project conventions

- Follow the existing structure and naming in this repository.
- Match the language idioms: Rails conventions for Ruby, React hooks patterns
  for TSX, typed functions with pydantic validation for Python.
- Tests accompany every new behavior; run the project's checks before pushing.
- Keep commits small and focused; reference the planned day (e.g. `D5`) in the
  commit message when applicable.
