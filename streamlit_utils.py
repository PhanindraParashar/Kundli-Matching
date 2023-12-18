from detailed_utils import * 

def data_phani_simple():
    nakshatra_male = 'Pushya'
    pada_male = 4
    
    Nakshatra = []
    Pada = []

    TS = []
    Varna = []
    Vashya = []
    Tara = []
    Yoni = []
    Gm = []
    Gana = []
    Bakoot = []
    Nadi = []

    for nakshatra_female in json.load(open('nakshatra_rashi_mapping.json')).keys():
        for pada_female in [1, 2, 3, 4]:
            total_score,varna_score,vashya_score,tara_score,yoni_score,gm_score,gana_score,bak_score,nadi_score = ashtaka_kuta(nakshatra_male, pada_male, nakshatra_female,pada_female)
                    
            Nakshatra.append(nakshatra_female)
            Pada.append(pada_female)
            
            TS.append(total_score)
            Varna.append(varna_score)
            Vashya.append(vashya_score)
            Tara.append(tara_score)
            Yoni.append(yoni_score)
            Gm.append(gm_score)
            Gana.append(gana_score)
            Bakoot.append(bak_score)
            Nadi.append(nadi_score)
                    
                    
                    
    df = pd.DataFrame()
    df['Nakshatra'] = Nakshatra
    df['Pada'] = Pada

    df['Total'] = TS
    df['Varna'] = Varna
    df['Vashya'] = Vashya
    df['Tara'] = Tara
    df['Yoni'] = Yoni
    df['Graha_Maitri'] = Gm 
    df['Gana'] = Gana
    df['Bakoot'] = Bakoot
    df['Nadi'] = Nadi

    df = df.sort_values(by=['Total'],ascending=False).pipe(pipe_reset_index)

    return df
        