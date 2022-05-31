from datetime import datetime, timedelta
import streamlit as st
from streamlit.elements.form import current_form_id
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
import pandas as pd

cg = CoinGeckoAPI()

st.write('# FOMO Kalkulator')

#Load Data
pris_naa = cg.get_price(ids='dogecoin', vs_currencies='usd')['dogecoin']['usd']

#Giving Choices
st.write(''' Velg Dato, og Beløp''')
dagens_dato = datetime.utcnow().date()
HIST_DATO = st.date_input("Date: ")
ORG_BELOP = st.number_input("Beløp: ")


#Reformat Historical Date for next function
HIST_DATO_REFORMAT = HIST_DATO.strftime("%d-%m-%Y")
doge_historisk = cg.get_coin_history_by_id(id='dogecoin', vs_currencies='usd', date=HIST_DATO_REFORMAT)['market_data']['current_price']['usd']


st.write("Historisk FOMO Analyse:")

total = ORG_BELOP/doge_historisk
verdi_naa = total * pris_naa

st.write("Dine dogecoin er verdt:", verdi_naa)

endring_prosent = ( verdi_naa -  ORG_BELOP)/(ORG_BELOP) * 100

st.write("Endringen i prosent er:", endring_prosent)

differanse = verdi_naa - ORG_BELOP

if differanse == 0:
   st.write("Du har gått i null")
elif differanse <= 0:
   st.write("Du har tapt penger!")
else:
   st.write("Du har tjent penger!") 
st.write('$', differanse)

tid_naa = datetime.now()
HIST_DATO_REFORMAT_2 = datetime.strptime(HIST_DATO_REFORMAT, "%d-%m-%Y")

historiske_priser = cg.get_coin_market_chart_range_by_id(id='dogecoin', vs_currency="usd", from_timestamp=HIST_DATO_REFORMAT_2, to_timestamp=tid_naa.timestamp())['prices']

dato, priser = [], []

for x,y in historiske_priser:
  dato.append(x)
  priser.append(y)

dictionary = {"Priser":priser,
        "Datoer":dato}
dataframe = pd.DataFrame(dictionary)
dataframe
dataframe['Datoer'] = pd.to_datetime(dataframe['Datoer'],unit='ms',origin='unix')

st.line_chart(dataframe.rename(columns={"Datoer":"index"}).set_index("index"))
