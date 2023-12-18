import pandas as pd 
import requests
import numpy as np  
import os 
import json
import warnings
from ambgious import yoni_list

Mesh_Yoni_Norm = {i:np.mean(j) for i,j in yoni_list['Mesh'].items() }
warnings.filterwarnings('ignore')
#https://colab.research.google.com/drive/1lYC2-axUPuvmPQRLi_g8sxGbCTpgNaYm?authuser=0#scrollTo=V1vtTO6PISWE
#https://www.findyourfate.com/indianastro/vedic-astrology/ashtakuta.html
#https://aaps.space/kundli-matching/



varna_map = {
    'Cancer': 'Brahmin', 'Scorpio': 'Brahmin', 'Pisces': 'Brahmin',
    'Aries': 'Kshatriya', 'Leo': 'Kshatriya', 'Sagittarius': 'Kshatriya',
    'Gemini': 'Vaishya', 'Libra': 'Vaishya', 'Aquarius': 'Vaishya',
    'Taurus': 'Shudra', 'Virgo': 'Shudra', 'Capricorn': 'Shudra'
}

# Define a ranking for each Varna to compare hierarchy
varna_rank = {
    'Brahmin': 4,
    'Kshatriya': 3,
    'Vaishya': 2,
    'Shudra': 1
}


nakshatra_deg = {nak:round(i*(360/27),3) for i,nak in enumerate(json.load(open('nakshatra_rashi_mapping.json')).keys())}

rashi_no_mapping = {
    'Aries': 1,
    'Taurus': 2,
    'Gemini': 3,
    'Cancer': 4,
    'Leo': 5,
    'Virgo': 6,
    'Libra': 7,
    'Scorpio': 8,
    'Sagittarius': 9,
    'Capricorn': 10,
    'Aquarius': 11,
    'Pisces': 12
}

nakshatra_to_gana = {
        'Ashwini': 'Deva', 'Bharani': 'Manushya', 'Krittika': 'Rakshasha',
        'Rohini': 'Manushya', 'Mrigashira': 'Deva', 'Ardra': 'Manushya',
        'Punarvasu': 'Deva', 'Pushya': 'Deva', 'Ashlesha': 'Rakshasha',
        'Magha': 'Rakshasha', 'Purva Phalguni': 'Manushya', 'Uttara Phalguni': 'Manushya',
        'Hasta': 'Deva', 'Chitra': 'Rakshasha', 'Swati': 'Deva',
        'Vishakha': 'Rakshasha', 'Anuradha': 'Deva', 'Jyeshtha': 'Rakshasha',
        'Mula': 'Rakshasha', 'Purva Ashadha': 'Manushya', 'Uttara Ashadha': 'Manushya',
        'Shravana': 'Deva', 'Dhanishta': 'Rakshasha', 'Shatabhisha': 'Rakshasha',
        'Purva Bhadrapada': 'Manushya', 'Uttara Bhadrapada': 'Manushya', 'Revati': 'Deva'
    }

rashi_lord_mapping = {
    'Aries': 'Mars',
    'Taurus': 'Venus',
    'Gemini': 'Mercury',
    'Cancer': 'Moon',
    'Leo': 'Sun',
    'Virgo': 'Mercury',
    'Libra': 'Venus',
    'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn',
    'Aquarius': 'Saturn',
    'Pisces': 'Jupiter'
    }

planetary_friendship = {
        'Mars': ['Sun', 'Moon', 'Jupiter'],
        'Sun': ['Moon', 'Mars', 'Jupiter'],
        'Moon': ['Sun', 'Mercury'],
        'Mercury': ['Sun', 'Venus'],
        'Jupiter': ['Sun', 'Moon', 'Mars'],
        'Venus': ['Mercury', 'Saturn'],
        'Saturn': ['Mercury', 'Venus'],
    }


bakoot_sign = [
    {
        "Sign": "Aries",
        "Aries": 7,
        "Taurus": 0,
        "Gemini": 7,
        "Cancer": 7,
        "Leo": 0,
        "Virgo": 0,
        "Libra": 7,
        "Scorpio": 0,
        "Sagittarius": 0,
        "Capricorn": 7,
        "Aquarius": 7,
        "Pisces": 0
    },
    {
        "Sign": "Taurus",
        "Aries": 0,
        "Taurus": 7,
        "Gemini": 0,
        "Cancer": 7,
        "Leo": 7,
        "Virgo": 0,
        "Libra": 0,
        "Scorpio": 7,
        "Sagittarius": 0,
        "Capricorn": 0,
        "Aquarius": 7,
        "Pisces": 7
    },
    {
        "Sign": "Gemini",
        "Aries": 7,
        "Taurus": 0,
        "Gemini": 7,
        "Cancer": 0,
        "Leo": 7,
        "Virgo": 7,
        "Libra": 0,
        "Scorpio": 0,
        "Sagittarius": 7,
        "Capricorn": 0,
        "Aquarius": 0,
        "Pisces": 7
    },
    {
        "Sign": "Cancer",
        "Aries": 7,
        "Taurus": 7,
        "Gemini": 0,
        "Cancer": 7,
        "Leo": 0,
        "Virgo": 7,
        "Libra": 7,
        "Scorpio": 0,
        "Sagittarius": 0,
        "Capricorn": 7,
        "Aquarius": 0,
        "Pisces": 0
    },
    {
        "Sign": "Leo",
        "Aries": 0,
        "Taurus": 7,
        "Gemini": 7,
        "Cancer": 0,
        "Leo": 7,
        "Virgo": 0,
        "Libra": 7,
        "Scorpio": 7,
        "Sagittarius": 0,
        "Capricorn": 0,
        "Aquarius": 7,
        "Pisces": 0
    },
    {
        "Sign": "Virgo",
        "Aries": 0,
        "Taurus": 0,
        "Gemini": 7,
        "Cancer": 7,
        "Leo": 0,
        "Virgo": 7,
        "Libra": 0,
        "Scorpio": 7,
        "Sagittarius": 7,
        "Capricorn": 0,
        "Aquarius": 0,
        "Pisces": 7
    },
    {
        "Sign": "Libra",
        "Aries": 7,
        "Taurus": 0,
        "Gemini": 0,
        "Cancer": 7,
        "Leo": 7,
        "Virgo": 0,
        "Libra": 7,
        "Scorpio": 0,
        "Sagittarius": 7,
        "Capricorn": 7,
        "Aquarius": 0,
        "Pisces": 0
    },
    {
        "Sign": "Scorpio",
        "Aries": 0,
        "Taurus": 7,
        "Gemini": 0,
        "Cancer": 0,
        "Leo": 7,
        "Virgo": 7,
        "Libra": 0,
        "Scorpio": 7,
        "Sagittarius": 0,
        "Capricorn": 7,
        "Aquarius": 7,
        "Pisces": 0
    },
    {
        "Sign": "Sagittarius",
        "Aries": 0,
        "Taurus": 0,
        "Gemini": 7,
        "Cancer": 0,
        "Leo": 0,
        "Virgo": 7,
        "Libra": 7,
        "Scorpio": 0,
        "Sagittarius": 7,
        "Capricorn": 0,
        "Aquarius": 7,
        "Pisces": 7
    },
    {
        "Sign": "Capricorn",
        "Aries": 7,
        "Taurus": 0,
        "Gemini": 0,
        "Cancer": 7,
        "Leo": 0,
        "Virgo": 0,
        "Libra": 7,
        "Scorpio": 7,
        "Sagittarius": 0,
        "Capricorn": 7,
        "Aquarius": 0,
        "Pisces": 7
    },
    {
        "Sign": "Aquarius",
        "Aries": 7,
        "Taurus": 7,
        "Gemini": 0,
        "Cancer": 0,
        "Leo": 7,
        "Virgo": 0,
        "Libra": 0,
        "Scorpio": 7,
        "Sagittarius": 7,
        "Capricorn": 0,
        "Aquarius": 7,
        "Pisces": 0
    },
    {
        "Sign": "Pisces",
        "Aries": 0,
        "Taurus": 7,
        "Gemini": 7,
        "Cancer": 0,
        "Leo": 0,
        "Virgo": 7,
        "Libra": 0,
        "Scorpio": 0,
        "Sagittarius": 7,
        "Capricorn": 7,
        "Aquarius": 0,
        "Pisces": 7
    }
]


bakoot_df = pd.DataFrame(bakoot_sign).set_index('Sign')


nadi_map = {
        'Ashwini': 'Aadi', 'Bharani': 'Madhya', 'Krittika': 'Anya', 'Rohini': 'Anya', 
        'Mrigashira': 'Madhya', 'Ardra': 'Aadi', 'Punarvasu': 'Aadi', 'Pushya': 'Madhya', 
        'Ashlesha': 'Anya', 'Magha': 'Anya', 'Purva Phalguni': 'Madhya', 
        'Uttara Phalguni': 'Aadi', 'Hasta': 'Aadi', 'Chitra': 'Madhya', 
        'Swati': 'Anya', 'Vishakha': 'Anya', 'Anuradha': 'Madhya', 'Jyeshtha': 'Aadi', 
        'Mula': 'Aadi', 'Purva Ashadha': 'Madhya', 'Uttara Ashadha': 'Anya', 
        'Shravana': 'Anya', 'Dhanishta': 'Madhya', 'Shatabhisha': 'Aadi', 
        'Purva Bhadrapada': 'Aadi', 'Uttara Bhadrapada': 'Madhya', 'Revati': 'Anya'
    }



def pipe_reset_index(df):
  df.index = range(len(df))
  return df 


def get_rashi(nakshatra,pada: int):
    n_map = json.load(open('nakshatra_rashi_mapping.json'))
    pada_no = f"pada {pada}"
    return n_map[nakshatra][pada_no]

def get_rashi_and_half(nakshatra, pada):
    degrees = nakshatra_deg[nakshatra] + (pada-1)*3.333
    rashi_no = int(degrees//30) + 1
    remainder = degrees - (rashi_no-1)*30 
    if remainder < 15:
        half = 1
    else:
        half = 2
    return rashi_no, half


def get_varna(nakshatra, pada: int):
    rashi = get_rashi(nakshatra, pada)
    return varna_map[rashi]


def get_vashya(nakshatra, pada: int):
    # Split the input into Rashi number and its half
    rashi_number,rashi_half = get_rashi_and_half(nakshatra, pada)
    
    # Define the Vashya categories for Rashis not including the special cases 9 and 10
    vashya_mapping = {
        'Dwipad': [3, 6, 7, 11],
        'Chatushpad': [1, 2],
        'Jalachar': [4, 12],
        'Vanchar': [5],
        'Keet': [8]
    }

    # Handle the special cases for Rashis 9 and 10
    if rashi_number == 9:
        return 'Dwipad' if rashi_half == 1 else 'Chatushpad'
    elif rashi_number == 10:
        return 'Chatushpad' if rashi_half == 1 else 'Jalachar'

    # Check the general Vashya category
    for vashya, rashis in vashya_mapping.items():
        if rashi_number in rashis:
            return vashya
    
    # Return None if Rashi number is not found in any category (should not happen with valid data)
    return None

def calculate_tara(nakshatra_from, nakshatra_to):
    tara_names = {
        1: 'Janma',
        2: 'Sampat',
        3: 'Vipat',
        4: 'Kshem',
        5: 'Pratyari',
        6: 'Sadhak',
        7: 'Vadha',
        8: 'Mitra',
        9: 'Atimitra'
    }
    
    inverse_tara_names = {v: k for k, v in tara_names.items()}
    
    # Calculate the distance between the two Nakshatras
    distance = (nakshatra_to - nakshatra_from) % 27
    # Calculate Tara by dividing the distance by 9 and taking the remainder
    tara_number = (distance % 9) + 1
    # Get the Tara name from the Tara number
    tara_name = tara_names[tara_number]
    return tara_number, tara_name

def get_yoni(nakshatra):    
    nakshatras_yoni = {
    'Ashwini': 'Ashwa', 'Bharani': 'Gaja', 'Krittika': 'Mesh',
    'Rohini': 'Sarpa', 'Mrigashira': 'Sarpa', 'Ardra': 'Shwan',
    'Punarvasu': 'Marjara', 'Pushya': 'Mesh', 'Ashlesha': 'Marjara',
    'Magha': 'Mushak', 'Purva Phalguni': 'Mushak', 'Uttara Phalguni': 'Gau',
    'Hasta': 'Mahish', 'Chitra': 'Vyaghra', 'Swati': 'Mahish',
    'Vishakha': 'Vyaghra', 'Anuradha': 'Mriga', 'Jyeshtha': 'Mriga',
    'Mula': 'Shwan', 'Purva Ashadha': 'Vanar', 'Uttara Ashadha': 'Nakul',
    'Shravana': 'Vanar', 'Dhanishta': 'Singh', 'Shatabhisha': 'Ashwa',
    'Purva Bhadrapada': 'Singh', 
    
    'Uttara Bhadrapada': 'Gau', ##
    
    'Revati': 'Gaja'
    }
    
    return nakshatras_yoni[nakshatra]

def get_planet_relationship(planet1, planet2, friendships):
    if planet1 == planet2:
        return 'same'
    elif planet2 in friendships[planet1]['friends']:
        return 'friends'
    elif planet2 in friendships[planet1]['neutrals']:
        return 'neutral'
    elif planet2 in friendships[planet1]['enemies']:
        return 'enemy'
    else:
        # This case should not occur as all relationships are covered
        return 'neutral'  # Defaulting to neutral if not found
    
def are_lords_friends(lord1, lord2):
    return lord2 in planetary_friendship[lord1]#['friends']






################ Varna Kuta################
def calculate_varna_score(nakshatra_male, pada_male, nakshatra_female, pada_female):
    varna_male = get_varna(nakshatra_male, pada_male)
    varna_female = get_varna(nakshatra_female, pada_female)
    
    # Calculate score
    if varna_male == varna_female:
        return 1
    elif varna_rank[varna_male] > varna_rank[varna_female]:
        return 1
    else:
        return 0
    

################ Vashya Kuta################

def calculate_vashya_kuta_score(nakshatra_male, pada_male, nakshatra_female, pada_female):
    vashya_boy = get_vashya(nakshatra_male, pada_male)
    vashya_girl = get_vashya(nakshatra_female, pada_female)
    
    # Vashya Kuta compatibility matrix
    vashya_kuta_matrix = {
        'Dwipad': {'Dwipad': 2, 'Chatushpad': 0, 'Jalachar': 0.5, 'Vanchar': 0, 'Keet': 1},
        'Chatushpad': {'Dwipad': 1, 'Chatushpad': 2, 'Jalachar': 1, 'Vanchar': 0.5, 'Keet': 1},
        'Jalachar': {'Dwipad': 0.5, 'Chatushpad': 1, 'Jalachar': 2, 'Vanchar': 1, 'Keet': 1},
        'Vanchar': {'Dwipad': 0, 'Chatushpad': 0.5, 'Jalachar': 1, 'Vanchar': 2, 'Keet': 0},
        'Keet': {'Dwipad': 1, 'Chatushpad': 1, 'Jalachar': 1, 'Vanchar': 0, 'Keet': 2}
    }

    # Calculate the Vashya Kuta score
    return vashya_kuta_matrix[vashya_boy][vashya_girl]

################ Tara Kuta################

def calculate_tara_kuta_score(nakshatra_male, nakshatra_female):
    # Calculate Tara for both directions
    nakshattra_numbers = {nak: i+1 for i, nak in enumerate(json.load(open('nakshatra_rashi_mapping.json')).keys())}
    male_nakshatra_number = nakshattra_numbers[nakshatra_male]
    female_nakshatra_number = nakshattra_numbers[nakshatra_female]
    tara_number_male, tara_name_male = calculate_tara(male_nakshatra_number, female_nakshatra_number)
    tara_number_female, tara_name_female = calculate_tara(female_nakshatra_number, male_nakshatra_number)
    
    # Determine if Tara is malefic or benefic
    malefic_taras = [3, 5, 7]
    tara_malefic_male = tara_number_male in malefic_taras
    tara_malefic_female = tara_number_female in malefic_taras

    # Calculate the score
    if not tara_malefic_male and not tara_malefic_female:
        # Both are benefic
        score = 3
    elif tara_malefic_male != tara_malefic_female:
        # One is benefic and the other is malefic
        score = 1.5
    else:
        # Both are malefic
        score = 0

    return score, tara_name_male, tara_name_female

################ Yoni Kuta################

def calculate_yoni_kuta(nakshatra_male, nakshatra_female):
    
    yoni_compatibility = {
        'Ashwa': {'Ashwa': 4, 'Gaja': 2, 'Mesh': 2, 'Sarpa': 3, 'Shwan': 2, 'Marjara': 2, 'Mushak': 2, 'Gau': 1, 'Mahish': 0, 'Vyaghra': 1, 'Mriga': 3, 'Vanar': 3, 'Nakul': 2, 'Singh': 1},
        'Gaja': {'Ashwa': 2, 'Gaja': 4, 'Mesh': 3, 'Sarpa': 3, 'Shwan': 2, 'Marjara': 2, 'Mushak': 2, 'Gau': 2, 'Mahish': 3, 'Vyaghra': 1, 'Mriga': 2, 'Vanar': 3, 'Nakul': 2, 'Singh': 0},
        'Mesh': {'Ashwa': 2, 'Gaja': 3, 'Mesh': 4, 'Sarpa': 2, 'Shwan': 1, 'Marjara': 2, 'Mushak': 1, 'Gau': 3, 'Mahish': 3, 'Vyaghra': 1, 'Mriga': 2, 'Vanar': 0, 'Nakul': 3, 'Singh': 1},
        'Sarpa': {'Ashwa': 3, 'Gaja': 3, 'Mesh': 2, 'Sarpa': 4, 'Shwan': 2, 'Marjara': 1, 'Mushak': 1, 'Gau': 1, 'Mahish': 1, 'Vyaghra': 2, 'Mriga': 2, 'Vanar': 2, 'Nakul': 0, 'Singh': 2},
        'Shwan': {'Ashwa': 2, 'Gaja': 2, 'Mesh': 1, 'Sarpa': 2, 'Shwan': 4, 'Marjara': 2, 'Mushak': 1, 'Gau': 2, 'Mahish': 2, 'Vyaghra': 1, 'Mriga': 0, 'Vanar': 2, 'Nakul': 1, 'Singh': 1},
        'Marjara': {'Ashwa': 2, 'Gaja': 2, 'Mesh': 2, 'Sarpa': 1, 'Shwan': 2, 'Marjara': 4, 'Mushak': 0, 'Gau': 2, 'Mahish': 2, 'Vyaghra': 1, 'Mriga': 3, 'Vanar': 3, 'Nakul': 2, 'Singh': 1},
        'Mushak': {'Ashwa': 2, 'Gaja': 2, 'Mesh': 1, 'Sarpa': 1, 'Shwan': 1, 'Marjara': 0, 'Mushak': 4, 'Gau': 2, 'Mahish': 2, 'Vyaghra': 2, 'Mriga': 2, 'Vanar': 2, 'Nakul': 1, 'Singh': 2},
        'Gau': {'Ashwa': 1, 'Gaja': 2, 'Mesh': 3, 'Sarpa': 1, 'Shwan': 2, 'Marjara': 2, 'Mushak': 2, 'Gau': 4, 'Mahish': 3, 'Vyaghra': 0, 'Mriga': 3, 'Vanar': 2, 'Nakul': 2, 'Singh': 1},
        'Mahish': {'Ashwa': 0, 'Gaja': 3, 'Mesh': 3, 'Sarpa': 1, 'Shwan': 2, 'Marjara': 2, 'Mushak': 2, 'Gau': 3, 'Mahish': 4, 'Vyaghra': 1, 'Mriga': 2, 'Vanar': 2, 'Nakul': 2, 'Singh': 1},
        'Vyaghra': {'Ashwa': 1, 'Gaja': 1, 'Mesh': 1, 'Sarpa': 2, 'Shwan': 1, 'Marjara': 1, 'Mushak': 2, 'Gau': 1, 'Mahish': 1, 'Vyaghra': 4, 'Mriga': 1, 'Vanar': 1, 'Nakul': 2, 'Singh': 1},
        'Mriga': {'Ashwa': 3, 'Gaja': 2, 'Mesh': 2, 'Sarpa': 2, 'Shwan': 0, 'Marjara': 3, 'Mushak': 2, 'Gau': 3, 'Mahish': 2, 'Vyaghra': 1, 'Mriga': 4, 'Vanar': 2, 'Nakul': 2, 'Singh': 1},
        'Vanar': {'Ashwa': 3, 'Gaja': 3, 'Mesh': 0, 'Sarpa': 2, 'Shwan': 2, 'Marjara': 3, 'Mushak': 2, 'Gau': 2, 'Mahish': 2, 'Vyaghra': 1, 'Mriga': 2, 'Vanar': 4, 'Nakul': 3, 'Singh': 2},
        'Nakul': {'Ashwa': 2, 'Gaja': 2, 'Mesh': 3, 'Sarpa': 0, 'Shwan': 1, 'Marjara': 2, 'Mushak': 1, 'Gau': 2, 'Mahish': 2, 'Vyaghra': 2, 'Mriga': 2, 'Vanar': 3, 'Nakul': 4, 'Singh': 2},
        'Singh': {'Ashwa': 1, 'Gaja': 0, 'Mesh': 1, 'Sarpa': 2, 'Shwan': 1, 'Marjara': 1, 'Mushak': 2, 'Gau': 1, 'Mahish': 1, 'Vyaghra': 1, 'Mriga': 1, 'Vanar': 2, 'Nakul': 2, 'Singh': 4}
    }
    
    male_yoni = get_yoni(nakshatra_male)
    female_yoni = get_yoni(nakshatra_female)
    yoni_kuta = yoni_compatibility[female_yoni][male_yoni]
    
    if male_yoni == 'Mesh':
        yoni_kuta = Mesh_Yoni_Norm[female_yoni]
    
    return yoni_kuta

################ Graha Maitri Kuta################

def calculate_graha_mitra_kuta(nakshatra_male, pada_male, nakshatra_female, pada_female):
    male_rashi = get_rashi(nakshatra_male,pada_male)
    female_rashi = get_rashi(nakshatra_female,pada_female)
    
    rashi_lord_mapping = {
    'Aries': 'Mars',
    'Taurus': 'Venus',
    'Gemini': 'Mercury',
    'Cancer': 'Moon',
    'Leo': 'Sun',
    'Virgo': 'Mercury',
    'Libra': 'Venus',
    'Scorpio': 'Mars',
    'Sagittarius': 'Jupiter',
    'Capricorn': 'Saturn',
    'Aquarius': 'Saturn',
    'Pisces': 'Jupiter'
    }
    
    male_rashi_lord = rashi_lord_mapping[male_rashi]
    female_rashi_lord = rashi_lord_mapping[female_rashi]
    
    gra_maitri_scores = {
    'Sun': {'Sun': 5, 'Moon': 5, 'Mars': 5, 'Mercury': 4, 'Jupiter': 5, 'Venus': 0, 'Saturn': 0},
    'Moon': {'Sun': 5, 'Moon': 5, 'Mars': 4, 'Mercury': 1, 'Jupiter': 4, 'Venus': 0.5, 'Saturn': 0.5},
    'Mars': {'Sun': 5, 'Moon': 4, 'Mars': 5, 'Mercury': 0.5, 'Jupiter': 5, 'Venus': 3, 'Saturn': 0.5},
    'Mercury': {'Sun': 4, 'Moon': 1, 'Mars': 0.5, 'Mercury': 5, 'Jupiter': 0.5, 'Venus': 5, 'Saturn': 4},
    'Jupiter': {'Sun': 5, 'Moon': 4, 'Mars': 5, 'Mercury': 0.5, 'Jupiter': 5, 'Venus': 0.5, 'Saturn': 3},
    'Venus': {'Sun': 0, 'Moon': 0.5, 'Mars': 3, 'Mercury': 5, 'Jupiter': 0.5, 'Venus': 5, 'Saturn': 5},
    'Saturn': {'Sun': 0, 'Moon': 0.5, 'Mars': 0.5, 'Mercury': 4, 'Jupiter': 3, 'Venus': 5, 'Saturn': 5}
    }
    
    return gra_maitri_scores[female_rashi_lord][male_rashi_lord]


################ Gana Kuta################

def calculate_gana_kuta(nakshatra_male, nakshatra_female):
    gana_male = nakshatra_to_gana[nakshatra_male]
    gana_female = nakshatra_to_gana[nakshatra_female]
    
    # Calculate basic Gana score
        
    gana_score = 0
    if gana_male == gana_female:
        gana_score = 6
    elif (gana_male == 'Deva' and gana_female == 'Manushya') or (gana_male == 'Manushya' and gana_female == 'Deva'):
        gana_score = 6 if gana_male == 'Deva' else 5
    elif (gana_male == 'Rakshasha' and gana_female == 'Deva'):
        gana_score = 1
        
    return gana_score
    

        
################ Bhakoot Kuta################
def get_bhakoot_score(nakshatra_male, pada_male, nakshatra_female, pada_female):
    male_rashi = get_rashi(nakshatra_male,pada_male)
    female_rashi = get_rashi(nakshatra_female,pada_female)
    return bakoot_df[male_rashi][female_rashi]

    
################ Nadi Kuta################

def calculate_nadi_kuta(nakshatra_male, nakshatra_female):
    male_nadi = nadi_map.get(nakshatra_male)
    female_nadi = nadi_map.get(nakshatra_female)
    
    nadi_dosha = True
    if male_nadi != female_nadi:
        nadi_dosha = False
    
    if nadi_dosha:
        score = 0
    else:
        score = 8

    return score
            

################ Ashtakaoota Matching################
def ashtaka_kuta(nakshatra_male, pada_male, nakshatra_female, pada_female,male_navamsa_rashi=None, female_navamsa_rashi=None,both_belong = False):
    varna_score = calculate_varna_score(nakshatra_male, pada_male, nakshatra_female, pada_female)
    vashya_score = calculate_vashya_kuta_score(nakshatra_male, pada_male, nakshatra_female, pada_female)
    tara_score = calculate_tara_kuta_score(nakshatra_male, nakshatra_female)[0]
    yoni_score = calculate_yoni_kuta(nakshatra_male, nakshatra_female)
    gm_score = calculate_graha_mitra_kuta(nakshatra_male, pada_male, nakshatra_female, pada_female)
    
    gana_score = calculate_gana_kuta(nakshatra_male, nakshatra_female)
    bak_score = get_bhakoot_score(nakshatra_male, pada_male, nakshatra_female, pada_female)
    nadi_score = calculate_nadi_kuta(nakshatra_male, nakshatra_female)
    
    total_score = varna_score + vashya_score + tara_score + yoni_score + gm_score + gana_score + bak_score + nadi_score
    return total_score,varna_score,vashya_score,tara_score,yoni_score,gm_score,gana_score,bak_score,nadi_score


    
    
    
            
    
    

