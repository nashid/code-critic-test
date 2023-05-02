import os
import requests

# get the open API key
openai_api_key = os.environ.get('OPENAI_API_KEY')

# if no key is found, exit
if not openai_api_key:
    print('No OpenAPI key found. Exiting...')
    exit()

# get file names of all files that changed
changed_files = os.popen('git diff --name-only HEAD^ HEAD').read().split('\n')

# if there are no differences, do nothing
if not changed_files:
    print('No differences found. Exiting...')
    exit()

# create package to send to the API
actual_diffs = []
for file_path in changed_files:
    # check if file exists
    if not os.path.exists(file_path):
        continue
    
    # run git diff on file and skip first 4 lines
    diff_code = os.popen(f'git diff HEAD^ HEAD {file_path} | tail -n +5').read()
    actual_diffs.append({
        'name': file_path,
        'code': diff_code
    })

package = {
    'key': openai_api_key,
    'files': actual_diffs
}

# make a POST request 
response = requests.post('https://tuneer.cis188.org/analyze', json=package)

# write the results to a file called "results.sarif"
with open('results.sarif', 'w') as f:
    f.write(response.text)

print('Analysis complete. Results written to "results.sarif"')