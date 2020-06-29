# requests for fetching html of website
import requests

# Make the request to a url
r = requests.get('http://www.cleveland.com/metro/index.ssf/2017/12/case_western_reserve_university_president_barbara_snyders_base_salary_and_bonus_pay_tops_among_private_colleges_in_ohio.html')

# Create soup from content of request
c = r.content

from bs4 import BeautifulSoup

soup = BeautifulSoup(c)

# Find the element on the webpage
main_content = soup.find('div', attrs = {'class': 'entry-content'})
main_content


# Extract the relevant information
content = main_content.find('ul').text

import pprint
pprint.pprint(content)


import re

# Create a pattern to match names
name_pattern = re.compile(r'^([A-Z]{1}.+?)(?:,)', flags = re.M)
name_pattern.findall(content)


names = name_pattern.findall(content)

# Remind ourselves what our soup looks like
pprint.pprint(content)


# Make school patttern and examine results
school_pattern = re.compile(r'(?:,|,\s)([A-Z]{1}.*?)(?:\s\(|:|,)')
school_pattern.findall(content)


# Extract the schools
schools = school_pattern.findall(content)


# Pattern to match the salaries
salary_pattern = re.compile(r'\$.+')
salary_pattern.findall(content)

# Messy salary
salary = '$876,001'

# Exclude the $ and split the string on the comma
salary[1:].split(',')

# Same operation but now join the list with no space
''.join(salary[1:].split(','))


# Finally convert the string to a float
float(''.join(salary[1:].split(',')))

# Messy salaries
salaries = ['$876,001', '$543,903', '$2453,896']

# Convert salaries to numbers using the above procedure in a list comprehension
[int(''.join(s[1:].split(','))) for s in salaries]

# Extract all the salaries and convert to integers
salaries = salary_pattern.findall(content)

# List comprehension to convert strings to floats
salaries = [int(''.join(s[1:].split(','))) for s in salaries]

# Sanity check to make sure everything is correct!
len(names) == len(schools) == len(salaries)

salaries


import pandas as pd

# Put information into a dataframe
df = pd.DataFrame({'salary': salaries,
                   'President': names,
                   'College': schools})

# Append information
df.loc[17, :] = ['CWRU', 'Barbara Synder', 1154000]

# Sort the values by highest to lowest salary
df = df.sort_values('salary', ascending=False).reset_index().drop(columns='index')

df.plot(kind='barh', x = 'President', y = 'salary');

import matplotlib.pyplot as plt
%matplotlib inline

# Pick a style
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 16

import seaborn as sns

# Sort the values by highest to lowest salary
df = df.sort_values('salary', ascending=False).reset_index()

# Shorten this one name for plotting
df.ix[df['College'] == 'University of Mount Union', 'College'] = 'Mount Union'

# Create the basic figure
plt.figure(figsize=(10, 8))
sns.barplot(x = 'salary', y = 'President', data = df,
            color = 'tomato', edgecolor = 'k', linewidth = 2)

# Add text showing values and colleges
for i, row in df.iterrows():
  plt.text(x = row['salary'] + 6000, y = i + 0.15, s = '$%d' % (round(row['salary'] / 1000) * 1000))
  plt.text(x = 5000, y = i + 0.15, s = row['College'], size = 14)

# Labels are a must!
plt.xticks(size = 16); plt.yticks(size = 18)
plt.xlabel('Total Compensation ($)')
plt.ylabel('President')
plt.title('2015 Compensation of Private Ohio College Presidents');


# Calculate value of 5 minutes of your presidents time
five_minutes_fraction = 5 / (2000 * 60)
total_df = pd.DataFrame(df.groupby('College')['salary'].sum())
total_df['five_minutes_cost'] = round(total_df['salary'] * five_minutes_fraction)
total_df = total_df.sort_values('five_minutes_cost', ascending = False).reset_index()

total_df



# Text for caption
txt = 'Calculated from 2015 Total Compensation assuming 2000 hrs worked/year. Source: Chronical of Higher Education'

# Create the basic barplot
plt.figure(figsize=(10, 8))
sns.barplot(x = 'five_minutes_cost', y = 'College', data = total_df,
            color = 'red', edgecolor = 'k', linewidth = 2)

# Add the text with the value
for i, row in total_df.iterrows():
  plt.text(x = row['five_minutes_cost'] + 0.5, y = i + 0.15,
           s = '$%d' % (row['five_minutes_cost']), size = 18)

# Add the caption
plt.text(x = -5, y = 20, s = txt, size = 14)

# Add the labels
plt.xticks(size = 16); plt.yticks(size = 18)
plt.xlabel('Value ($)')
plt.ylabel('')
plt.title("Value of Five Minutes of Your President's Time");






