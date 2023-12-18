from streamlit_utils import *
import streamlit as st
from detailed_utils import *

df = data_phani_simple()

st.title('Phani\'s Kundali Matching')

st.header('Some Good Combinations for Phani')
st.write(df[df['Nadi']>0][df['Total']>=22].head(30))


nak = st.selectbox('Female Nakshatra', list(json.load(open('nakshatra_rashi_mapping.json')).keys()))
pada = st.selectbox('Pada', [1, 2, 3, 4])



dx = df[df['Nakshatra'] == nak][df['Pada'] == pada]

st.write(dx)





