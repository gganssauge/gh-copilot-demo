# Python Best Practices

When writing Python code, strictly adhere to the following best practices:

## Code Style & Formatting

- Follow **PEP 8** style guide for all Python code
- Use 4 spaces for indentation (never tabs)
- Limit lines to 79 characters for code, 72 for docstrings/comments
- Use snake_case for functions and variables, PascalCase for classes, UPPER_CASE for constants
- Add two blank lines before top-level functions and classes, one blank line between methods
- Use trailing commas in multi-line data structures for cleaner diffs

## Type Hints & Documentation

- Always use type hints for function parameters and return values
- Import types from `typing` module when needed (List, Dict, Optional, Union, etc.)
- Use Python 3.10+ syntax where appropriate (`list[str]` instead of `List[str]`)
- Write comprehensive docstrings for all modules, classes, and public functions using Google or NumPy style
- Include Examples section in docstrings for complex functions

## Error Handling

- Use specific exceptions rather than bare `except:` clauses
- Create custom exception classes for domain-specific errors
- Use context managers (`with` statements) for resource management
- Log exceptions appropriately with proper severity levels
- Validate inputs early and raise clear, informative exceptions

## Code Quality

- Follow DRY (Don't Repeat Yourself) principle - extract common logic into functions
- Keep functions focused and small (ideally < 20 lines)
- Use list comprehensions and generator expressions for simple transformations
- Prefer `pathlib.Path` over `os.path` for file operations
- Use f-strings for string formatting (not % or .format())
- Avoid mutable default arguments - use `None` and initialize inside function

## Testing

- Write unit tests for all functions using `pytest`
- Aim for at least 80% code coverage
- Use fixtures for test setup and teardown
- Follow AAA pattern: Arrange, Act, Assert
- Use descriptive test names: `test_<function>_<scenario>_<expected_outcome>`
- Mock external dependencies in unit tests

## Dependencies & Environment

- Use virtual environments (venv or poetry) for all projects
- Pin exact dependency versions in requirements.txt or pyproject.toml
- Separate dev dependencies from production dependencies
- Keep dependencies minimal and up-to-date
- Use `pyproject.toml` for modern Python projects

## Security

- Never hardcode secrets, credentials, or API keys - use environment variables
- Validate and sanitize all user inputs
- Use `secrets` module for cryptographically secure random values
- Be cautious with `eval()`, `exec()`, and `pickle` - avoid when possible
- Use parameterized queries to prevent SQL injection

## Project Structure

```
project/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       └── utils/
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml
├── README.md
└── .gitignore
```

## Performance & Pythonic Code

- Use built-in functions and standard library when possible (they're optimized)
- Leverage itertools and functools for efficient iteration and functional programming
- Use `enumerate()` instead of manual counters
- Use `zip()` for parallel iteration
- Prefer `any()` and `all()` for boolean checks on iterables
- Use dictionary comprehensions and set operations for performance
- Profile before optimizing - don't guess at bottlenecks

## Logging

- Use the `logging` module instead of print statements
- Configure logging at application startup
- Use appropriate log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include contextual information in log messages
- Never log sensitive information (passwords, tokens, PII)

## Async Programming

- Use `async`/`await` for I/O-bound operations
- Use `asyncio.gather()` for concurrent operations
- Properly handle event loops and cleanup
- Be aware of blocking calls in async functions

## Example Implementation

When implementing Python code, it should look like this:

```python
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Process and validate data from multiple sources.
    
    Attributes:
        input_path: Path to input data directory
        max_retries: Maximum number of retry attempts
    """
    
    def __init__(self, input_path: Path, max_retries: int = 3) -> None:
        self.input_path = input_path
        self.max_retries = max_retries
        
    def process_file(self, filename: str) -> Optional[dict[str, any]]:
        """Process a single data file and return parsed content.
        
        Args:
            filename: Name of the file to process
            
        Returns:
            Dictionary containing processed data, or None if processing fails
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            ValueError: If file content is invalid
            
        Example:
            >>> processor = DataProcessor(Path("./data"))
            >>> result = processor.process_file("input.json")
            >>> print(result["status"])
            'success'
        """
        file_path = self.input_path / filename
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Cannot find {filename}")
            
        try:
            # Process file logic here
            return {"status": "success", "data": []}
        except Exception as e:
            logger.exception(f"Failed to process {filename}")
            raise ValueError(f"Invalid file format: {e}") from e
```

Apply these practices consistently to all Python code you write or review.
