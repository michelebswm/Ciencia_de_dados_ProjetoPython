import pandas as pd
import streamlit as st
import joblib




#Caracteristicas numéricas
x_numericos ={'host_listings_count': 0,'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0,
              'beds': 0, 'extra_people': 0, 'minimum_nights': 0, 'ano': 0, 'mes': 0, 'qtd_amenities': 0}

#Valores que se referente a true ou false
x_true_false = {'host_is_superhost': 0, 'instant_bookable': 0}

#Categorias
x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Hostel', 'Guesthouse', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }

# Dicionário com as categorias concatenadas x_listas key_value
dicionario = {}
for item in x_listas:
    for i in x_listas[item]:
        concatenacao = item + '_' + i
        dicionario[concatenacao] = 0



# Criando campos numéricos
for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        # spep, de quanto varia quando clica no + ou -
        # value é o valor inicial
        # format "%.5f" formata para ter 5 casas decimais
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f")
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0) #Como padrão pega 2 casas decimais
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor #Preenchendo valor do input no dicionário


# Criando campos Boleanos
for item in x_true_false:
    valor_tf = st.selectbox(f'{item}', ('Sim', 'Não'))
    # Preenchendo valor do input no dicionário
    if valor_tf == 'Sim':
        x_true_false[item] = 1
    else:
        x_true_false[item] = 0

# Criando campos para as listas
for item in x_listas:
    valor_lista = st.selectbox(f'{item}', x_listas[item])
    #A informação selecionada recebe 1, as demais permanecem com 0
    dicionario[f'{item}_{valor_lista}'] = 1

# Botão
botao = st.button('Prever valor do Imóvel')
if (botao):
    dicionario.update(x_numericos)
    dicionario.update(x_true_false)
    # Se não incluir o indice da erro, a solução é incluir o indice 0 porque será apenas uma linha
    valores_x = pd.DataFrame(dicionario, index=[0])
    dados = pd.read_csv('dados.csv')
    colunas = list(dados.columns)[1:-1]  # para excluir as colunas Unnamed e price
    # Reordenar as colunas de um DataFrame
    valores_x = valores_x[colunas]
    #Carrega o modelo para fazer a previsão
    modelo = joblib.load('modelo.joblib')
    preco = modelo.predict(valores_x)
    st.write(preco[0])
