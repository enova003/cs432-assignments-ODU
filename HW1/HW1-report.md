# HW1 - Web Science Intro
### Ethan Novak
### CS 432, Spring 2025
### Sun Feb 2, 2025 11:59pm

# Q1 Answer
For question 1, I drew a directed graph based on the following links:
```text
A --> B
B --> A
B --> C
C --> D
C --> G
D --> A
D --> H
E --> F
E --> O
F --> G
G --> C
H --> L
J --> N
K --> I
M --> A
N --> L
O --> J
```

My graph can be seen in the photo below. 

![Q1](q1.jpg)

Now, I will list each node of the graph in alphabetical order and state their category (i.e., SCC, IN, OUT, Tendrils, Tubes, Disconnected).
```
A: SCC 
B: SCC 
C: SCC 
D: SCC 
E: Tendril (This can reach IN node F)
F: IN
G: SCC 
H: OUT
I: Disconnected
J: Tube (connects F to H in a sense)
K: Disconnected
L: Tube (connects F to H in a sense)
M: IN
N: Tube (connects F to H in a sense)
O: Tube (connects F to H in a sense)
```
# Q2 Answer
a)
For part a, as the instructions state, I opened the following link and captured a screenshot:
https://www.cs.odu.edu/~mweigle/courses/cs532/ua_echo.php

![Q2 A](q2_a.png)

b)
For part b, I used a single curl command to request the URI, show the HTTP response headers, follow any redirects, and change the User-Agent HTTP request field to "CS432/532".
My results are shown in the photo below. The `-i` flag includes the HTTP response headers.  The `-L` flag follows the redirects.  The `-A` flag changes the User-Agent to "CS432/532".

![Q2 B](q2_b.png)

c)
For part c, I used a single curl command to request the URI, follow any redirects, change the User-Agent HTTP request field to "CS432/532", and save the HTML output to a file.
My results are shown in the photo below. The `-L` flag follows the redirects.  The `-A` flag changes the User-Agent to "CS432/532". The `-o` flag saves the HTML output file named `output.html`.

![Q2 C](q2_c.png)

d)
For part d, I viewed the HTML output file that was produced by curl from part c in a web browser and captured a screenshot to include in my report.

![Q2 D](q2_d.png)

# Q3 Answer
Python script:

```
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import sys

def extract_links(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            link = anchor['href']
            full_url = urljoin(url, link)  # Resolve relative links
            links.add(full_url)
        return links
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set()

def is_valid_html_page(url):
    try:
        response = requests.head(url, timeout=5)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')
        content_length = response.headers.get('Content-Length', '0')

        # Check for content type text/html and content length > 1000
        if 'text/html' in content_type and int(content_length) > 1000:
            return response.url 
        return None
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
        return None

def collect_webpages(seed_url, target_count=500):
    collected_urls = set()
    to_visit = [seed_url]
    
    while len(collected_urls) < target_count and to_visit:
        current_url = to_visit.pop(0)
        print(f"Visiting {current_url}")
        
        links = extract_links(current_url)
        
        for link in links:
            if link not in collected_urls:
                valid_url = is_valid_html_page(link)
                if valid_url:
                    collected_urls.add(valid_url)
                    print(valid_url)
                    to_visit.append(valid_url)
        
        time.sleep(random.uniform(1, 3))
    
    return collected_urls

def save_urls(urls, filename="collected_urls.txt"):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + "\n")
    print(f"Saved {len(urls)} URLs to {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 collect-webpages.py <seed_url>")
        sys.exit(1)

    seed_url = sys.argv[1]
    collected_urls = collect_webpages(seed_url)

    print(f"Collected {len(collected_urls)} unique URLs.")
    save_urls(collected_urls)

```

The seed webpages that I used to run the program are 'https://weiglemc.github.io/', 'https://www.odu.edu/', and 'https://www.youtube.com/'.

To collect the 500 URIs, I first started with a seed webpage, which was provided as an CLI argument. The script obtained the content of this seed webpage and extracted all the links from the webpage's HTML. This link extraction was accomplished by using the BeautifulSoup library to parse through the embedded HTML file.  The links were then resolved to the full URLs using urljoin.  After each link was obtained, a HEAD request was made to the server to ensure that the content-type header contained text/html and the content-lendth header had more than 1000 bytes.  The script was designed to follow any redirects.  After visiting a page and collecting the links, the script added new pages to a queue of pages to visit.  It did this until at least 500 unique URLs were obtained.  Then, the output is sent to a file called 'collected_urls.txt'. 

# References
* List of `curl` Options, <https://gist.github.com/eneko/dc2d8edd9a4b25c5b0725dd123f98b10>
