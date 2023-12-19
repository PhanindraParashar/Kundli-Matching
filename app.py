from streamlit_utils import *
import streamlit as st
from detailed_utils import *

df = data_phani_simple()
df = df.sort_values(['Total','Nakshatra','Pada'],ascending= [False,True,True]).pipe(pipe_reset_index)


st.title('Phani\'s Kundali Matching')

st.header('List Of Nakshatras That are good - All Padas')
st.write('Ashlesha, Ashwini, Hasta, Krittika, Punarvasu, Revati, Rohini, Shravana, Swati, Uttara Ashadha, Uttara Phalguni')

st.subheader('Only A Specific Pada Nakshatra Combination Works')
st.write('Purva Bhadrapada : Pada 4 is Also Good')

st.header('Some Good Combinations for Phani')
st.write(df[df['Nadi']>0][df['Total']>=22])





nak = st.selectbox('Female Nakshatra', list(json.load(open('nakshatra_rashi_mapping.json')).keys()))
pada = st.selectbox('Pada', [1, 2, 3, 4])



dx = df[df['Nakshatra'] == nak][df['Pada'] == pada]

st.write(dx)





