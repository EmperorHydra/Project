list1 = ["Alice", "Bob", "Charlie", "David"]
list2 = ["Bob", "Charlie", "Eve", "Frank"]

# Find names in list1 but not in list2
names_only_in_list1 = list(set(list1) - set(list2))

# Find names in list2 but not in list1
names_only_in_list2 = list(set(list2) - set(list1))

print(f"Names only in list1: {names_only_in_list1}")
print(f"Names only in list2: {names_only_in_list2}")