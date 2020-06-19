import pandas as pd
import plotly.express as px

url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series' \
      '/time_series_covid19_deaths_global.csv '

df = pd.read_csv(url, delimiter=',', header='infer')
df_interest = df.loc[
    df['Country/Region'].isin(['United Kingdom', 'US', 'Italy', 'Brazil', 'India'])
    & df['Province/State'].isna()]
df_interest.rename(index=lambda x: df_interest.at[x, 'Country/Region'], inplace=True)
df1 = df_interest.transpose()
df1 = df1.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])
df1 = df1.loc[(df1 != 0).any(1)]
df1.index = pd.to_datetime(df1.index)
df1 = df1.diff()  # day on day changes

fig = px.line()

for i, n in enumerate(df1.columns):
    fig.add_scatter(x=df1.index, y=df1[df1.columns[i]], name=df1.columns[i])

fig.update_traces(mode='markers+lines')

fig.update_layout(
    title='Daily Deaths due to COVID-19',
    xaxis_title='Dates',
    yaxis_title='Number of Deaths',
    font=dict(size=25),
    template='plotly'  # "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
)

fig.update_xaxes(rangeslider_visible=True)

fig.show()

fig = px.bar(x=df1.index, y=df1[df1.columns[0]])
for i, n in enumerate(df1.columns):
    fig.add_bar(x=df1.index, y=df1[df1.columns[i]], name=df1.columns[i])
fig.update_layout(
    title='Daily Deaths due to COVID-19',
    xaxis_title='Dates',
    yaxis_title='Number of Deaths',
    font=dict(size=25),
    template='plotly'  # "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
)

fig.show()

df1 = df1.tail(1).transpose()
fig = px.pie(df1, values=str(df1.columns[0]), names=df1.index)
fig.update_traces(textposition='inside', textinfo='percent+label')
ddate = str(df1.columns[0])[:10]  # chop timestamp
fig.update_layout(
    title=f'Deaths on {ddate} due to COVID-19',
    xaxis_title='Dates',
    yaxis_title='Number of Deaths',
    font=dict(size=25),
    template='plotly'  # "plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
)

fig.show()
