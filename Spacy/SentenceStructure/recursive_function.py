def build_string_recursive(n):
    # Base case: When n reaches 0, return an empty string
    if n == 0:
        return ""

    # Recursive case: Append the current value of n to the string
    current_value = str(n)
    recursive_result = build_string_recursive(n - 1)

    # Concatenate the current value and the result of the recursive call
    result = current_value + recursive_result

    return result


# Test the recursive function
final_string = build_string_recursive(5)
print(final_string)  # Output: "54321"
