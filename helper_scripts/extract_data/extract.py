import os
import csv
import sys

repo = sys.argv[1]
author = repo.split('/')[0]
project = repo.split('/')[1]

# Get the list of directories in 'logs/' and sort them
absolute_path = os.path.dirname(__file__)
logs_path = os.path.join(absolute_path, f'../../logs/{author}/{project}')
methods_dirs = os.listdir(f'{logs_path}/methods')
classes_dirs = os.listdir(f'{logs_path}/classes')
methods_dirs = sorted(methods_dirs, key=lambda x: int(x))
classes_dirs = sorted(classes_dirs, key=lambda x: int(x))

def count(granularity, dirs, projection=False):
    result = []
    # For each directory (which is a commit SHA)
    for d in dirs:
        # If granularity is methods, project methods to classes.
        # Read the impacted.txt and changed.txt files
        if projection == True:
            impacted_lines = set() # Essentially keeps the classes for impacted
            changed_lines = set() # Keeps the classes for changed methods
            with open(os.path.join(logs_path, granularity, d, f'impacted-{granularity}'), 'r') as impacted_file:
                lines = impacted_file.readlines()
                for method in lines:
                    the_class = method.strip().split('#')[0]
                    impacted_lines.add(the_class)
            with open(os.path.join(logs_path, granularity, d, f'changed-{granularity}'), 'r') as changed_file:
                lines = changed_file.readlines()
                for method in lines:
                    the_class = method.strip().split('#')[0]
                    changed_lines.add(the_class)
        else:
            with open(os.path.join(logs_path, granularity, d, f'impacted-{granularity}'), 'r') as impacted_file:
                impacted_lines = impacted_file.readlines()
            with open(os.path.join(logs_path, granularity, d, f'changed-{granularity}'), 'r') as changed_file:
                changed_lines = changed_file.readlines()
        with open(os.path.join(logs_path, granularity, d, f'commit'), 'r') as commit_file:
            commit_sha = commit_file.readlines()[0].strip()

        # Count the number of lines in each file
        impacted_count = len(impacted_lines)
        changed_count = len(changed_lines)
        result.append((commit_sha, changed_count, impacted_count))
    return result


def main():
    output_path = os.path.join(absolute_path, f'../../outputs/{author}_{project}_output.csv')
    # Create a CSV file with the specified header
    with open(output_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['number', 'commit_sha', 'methods_changed', 'methods_impacted', 'projected_changed_classes', 'projected_impacted_classes', 'classes_changed', 'classes_impacted'])

        # Find the number of classes of methods
        methods_projected_result = count('methods', methods_dirs, True)
        methods_result = count('methods', methods_dirs)
        classes_result = count('classes', classes_dirs)

        for i in range(min(len(methods_result), len(classes_result))):
            # Write the data to the CSV file
            # number, commit, methods_changed
            writer.writerow([i, methods_result[i][0], methods_result[i][1], methods_result[i][2], methods_projected_result[i][1], methods_projected_result[i][2], classes_result[i][1], classes_result[i][2]])

         # Calculate the sum and average
        methods_changed_sum = sum(methods_result[i][1] for i in range(len(methods_result)))
        methods_impacted_sum = sum(methods_result[i][2] for i in range(len(methods_result)))
        methods_projected_changed_sum = sum(methods_projected_result[i][1] for i in range(len(methods_projected_result)))
        methods_projected_impacted_sum = sum(methods_projected_result[i][2] for i in range(len(methods_projected_result)))
        classes_changed_sum = sum(classes_result[i][1] for i in range(len(classes_result)))
        classes_impacted_sum = sum(classes_result[i][2] for i in range(len(classes_result)))

        methods_changed_avg = methods_changed_sum / len(methods_result)
        methods_impacted_avg = methods_impacted_sum / len(methods_result)
        methods_projected_changed_avg = methods_projected_changed_sum / len(methods_projected_result)
        methods_projected_impacted_avg = methods_projected_impacted_sum / len(methods_projected_result)
        classes_changed_avg = classes_changed_sum / len(classes_result)
        classes_impacted_avg = classes_impacted_sum / len(classes_result)

        # Write the sum and average rows to the CSV file
        writer.writerow(['SUM', '0', methods_changed_sum, methods_impacted_sum, methods_projected_changed_sum, methods_projected_impacted_sum, classes_changed_sum, classes_impacted_sum])
        writer.writerow(['AVERAGE', '0', methods_changed_avg, methods_impacted_avg, methods_projected_changed_avg, methods_projected_impacted_avg, classes_changed_avg, classes_impacted_avg])

    print("DONE!")

if __name__ == "__main__":
    main()