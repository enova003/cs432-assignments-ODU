import os
import requests

uri_to_hash_map_path = 'uri_to_hash_map.txt'

def read_uri_to_hash_map(file_path):
    url_to_hash_map = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                url, hash_value = parts
                url_to_hash_map[url] = hash_value
    return url_to_hash_map

def check_url_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return None

def main():
    url_to_hash_map = read_uri_to_hash_map(uri_to_hash_map_path)
    
    status_200_count = 0
    non_status_200_count = 0

    for url, hash_value in url_to_hash_map.items():
        status_code = check_url_status(url)
        
        if status_code == 200:
            status_200_count += 1
        else:
            non_status_200_count += 1

    print(f"URLs with status code 200: {status_200_count}")
    print(f"URLs with other status codes: {non_status_200_count}")

if __name__ == '__main__':
    main()
