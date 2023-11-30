import streamlit as st
import json
import pandas as pd
import plotly.express as px
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Bike Store-StormzzG', page_icon=':bike:',layout='wide')
st.title(':bike: Bike Store EDA')
st.markdown('<style>div.block-container{padding-top: 2rem}<style>', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=['Intro', 'Data Visualization'],
    icons=['person-fill', 'bar-chart-fill'],
    default_index=0,
    orientation='horizontal'
)

if selected == 'Intro':
    with open('Animation 1.json', 'r') as f:
        animation = json.load(f)

    col1,col2 = st.columns((2))
 
    with col1:
        st_lottie(animation, key='hello1', quality='high', width=500, height=500, loop=True)
        image_alignment= """
            <style>
            animation {
            padding-top: -200px
            }
            </style>
            """
        st.markdown(image_alignment, unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='text-align: center; font-family: Cursive; font-size: 20px; padding-top: 250px; margin-left: -350px;'>Hi there! My name is Stormy Ndonga, a Data Science Student at Moringa School Kenya.This is my simple Exploratory Data Analysis for a Bike Store Sample Data. Click on the Data Visualization tab to have a look at it.</p>", unsafe_allow_html=True)



if selected == 'Data Visualization':
    #st.title(':bike: Bike Store EDA')
    #st.markdown('<style>div.block-container{padding-top: 2rem}<style>', unsafe_allow_html=True)

    fl = st.file_uploader(':file_folder: Upload a File', type=(['csv','xlsx','xls','txt']))
    st.warning('All this Data is affected by what you pick in the Sidebar Multiselect. Enjoy!')
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename)
    else:
        df = pd.read_csv('Sales.csv')


    st.sidebar.header('Choose Filter')
    country = st.sidebar.multiselect('Choose Country', df['Country'].unique())
    if not country:
        df2 = df.copy()
    else:
        df2 = df[df['Country'].isin(country)]
    state = st.sidebar.multiselect('Choose State', df2['State'].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2['State'].isin(state)]

    product_df = df3.groupby(by = ['Product_Category'], as_index=False)['Revenue'].sum()
    country_df = df3.groupby(by = ['Country'], as_index=False)['Revenue'].sum()
    subcategory_df = df3.groupby(by = ['Sub_Category'], as_index=False)['Profit'].sum()
    category_df = df3.groupby(by = ['Sub_Category'], as_index=False)['Revenue'].sum()
    col4, col5 = st.columns((2))
    with col4:
        st.subheader('Product Category Revenue')
        fig = px.bar(product_df, x='Product_Category', y='Revenue', text=['${:,.2f}'.format(x) for x in product_df['Revenue']], template='seaborn')
        st.plotly_chart(fig,use_container_width=True)

        with st.expander('Product Category Data'):
            st.write(product_df.style.background_gradient(cmap='YlOrBr'))
            csv = product_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name='Product CSV', mime='text/csv')
    with col5:
        st.subheader('Country Revenue')
        fig = px.pie(country_df, values='Revenue', names='Country')
        fig.update_traces(text=country_df['Country'], textposition='outside')
        st.plotly_chart(fig,use_container_width=True)

        with st.expander('Country Profits Data'):
            st.write(country_df.style.background_gradient(cmap='YlOrBr'))
            csv = country_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name='Country CSV', mime='text/csv')

    col6, col7 = st.columns((2))
    with col6:
        st.subheader('Sub Category Profits')
        fig = px.bar(subcategory_df, x='Sub_Category', y='Profit',template='seaborn')
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander('Sub Category View Data'):
            st.write(subcategory_df.style.background_gradient(cmap='YlOrBr'))
            csv = subcategory_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name='Subcategory CSV', mime='text/csv')
    with col7:
        st.subheader('Sub Category Total Revenue')
        fig = px.bar(category_df, x='Sub_Category', y='Revenue',template='seaborn')
        st.plotly_chart(fig, use_container_width=True)

        with st.expander('Sub Category Tota Revenue'):
            st.write(category_df.style.background_gradient(cmap='YlOrBr'))
            csv = category_df.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name='Revenue CSV', mime='text/csv')

    df3['Date'] = pd.to_datetime(df3['Date'])
    df3['month_year'] = df3['Date'].dt.to_period('M')
    st.subheader('Time Series Revenue Analysis')

    new_df = df3.groupby(['month_year'],as_index=False)['Revenue'].sum()
    new_df2 = pd.DataFrame(new_df)
    new_df2['month_year'] = new_df2['month_year'].dt.strftime("%Y : %B")
    #linechart = pd.DataFrame(df3.groupby(df3['month_year'].dt.strftime('%Y : %b'))['Revenue'].sum()).reset_index()

    fig2 = px.line(new_df2, x='month_year', y='Revenue', height=500)
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander('View Time Series Data Analysis'):
        st.write(new_df2.T.style.background_gradient(cmap='YlOrBr'))
        csv = new_df2.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name='Time Series Data', mime='text/csv')

    st.subheader('Hierarchial View of Revenue using Treemap')
    fig3 = px.treemap(df3, path=['Country','Product_Category','Sub_Category'], values='Revenue', color='Sub_Category', height=650)
    st.plotly_chart(fig3, use_container_width=True)

    correlation_data = df3[['Unit_Cost', 'Unit_Price', 'Profit', 'Cost', 'Revenue']]
    corr_matrix = correlation_data.corr()
    fig4 = px.imshow(corr_matrix, text_auto=True)
    st.subheader('Correlation Between Features using Heatmap')
    st.plotly_chart(fig4,use_container_width=True)
    with st.expander('View Correlation Data'):
        st.write(corr_matrix.style.background_gradient(cmap='YlOrBr'))
        csv = corr_matrix.to_csv(index=False).encode('utf-8')
        st.download_button('Download Data', data=csv, file_name='Correlation Data', mime='text/csv')

    st.subheader('Relationship Between Profit and Revenue')
    fig5 = px.scatter(correlation_data, x='Revenue', y='Profit')
    st.plotly_chart(fig5, use_container_width=True)

    product_df2 = df3.groupby(by = ['Product_Category'], as_index=False)['Profit'].sum()
    country_df2 = df3.groupby(by = ['Country'], as_index=False)['Profit'].sum()
    col8, col9 = st.columns((2))
    with col8:
        st.subheader('Product Category Profit')
        fig = px.pie(product_df2, names='Product_Category', values='Profit', template='plotly_dark')
        fig.update_traces(text=product_df['Product_Category'], textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        with st.expander('View Data'):
            st.write(product_df2.style.background_gradient(cmap='YlOrBr'))
            csv = product_df2.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name='Profit CSV', mime='text/csv')
    with col9:
        st.subheader('Country Profit')
        fig = px.pie(country_df2, names='Country', values='Profit')
        fig.update_traces(text=country_df2['Country'],textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        with st.expander('View Data'):
            st.write(country_df2.style.background_gradient(cmap='YlOrBr'))
            csv = country_df2.to_csv(index=False).encode('utf-8')
            st.download_button('Download Data', data=csv, file_name='Country Profit CSV', mime='text/csv')
