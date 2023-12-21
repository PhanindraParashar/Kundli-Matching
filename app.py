from streamlit_utils import *
import streamlit as st
from detailed_utils import *

def Vedic_Rashi(df):
    vedic_rashi_map = {
    "Aries": "Mesha",
    "Taurus": "Vrishabha",
    "Gemini": "Mithuna",
    "Cancer": "Karka",
    "Leo": "Simha",
    "Virgo": "Kanya",
    "Libra": "Tula",
    "Scorpio": "Vrishchika",
    "Sagittarius": "Dhanu",
    "Capricorn": "Makara",
    "Aquarius": "Kumbha",
    "Pisces": "Meena"
    }
    
    n = df['Nakshatra']
    p = df['Pada']
    
    vr = vedic_rashi_map[get_rashi(n,p)]
    return vr

map_rename_nakshatra = {'Purva Phalguni':'Purva Phalguni (Pubbha)',
                        'Uttara Phalguni': 'Uttara Phalguni (Uttara)',
                        }



df = data_phani_simple()
df = df.sort_values(['Total','Nakshatra','Pada'],ascending= [False,True,True]).pipe(pipe_reset_index)
df['Rashi'] = df.apply(Vedic_Rashi,axis=1)
df['Nakshatra'] = df['Nakshatra'].replace(map_rename_nakshatra)
df = df[['Rashi','Nakshatra', 'Pada', 'Total', 
    'Nadi','Bakoot', 'Gana', 'Graha_Maitri', 'Yoni', 'Tara', 'Vashya', 'Varna'
    ]]

st.title('Phani\'s Kundali Matching')

st.header('List Of Nakshatras That are good - All Padas')
st.write('Ashlesha, Ashwini, Hasta, Krittika, Punarvasu, Revati, Rohini, Shravana, Swati, Uttara Ashadha, Uttara Phalguni (Uttara)')


st.header('Purva Bhadrapada : Pada 4 is Also Good')


st.header('Other Names Of Nakshatras')
st.write('Uttara Phalguni : Uttara')
st.write('Purva Phalguni : Pubbha')

st.header('Some Good Combinations for Phani')
st.write(df[df['Nadi']>0][df['Total']>=22])



new_nak_names = list(json.load(open('nakshatra_rashi_mapping.json')).keys())

for i, nak in enumerate(new_nak_names):
    if nak in map_rename_nakshatra:
        new_nak_names[i] = map_rename_nakshatra[nak]

nak = st.selectbox('Female Nakshatra', new_nak_names)
#pada = st.selectbox('Pada', [1, 2, 3, 4])



dx = df[df['Nakshatra'] == nak].pipe(pipe_reset_index)#[df['Pada'] == pada]

st.write(dx)





