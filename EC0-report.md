# EC 0.6 - Reports
### Ethan Novak
### CS 432, Spring 2025
### 1/25/2025

# Q1

*You may copy the question into your report, but make sure that you make it clear where the question ends and your answer begins.*

## Answer

The image below shows an intersection in a busy city.

![\label{fig:intersection}](City_Intersection.JPG)

*If you want to include code in your report, you can insert a screenshot (if it's legible), or you can copy/paste the code into a fenced code block.*

```python
#!/usr/local/bin/python3
# area-of-circle.py

import math

def calculate_area(radius):
    """Calculates the area of a circle given the radius."""
    return math.pi * radius ** 2

if __name__ == "__main__":
    radius = float(input("Enter the radius of the circle: "))
    area = calculate_area(radius)
    print(f"The area of the circle is: {area:.2f}")
```

The table below shows the first 4 weeks of our class schedule, as outlined in the syllabus.

|Week|Date|Topic|
|:---|:---|:---|
|1|Jan 11|Introduction to Web Science and Web Architecture|
|2|Jan 18|Introduction to Python|
|3|Jan 25|Measuring the Web|
|4|Feb 1|Searching the Web|

The table below shows an example confusion matrix (you'll see this term later) from <https://en.wikipedia.org/wiki/Confusion_matrix>.

| | |Actual||
|---|---|---|---|
|**Predicted**| |Cat|Dog|
| |Cat|5 (TP)|3 (FP)|
| |Dog|2 (FN)|3 (TN)|

*You must provide some discussion of every answer. Discuss how you arrived at the answer and the tools you used. Discuss the implications of your answer.*

# Q2

## Answer

# Q3

## Answer

# References

References:

* The Oracle of Bacon, <https://oracleofbacon.org/>
* Python Tutorial, <https://www.w3schools.com/python/>
* SCC Network Topology, <https://creately.com/diagram/example/itx423181/scc-network-topology>