# Sample Python code with intentional issues for testing
# NOTE: This is demonstration code showing common vulnerabilities

import os
import sys

# Use environment variables for secrets
API_KEY = os.getenv("API_KEY", "")
PASSWORD = os.getenv("PASSWORD", "")

# Debug mode should be disabled in production
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

def unused_function():
    """This function is never called"""
    return 42

def calculate_total(items):
    """Optimized loop implementation"""
    # Use direct iteration instead of indexing
    return sum(items)

def query_user(user_id, cursor):
    """Secure parameterized query to prevent SQL injection"""
    # Use parameterized queries instead of string formatting
    query = "SELECT * FROM users WHERE id=?"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()

def process_data():
    """Function with clean return"""
    result = calculate_total([1, 2, 3])
    return result

def string_concat_loop(items):
    """Optimized string concatenation using join()"""
    # Use join() for efficient string concatenation
    return ''.join(str(item) for item in items)

# Redundant operation fixed
value = str(42)

# Main execution
if __name__ == "__main__":
    result = process_data()
    print(result)

# Made with Bob
