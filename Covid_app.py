import streamlit as st 
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

st.title('COVID 19 DATA ANALYSIS')
st.markdown('By Rajiv')

 
data= 'https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'
df = pd.read_csv(data)
 
df['Active cases'] = df['Confirmed'] - (df['Recovered'] + df['Deaths'])
df['Daily cases'] = df.groupby(['Country'])['Confirmed'].diff().fillna(df['Confirmed'])
 
df['Date'] = pd.to_datetime(df['Date'])
 
a = df.groupby(['Country'])['Confirmed'].max().sort_values(ascending = False).head()
 
highest = None
 
 
for i in a.index:
  if highest is None:
    highest =  df[ df['Country']== i ]
  else:
    x = df[ df['Country']== i ]
    highest= highest.merge(x,how='outer')
 
b = highest.groupby(['Country'])['Deaths'].max()
c = highest.groupby(['Country'])['Recovered'].max()
maxi = pd.DataFrame({'Total cases': a, 'Total Recovered':c,'Total deaths': b })
maxi.sort_values(by = ['Total cases'],inplace = True, ascending = False)

idx = df.groupby(['Country'])['Confirmed'].transform(max) == df['Confirmed']
Latest =df[idx]
Latest= Latest.drop_duplicates(subset = 'Confirmed', keep ='last')
Latest.reset_index(inplace = True)
Latest['Date']= Latest['Date'].dt.date


if st.sidebar.button(' top 5 Wrost affected countries'):
  maxi
  fig,ax = plt.subplots()
  maxi.plot.bar(figsize = (16,7), fontsize = 21, color = {'Total cases':'#FFA500','Total Recovered':'g','Total deaths':'r'} ,ax=ax)
  plt.title( 'TOP 5 WROST AFFECTED COUNTRIES\n(By total cases)',fontsize = 30)
  plt.ylabel('No. of people',fontsize = 21)
  plt.xlabel('Countries',fontsize = 21)
  st.pyplot(fig)


if st.sidebar.button('Most Active cases'):
  fig,ax = plt.subplots()
  active = df.groupby(['Country'])['Active cases'].max().sort_values(ascending = False).head(6)
  active
  active.plot(figsize =(12,6), kind = 'bar',fontsize = 18,color = {'r','b','y','#FFA500','g'},ax=ax)
  plt.title( 'Most Active cases',fontsize = 30)
  plt.ylabel('No. of people (in millions)',fontsize = 21)
  plt.xlabel('Countries',fontsize = 21)
  st.pyplot(fig)

if st.sidebar.button('peak of various countries'):
  idx = df.groupby(['Country'])['Daily cases'].transform(max) == df['Daily cases']
  Max_daily_cases = df[idx]
  M = Max_daily_cases.sort_values(by = ['Daily cases'],ascending =False).head(8)
  fig,ax = plt.subplots()
  sns.scatterplot(x = 'Date', y = 'Daily cases', hue = 'Country', data = M, s = 190,ax=ax)
  sns.set(rc={'figure.figsize':(18,5)})
  sns.set_context('paper')
  plt.title('Peak of various countries',fontsize = 28)
  plt.ylabel('Daily Cases',fontsize = 21)
  plt.xlabel('Date',fontsize = 21)
  st.pyplot(fig)

if st.sidebar.button('Highest recovery rate'):
  Latest = Latest[Latest['Confirmed'] > 1000]
  Latest['Recovery_rate'] = Latest['Recovered']/Latest['Confirmed']*100
  high_recover = Latest.sort_values(by = 'Recovery_rate',ascending = False).head(4)
  high_recover.reset_index()
  high_recover = high_recover[['Date','Country','Confirmed','Recovered','Recovery_rate']]
  high_recover
  fig,ax = plt.subplots()
  high_recover.plot.barh(y = 'Recovery_rate', x = 'Country', color = {'#ee2536','#009E60','y','#6ab2e7'},legend = None,fontsize = 16,ax=ax)
  plt.ylabel('Countries',fontsize = 19)
  plt.xlabel('Recovery Percent',fontsize = 19)
  plt.title('Countries with highest recovery rate',fontsize = 28)
  plt.suptitle('\n\n(Minimum 1000 cases)',fontsize = 18)
  st.pyplot(fig)


if st.sidebar.checkbox('Search country data'):
  y = st.selectbox('Select country:',Latest['Country'])
  Country = y
  if st.button('Go'):
    
    Latest_date =Latest.loc[Latest['Country']==y]['Date'].values
    confirmed =  Latest.loc[Latest['Country']==y]['Confirmed'].values
    recovered =Latest.loc[Latest['Country']==y]['Recovered'].values
    deaths =Latest.loc[Latest['Country']==y]['Deaths'].values
    act_case =Latest.loc[Latest['Country']==y]['Active cases'].values
    daily =Latest.loc[Latest['Country']==y]['Daily cases'].values
    st.write('Country = ',y,'  \n''Latest date = ', Latest_date[0],'  \n''Total Cases = ',+confirmed[0],'  \n''Total Recovered =',+recovered[0],'  \n''Total Deaths = ',+deaths[0],'  \n''Active cases = ',+act_case[0],'  \n''New cases = ',+daily[0])

    fig_dims = (18,6)
    fig, ax = plt.subplots(figsize=fig_dims)
    sns.lineplot(x = 'Date', y = 'Daily cases', hue = 'Country',data = df[(df.Country == y)],ax=ax)
    sns.set_context('talk')
    plt.title('Daily cases Timeline  ', fontsize = 24)
    st.pyplot(fig)
