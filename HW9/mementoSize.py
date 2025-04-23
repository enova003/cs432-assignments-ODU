import os
import json
from collections import defaultdict

timemaps_directory = 'timemaps'

memento_groups = defaultdict(int)

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
overOneThousand = 0

for memento_count, file_count in memento_groups.items():
    if 0 < memento_count <= 10:
        zeroToTen += file_count
    elif 10 < memento_count <= 25:
        tenToTwentyFive += file_count
    elif 25 < memento_count <= 50:
        twentyFiveToFifty += file_count
    elif 50 < memento_count <= 75:
        fiftyToSeventyFive += file_count
    elif 75 < memento_count <= 100:
        seventyFiveToHundred += file_count
    elif 100 < memento_count <= 150:
        hundredToOneFifty += file_count
    elif 150 < memento_count <= 200:
        oneFiftyToTwoHundred += file_count
    elif 200 < memento_count <= 250:
        twoHundredToTwoFifty += file_count
    elif 250 < memento_count <= 300:
        twoFiftyToThreeHundred += file_count
    elif 300 < memento_count <= 400:
        threeHundredToFourHundred += file_count
    elif 400 < memento_count <= 500:
        fourHundredToFiveHundred += file_count
    elif 500 < memento_count <= 600:
        fiveHundredToSixHundred += file_count
    elif 600 < memento_count <= 700:
        sixHundredToSevenHundred += file_count
    elif 700 < memento_count <= 800:
        sevenHundredToEightHundred += file_count
    elif 800 < memento_count <= 900:
        eightHundredToNineHundred += file_count
    elif 900 < memento_count <= 1000:
        nineHundredToTenHundred += file_count
    elif memento_count > 1000:
        overOneThousand += file_count
        print(f"{filename} has {memento_count} mementos")

print("\nMemento groups:")
print(f"1-10: {zeroToTen}")
print(f"11-25: {tenToTwentyFive}")
print(f"26-50: {twentyFiveToFifty}")
print(f"51-75: {fiftyToSeventyFive}")
print(f"76-100: {seventyFiveToHundred}")
print(f"101-150: {hundredToOneFifty}")
print(f"151-200: {oneFiftyToTwoHundred}")
print(f"201-250: {twoHundredToTwoFifty}")
print(f"251-300: {twoFiftyToThreeHundred}")
print(f"301-400: {threeHundredToFourHundred}")
print(f"401-500: {fourHundredToFiveHundred}")
print(f"501-600: {fiveHundredToSixHundred}")
print(f"601-700: {sixHundredToSevenHundred}")
print(f"701-800: {sevenHundredToEightHundred}")
print(f"801-900: {eightHundredToNineHundred}")
print(f"901-1000: {nineHundredToTenHundred}")
print(f"Over 1000: {overOneThousand}")