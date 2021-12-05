# Analysis of Medals won in Summer Olympics 1896 - 2012

# Patricia Wilson, UCD Professional Academy - Introduction to Data Analytics

# Data Import
# Data Preparation
# 1. Do countries with greater GDP win more medals?
# 2. Count Gold, silver, Bronze medals by Gender
# 3. Who are the top 10 most successful athletes at the summer olympics from 1896 -2012?
# 4. How many Gold, Silver and Bronze Medals have been won by Ireland between 1896 - 2012?
# 5. In which years did Irish Olympians win medals?
# 6.  How many medals were won by Ireland in the 2020 Tokyo Olympics?
# Define a custom function to get min, max and average populations from the complete country details dataframe and print the results

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Import required modules

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import pyplot
import seaborn as sns
import numpy as np
from collections import Counter
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Data Import
# load excel files of countries and population details and convert to dataframe
# Assign the filename: country

with pd.ExcelFile("https://raw.githubusercontent.com/patriciawilson2021/UCDPA_Patricia-Wilson/main/dictionary.xlsx") as reader:
    country_details = pd.read_excel(reader, sheet_name='dictionary')

# Show details of the country_details dataframe
print(country_details.head())
print(type(country_details))
print(country_details.shape)

# load a dataframe of olympics data and convert to dataframe

with pd.ExcelFile("https://raw.githubusercontent.com/patriciawilson2021/UCDPA_Patricia-Wilson/main/summer.xlsx") as reader:
    summer_olympics = pd.read_excel(reader, sheet_name='summer')

# View the head of the DataFrame
print(summer_olympics.head())
print(type(summer_olympics))
print(summer_olympics.shape)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Data Preparation
# check the dataframes for empty values
# examine if there are blank rows
print(country_details.isnull())

# Fill any blanks in country_details with '0' and create new dataframe: Complete_country_details
complete_country_details = country_details.fillna(0)
# check complete country details to make sure that no nulls remain
print(complete_country_details.isnull())

# Check summer olympics for null values
print(summer_olympics.isna())


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 1. Do countries with greater GDP win more medals?

# join 2 dataframes based on country code
# set index of country_details to 'code'
country_details_ind = complete_country_details.set_index("Code")

# merge country details and summer olympics dataframe to create a new dataframe called 'data with gdp'
data_with_gdp = country_details_ind.merge(summer_olympics, on='Code', how="left")

print(type(data_with_gdp))
print(data_with_gdp.head())

# use Seaborn scatterplot to visualise that data
gdp_plot = sns.scatterplot(x="Country", y="GDP", data=data_with_gdp, hue="Medal")
plt.xticks(rotation=90)
gdp_plot.set_title("Number of medals won per GDP")
gdp_plot.set(xlabel="Countries", ylabel="GDP Per Capita")
plt.show()

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 2. Count Gold, silver, Bronze medals by Gender

# create separate dictionaries for medals won by men and women.
men = dict()
women = dict()

# loop through summer olympics dataframe to populate dictionaries and count values of gold, silver & bronze medals.
summer_olympics_grp = summer_olympics.groupby(['Gender'])
for ge, me in summer_olympics_grp:
    if ge == 'Men':
        med = me.groupby(['Medal'])
        for k, l in med:
            men[k] = len(l)
    elif ge == 'Women':
        med = me.groupby(['Medal'])
        for k, l in med:
            women[k] = len(l)

#print resulting dictionaries
print(men)
print(women)

# plot the information on a grouped bar chart.
# I had trouble getting this to work properly so ended up needing help from
# https://stackoverflow.com/questions/45968359/plotting-two-dictionaries-in-one-bar-chart-with-matplotlib

X = np.arange(len(men))
ax = plt.subplot(111)
ax.bar(X, men.values(), width=0.2, color='lightsteelblue', align='center')
ax.bar(X-0.2, women.values(), width=0.2, color='pink', align='center')
ax.legend(('men', 'women'))
plt.xticks(X, men.keys())
plt.title("Medal Winners by Gender", fontsize=17)

# display grouped bar chart
plt.show()


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 3. Who are the top 10 most successful athletes at the summer olympics from 1896 -2012?

# extract athletes column from summer_olympics dataframe into a list
top10 = summer_olympics['Athlete'].to_list()
print(type(top10))

# count how many times each athlete appears in the list
count_top10 = pd.Series(top10).value_counts()
print(count_top10)

# create a list of the top 10 athletes only
top_10_list = count_top10[0:10]
print(top_10_list)

# create a word cloud visualisation of the top 10 athletes
data = summer_olympics['Athlete'].value_counts().to_dict()
top_10_dict = dict(Counter(data).most_common(10))
wc = WordCloud(background_color="blue").generate_from_frequencies(top_10_dict)
plt.imshow(wc)
plt.axis('off')

# display wordcloud
plt.show()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 4. How many Gold, Silver and Bronze Medals have been won by Ireland between 1896 - 2012?

# Set index of dataframe to country code and use .loc to extract all rows where code is 'IRL'
Ireland_srt = summer_olympics.set_index("Code")
Ireland = Ireland_srt.loc["IRL"]
print(Ireland.head())

# sum of number of each medal type won.  This code returns a series.
Ireland_medals_by_amount = Ireland.groupby("Medal")
medal_totals = Ireland.value_counts("Medal")

print(type(medal_totals))
print(medal_totals)

# Create a bar plot of the number of medals won by type
medal_bar_chart = medal_totals.plot(kind="bar", color=['darkgoldenrod', 'gold', 'silver'])

# set axis labels
medal_bar_chart.set_xlabel("Medals")
medal_bar_chart.set_ylabel("Number of medals won")
medal_bar_chart.set_title("Gold, Silver and Bronze medals won by Ireland 1896 - 2012")

# Show the plot
plt.show()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 5. In which years did Irish Olympians win medals?

# create dictionary of years in which medals were won by ireland
year_medal = dict()
summer_olympics_grp = summer_olympics.groupby(['Code'])
for co, yr in summer_olympics_grp:
    if co == 'IRL':
        Ire = yr.groupby(['Year'])
        for k, l in Ire:
            year_medal[k] = len(l)
print(year_medal)

# convert dictionary to dataframe for visualisation
data_items = year_medal.items()
data_list = list(data_items)
medals = pd.DataFrame(data_list)
medals.columns = ['Year', 'Total']
print(medals)

# check type of items in list
print(medals.columns.dtype)

# convert year column to numeric to allow it to be used as x axis
medals['Year'] = pd.to_numeric(medals['Year'])

# create medal_plot
medal_plot = medals.plot(x="Year", y="Total", kind="line", marker = 'o', color="green")
medal_plot.set_xlabel("Years medals were won")
medal_plot.set_ylabel("Number of medals won")
medal_plot.set_title("Years in which Ireland won Olympic medals")

# set x axis to show all years from first year in which Ireland won medals to the last.
# set x axis to show all years in steps of 4 (as olympic games occur every 4 years)
medal_plot.set_xticks((np.arange(min(medals['Year']), max(medals['Year'])+1, 4.0)))
medal_plot.tick_params(axis='x', labelrotation=45)

# add grid to make it easier to match x and y values
plt.grid()
# show plot
plt.show()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6. How many medals were won by Ireland in the 2020 Tokyo Olympics?
# use beautifulsoup to scrape a table from Wikipedia
# Got help with this part of the project from the following site https://stackoverflow.com/questions/59054480/assertionerror-5-columns-passed-passed-data-had-1-columns

url = 'https://en.wikipedia.org/wiki/Ireland_at_the_2020_Summer_Olympics'
website_url = requests.get(url)
soup = BeautifulSoup(website_url.text, features="lxml")
table = soup.find_all('table')[2]
table_rows = table.find_all('tr')
res = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text.strip() for tr in td if tr.text.strip()]
    if row:
        res.append(row)

tokyo = pd.DataFrame(res, columns=["Sport", "Gold", "Silver", "Bronze", "Total"])
print(tokyo)

# check data types of columns in tokyo dataframe
print(tokyo.dtypes)

# all columns are displaying as objects so need to change these to numerical values to be able to create visualisations
tokyo['Gold'] = pd.to_numeric(tokyo['Gold'])
tokyo['Silver'] = pd.to_numeric(tokyo['Silver'])
tokyo['Bronze'] = pd.to_numeric(tokyo['Bronze'])
tokyo['Total'] = pd.to_numeric(tokyo['Total'])

# print types of columns again to see if type has changed
print(tokyo.dtypes)

# create visualisation to show number of medals won in each sport by Ireland in Tokyo 2020
ax = sns.barplot(x='Sport', y='Total', data=tokyo)
ax.bar_label(ax.containers[0])
ax.set_title("Medals won by Ireland in Tokyo 2020")

# show plot
plt.show()

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Define a custom function to get min, max and average populations from the complete country details dataframe and print the results
def population_details():

    max_pop = np.max(population)
    min_pop = np.min(population)
    avg_pop = np.mean(population)

    print("min of population : ", min_pop)
    print("max of population : ", max_pop)
    print("mean of population : ", avg_pop)


# create an array of the population column from the complete country details DataFrame
population = complete_country_details['Population'].to_numpy().astype(float)
print(type(population))

# get details from the Population array using the defined Population details function
population_details()
