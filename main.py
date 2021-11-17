import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests

# Analysis of Summer Olympics 1896 - 2012

# load a dataframe of countries and population details
# Assign the filename: country
country = "C://Users/patriciawilson/Downloads/dictionary.xlsx"

# Read the file into a DataFrame: country_details
dictionary = pd.ExcelFile(country)
country_details = dictionary.parse((0), skiprows=[0], names=['Country', 'Code', 'Population', 'GDP'])
# View the head of the DataFrame
print(country_details.head())
print(type(country_details))


# examine if there are blank rows
print(country_details.isna())
complete_country_details = country_details.fillna(0)
complete_country_details['GDP'].hist()
plt.show()


# load a dataframe of olympics data related to the countries in the previous dataframe
# Assign the filename: data
data = "C://Users/patriciawilson/Downloads/summer.xlsx"

# Read the file into a DataFrame: summer
summer = pd.ExcelFile(data)
summer_olympics = summer.parse((0), skiprows=[0], names=['Year', 'City', 'Sport', 'Discipline', 'Athlete', 'Code', 'Gender', 'Event', 'Medal'])

# View the head of the DataFrame
print(summer_olympics.head())
print(type(summer_olympics))

# subset of summer dataframe showing medals won by Ireland between 1896 - 2012
Ireland = summer_olympics[summer_olympics["Code"] == "IRL"]
print(Ireland.head())

# sum of number of each medal type won
Ireland_medals_by_amount = Ireland.groupby("Medal").sum()
print(Ireland_medals_by_amount)

# Create a bar plot of the number of medals won by type
Ireland_medals_by_amount.plot(kind="bar")

# Show the plot
plt.show()

# Do countries with greater GDP win more medals?
# join 2 dataframes based on country code
# set index of country_details to 'code'
country_details_ind = complete_country_details.set_index("Code")
# summer_olympics_ind = summer_olympics.set_index("Country")


data_with_gdp = country_details_ind.merge(summer_olympics, on='Code', how="left")

print(type(data_with_gdp))
print(data_with_gdp.head())

# data_with_gdp by gdp
# country_by_gdp = data_with_gdp.sort_values("GDP", ascending=True)
sns.scatterplot(x="Country", y="GDP", data=data_with_gdp, hue="Medal")
plt.xticks(rotation=90)
plt.show()

medals_per_country_discipline = []
# which countries win the most gold medals in each sport?
for code in summer_olympics.iterrows():
    for i in 'Discipline':
        i.count('Medal')
        medals_per_country_discipline.append('Code', 'Discipline', 'Medal')
















