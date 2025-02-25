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
|   0-10     |  230   |
|   10-25     |  54   |
|   25-50     |   61   |
|   50-75     |   52   |
|   75-100     |   38   |
|   100-150     |  55  |
|   150-200     |   22   |
|  200-250     |    11   |
|    250-300      |   10    |
|    300-400      |       |
|     400-500     |    3   |
|    500 - 600  |    0   |
|    600-700      |   1    |
|    700-800      |   0    |
|     800-900     |     0  |
|    900-1000      |   0    |
|    > 1000      |   3    | 

The file that had the most mementos was `ff825663428d986bc4ad8b7e1831756a-tm.json`.  This file has has 11574 mementos.  This surprised me a lot.  

I created this Python script to help count the mementos: 

```
import os
import json
from collections import defaultdict

timemaps_directory = 'timemaps'

memento_groups = defaultdict(int)

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

sorted_memento_groups = sorted(memento_groups.items())

for memento_count, file_count in sorted_memento_groups:
    if memento_count > 0 and memento_count < 10:
        zeroToTen += file_count
    if memento_count > 10 and memento_count < 25:
        tenToTwentyFive += file_count
    if memento_count > 25 and memento_count < 50:
        twentyFiveToFifty += file_count
    if memento_count > 50 and memento_count < 75:
        fiftyToSeventyFive += file_count
    if memento_count > 75 and memento_count < 100:
        seventyFiveToHundred += file_count
    if memento_count > 100 and memento_count < 150:
        hundredToOneFifty += file_count
    if memento_count > 150 and memento_count < 200:
        oneFiftyToTwoHundred += file_count
    if memento_count > 200 and memento_count < 250:
        twoHundredToTwoFifty += file_count
    if memento_count > 250 and memento_count < 300:
        twoFiftyToThreeHundred += file_count
    if memento_count > 300 and memento_count < 400:
        threeHundredToFourHundred += file_count
    if memento_count > 400 and memento_count < 500:
        fourHundredToFiveHundred += file_count
    if memento_count > 500 and memento_count < 600:
        fiveHundredToSixHundred += file_count
    if memento_count > 600 and memento_count < 700:
        sixHundredToSevenHundred += file_count
    if memento_count > 700 and memento_count < 800:
        sevenHundredToEightHundred += file_count
    if memento_count > 800 and memento_count < 900:
        eightHundredToNineHundred += file_count
    if memento_count > 900 and memento_count < 1000:
        nineHundredToTenHundred += file_count
    if memento_count > 1000:
        print(f"File {filename} has {memento_count} mementos.")

print(f"0-10: {zeroToTen}")
print(f"10-25: {tenToTwentyFive}")
print(f"25-50: {twentyFiveToFifty}")
print(f"50-75: {fiftyToSeventyFive}")
print(f"75-100: {seventyFiveToHundred}")
print(f"100-150: {hundredToOneFifty}")
print(f"150-200: {oneFiftyToTwoHundred}")
print(f"200-250: {twoHundredToTwoFifty}")
print(f"250-300: {twoFiftyToThreeHundred}")
print(f"300-400: {threeHundredToFourHundred}")
print(f"400-500: {fourHundredToFiveHundred}")
print(f"500-600: {fiveHundredToSixHundred}")
print(f"600-700: {sixHundredToSevenHundred}")
print(f"700-800: {sevenHundredToEightHundred}")
print(f"800-900: {eightHundredToNineHundred}")
print(f"900-1000: {nineHundredToTenHundred}")
```

# References
