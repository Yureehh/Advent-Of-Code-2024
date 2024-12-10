# Input path
input_path = "inputs/day1_input.txt"

# Read and process input in one step
list1, list2 = [], []
with open(input_path, "r") as file:
    data = [line.split() for line in file]
    list1 = sorted(int(parts[0].strip()) for parts in data)
    list2 = sorted(int(parts[1].strip()) for parts in data)

# Part 1: Calculate total distance
total_distance = sum(abs(x - y) for x, y in zip(list1, list2))
print(total_distance)

# Part 2: Calculate similarity score using built-in count method
similarity_score = sum(x * list2.count(x) for x in set(list1))
print(similarity_score)
