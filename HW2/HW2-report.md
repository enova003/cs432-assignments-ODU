# HW2 - Ranking Webpages
### Ethan Novak
### CS 432, Spring 2025
### Sun Feb 16, 2025 11:59pm

# Q1 Answer
For question 1 of Homework 2, I took the URIs that I obtained from Homework 1, and I downloaded the HTML content of the URIs and removed the boilerplate. I created python scripts to help me accomplish the before mentioned tasks. My python script files, .txt files related to this question, and folders containing the raw and processed HTML are available in this GitHub repository. 

From Homework 1, I used https://www.odu.edu/ as the seed webpage, and I ran it through my original python script, which is available in my spr25-enova003/HW1/HW1-report.md file. The script collected 618 unique URIs and stored them in an output file named "collected_urls.txt".

Using those collected URIs, I created a python script called `downloadHTML.py` to download the HTML content of each URI.  The script is 657 lines in length, so I decided to omit it from the report, however, I did push the script to my GitHub repositry.  It can be found in this folder at "spr25-enova003/HW2/downloadHTML.py".  The script utilizes the `requests` library to look through each URI, fetch the HTML content, and save it in a file named after the MD5 hash of the URI. Additionally, this file is available in this GitHub repository at "spr25-enova003/HW2/uri_to_hash_map.txt".  The mapping for the URI and the generated hash is saved in this text file. The script also saves the raw HTML files and stores them in a folder called "raw_html_files". 

After this, I created another python script called `removeHTMLboilerplate.py`.  This script is available in this repository as well. The script, as the name implies, is designed to remove the HTML boilerplate by stripping the HTML tags. The script reads each raw HTML files, and uses `boilerpy3` to extract the main content and save it to a new file. The process content is stored in a folder called "processed_html_files"; this folder is also in this repository. The script is designed to skip any file that is empty or fails to process. 

To answer the question asked in the homework, of the original 618 unique URIs that I obtained, only 602 of them contained useful text. This was slightly surprising to me, as I thought all of the URIs would have contained meaningful text. 

# Q2 Answer


# Q3 Answer


# References
