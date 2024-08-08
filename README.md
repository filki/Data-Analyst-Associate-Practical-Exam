
# Data Analyst Associate Practical Exam Submission



## Task 1

### Data Loading and Initial Inspection

We loaded the dataset `food_claims_2212.csv` and performed an initial inspection.

- **First Rows and Shape**: The dataset contains 2000 rows and 8 columns.
- **Information and Missing Values**: We observed missing values in `amount_paid` (36 missing) and `linked_cases` (26 missing).
- **Aggregated Statistics**: General statistics were computed.
- **Unique Values**: Unique values were determined for further investigation.
- **Non-standardized Values**: Some non-standardized values were detected and addressed.

### Data Cleaning

- **Missing Values**: 
  - `amount_paid`: Missing values replaced with the median.
  - `linked_cases`: Missing values replaced with `False`.
- **Standardization**: 
  - Trimmed and standardized the `cause` column.
  - Replaced non-standard values like 'vegetables' with 'vegetable'.

### Summary of Cleaned Data

The dataset after cleaning still contains 2000 rows and 8 columns. Here are the specific actions taken:

- **claim_id**: 2000 unique values, as expected.
- **time_to_close**: Positive integer values, as expected.
- **claim_amount**: Continuous, currency of Brazil, rounded to 2 decimal places.
- **amount_paid**: Continuous, missing values replaced with median.
- **location**: Nominal, valid locations.
- **individuals_on_claim**: Discrete, minimum 1 person.
- **linked_cases**: Nominal, missing values replaced with `False`.
- **cause**: Nominal, values standardized to 'vegetable', 'meat', or 'fish'.

### Code:
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, skew

df = pd.read_csv('food_claims_2212.csv')
df.head()
df.shape
df.info()
df.describe()
df['cause'].unique()

df['amount_paid'] = df['amount_paid'].fillna(df['amount_paid'].median())
df['linked_cases'] = df['linked_cases'].fillna(False)
df['cause'] = df['cause'].str.strip()
df['cause'] = df['cause'].replace(['vegetables'], 'vegetable')
df['cause'].unique()
```

## Task 2

### Analysis of Location

- **Most Frequent Location**: Recife has the highest number of observations.
- **Distribution of Observations**: The observations are not balanced across categories. Recife and Sao Luis have more claims, while Natal and Fortaleza are fairly balanced.

### Code:
```python
plt.subplots(figsize=(20, 15))
count = df["location"].value_counts(ascending=False)
df_plat = df.filter(["location"], axis=1)
df_plat['count'] = 1

grouped_plat_genre = df_plat.groupby("location", as_index=False, sort=False).sum()
grouped_plat_genre = grouped_plat_genre.sort_values('count', ascending=False)
sns.barplot(data=grouped_plat_genre, x="count", y="location")
plt.title("Claim per location", fontsize=17)
```

## Task 3

### Distribution Analysis of `time_to_close`

- **Distribution Shape**: The distribution of `time_to_close` resembles a normal distribution with some outliers.
- **Kurtosis and Skewness**: 
  - Positive kurtosis indicates many outliers.
  - Positive skewness indicates right-skewed distribution.

### Code:
```python
sns.histplot(data=df, x="time_to_close").set(title='Distribution of time_to_close')
print(kurtosis(df['time_to_close'], fisher=False))
print(skew(df['time_to_close']))
```

## Task 4

### Correlation Analysis

- **Correlation Heatmap**: After converting `location` to categorical, we observed very small correlations, indicating no significant relationship between `time_to_close` and `location`.

### Code:
```python
df_with_category = df.copy()
df_with_category['location'] = df_with_category['location'].astype('category').cat.codes

plt.subplots(figsize=(20, 15))
sns.heatmap(df_with_category.corr(), annot=True, robust=True).set(title='Correlation Heatmap')
```
