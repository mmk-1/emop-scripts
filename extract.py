import os
import csv

# Get the list of directories in 'logs/'
methods_dirs = os.listdir('logs/methods')
classes_dirs = os.listdir('logs/classes')

methods_dirs.sort()
classes_dirs.sort()

def count(granularity, dirs):
    result = []

    print("DIRS")
    print(dirs)
    # For each directory (commit SHA)
    for d in dirs:
        # Read the impacted.txt and changed.txt files
        with open(os.path.join('logs/', granularity, d, f'impacted-{granularity}'), 'r') as impacted_file:
            impacted_lines = impacted_file.readlines()
        with open(os.path.join('logs/', granularity, d, f'changed-{granularity}'), 'r') as changed_file:
            changed_lines = changed_file.readlines()
        with open(os.path.join('logs/', granularity, d, f'commit'), 'r') as commit_file:
            commit_sha = commit_file.readlines()[0].strip()

        # Count the number of lines in each file
        impacted_count = len(impacted_lines)
        changed_count = len(changed_lines)
        result.append((commit_sha, changed_count, impacted_count))
    return result

# Create a CSV file with the specified header
with open('output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['number', 'commit_sha', 'methods_changed', 'methods_impacted', 'classes_changed', 'classes_impacted'])

    methods_result = count('methods', methods_dirs)
    classes_result = count('classes', classes_dirs)

    for i in range(min(len(methods_result), len(classes_result))):
        # Write the data to the CSV file
        writer.writerow([i, methods_result[i][0], methods_result[i][1], methods_result[i][2], classes_result[i][1], classes_result[i][2]])

print("DONE!")
