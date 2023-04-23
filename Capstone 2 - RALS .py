#!/usr/bin/env python
# coding: utf-8

# # CAPSTONE 2

# ### RALS SUSTAINABLE COSMETIC COMPANY 

# RALS aims to provide eco-friendly and vegan makeup products. We plan to conduct market research using Google Trends and Sephora sales data to identify the most popular wellness products. Our goal is to create high-quality makeup that aligns with the growing demand for environmentally conscious and cruelty-free options. We believe that RALS can make a significant contribution to the beauty industry by offering sustainable makeup alternatives.

# #### 1. SEPHORA'S SALES DATA SET ANALYSIS 

# In[1]:


import pandas as pd 
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objects import Layout
import plotly.offline as pyo 
pyo.init_notebook_mode() ## ensures that the plotly graphics convert to HTML
from plotly.validators.scatter.marker import SymbolValidator
from pytrends.request import TrendReq


# In[2]:


products = pd.read_csv('skincare_df.csv')
products.columns


# In[3]:


#Dropping columns 
products = products.drop(columns=['Unnamed: 0']).drop_duplicates()


# In[4]:


#Changing name of the columns 
# clean up column names
products= products.rename(columns={'category_Anti-Aging' : 'Anti_Aging',
                                 'category_BB_&_CC_Cream': 'BB_&_CC_Cream', 
                                 'category_Bath_&_Shower' : 'Bath_&_Shower',
                                 'category_Beauty_Supplements':'Beauty_Supplements', 
                                 'category_Blemish_&_Acne_Treatments':'Blemish_&_Acne_Treatments',
                                 'category_Blotting_Papers': 'Blotting_Papers', 
                                 'category_Body_Lotions_&_Body_Oils': 'Body_Lotions_&_Body_Oils',
                                 'category_Cellulite_&_Stretch_Marks': 'Cellulite_&_Stretch_Marks',
                                 'category_Decollete_&_Neck_Creams': 'Decollete_&_Neck_Creams', 
                                 'category_Exfoliators' : 'Exfoliators',
                                 'category_Eye_Creams_&_Treatments':'Eye_Creams_&_Treatments',
                                 'category_Eye_Masks':'Eye_Masks',
                                 'category_Face_Masks':'Face_Masks', 
                                 'category_Face_Oils':'Face_Oils',
                                 'category_Face_Primer':'Face_Primer',
                                 'category_Face_Serums':'Face_Serums',
                                 'category_Face_Sunscreen':'Face_Sunscreen',
                                 'category_Face_Wash_&_Cleansers':'Wash_&_Cleansers', 
                                 'category_Facial_Peels':'Facial_Peels',
                                 'category_Foundation':'Foundation', 
                                 'category_Hair_Oil':'Hair_Oil', 
                                 'category_Highlighter':'Highlighter',
                                 'category_Holistic_Wellness':'Holistic_Wellness', 
                                 'category_Mini_Size':'Mini_Size',
                                 'category_Mists_&_Essences':'Mists_&_Essences', 
                                 'category_Moisturizer_&_Treatments':'Moisturizer_&_Treatments',
                                 'category_Moisturizers': 'Moisturizers', 
                                 'category_Night_Creams':'Night_Creams',
                                 'category_Setting_Spray_&_Powder':'Setting_Spray_&_Powder', 
                                 'category_Sheet_Masks':'Sheet_Masks',
                                 'category_Skincare':'Skincare', 
                                 'category_Tinted_Moisturizer':'Tinted_Moisturizer', 
                                 'category_Toners':'Toners',
                                 'category_Tools':'Tools', 
                                 'category_Value_&_Gift_Sets':'Value_&_Gift_Sets'})


# In[5]:


products.head()


# In[6]:


products.tail()


# In[7]:


#checking the shape of our dataset
products.shape


# In[8]:


#cheching the type of data in each column
products.info()


# In[9]:


#checking for missing values
products.isna().sum()


# ### Visualization of the dataset

# In[10]:


# colors
tan='#bc6d4c'
burgundy='#7e0f12'
red='#b71a3b'
forest='#6a7045'
green='#313c33'
colors_list= [tan,burgundy,red,forest,green]


# In[11]:


#Creating a graph with all the sephora products and brands, the scale next to it show how many 'loves' they have
#the more they have the more people love them and can be an inspiration for RALS

title = """
Sephora brands and products
"""
fig = px.treemap(products, 
                 path=[px.Constant('Skincare Brands'),'brand','name'], 
                 values='n_of_reviews',
                 color='n_of_loves',
                 hover_data=['n_of_reviews'], title=title)

fig.update_layout(
    font_family="Courier New",
    font_color=green,
    title_font_family="Courier New",
    title_font_color=green,
    legend_title_text='Number of Saves',
    legend=dict(title_font_color=green,title_text='Number of Saves'),
    title={'text': title,
           'x': .12,
           'xanchor': 'left',
           'yanchor': 'top',
           'font_size':25},
    width=1300,
    height=600,
    font_size=15,
)
fig.show()


# ### Most purchased brands at Sephora 

#     These are the 5 most purchased and saved (hearted on the Sephora website) brands by sheer volume. 
#     I am planning on using this data by seeing which brands are more likely to attract more customers.

# In[12]:


brands = products.groupby('brand').sum().reset_index()[['brand', 'n_of_reviews','n_of_loves']]
most_purchased=brands.sort_values(by=['n_of_reviews'], ascending=False)[:10]
most_desired=brands.sort_values(by=['n_of_loves'], ascending=False)[:10]
both_most_purchased_and_desired= pd.merge(most_purchased, most_desired[['brand']], how='inner', on=['brand'])
both_most_purchased_and_desired.set_index('brand')


# ### Visualizaiton of the most purchased brands

# In[13]:


layout = Layout(plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'showgrid': False},
                yaxis={'showgrid':False},
                paper_bgcolor='rgba(0,0,0,0)')


# In[14]:


colors = [tan,] * 5
colors[0] = red

title = """
Most <b>Purchased</b> and <b>Desired</b> Brands by Total Volume
"""

fig = go.Figure(layout=layout,data=[go.Bar(x=both_most_purchased_and_desired.brand,
                                           y=both_most_purchased_and_desired['n_of_reviews'],
                                           marker_color=colors,
                                           name="Reviews",
                                           hovertemplate = '<extra></extra>' + 'Purchases: %{y}')])

fig.add_trace(go.Bar(x=both_most_purchased_and_desired.brand, 
                     y=both_most_purchased_and_desired['n_of_loves'],
                     name='Hearts',
                     marker_color=colors,
                     hovertemplate = '<extra></extra>' + 'Saves: %{y}'))

fig.update_layout(barmode='stack', 
                  xaxis_title="Brand", 
                  yaxis_title="Number of Reviews and Loves",
                  xaxis={'categoryorder':'total descending','showgrid': False}, 
                  yaxis={'showgrid': False},
                  showlegend=False,
                  paper_bgcolor=green,
                  hoverlabel={
                      'bgcolor': 'white',
                      'font_family':'Courier New'},
                  title={'text': title,
                         'x': .23,
                         'xanchor': 'left',
                         'yanchor': 'top'}
                 )

fig.update_layout(
    hovermode='x',
    font_family="Courier New",
    width=1300,
    height=400,
    title_font_size=20,
    font_size=15,
    font_color='white',
    title_font_color='white',
)

fig.update_xaxes(showline=False)
#fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)


# Looking at the most purchased and desired brands can help us to understand why some brands can be more attractive than other. Different factors can play a role in this analysis: Brand image, Marketing, Price, Ingreients or simply popularity of the brand.
# In this case we can say that Clinique bases his marketing on how their proucts are doctor raccomandated and safe to use, is also a brand that has been there for many years so this helps the company resources on investing in it.
# Clinique is not entirely vegan, but they're fragrance-free, phthalate-free, and paraben-free.
# Clinique is committed to sustainability. Clinique's goal: by 2025, 75% of their packaging will be recyclable, refillable, reusable, recycled, or recoverable, and 100% of their secondary packaging will be Forest Stewardship Council.

# ### The Best products
# With no consideration for price, this list contains the highest rated items for each category. Meaning all products on this list are either (1) rated 5 stars more than 10 times or (2) the highest rated in their category with more 10 reviews. If a category does not have a product that fits these characteristics, it is excluded from this list.

# In[15]:


# selecting only category columns 
all_cat=products.columns.values
all_cat = np.delete(all_cat, np.argwhere( (all_cat == 'brand') | (all_cat=='name') | (all_cat=='price') | (all_cat=='n_of_reviews') | (all_cat=='n_of_loves') |
                                         (all_cat=='review_score') | (all_cat=='size') | (all_cat=='reviews_to_loves_ratio') | (all_cat=='return_on_reviews') |
                                         (all_cat== 'price_per_ounce') | (all_cat=='reviews_to_loves') ))
all_cat=all_cat.tolist()


# In[16]:


# collapsing all category columns into one 
category = pd.DataFrame(products[all_cat].idxmax(axis=1)).rename(columns={0:'Category'})
# join with orginal 
products2 = products.merge(category, on=products.index, how='inner').drop(columns=all_cat)
products2 = products2.sort_values('review_score', ascending=False)
products2['Category'] = products2['Category'].str.replace('_', ' ')


# In[17]:


# top review in each category 
reviews= products2.groupby("Category")['review_score'].max().values
reviews


# In[18]:


# filtering for products that met the either 5 stars or highest rated in their category
all_stars = products2[(products2['review_score'].isin(reviews)) & (products2['n_of_reviews']>10)].sort_values('review_score', ascending=False)
all_stars


# In[19]:


#To see how many products are there in total
len(all_stars)


# In[20]:


#To see which category is the most loved

category_counts = all_stars['Category'].value_counts()
print(category_counts)


# In[21]:


colors = colors_list
colors[0] = 'cadetblue'

title5 = """
     Top products from each Skincare category
"""
fig5= go.Figure()
# plot the box
fig5.add_trace(go.Scatter(mode='markers',
                          x=all_stars['price'], 
                          y=all_stars['review_score'], 
                          customdata=all_stars[['name','brand', 'Category']],
                          hoveron='points', # or fill
                          hovertemplate='<extra></extra>' + '<b>%{customdata[0]}</b>' +
                        '<br>      Brand : %{customdata[1]}' +
                        '<br>     Rating : %{y:.2f}'+
                        '<br>   Category : <b>%{customdata[2]}</b>'+
                        '<br>      Price : $%{x}',
                          hoverlabel= {'font_size':12},
                           opacity=.9,
                          marker=dict(size=25,
                                      color=all_stars['n_of_reviews'],
                                      colorscale=colors,
                                      #color= [tan,forest,'rebeccapurple',forest,forest,forest,forest,forest,'darkturquoise', tan, tan],
                                      line=dict(width=2, color="DarkSlateGrey"))
                         )
              )

# adding the diamonds =SymbolValidator().values[SymbolValidator().values.index('diamond')
fig5.add_trace(go.Scatter(mode='markers',
                          x=all_stars['price'], 
                          y=all_stars['review_score']+.08,
                          hoverinfo='skip',
                           opacity=.8,
                          marker_symbol= SymbolValidator().values[SymbolValidator().values.index('diamond')],
                          marker=dict(
                                  color='LightSkyBlue',
                                  size=17,
                                  line_width=3),
                          showlegend=False,
                         )
              )

fig5.update_layout(xaxis_title="Price (USD)", 
                   yaxis_title="Ratings",
                   xaxis={'showgrid': False},
                   yaxis={'showgrid':True},
                   paper_bgcolor=tan,
                   hoverlabel= {
                       'bgcolor':green,
                       'bordercolor':'white',
                       'font_family':'Courier New',
                       'font_size':15},
                   title={'text': title5,
                         'x': .050,
                         'xanchor': 'left',
                         'yanchor': 'top'},
                   plot_bgcolor=tan,
                   showlegend=False
                 )

fig5.update_layout(
    hovermode='x',
    width=1300,
    height=400,
    font_family="Courier New",
    title_font_size=20,
    font_size=15,
    font_color='white',
    title_font_color='white',
)

fig5.show()


# Now I wanted to see the 10 most loved proucts without deviding them by catgeroy

# In[22]:


# sort the products by n_of_loves
most_loved = products.sort_values('n_of_loves', ascending=False)

# select the top 10 most loved products
top_loved_products = most_loved.head(10)

top_loved_products


# #### 2. WEB SCRAPING

# In[23]:


# Set up the Google Trends API
pytrends = TrendReq()

# Set up the search parameters
keyword = 'Sephora'
location = 'US-NY'
timeframe = 'now 1-d'

# Get the top searched queries related to "Sephora" in the specified location and timeframe
pytrends.build_payload(kw_list=[keyword], geo=location, timeframe=timeframe)
related_queries_dict = pytrends.related_queries()

# Extract the top related queries and their search volumes
top_related_queries = related_queries_dict[keyword]['top']
related_queries_df = pd.DataFrame(top_related_queries, columns=['query', 'search_volume'])

# Print the results
print(related_queries_df)


# In[24]:


# Set up the Google Trends API
pytrends = TrendReq()

# Set up the search parameters
keywords = ['makeup', 'skincare', 'Sephora products']
location = 'US-NY'
timeframe = 'today 5-y'

# Get the top searched queries related to each keyword in the specified location and timeframe
related_queries_dict = {}
for keyword in keywords:
    pytrends.build_payload(kw_list=[keyword], geo=location, timeframe=timeframe)
    related_queries_result = pytrends.related_queries().get(keyword)
    if related_queries_result is not None:
        related_queries_dict[keyword] = related_queries_result['top']

# Extract the top related queries and their search volumes for each keyword into a single DataFrame
related_queries_list = []
for keyword in related_queries_dict:
    related_queries = related_queries_dict[keyword]
    related_queries['keyword'] = keyword
    related_queries_list.append(related_queries)
related_queries_df = pd.concat(related_queries_list, ignore_index=True)

# Print the results
print(related_queries_df)


# In[28]:


# Define the search terms
keywords = ['Sephora face serum', 'Sephora face mask', 'Sephora hair care']

# Set the geographic location and time range
location = 'US-NY'
timeframe = 'today 5-y'

# Connect to Google Trends API
pytrends = TrendReq()

# Build the payload
pytrends.build_payload(kw_list=keywords, timeframe=timeframe, geo=location)

# Get the search volume data
search_data = pytrends.interest_over_time()

# Plot the search volume trends
search_data.plot(figsize=(10, 6), title='Search Volume Trends for Sephora Products')


# In[30]:


# Define the search terms
keywords = ['vegan makeup', 'vegan cosmetics', 'sustainable beauty']

# Set the geographic location and time range
location = 'US-NY'
timeframe = 'today 5-y'

# Connect to Google Trends API
pytrends = TrendReq()

# Build the payload
pytrends.build_payload(kw_list=keywords, timeframe=timeframe, geo=location)

# Get the search volume data
search_data = pytrends.interest_over_time()

# Plot the search volume trends
search_data.plot(figsize=(10, 6), title='Search Volume Trends for Vegan Makeup Products')


# The search volume for vegan makeup products has been steadily increasing over the past 5 years, indicating a growing interest in this category.
# 
# The search volume for "vegan cosmetics" and "vegan beauty" is higher than that for "vegan makeup," suggesting that consumers may be interested in a wider range of vegan beauty products beyond just makeup.
# 
# The search volume for all three search terms peaked in 2020, which could be attributed to the growing awareness of sustainability and ethical consumerism in the beauty industry.
