# HW3 - Web Archiving Part 1
### Ethan Novak
### CS 432, Spring 2025
### Sunday March 2, 2025 11:59pm

# Q1 Answer
In HW1 and HW2, I obtained the list of 500 unique URIs from https://www.odu.edu/, therefore, for this problem, I obtained the TimeMaps for each of the unique URIs that I collected from https://www.odu.edu/ using MemGator Memento Aggregator. I installed a stand-alone version of MemGator on my own machine, as described in the EC-memgator assignment. My machine utilizes Windows, therefore, I downloaded the MemGator Windows AMD 64 version of MemGator. After this was downloaded, I created a Python script that reads over my URI to hash map file from HW2, iterates through each URI, and runs the MemGator command to fetch the TimeMap for each URI.  The script completely handles the process of calling MemGator, generating the corresponding output filenames using the MD5 hash, and adding a delay between requests.  

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
The script reads my uri_to_hash_map.txt file from HW2 and splits the line into two parts, the first part contains the URI and the second part contains the corresponding hash. For each URI, the script constructs a command to run MemGator with the appropriate arguments as described in the assignment instructions.  These arguments are `-c`, `-a`, `-F 2`, and `-f JSON`. The program sleeps in between requests for 15 seconds, and for each URI, the TimeMap is saved as a JSON file with the format `URI-HASH-tm.json`. 

Additionally, the program checks the size of each file, and if a file is greater than 10 MB, the script automatically handles compressing the file using gzip, as the assignment instructions stated. The function that is responsible for compressing the file is called `compress_file()`, and this function uses the gzip utility to compress the file.  After the file is compressed, the original uncompressed file is deleted. 

The TimeMap files for each of the URIs can be found at this file path: `spr25-enova003/HW3/TimeMaps-Q1`. 

# Q2 Answer

# References
