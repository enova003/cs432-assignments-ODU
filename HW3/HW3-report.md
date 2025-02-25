# HW3 - Web Archiving Part 1
### Ethan Novak
### CS 432, Spring 2025
### Sunday March 2, 2025 11:59pm

# Q1 Answer
In HW1 and HW2, I obtained the list of 500 unique URIs from https://www.odu.edu/, therefore, for this problem, I obtained the TimeMaps for each of the unique URIs that I collected from https://www.odu.edu/ using MemGator Memento Aggregator. I installed a stand-alone version of MemGator on my own machine, as described in the EC-memgator assignment. My machine utilizes Windows, therefore, I downloaded the MemGator Windows AMD 64 version of MemGator. After this was downloaded, I created a Python script that reads over my URI to hash map file from HW2, iterates through each URI, and runs the MemGator command to fetch the TimeMap for each URI.  The script completely handles the process of calling the MemGator command with all the correct arguments, generating the corresponding output filenames using the MD5 hash, and adding a delay between requests.  

Here is the Python script:

```
import subprocess
import time
import os

input_file = 'uri_to_hash_map.txt'
memgator_command = './memgator-windows-amd64' 

contact_info = '"ODU CS432/532 enova003@odu.edu"' 
archives_url = 'https://raw.githubusercontent.com/odu-cs432-websci/public/main/archives.json'

FILE_SIZE_LIMIT = 10 * 1024 * 1024 # 10MB

uri_hash_map = []
with open(input_file, 'r') as file:
    for line in file:
        uri, hash_value = line.strip().split()
        uri_hash_map.append((uri, hash_value))

def fetch_timemap(uri, hash_value):
    output_filename = f"{hash_value}-tm.json" 
    command = [
        memgator_command,
        '-c', contact_info,
        '-a', archives_url,
        '-F', '2',
        '-f', 'JSON',
        uri
    ]

    try:
        with open(output_filename, 'w') as outfile:
            subprocess.run(command, stdout=outfile, check=True)
        print(f"TimeMap for {uri} saved as {output_filename}")
        
        file_size = os.path.getsize(output_filename)
        
        if file_size > FILE_SIZE_LIMIT:
            print(f"File {output_filename} is large, compressing...")
            compress_file(output_filename)
        else:
            print(f"File {output_filename} is within size limit.")
            
    except subprocess.CalledProcessError as e:
        print(f"Error fetching TimeMap for {uri}: {e}")
    except Exception as e:
        print(f"Unexpected error for {uri}: {e}")

def compress_file(filename):
    gzip_filename = filename + '.gz'
    command = f'gzip -c {filename} > {gzip_filename}'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Compressed {filename} to {gzip_filename}")
        os.remove(filename)
    except subprocess.CalledProcessError as e:
        print(f"Error compressing {filename}: {e}")
    except Exception as e:
        print(f"Error compressing {filename}: {e}")

for uri, hash_value in uri_hash_map:
    fetch_timemap(uri, hash_value)
    time.sleep(15)  

print("Processed all files. Exiting...")

```
The script reads my uri_to_hash_map.txt file from HW2 and splits the line into two parts, the first part contains the URI and the second part contains the corresponding hash. For each URI, the script constructs a command to run MemGator with the appropriate arguments as described in the assignment instructions.  These arguments are `-c`, `-a`, `-F 2`, and `-f JSON`. The `-c` option specifies my contact information, the `-a` option allows MemGator to use the alternate archive list that was provided in the assignment instructions, the `-F 2` option specifies the format of each TimeMap, and the `-f JSON` option tells MemGator to output the results in JSON format. The program sleeps in between requests for 15 seconds, and for each URI, the TimeMap is saved as a JSON file with the format `URI-HASH-tm.json`. 

Additionally, the program checks the size of each file, and if a file is greater than 10 MB, the script automatically handles compressing the file using gzip, as the assignment instructions stated. The function that is responsible for compressing the file is called `compress_file()`, and this function uses the gzip utility to compress the file.  After the file is compressed, the original uncompressed file is deleted. 

The TimeMap files for each of the URIs can be found at this file path: `spr25-enova003/HW3/timemaps`. 

# Q2 Answer

|Mementos | URI-Rs |
|---------:|--------:|
|1-10 | 241 |
|11-25 | 57 |
| 26-50 | 63 |
| 51-75 | 53 |
| 76-100 | 43 |
| 101-150 | 56 |
| 151-200 | 24 |
| 201-250 | 11 |
| 251-300 | 12 |
| 301-400 | 14 |
| 401-500 | 3 |
| 501-600 | 0 |
| 601-700 | 1 |
| 701-800 | 0 |
| 801-900 | 0 |
| 901-1000 | 0 |
| Over 1000 | 11 |

The files that had the most mementos were `81fb90c387b8a021235f6a4396be1fd7-tm.json`, `7d51e0fc5b5da98f5d37fdba731db1b0-tm.json`, and `a3e286cff87559bfdf9bad1aa1eff92f-tm.json`.  These files had over 40,000 mementos. This information surprised me a lot because I did not think a file could have that many mementos. 

I created this Python script to help count the mementos: 

```
import os
import json
from collections import defaultdict

timemaps_directory = 'timemaps'

memento_groups = defaultdict(int)

for filename in os.listdir(timemaps_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(timemaps_directory, filename)
        
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()  
                if content:  
                    data = json.loads(content) 
                    if 'mementos' in data and 'list' in data['mementos']:
                        memento_count = len(data['mementos']['list'])
                    else:
                        memento_count = 0
                    memento_groups[memento_count] += 1
                else:
                    print(f"Warning: {filename} is empty.")
        except json.JSONDecodeError:
            print(f"Warning: {filename} is not a valid JSON file.")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

zeroToTen = 0
tenToTwentyFive = 0
twentyFiveToFifty = 0
fiftyToSeventyFive = 0
seventyFiveToHundred = 0
hundredToOneFifty = 0
oneFiftyToTwoHundred = 0
twoHundredToTwoFifty = 0
twoFiftyToThreeHundred = 0
threeHundredToFourHundred = 0
fourHundredToFiveHundred = 0
fiveHundredToSixHundred = 0
sixHundredToSevenHundred = 0
sevenHundredToEightHundred = 0
eightHundredToNineHundred = 0
nineHundredToTenHundred = 0
overOneThousand = 0

for memento_count, file_count in memento_groups.items():
    if 0 < memento_count <= 10:
        zeroToTen += file_count
    elif 10 < memento_count <= 25:
        tenToTwentyFive += file_count
    elif 25 < memento_count <= 50:
        twentyFiveToFifty += file_count
    elif 50 < memento_count <= 75:
        fiftyToSeventyFive += file_count
    elif 75 < memento_count <= 100:
        seventyFiveToHundred += file_count
    elif 100 < memento_count <= 150:
        hundredToOneFifty += file_count
    elif 150 < memento_count <= 200:
        oneFiftyToTwoHundred += file_count
    elif 200 < memento_count <= 250:
        twoHundredToTwoFifty += file_count
    elif 250 < memento_count <= 300:
        twoFiftyToThreeHundred += file_count
    elif 300 < memento_count <= 400:
        threeHundredToFourHundred += file_count
    elif 400 < memento_count <= 500:
        fourHundredToFiveHundred += file_count
    elif 500 < memento_count <= 600:
        fiveHundredToSixHundred += file_count
    elif 600 < memento_count <= 700:
        sixHundredToSevenHundred += file_count
    elif 700 < memento_count <= 800:
        sevenHundredToEightHundred += file_count
    elif 800 < memento_count <= 900:
        eightHundredToNineHundred += file_count
    elif 900 < memento_count <= 1000:
        nineHundredToTenHundred += file_count
    elif memento_count > 1000:
        overOneThousand += file_count

print("\nMemento groups:")
print(f"1-10: {zeroToTen}")
print(f"11-25: {tenToTwentyFive}")
print(f"26-50: {twentyFiveToFifty}")
print(f"51-75: {fiftyToSeventyFive}")
print(f"76-100: {seventyFiveToHundred}")
print(f"101-150: {hundredToOneFifty}")
print(f"151-200: {oneFiftyToTwoHundred}")
print(f"201-250: {twoHundredToTwoFifty}")
print(f"251-300: {twoFiftyToThreeHundred}")
print(f"301-400: {threeHundredToFourHundred}")
print(f"401-500: {fourHundredToFiveHundred}")
print(f"501-600: {fiveHundredToSixHundred}")
print(f"601-700: {sixHundredToSevenHundred}")
print(f"701-800: {sevenHundredToEightHundred}")
print(f"801-900: {eightHundredToNineHundred}")
print(f"901-1000: {nineHundredToTenHundred}")
print(f"Over 1000: {overOneThousand}")
```

# References
