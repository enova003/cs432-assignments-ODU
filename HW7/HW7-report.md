# HW7 - Email Classification
### Ethan Novak
### CS 432, Spring 2025
### Sunday April 13, 2025 11:59pm

# Script
The script for this assignment can be found in this directory under the filename `classifyEmail.py`. Additionally, I pasted the script below:

```
import re
import math
import os
import random
from pathlib import Path

def getwords(doc):
    splitter = re.compile(r'\W+')
    words = [s.lower() for s in splitter.split(doc) if len(s) > 2 and len(s) < 20]
    return dict([(w, 1) for w in words])

class basic_classifier:
    def __init__(self, getfeatures):
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures
    
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1
    
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    
    def catcount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0
    
    def totalcount(self):
        return sum(self.cc.values())
    
    def categories(self):
        return self.cc.keys()
    
    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f, cat)
        
        self.incc(cat)
    
    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        
        return self.fcount(f, cat) / self.catcount(cat)
    
    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        basicprob = prf(f, cat)
        
        totals = sum([self.fcount(f, c) for c in self.categories()])
        
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp

class naivebayes(basic_classifier):
    def __init__(self, getfeatures):
        basic_classifier.__init__(self, getfeatures)
        self.thresholds = {}
    
    def docprob(self, item, cat):
        features = self.getfeatures(item)
        
        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
        return p
    
    def prob(self, item, cat):
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob
    
    def setthreshold(self, cat, t):
        self.thresholds[cat] = t
    
    def getthreshold(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]
    
    def classify(self, item, default=None):
        probs = {}
        max_prob = 0.0
        best = default
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max_prob:
                max_prob = probs[cat]
                best = cat
        
        for cat in probs:
            if cat == best:
                continue
            if probs[cat] * self.getthreshold(best) > probs[best]:
                return default
        return best

def create_directories():
    directories = [
        'data/training/promotional',
        'data/training/non-promotional',
        'data/testing/promotional',
        'data/testing/non-promotional'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def process_email_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    return content

def main():
    create_directories()
    cl = naivebayes(getwords)
    
    for category in ['promotional', 'non-promotional']:
        directory = f'data/training/{category}'
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory, filename)
                content = process_email_file(filepath)
                cl.train(content, category)
    
    results = []
    
    for category in ['promotional', 'non-promotional']:
        directory = f'data/testing/{category}'
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory, filename)
                content = process_email_file(filepath)
                prediction = cl.classify(content)
                results.append((category, prediction, filename))
    
    print("\nClassification Results:")
    print("-------------------------")
    print("Filename | Actual | Predicted")
    print("-------------------------")
    
    for actual, predicted, filename in results:
        print(f"{filename} | {actual} | {predicted}")
    
    # Calculate confusion matrix
    tp = sum(1 for actual, predicted, _ in results if actual == "promotional" and predicted == "promotional")
    fp = sum(1 for actual, predicted, _ in results if actual == "non-promotional" and predicted == "promotional")
    fn = sum(1 for actual, predicted, _ in results if actual == "promotional" and predicted == "non-promotional")
    tn = sum(1 for actual, predicted, _ in results if actual == "non-promotional" and predicted == "non-promotional")
    
    print("\nConfusion Matrix:")
    print(f"True Positives: {tp}  |  False Positives: {fp}")
    print(f"False Negatives: {fn} |  True Negatives: {tn}")
    
    accuracy = (tp + tn) / len(results)
    print(f"\nAccuracy: {accuracy:.2%}")

if __name__ == "__main__":
    main()
```

When the script is run, the output is as follows:

```
Ethan@DESKTOP-KDIRTV9 MINGW64 ~/Downloads/spr25-enova003/HW7 (main)
$ python classifyEmail.py 

Classification Results:
-------------------------
Filename | Actual | Predicted
-------------------------
1.txt | promotional | promotional
2.txt | promotional | promotional
3.txt | promotional | promotional
4.txt | promotional | promotional
5.txt | promotional | non-promotional
1.txt | non-promotional | non-promotional
2.txt | non-promotional | non-promotional
3.txt | non-promotional | non-promotional
4.txt | non-promotional | non-promotional
5.txt | non-promotional | non-promotional

Confusion Matrix:
True Positives: 4  |  False Positives: 0
False Negatives: 1 |  True Negatives: 5

Accuracy: 90.00%
```

# Q1 Answer
Q: What topic did you decide to classify on?

A:

For this assignment, I classified emails based on two categories: promotional and non-promotional. This classification was utilized to filter marketing emails from personal/work emails. For this assignment, promotional emails are any email that contains advertisements, special offers, newsletters, or discounts. Whereas, non-promotional emails are personal emails, relating to work, accounts, school, etc.

I created the dataset as described in the instructions. The training dataset consists of 20 .txt documents for promotional emails and 20 .txt files for non-promotional emails. Furthermore, the testing dataset consists of 5 .txt files for promotional emails and 5 .txt files for non-promotional emails. All .txt files are saved as plain text files that do not have HTML tags. The content in each .txt file is based on promotional and non-promotional emails that I have recieved. However, the content does not include any personal information; some of the email content is fiction, written to resemble a promotional or non-promotional email, in order to maintain my privacy. 

The entire dataset can be found in the `data` folder in this directory. 

# Q2 Answer

I implemented the Naive Bayes classifier using the code examples provided. The code that I utilized included the `getwords()` function, the `basic_classifier` class, and the `naivebayes` class. The `getwords()` function is used to extract words from emails. The `basic_classifier` class is used to store and calculate feature probabilities. The `naivebayes` class is a class that implements the Baye's theorem for classification. 

Classifiying the data involves training the dataset with each email. The classifier extracts words and updates the counts for each word in each category. After this, for each email in the training dataset, the classifier calculates the probability that the email belongs to each category and assigns it to the most likely category.

Below is the table to report the classification results for each email message in the testing dataset. The table includes what the classifier reported and the actual classification. 

Folder | Filename | Actual | Predicted | Correct?
|---------:|--------:|---------:|--------:|--------:|
testing/promotional | 1.txt | promotional | promotional | Yes
testing/promotional | 2.txt | promotional | promotional | Yes
testing/promotional | 3.txt | promotional | promotional | Yes
testing/promotional | 4.txt | promotional | promotional | Yes
testing/promotional | 5.txt | promotional | non-promotional | **No**
testing/non-promotional | 1.txt | non-promotional | non-promotional | Yes
testing/non-promotional | 2.txt | non-promotional | non-promotional | Yes
testing/non-promotional | 3.txt | non-promotional | non-promotional | Yes
testing/non-promotional | 4.txt | non-promotional | non-promotional | Yes
testing/non-promotional | 5.txt | non-promotional | non-promotional | Yes

Q: For those emails that the classifier got wrong, what factors might have caused the classifier to be incorrect? You will need to look at the text of the email to determine this.

A: The classifier incorrectly categorized `testing/promotional/5.txt`. The classifier labeled it as non-promotional, however, it was in fact a promotional email. The contents of the email is as follows:

```
New Restaurant Opening: Join us for 50% off your entire meal during our grand opening week! Make reservations online or call 555-234-5678. We can't wait to serve you!
```

One reason that the classifier may have incorrectly labeled this email are because the email contained fewer typical promotional words, like "sale", "discount", and "offer". Another reason may be because the email reads like a personal email due to the fact that it contains the phrase "we can't wait to serve you!". Overall, the classifier only looks at individual words without considering the overall structure of the email, and this is most likely the reason that the email was incorrectly classified. 

# Q3 Answer

Below is the confusion matrix:

|   | Actual: on-topic (promotional)  | Actual: off-topic (non-promotional)  |
|----|----|----|
| Predicted: on-topic (promotional) | 4 (TP)  | 0 (FP)  |
| Predicted: off-topic (non-promotional) | 1 (FN)  | 5 (TN)  |

The above matrix corresponds with the output of the script. Below is the outputted matrix from running the script:

```
Confusion Matrix:
True Positives: 4  |  False Positives: 0
False Negatives: 1 |  True Negatives: 5
```

Q: Based on the results in the confusion matrix, how well did the classifier perform?

A: Based on the results the classifier performed very well. The accuracy was 90% ((TP + TN)/Total = 9 / 10 = 90%). With an accuracy of 90%, the classifier performed quite well, especially considering the fact that the training dataset was small. 

Q: Would you prefer an email classifier to have more false positives or more false negatives? Why?

A: For an email classifier that identifies promotional emails, I would prefer to have more false positives than false negatives. The reason for this is because false negatives mean that promotional emails are incorrectly labeled as non-promotional emails. This would mean that a person's inbox would have much more promotional emails in it. However, I would prefer to only occasionally find promotional emails in my inbox, as my inbox would be less cluttered, therefore, I would prefer to have more false positives.  

# Q4 Answer (Extra Credit)
The accuracy for the scores of the classification was 90.00%. The formula that was used to compute this value was `accuracy = (tp + tn) / len(results)` where `tp` is the true-positive value obtained from the confusion matrix and `tn` was the true-negative value obtained from the confusion matrix. 

# References
* Document Filtering lecture slides, <https://docs.google.com/presentation/d/1OpfBDl2YEE7AONVeKUyHA-J7a1mRjncD7cen8F6BG1A/edit#slide=id.g7244591710_0_3>
* Class Colab Notebook, <https://github.com/odu-cs432-websci/public/blob/main/432_PCI_Ch06.ipynb>
* Programming Collective Intelligence Chapter 6 Code, <https://github.com/arthur-e/Programming-Collective-Intelligence/tree/master/chapter6>