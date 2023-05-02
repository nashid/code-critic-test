import json
import os
import requests

# Get the open API key from GitHub secrets or input
openapi_key = os.environ.get('OPENAPI_KEY')

# Run git diff to get the difference created by the last commit
diff_output = os.popen('git diff HEAD^ HEAD').read()

# If there are no differences, do nothing
if not diff_output:
    print('No differences found. Exiting...')
    exit()

print("diff_output: ", diff_output)

# Split the diff output into separate files
diff_files = diff_output.split('diff --git ')[1:]
print("diff_files: ", diff_files)

# Create a list to hold the JSON package for each file
json_packages = []

# Loop through each file and create the JSON package
for diff_file in diff_files:
    print("diff_file: ", diff_file)

    # Get the file name
    file_name = diff_file.split(' b/')[1].strip()

    # Get the diff code
    diff_code = diff_file.split('@@')[1].split('\n@@')[0].strip()

    # Create the JSON package
    json_package = {
        'key': openapi_key,
        'files': [{
            'name': file_name,
            'code': diff_code
        }]
    }

    # Add the JSON package to the list
    json_packages.append(json_package)

print("json_packages: ", json_packages)

# Make a POST request to https://tuneer.cis188.org/analyze with the JSON package
# response = requests.post('https://tuneer.cis188.org/analyze', json=json_packages)

# Write the results to a file called "results.sarif"
# with open('results.sarif', 'w') as f:
#     f.write(response.text)

# print('Analysis complete. Results written to "results.sarif"')