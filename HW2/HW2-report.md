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
### Important Note: I checked all 19 html files, and there were not 10 different domains.  They were all different URIs, however, many of them shared a common domain. 

### I used the term "gift" for this question.  The total number of documents that contained this term was 19.  However, these are the ten documents that I selected, and the result of each document after I ran the following command:
 `grep -c "gift" *.txt`
 ```
1.) f8d5b9d5f1efef4cadd56f1bcd132b75_processed.txt:1
2.) 3871f5d6ea6bedfd85c71a6ac01a8f77_processed.txt:1   
3.) 4a544ef247d7a5640c8a196af4229b02_processed.txt:1
4.) e66d8fb3b87a52a0769553bb94df56a2_processed.txt:2
5.) 2c8adf3a27454c5cb367b83a0124beaa_processed.txt:5
6.) d6f771f500f797bff9b8b9039383594f_processed.txt:1
7.) 172480efeaa0d98a7987f2d13ec04dba_processed.txt:1
8.) b10c01549227c83825e3c82761084462_processed.txt:1
9.) 8c8c1acc9f3a93a1a2b7ed6c1c1123e6_processed.txt:1
10.) 30eedd0632a5c9369deea1bdc7822cec_processed.txt:2
```

### URI of each document:
```
1.) https://catalog.odu.edu/undergraduate/studentfinancialaid/
2.) https://catalog.odu.edu/courses/tax/
3.) https://catalog.odu.edu/graduate/business/accounting/
4.) https://catalog.odu.edu/undergraduate/education/educational-leadership-workforce-development/
5.) https://catalog.odu.edu/courses/sped/
6.) https://catalog.odu.edu/courses/fin/
7.) https://catalog.odu.edu/undergraduate/business/financial-management/
8.) https://www.odu.edu/life/culture/arts/diehn
9.) https://catalog.odu.edu/undergraduate/continuing-education/
10.) https://catalog.odu.edu/graduate/financialawardsforgraduatestudents/
```

### I used `wc -w` to find the word count of each .txt file:
```
1.) f8d5b9d5f1efef4cadd56f1bcd132b75_processed.txt  29662
2.) 3871f5d6ea6bedfd85c71a6ac01a8f77_processed.txt  707
3.) 4a544ef247d7a5640c8a196af4229b02_processed.txt  2260
4.) e66d8fb3b87a52a0769553bb94df56a2_processed.txt  6767
5.) 2c8adf3a27454c5cb367b83a0124beaa_processed.txt  9851
6.) d6f771f500f797bff9b8b9039383594f_processed.txt  2431
7.) 172480efeaa0d98a7987f2d13ec04dba_processed.txt  2031
8.) b10c01549227c83825e3c82761084462_processed.txt  3435
9.) 8c8c1acc9f3a93a1a2b7ed6c1c1123e6_processed.txt  6165
10.) 30eedd0632a5c9369deea1bdc7822cec_processed.txt  3737
```

## Calculating TF, IDF, TF-IDF
The formulas for each of these equations can be found in the Module-04 Searching slides for CS432, so I used each provided formula. Please find my work below.

Total Number of documents = 602 

### Compute Document Frequency:
The term "gift" was found in 19 documents
DF = 19

### Compute Term frequency (TF) for each .txt file:
TF = number of times "gift" appears in the document / total number of words in the document
```
1.) TF = 1 / 29662 = 0.00003371316
2.) TF = 1 / 707 = 0.00141442715
3.) TF = 1 / 2260 = 0.00044247787
4.) TF = 2 / 6767 = 0.00029555194
5.) TF = 5 / 9851 = 0.00050756268
6.) TF = 1 / 2431 = 0.00041135335
7.) TF = 1 / 2031 = 0.00049236829
8.) TF = 1 / 3435 = 0.00029112081
9.) TF = 1 / 6165 = 0.000162206
10.) TF = 2 / 3737 = 0.00053518865
```

### Compute IDF:

IDF = log_2 ( total number of documents / number of documents that contain "gift")
= log_2 (602 / 19) = 4.98569216332

### Compute TF-IDF for each .txt file:

TF-IDF = TF * IDF
```
1.) TF-IDF = 0.00003371316 * 4.98569216332 = 0.00016808343
2.) TF-IDF = 0.00141442715 * 4.98569216332 = 0.00705189835
3.) TF-IDF = 0.00044247787 * 4.98569216332 = 0.00220605844
4.) TF-IDF = 0.00029555194 * 4.98569216332 = 0.00147353099
5.) TF-IDF = 0.00050756268 * 4.98569216332 = 0.00253055127
6.) TF-IDF = 0.00041135335 * 4.98569216332 = 0.00205088117
7.) TF-IDF = 0.00049236829 * 4.98569216332 = 0.00245479672
8.) TF-IDF = 0.00029112081 * 4.98569216332 = 0.00145143874
9.) TF-IDF = 0.000162206 * 4.98569216332 = 0.00080870918
10.) TF-IDF = 0.00053518865 * 4.98569216332 = 0.00266828585
```
### Table (decreasing order by TF-IDF values)

|TF-IDF	|TF	|IDF	|URI
|------:|--:|---:|---
|0.00705189835	|0.00141442715	|4.98569216332 |https://catalog.odu.edu/courses/tax/
|0.00266828585	|0.00053518865	|4.98569216332	|https://catalog.odu.edu/graduate/financialawardsforgraduatestudents/
|0.00253055127	|0.00050756268	|4.98569216332	|https://catalog.odu.edu/courses/sped/
|0.00245479672	|0.00049236829	|4.98569216332	|https://catalog.odu.edu/undergraduate/business/financial-management/
|0.00220605844	|0.00044247787	|4.98569216332	|https://catalog.odu.edu/graduate/business/accounting/
|0.00205088117	|0.00041135335	|4.98569216332	|https://catalog.odu.edu/courses/fin/
|0.00147353099	|0.00029555194	|4.98569216332	|https://catalog.odu.edu/undergraduate/education/educational-leadership-workforce-development/
|0.00145143874	|0.00029112081	|4.98569216332	|https://www.odu.edu/life/culture/arts/diehn
|0.00080870918	|0.000162206	|4.98569216332	|https://catalog.odu.edu/undergraduate/continuing-education/
|0.00016808343	|0.00003371316	|4.98569216332	|https://catalog.odu.edu/undergraduate/studentfinancialaid/

# Q3 Answer


# References
* Module-04 Searching, <https://docs.google.com/presentation/d/1xHWYidHcqPljtvqcGsUXgXU7j6KEFDVXrTftHmkv6OA/edit?pli=1#slide=id.g32fc6d3dd1_0_4>
