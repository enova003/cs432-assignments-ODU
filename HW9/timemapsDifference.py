import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('ggplot')
sns.set_style("whitegrid")

hw3_data = {
    '1-10': 241,
    '11-25': 57,
    '26-50': 63,
    '51-75': 53,
    '76-100': 43,
    '101-150': 56,
    '151-200': 24,
    '201-250': 11,
    '251-300': 12,
    '301-400': 14,
    '401-500': 3,
    '501-600': 0,
    '601-700': 1,
    '701-800': 0,
    '801-900': 0,
    '901-1000': 0,
    'Over 1000': 11
}

new_data = {
    '1-10': 230,
    '11-25': 63,
    '26-50': 65,
    '51-75': 46,
    '76-100': 48,
    '101-150': 60,
    '151-200': 23,
    '201-250': 13,
    '251-300': 12,
    '301-400': 13,
    '401-500': 3,
    '501-600': 1,
    '601-700': 1,
    '701-800': 0,
    '801-900': 0,
    '901-1000': 1,
    'Over 1000': 10
}

differences = {}
for key in hw3_data:
    differences[key] = new_data[key] - hw3_data[key]

diff_values = list(differences.values())

plt.figure(figsize=(10, 8))

sns.boxplot(y=diff_values, color='lightgray', width=0.3)

sns.stripplot(y=diff_values, color='black', size=5, alpha=0.7)

plt.ylabel('Growth in Mementos Since January (HW3)', fontsize=12)
plt.title('Changes in TimeMap Sizes', fontsize=14)

plt.axhline(y=0, color='black', linestyle='-', alpha=0.7)

plt.ylim(-35, 30)

plt.tight_layout()
plt.savefig('timemap_changes_boxplot.png', dpi=300)
plt.show()