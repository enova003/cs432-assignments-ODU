import os
import json
import datetime
import matplotlib.pyplot as plt

json_folder_path = 'timemaps'

if not os.path.exists(json_folder_path):
    print(f"Error: The folder '{json_folder_path}' does not exist.")
else:
    uri_data = []

    current_date = datetime.datetime.now(datetime.timezone.utc)

    for filename in os.listdir(json_folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(json_folder_path, filename)

            try:
                with open(file_path, 'r') as f:
                    if f.readable():
                        f.seek(0) 
                        data = json.load(f)
                    else:
                        print(f"Skipping empty file: {filename}")
                        continue

                if 'mementos' in data and 'list' in data['mementos'] and len(data['mementos']['list']) > 0:
                    uri_r = data['original_uri']

                    mementos = data['mementos']['list']
                    earliest_memento = min(mementos, key=lambda x: x['datetime'])
                    earliest_memento_datetime = datetime.datetime.strptime(earliest_memento['datetime'], '%Y-%m-%dT%H:%M:%SZ')

                    earliest_memento_datetime = earliest_memento_datetime.replace(tzinfo=datetime.timezone.utc)

                    age_in_days = (current_date - earliest_memento_datetime).days

                    num_mementos = len(mementos)

                    uri_data.append((age_in_days, num_mementos))

            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON file: {filename} ({str(e)})")
            except Exception as e:
                print(f"An error occurred with file {filename}: {str(e)}")

    if uri_data:
        ages = [data[0] for data in uri_data]
        num_mementos = [data[1] for data in uri_data]

        plt.figure(figsize=(10, 6))
        plt.scatter(ages, num_mementos, alpha=0.6)
        plt.title('Scatterplot of URI-R Age vs Number of Mementos')
        plt.xlabel('Age in Days')
        plt.ylabel('Number of Mementos')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    else:
        print("No valid data to plot.")
