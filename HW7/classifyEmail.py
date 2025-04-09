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