import re

# Input path
input_path = "inputs/day3_input.txt"


# Function to calculate the total sum from 'mul' operations
def calculate_mul_sum(file_path):
    # Define regex to match 'mul(num1,num2)' and capture numbers
    pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\))"
    total_sum = 0
    compute = True

    # Read and process the file line by line for memory efficiency
    with open(file_path, "r") as file:
        for line in file:
            # Find all matches in the current line
            for match in re.finditer(pattern, line):
                if match.group(1) == "do()":
                    compute = True
                elif match.group(1) == "don't()":
                    compute = False
                elif compute:
                    numbers = match.group()[4:-1].split(",")
                    total_sum += int(numbers[0]) * int(numbers[1])

    return total_sum


# Calculate and print the result
print(calculate_mul_sum(input_path))
