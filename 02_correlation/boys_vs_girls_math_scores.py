import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt

df_math = pd.read_csv("math.csv")
#print(df_math.head())

covariance = df_math["Girls"].cov(df_math["Boys"])
correlation_pearson = df_math["Girls"].corr(df_math["Boys"])
#print(covariance)
print(f"Correlation pearson: {correlation_pearson:.3f}")
#strong positive correlation
correlation_spearman = df_math["Girls"].corr(df_math["Boys"], method = 'spearman')
print(f"Correlation spearman: {correlation_spearman:.3f}")

mean_boys = df_math["Boys"].mean()
mean_girls = df_math["Girls"].mean()
print(f"Mean boys: {mean_boys:.2f}\nMean girls: {mean_girls:.2f}")
#mean for all the years per region
df_mean_by_regions = df_math.groupby("Region")[['Girls','Boys']].mean()
print(df_mean_by_regions.round(2))
df_mean_by_regions.plot.bar(y = ['Girls', 'Boys'])
#plt.show()

#un-weighted average representing the average country
df_mean_by_regions_per_year = df_math.groupby(['Region', 'Year'])[['Girls','Boys']].mean().reset_index()
europe = df_mean_by_regions_per_year[df_mean_by_regions_per_year['Region'] == 'Europe']
print(europe)
ax_unweighted = europe.plot(x='Year', y = ['Girls', 'Boys'], title = 'Unweighted average in Europe')
ax_unweighted.set_xticks(europe['Year'])
#plt.show()

def weighted_average(dataframe, value, weight):
    val = dataframe[value]
    wt = dataframe[weight]
    return (val * wt).sum() / wt.sum()
#weighted average representing the average student
europe_weighted_average = df_math[df_math['Region'] == 'Europe'].groupby('Year').apply(lambda group: pd.Series({
    'Girls':weighted_average(group, 'Girls', 'Population'),
    'Boys':weighted_average(group, 'Boys', 'Population')
}))
#print("Europe weighted average")
#print(europe_weighted_average)
europe_weighted_average= europe_weighted_average.reset_index()
ax_europe = europe_weighted_average.plot(x='Year', y = ['Girls', 'Boys'], title = 'Weighted average in Europe')
ax_europe.set_xticks(europe_weighted_average['Year'])

plt.figure()
#weighted average of multiple regions
regions_weighted_average = df_math[df_math['Region'].isin(['Europe', 'Asia'])].groupby(['Region', 'Year']).apply(lambda group: pd.Series({
    'Girls':weighted_average(group, 'Girls', 'Population'),
    'Boys':weighted_average(group, 'Boys', 'Population')
}))
regions_weighted_average = regions_weighted_average.reset_index()

for region in ["Europe", "Asia"]:
    tmp = regions_weighted_average[regions_weighted_average["Region"] == region]
    plt.plot(tmp["Year"], tmp["Girls"], marker="o", label=f"{region} - Girls")
    plt.plot(tmp["Year"], tmp["Boys"],  marker="o", label=f"{region} - Boys")

plt.xticks(sorted(regions_weighted_average["Year"].unique()))
plt.xlabel("Year")
plt.ylabel("Score")
plt.title("Weighted average maths performance – Europe and Asia")
plt.legend()
plt.show()




