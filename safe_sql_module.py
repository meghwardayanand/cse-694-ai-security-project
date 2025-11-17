import re
from langchain_community.utilities import SQLDatabase


# Define regex patterns for SQL injection indicators (case-insensitive)
INJECTION_PATTERNS = [
    re.compile(r"\bor\s+1\s*=\s*1\b", re.IGNORECASE),           # OR 1=1 tautology
    re.compile(r"\bor\s+'1'\s*=\s*'1'\b", re.IGNORECASE),       # OR '1'='1' tautology
    re.compile(r"\bDROP\b", re.IGNORECASE),                     # DROP (table/database)
    re.compile(r"\bDELETE\b", re.IGNORECASE),                   # DELETE (rows)
    re.compile(r"\bUPDATE\b", re.IGNORECASE),                   # UPDATE (data)
    re.compile(r"\bINSERT\b", re.IGNORECASE),                   # INSERT (data)
    re.compile(r"--|/\*.*\*/", re.IGNORECASE),                  # Inline comment start (-- or /* */)
    re.compile(r"\bUNION\s+SELECT\b", re.IGNORECASE),           # UNION SELECT combination
    # Optionally, pattern to catch semicolon followed by another statement:
    re.compile(r";\s*\S", re.IGNORECASE)                        # semicolon not at end (another stmt)
]

def is_safe_sql(query: str) -> bool:
    """
    Check if a SQL query is safe (contains no obvious SQL injection patterns).
    Returns True if no injection patterns are found, False if any pattern is detected.
    """
    # Basic cleanup: strip whitespace and remove a trailing semicolon if present.
    sanitized_query = query.strip()
    # Remove trailing semicolons to avoid false flag for ending ';'
    sanitized_query = re.sub(r";\s*$", "", sanitized_query)
    # Check each pattern; if any matches, the query is unsafe.
    for pattern in INJECTION_PATTERNS:
        if pattern.search(sanitized_query):
            return False

    return True


def sanitize_sql(query: str) -> str:
    """
    Sanitize and validate a SQL query string. If the query is safe, return a cleaned version of it.
    If the query contains SQL injection patterns, raise an exception to block it.
    """
    sanitized_query = query.strip()
    # Remove any trailing semicolon (common benign termination in SQL queries)
    sanitized_query = re.sub(r";\s*$", "", sanitized_query)
    # If any dangerous pattern is found, we do not attempt to correct it – block execution.
    if not is_safe_sql(sanitized_query):
        raise ValueError("Blocked SQL query due to potential SQL injection attempt.")

    return sanitized_query


class SafeSQLDatabase(SQLDatabase):
    """
    Subclass of LangChain's SQLDatabase that intercepts queries and blocks unsafe SQL.
    Use this in place of SQLDatabase to automatically apply injection filtering.
    """
    def run(self, command: str, fetch: str = "all", include_columns: bool = False, **kwargs) -> str:
        # Check the raw SQL command using our regex filters
        if not is_safe_sql(command):
            # If unsafe, raise an error instead of executing
            raise ValueError("Blocked SQL query due to potential SQL injection.")
        # If safe, delegate to the base class's run method to execute the query
        return super().run(command, fetch=fetch, include_columns=include_columns, **kwargs)
