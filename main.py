from bs4 import BeautifulSoup
# import requests
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
import requests
# import io

# scrape table from wikipedia page and import to list showing covid deaths from jan - nov 2021 across all countries
wiki_url = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_by_country_and_territory#Europe'
table_id = "thetable"

response = requests.get(wiki_url)
soup = BeautifulSoup(response.text, 'html.parser')

covid_table = soup.find('table', attrs={'id': table_id})
deaths = pd.read_html(str(covid_table))

print(deaths)
print(type(deaths))

# ---------------------------------------------------------------------------------------------------------------------
# Analysis of Summer Olympics 1896 - 2012

# load a dataframe of countries and population details
# Assign the filename: country
country = "C://Users/patriciawilson/Downloads/dictionary.csv"

# Read the file into a DataFrame: dictionary
dictionary = pd.read_csv(country)

# View the head of the DataFrame
print(dictionary.head())
print(type(dictionary))
# load a dataframe of olympics data related to the countries in the previous dataframe
# Assign the filename: data
data = "C://Users/patriciawilson/Downloads/summer.xlsx"

# Read the file into a DataFrame: summer
summer = pd.excelfile(data)
summer_olympics = summer.parse((0), skiprows=[0], names=['Year', 'City', 'Sport', 'Discipline', 'Athlete', 'Country', 'Gender', 'Event', 'Medal'])

# View the head of the DataFrame
print(summer_olympics.head())
print(type(summer_olympics))

# subset of summer dataframe showing medals won by Ireland between 1896 - 2012
Ireland = summer_olympics[summer_olympics["Country"] == "IRL"]
print(Ireland.head())

# sum of number of each medal type won
Ireland_medals_by_amount = Ireland.groupby("Medals")["number_won"].sum()

# Create a bar plot of the number of medals won by type
Ireland_medals_by_amount.plot(kind="bar")

# Show the plot
plt.show()

# Do countries with greater GDP win more medals?
















