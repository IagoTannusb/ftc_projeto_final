# Libraries
import plotly.express as px
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import plotly.io as pio

# Bibliotecas necessarias 
import pandas as pd
import streamlit as st 
import inflection
import folium
# import dataset
df = pd.read_csv('zomato.csv')
df1 = df.copy()


# Funcoes utilizadas
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df

COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df

# Renomeando as Colunas
df1 = rename_columns(df1)

# Alerando as colunas
df1['country_code'] = df1.loc[:, 'country_code'].apply(lambda x: country_name(x))
df1['price_range'] = df1.loc[:, 'price_range'].apply(lambda x: create_price_tye(x))
df1["rating_color"] = df1.loc[:, "rating_color"].apply(lambda x: color_name(x))

# Tipo primario de culinaria
df1['cuisines'] = df1.loc[:, 'cuisines'].astype(str).apply(lambda x: x.split(',')[0])
# Removendo colunas desnecessarias 
df1.drop( columns = ['locality_verbose','switch_to_order_menu'])

# Revomendo NaN
df1 = df1.dropna()
# Removendo dados duplicados
df1 = df1.drop_duplicates()

#Maks
df1_country_city = df1.drop_duplicates(subset='city', keep='first')
df1_country_restaurant = df1.drop_duplicates(subset='restaurant_id', keep='first')
df1_unique_cuisines = df1.drop_duplicates(subset='cuisines', keep='first')



# =======================================
# Barra Lateral
# =======================================
st.set_page_config(page_title="The Ramsey Highlights", layout="wide")

#st.sidebar.markdown( '# AtlasFood' )
st.sidebar.markdown( '## O Melhor lugar para encontrar seu mais novo restaurante favorito!' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione os Países' )
traffic_options = st.sidebar.multiselect( 
    '**Selecione os Países**',
    ( ['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'] ), 
    default=['Brazil', 'United States of America', 'England', 'South Africa','New Zeland'] )

def convert_df(df1):
    return df1.to_csv().encode('utf-8')
csv = convert_df(df1)

st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de transito
df1_linhas_selecionadas = df1['country_code'].isin( traffic_options )
df1 = df1.loc[df1_linhas_selecionadas, :]


# =======================================
# Layout no Streamlit
# =======================================
# Introducao 

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title('AtlasFood')
with row0_2:
    st.text("")
    st.subheader('Streamlit App by [Iago Tannus](www.linkedin.com/in/iagotannus)')
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("Bem vindo ao meu primeiro projeto de conclusão de curso. FTC – Analisando Dados com Python, ministrado pela [Comunidade DS](https://comunidadeds.com/)")
    st.markdown("Contexto de Negócio:")
    st.markdown("A empresa AtlasFood é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da AtlasFood, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.")
    st.markdown("Agradecimento aos professores [Pedro Ferraresi](https://www.linkedin.com/in/pedro-ferraresi/) e [Meigarom Lopes](https://www.linkedin.com/in/meigarom/) por o conhecimento passado ao longo desses dois meses de curso.")
    st.markdown("layout inspired by: [BuLiAn - Bundesliga Analyzer](https://tdenzl-bulian-bulian-ifeiih.streamlit.app/)")

#with tab1:
with st.container():
    
    st.markdown( '# Metricas Gerais' )

    row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3, row2_3, row2_spacer4, row2_4, row2_spacer5 = st.columns((.2, 1.3, .1, 1, .2, 1, .2, 1, .2))
    with row2_1:
        restaurantes_cadastrados = len(df1['restaurant_id'].unique())
        restaurantes_cadastrados ="📊 " + str(restaurantes_cadastrados) + " Restaurantes"
        st.markdown(restaurantes_cadastrados)

        
    with row2_2:
        paises = len(df1['country_code'].unique())
        paises = "🌍 " + str(paises) + " Paises"
        st.markdown(paises)

    with row2_3:
        cidades = len(df1['city'].unique())
        #total_goals_in_df = df_data_filtered['goals'].sum()
        cidades = "🏙️ " + str(cidades) + " Cidades"
        st.markdown(cidades)
        
        

    with row2_4:
        culinarias = len( df1['cuisines'].unique() )
        culinarias = "🍽️ " + str(culinarias) + " Culinarias"
        st.markdown(culinarias)
    
    see_data = st.expander('Clique para ver o conjunto de dados')
    with see_data:
        st.dataframe(data=df1.reset_index(drop=True))
st.text('')
       
        
with st.container():
    col1, col2, col3 = st.columns((2, 7.1, .2))

    with col1:
        st.write('')

    with col2:
        st.markdown( '## Mapa' )
        data_plot = df1.loc[:, ['city', 'restaurant_name', 'longitude', 'latitude']].reset_index()
        # Desenhar o mapa
        map_ = folium.Map( zoom_start=11 )
        cluster = MarkerCluster().add_to(map_)
    
        for index, location_info in data_plot.iterrows():
            folium.Marker( [location_info['latitude'],
                location_info['longitude']],
                popup=location_info['restaurant_name'], icon= folium.Icon(color='lightgray', icon='home', prefix='fa') ).add_to( cluster )
        folium_static(map_)

    with col3:
        st.write(' ')
   

with st.container():
    st.markdown("""___""")
    st.markdown("## Visão Países")

    df1_country_city_group = (df1.loc[:, ['city', 'country_code']]
                       .drop_duplicates()
                       .groupby('country_code')
                       .count()
                       .sort_values( by='city',ascending = False)
                       .reset_index() )
    
    df1_country_city_group.columns = ['Paises', 'Quantidade de Cidades']
    fig = px.bar(df1_country_city_group, x='Paises', y='Quantidade de Cidades', title= 'Quantidade de Cidades Registradas por Países', text='Quantidade de Cidades')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
         })
    fig.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True )

    

    col1, col2 = st.columns( 2 )

    with col1:
        qty_votes_by_country = ( df1.loc[:, ['votes','country_code']]
                            .groupby('country_code')
                            .mean()
                            .round(2)
                            .sort_values(by='votes', ascending=False)
                            .reset_index() )

    
        qty_votes_by_country.columns = ['Paises', 'Quantidade de Avaliações']

        fig = px.bar(qty_votes_by_country, x='Paises', y='Quantidade de Avaliações', title='Média de Avaliações feitas por País', text='Quantidade de Avaliações')
        fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
        })
        fig.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False),
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        mean_average_cost_for_two = ( df1.loc[:, ['average_cost_for_two','country_code']]
                              .groupby('country_code')
                              .mean()
                              .round(2)
                              .sort_values(by='average_cost_for_two', ascending=False)
                              .reset_index() )
  
        mean_average_cost_for_two.columns = ['Paises', 'Preço de um prato para dois']
        fig = px.bar(mean_average_cost_for_two, x='Paises', y='Preço de um prato para dois', title= 'Média do Preço de um Prato para Dois',text='Preço de um prato para dois')
        fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
         })
        fig.update_layout(xaxis=dict(showgrid=False),
                  yaxis=dict(showgrid=False),
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

        
with st.container():
    df1_restaurants_by_city = ( df1.loc[:, ['restaurant_id', 'country_code']]
                                                .drop_duplicates()
                                                .groupby('country_code')
                                                .count()
                                                .sort_values( by='restaurant_id',ascending = False)
                                                .reset_index() )    

    df1_restaurants_by_city.columns = ['Paises', 'Quantidade de Restaurantes']
    fig = px.bar(df1_restaurants_by_city, x='Paises', y='Quantidade de Restaurantes', title= 'Quantidades de Restaurantes por País',text='Quantidade de Restaurantes')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
         })
    fig.update_layout(xaxis=dict(showgrid=False),
              yaxis=dict(showgrid=False),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

row8_spacer1, row8_1, row8_spacer2 = st.columns((.2, 7.1, .2))
with row8_1:
    st.markdown('## Tipos de Cusinhas')

with st.container():
    st.markdown( '### Metricas Gerais' )

    col1_space, col1, col2, col3, col4 = st.columns((1, 1.6, 1.6,1.6,1.6))
    with col1:
        teste = 1
        teste2 = 10
        help_input='Restaurant: Fairmount Bagel \n\n Pais: Canada \n\n Cidade: Montreal \n\n Prato para Dois: 10 Dollar($)'
        col1.metric(label="Others", value="4.9/5.0", delta="0.68", help=help_input)

        
    with col2:
        teste = 1
        teste2 = 10
        help_input='Restaurant: Ippudo \n\n Pais: England \n\n Cidade: Glasgow \n\n Prato para Dois: 20 Pounds(£)'
        col2.metric(label="Ramen", value="2.9/5.0", delta="0.68", help=help_input)

    with col3:
        teste = 1
        teste2 = 10
        help_input='Restaurant: Lee Palace \n\n Pais: United States of America \n\n Cidade: Durban \n\n Prato para Dois: 200 Rand(R)'
        col3.metric(label="Cantonese", value="3.4/5.0", delta="-0.72", help=help_input)

    with col4:
        teste = 1
        teste2 = 10
        help_input='Restaurant: House of Curries on Florida \n\n Pais: South Africa \n\n Cidade: New York City \n\n Prato para Dois: 40 Dollar($)'
        col4.metric(label="Durban", value="2.9", delta="- 1.22", help=help_input)



row9_spacer1, row9_1, row9_spacer2, row9_2, row9_spacer3  = st.columns((.2, 2.3, .4, 8.8, .1))
with row9_1:
    st.markdown('')
    top_rest = st.slider('**Quantidade de Restaurantes?**', 0, 20, 10)
    df_cousines_filter = df1['cuisines'].unique()
    
    options = st.multiselect(
    '**Tipos de Culinaria**', ( df_cousines_filter ) , ['Brazilian'])
    df1_linhas_selecionadas = df1['cuisines'].isin( options )
    df2 = df1.loc[df1_linhas_selecionadas, :]

with row9_2:
    st.markdown('#### Top ' + str(top_rest) + ' Restaurantes')
    df1_linhas_selecionadas = df2.iloc[0 : top_rest , :].sort_values(by='aggregate_rating', ascending=False)
    st.dataframe(data=df1_linhas_selecionadas, use_container_width=False)

col1, col2 = st.columns( 2 )
with st.container():
    with col1:
        df_aux = df1.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().round(2).sort_values('aggregate_rating', ascending = False).reset_index()
        df_top = df_aux.head(top_rest)


  
        df_top.columns = ['Tipo de Culinária', 'Avaliação Média']
        fig = px.bar(df_top, x='Tipo de Culinária', y='Avaliação Média', title= 'Melhores Tipos de Culinárias', text='Avaliação Média')
        fig.update_layout({
         'plot_bgcolor': 'rgba(0,0,0,0)',
         'paper_bgcolor': 'rgba(0,0,0,0)'
          })
        fig.update_layout(xaxis=dict(showgrid=False),
                   yaxis=dict(showgrid=False),
         )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True )
        
    with col2:
        df_aux = df1.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().round(2).sort_values('aggregate_rating', ascending = True).reset_index()
        df_top = df_aux.head(top_rest)


  
        df_top.columns = ['Tipo de Culinária', 'Avaliação Média']
        fig = px.bar(df_top, x='Tipo de Culinária', y='Avaliação Média', title= 'Piores Tipos de Culinárias', text='Avaliação Média')
        fig.update_layout({
         'plot_bgcolor': 'rgba(0,0,0,0)',
         'paper_bgcolor': 'rgba(0,0,0,0)'
          })
        fig.update_layout(xaxis=dict(showgrid=False),
                   yaxis=dict(showgrid=False),
         )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True )

with st.container():
    st.markdown("""___""")
    st.markdown("## Visão Cidades")

    df1_country_city_group = df1.loc[:, ['cuisines', 'city']].drop_duplicates().groupby('city').count().sort_values('cuisines', ascending=False ).reset_index()

    df1_country_city_group.columns = ['Paises', 'Quantidade de Cidades']
    fig = px.bar(df1_country_city_group, x='Paises', y='Quantidade de Cidades', title= 'Quantidade de Cidades Registradas por Países', text='Quantidade de Cidades')
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
         })
    fig.update_layout(xaxis=dict(showgrid=False),
                  yaxis=dict(showgrid=False),
        )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True )

    col1, col2 = st.columns( 2 )

    with col1:
        df1_aggregate_rating_by_city_4 = ( df1.loc[df1['aggregate_rating'] > 4, ['restaurant_id', 'city']]
                                                        .drop_duplicates()
                                                        .groupby('city')
                                                        .count()
                                                        .sort_values( by='restaurant_id',ascending = False)
                                                        .reset_index() )
    
        #df1_country_city_group = df1.loc[:, ['cuisines', 'city']].drop_duplicates().groupby('city').count().sort_values('cuisines', ascending=False ).reset_index()
    
        df1_aggregate_rating_by_city_4.columns = ['Cidades', 'Quantidade de Restaurantes']
        fig = px.bar(df1_aggregate_rating_by_city_4, x='Cidades', y='Quantidade de Restaurantes', title= 'Restaurantes Com Media Maior que Quatro', text='Quantidade de Restaurantes')
        fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
         })
        fig.update_layout(xaxis=dict(showgrid=False),
                  yaxis=dict(showgrid=False),
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True )
        
    with col2:
        df1_aggregate_rating_by_city_2 = ( df1.loc[df1['aggregate_rating'] < 2.5, ['restaurant_id', 'city']]
                                                       .drop_duplicates() 
                                                       .groupby('city')
                                                       .count()
                                                       .sort_values( by='restaurant_id',ascending = False)
                                                       .reset_index() )

        df1_aggregate_rating_by_city_2.columns = ['Cidades', 'Quantidade de Restaurantes']
        fig = px.bar(df1_aggregate_rating_by_city_2, x='Cidades', y='Quantidade de Restaurantes', title= 'Restaurantes Com Media Menor que Dois e Meio', text='Quantidade de Restaurantes')
        fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
         })
        fig.update_layout(xaxis=dict(showgrid=False),
                  yaxis=dict(showgrid=False),
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True )
