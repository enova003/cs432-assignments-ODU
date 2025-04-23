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
