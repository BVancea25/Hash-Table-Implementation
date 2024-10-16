import random
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

# Load CNPs from the CSV file into a list
cnps = []
names=[]

with open("cnpuri.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header
    for row in reader:
        cnps.append(row[0])  # Assuming the CNP is the first column
        names.append(row[1])


# Randomly select 1000 unique CNPs from the list
selected_cnps = random.sample(cnps, 1000)

# Hash table initialization (using the same hashing logic as before)
num_buckets = 1000  # Number of buckets
hash_table = defaultdict(list)

def my_custom_hash(cnp, num_buckets, P=31):
    """Computes a hash value using polynomial hashing."""
    hash_value = 0
    for i, char in enumerate(cnp):
        hash_value = (hash_value + ord(char) * (P ** i)) % num_buckets
    return hash_value

# Populate the hash table
for cnp,name in zip(cnps,names):
    bucket = my_custom_hash(cnp, num_buckets)
    hash_table[bucket].append((cnp,name))

# Function to query the hash table for selected CNPs
def query_selected_cnps(selected_cnps, hash_table):
    found_cnps = set()  # To store found CNPs
    iterations = 0  # Counter for iterations
    i=0
    while len(found_cnps) < len(selected_cnps):
        # Randomly select a CNP from the selected ones
        cnp_to_find = selected_cnps[i]
        i+=1
        # Calculate the hash for the selected CNP
        bucket = my_custom_hash(cnp_to_find, num_buckets)
        iterations += 1  # Increment the iteration counter
        # Check if it exists in the corresponding bucket
        
        for entry in hash_table[bucket]:
            iterations+=1
            if(entry[0]==cnp_to_find):
                found_cnps.add(cnp_to_find)
                break
        
        

    return iterations, found_cnps

# Query the hash table
iterations_needed, retrieved_cnps = query_selected_cnps(selected_cnps, hash_table)

# Print the results
print(f"Iterations needed to find all selected CNPs: {iterations_needed}")
print(f"Total CNPs successfully found: {len(retrieved_cnps)}")



bucket_sizes = [len(hash_table[bucket]) for bucket in hash_table]


min_bucket_size = min(bucket_sizes)
max_bucket_size = max(bucket_sizes)
median_bucket_size = np.median(bucket_sizes)  # Using NumPy for median calculation

# Print min, max, and median bucket sizes
print(f"Minimum bucket size: {min_bucket_size}")
print(f"Maximum bucket size: {max_bucket_size}")
print(f"Median bucket size: {median_bucket_size:.2f}")

plt.hist(bucket_sizes, bins=50, color='blue', edgecolor='black')
plt.title('Distribution of Bucket Sizes')
plt.xlabel('Bucket Size')
plt.ylabel('Frequency')
plt.grid(axis='y')
plt.show()

# Calculate average iterations per CNP found
average_iterations = iterations_needed / len(retrieved_cnps)
print(f"Average iterations per CNP found: {average_iterations:.2f}")