# Sample Python code with intentional issues for testing

import os
import sys
import unused_module  # Unused import

# Hardcoded secret
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"

DEBUG = True  # Debug mode enabled

def unused_function():
    """This function is never called"""
    return 42

def calculate_total(items):
    """Inefficient loop implementation"""
    total = 0
    for i in range(len(items)):  # Should use: for item in items
        total += items[i]
    return total

def query_user(user_id):
    """SQL injection vulnerability"""
    query = f"SELECT * FROM users WHERE id={user_id}"
    cursor.execute(query)
    return cursor.fetchall()

def process_data():
    """Function with unreachable code"""
    result = calculate_total([1, 2, 3])
    return result
    print("This code is unreachable")  # Dead code after return

def string_concat_loop(items):
    """Inefficient string concatenation"""
    result = ""
    for item in items:
        result += str(item)  # Should use join()
    return result

# Unused variable
unused_var = "never used anywhere"

# Redundant operation
value = str(str(42))

# Main execution
if __name__ == "__main__":
    result = process_data()
    print(result)

# Made with Bob
