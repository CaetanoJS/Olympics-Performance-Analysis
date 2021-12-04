import pymongo
import pandas as pd
import numpy as np

hdi2olympics = {
    'Bolivia (Plurinational State of)' : 'Bolivia',
    'Cabo Verde' : 'Cape Verde',
    'Czechia' : 'Czech Republic',
    'Congo (Democratic Republic of the)' : 'D.R. Congo',
    'Eswatini (Kingdom of)' : 'Eswatini',
    'United Kingdom' : 'Great Britain',
    'Hong Kong, China (SAR)' : 'Hong Kong, China',
    'Iran (Islamic Republic of)' : 'Islamic Republic of Iran',
    "Lao People's Democratic Republic" : 'Lao P.D.R.',
    'Micronesia (Federated States of)' : 'Micronesia',
    'Palestine, State of' : 'Palestine',
    'China' : "People's Republic of China",
    'Korea (Republic of)' : 'Republic of Korea',
    'Moldova (Republic of)' : 'Republic of Moldova',
    'Saint Vincent and the Grenadines' : 'St Vincent & Grenadines',
    'Tanzania (United Republic of)' : 'Tanzania',
    'United States' : 'United States of America',
    'Venezuela (Bolivarian Republic of)' : 'Venezuela',
    'Viet Nam' : 'Vietnam'
}

olympics2hdi = {v: k for k, v in hdi2olympics.items()}

gdp2olympics = {
    'Bahamas, The' : 'Bahamas',
    'Cabo Verde' : 'Cape Verde',
    'Congo, Rep.' : 'Congo',
    'Congo, Dem. Rep.' : 'D.R. Congo',
    "Cote d'Ivoire" : "Côte d'Ivoire",
    'Egypt, Arab Rep.' : 'Egypt',
    'Swaziland' : 'Eswatini',
    'Gambia, The' : 'Gambia',
    'United Kingdom' : 'Great Britain',
    'Hong Kong SAR, China' : 'Hong Kong, China',
    'Iran, Islamic Rep.' : 'Islamic Republic of Iran',
    'Kyrgyz Republic' : 'Kyrgyzstan',
    'Lao PDR' : 'Lao P.D.R.',
    'Micronesia, Fed. Sts.' : 'Micronesia',
    'Macedonia, FYR' : 'North Macedonia',
    'China' : "People's Republic of China",
    'Korea, Rep.' : 'Republic of Korea',
    'Moldova' : 'Republic of Moldova',
    'St. Kitts and Nevis' : 'Saint Kitts and Nevis',
    'St. Lucia' : 'Saint Lucia',
    'Slovak Republic' : 'Slovakia',
    'St. Vincent and the Grenadines' : 'St Vincent & Grenadines',
    'United States' : 'United States of America',
    'Venezuela, RB' : 'Venezuela',
    'Virgin Islands (U.S.)' : 'Virgin Islands, US',
    'Yemen, Rep.' : 'Yemen'
}

olympics2gdp = {v: k for k, v in gdp2olympics.items()}

class OlympicsQueries:
    def __init__(self, db_name):
        self.db_name = db_name

    # BASICAS

    def get_medal_count_by_country(self, country_name):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]
            org_dict = db['Organisation'].find_one({'attributes.name': country_name})

            medal_count = {'gold': org_dict['attributes']['statistics']['gold'],
                           'silver': org_dict['attributes']['statistics']['silver'],
                           'bronze': org_dict['attributes']['statistics']['bronze']}
            
        return medal_count

    def get_medals_by_competitor(self, competitor_name):
        pass


    def get_medal_count_by_competitor(self, competitor_name):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]
            part_dict = db['Participant'].find_one({'attributes.name': competitor_name})

            medal_count = {'gold': part_dict['attributes']['statistics']['gold'],
                           'silver': part_dict['attributes']['statistics']['silver'],
                           'bronze': part_dict['attributes']['statistics']['bronze']}
            
        return medal_count


    def get_medalists_by_country(self, country_name):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]
            org_dict = db['Organisation'].find_one({'attributes.name': country_name})
            org_id = org_dict['id']
            country_participants = db['Participant'].find({'relationships.organisation.data.id':org_id})

            medalists = [participant for participant in country_participants if participant['attributes']['statistics']['total'] > 0]
            top_10_medalists = sorted(medalists, key=lambda  medalist: medalist['attributes']['statistics']['totalRank'])[:10]

            medalists_dict = {}

            for medalist in top_10_medalists:
                discipline_id = medalist['relationships']['discipline']['data']['id']
                discipline_dict = db['Discipline'].find_one({'id': discipline_id})
                discipline_name = discipline_dict['attributes']['name']

                if medalist['attributes']['participantType'] == 'TEAM':
                    medalist['attributes']['name'] = medalist['attributes']['name'] + ' ' + discipline_name + ' ' + 'Team'

                medalists_dict[medalist['attributes']['name']] = {'gold': medalist['attributes']['statistics']['gold'], 
                                                                  'silver': medalist['attributes']['statistics']['silver'],
                                                                  'bronze': medalist['attributes']['statistics']['bronze'],
                                                                  'discipline': discipline_name}

        return medalists_dict
    
    def get_countries_with_most_medals(self, num_countries):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]
            best_countries = db['Organisation'].find().sort('attributes.statistics.totalRank', pymongo.ASCENDING).limit(num_countries)

            best_countries_dict = {}
            for country in best_countries:
                best_countries_dict[country['attributes']['name']] = {'gold':country['attributes']['statistics']['gold'],
                                                                      'silver':country['attributes']['statistics']['silver'],
                                                                      'bronze':country['attributes']['statistics']['bronze']}

        return best_countries_dict

    def get_countries_with_most_medals_df(self, num_countries):
        best_countries = self.get_countries_with_most_medals(10)

        best_countries_df = pd.DataFrame(columns=['gold', 'silver', 'bronze'])
        for country in best_countries.keys():
            best_countries_df.loc[country] = best_countries[country]

        return best_countries_df


    # AVANCADAS

    def get_hdi_by_country(self, country_name):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]
            hdi_dict = db['hdi'].find_one({'country': country_name})

        return hdi_dict

    def get_gdp_by_country(self, country_name):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]
            gdp_dict = db['gdp'].find_one({'country': country_name})

        return gdp_dict

    def get_countries_with_no_medals(self):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]
            no_medal_countries = db['Organisation'].find({'attributes.statistics.total': 0})

        return [country['attributes']['name'] for country in no_medal_countries]

    def get_country_top_10_with_soceconomic_markers(self, gdp_year='2016', hdi_year='2019'):
        top_10_countries = self.get_countries_with_most_medals(10)
        
        result_df = pd.DataFrame(columns =['gold','silver', 'bronze', 'gdp 2016', 'hdi 2019'])

        for country in top_10_countries.keys():
            if country in list(olympics2gdp.keys()):
                country_gdp = self.get_gdp_by_country(olympics2gdp[country])
            else:
                country_gdp = self.get_gdp_by_country(country)
            if country in list(olympics2hdi.keys()):
                country_hdi = self.get_hdi_by_country(olympics2hdi[country])
            else:
                country_hdi = self.get_hdi_by_country(country)
                        
            if country_gdp == None:
                top_10_countries[country]['gdp '+str(gdp_year)] = None
            else:
                top_10_countries[country]['gdp '+str(gdp_year)] = country_gdp[gdp_year]
            
            if country_hdi == None:
                top_10_countries[country]['hdi '+str(hdi_year)] = None
            else:
                top_10_countries[country]['hdi '+str(hdi_year)] = country_hdi[hdi_year]

            result_df.loc[country] = top_10_countries[country]
        
        result_df.gold = result_df.gold.astype(int)
        result_df.silver = result_df.silver.astype(int)
        result_df.bronze = result_df.bronze.astype(int)

        result_df['gdp '+str(gdp_year)] = result_df['gdp '+str(gdp_year)].apply(lambda x: '${:,}'.format(int(x)) if not np.isnan(x) else 'Invalid')
        result_df['hdi '+str(hdi_year)] = result_df['hdi '+str(hdi_year)].apply(lambda x: x if not np.isnan(x) else 'Invalid')

        return result_df

    def get_top_medalists_df(self, country):
        
        top_medalists = self.get_medalists_by_country(country)

        result_df = pd.DataFrame(columns=['gold', 'silver','bronze','discipline'])
        for top_medalist in top_medalists.keys():
            result_df.loc[top_medalist] = top_medalists[top_medalist]

        return result_df


    def get_medal_count_x_socialeconomics(self, gdp_year='2016', hdi_year='2019'):
        with pymongo.MongoClient() as client:
            db = client[self.db_name]

            olympics_countries = db['Organisation'].find({},{'attributes.name': 1, 'attributes.statistics.total': 1})

            medal_count_by_hdi = []
            medal_count_by_gdp = []

            for country in olympics_countries:
                country_name = country['attributes']['name']
                country_medal_count = country['attributes']['statistics']['total']

                if country_name in list(olympics2hdi.keys()):
                    country_hdi = self.get_hdi_by_country(olympics2hdi[country_name])
                else:
                    country_hdi = self.get_hdi_by_country(country_name)
                if country_hdi:
                    medal_count_by_hdi.append((country_medal_count, country_hdi[hdi_year]))

                if country_name in list(olympics2gdp.keys()):
                    country_gdp = self.get_gdp_by_country(olympics2gdp[country_name])
                else:
                    country_gdp = self.get_gdp_by_country(country_name)
                if country_gdp:
                    medal_count_by_gdp.append((country_medal_count, country_gdp[gdp_year]))
            
            return {'medal_count_by_hdi': medal_count_by_hdi, 'medal_count_by_gdp': medal_count_by_gdp}
    
    def get_med_count_soceconomics_scatter_plot(self):
        med_count_socesonomics = self.get_medal_count_x_socialeconomics()

        medal_count_by_hdi = med_count_socesonomics['medal_count_by_hdi']
        medal_count_by_gdp = med_count_socesonomics['medal_count_by_gdp']

        hdi_data = [{'x': med_count, 'y': hdi} for med_count, hdi in medal_count_by_hdi]
        gdp_data = [{'x': med_count, 'y': gdp} for med_count, gdp in medal_count_by_gdp]

        return hdi_data, gdp_data

    def get_no_medal_countries_by_soceconomics(self, reverse=False, gdp_years=['2014', '2015', '2016'], hdi_years=['2017', '2018', '2019']):
        
        no_medal_countries = self.get_countries_with_no_medals()

        country_with_gdp = []
        country_with_hdi = []

        for country_name in no_medal_countries:

            if country_name in list(olympics2hdi.keys()):
                country_hdi = self.get_hdi_by_country(olympics2hdi[country_name])
            else:
                country_hdi = self.get_hdi_by_country(country_name)
            if country_hdi:
                country_with_hdi.append((country_name, np.mean([country_hdi[hdi_year] for hdi_year in hdi_years])))

            if country_name in list(olympics2gdp.keys()):
                country_gdp = self.get_gdp_by_country(olympics2gdp[country_name])
            else:
                country_gdp = self.get_gdp_by_country(country_name)
            if country_gdp:
                country_with_gdp.append((country_name, np.mean([country_gdp[gdp_year] for gdp_year in gdp_years])))
        
        country_with_hdi = [country for country in country_with_hdi if not np.isnan(country[1]) ]
        country_with_gdp = [country for country in country_with_gdp if not np.isnan(country[1]) ]
        
        return sorted(country_with_gdp, key=lambda x : x[1], reverse=reverse)[:10], sorted(country_with_hdi, key=lambda x : x[1], reverse=reverse)[:10]

    def get_no_medal_best_hdi(self):
        _, country_with_hdi = self.get_no_medal_countries_by_soceconomics(reverse=True)

        result_df = pd.DataFrame(columns=['hdi avg (2017-2019)'])
        for country in country_with_hdi:
            print(country)

            result_df.loc[country[0]] = country[1]

        return result_df

    def get_no_medal_best_gdp(self):
        country_with_gdp, _ = self.get_no_medal_countries_by_soceconomics(reverse=True)

        result_df = pd.DataFrame(columns=['gdp avg (2014-2016)'])
        for country in country_with_gdp:
            print(country)

            result_df.loc[country[0]] = country[1]

        return result_df

    def get_no_medal_worst_hdi(self):
        _, country_with_hdi = self.get_no_medal_countries_by_soceconomics()

        result_df = pd.DataFrame(columns=['hdi avg (2017-2019)'])
        for country in country_with_hdi:
            print(country)

            result_df.loc[country[0]] = country[1]

        return result_df

    def get_no_medal_worst_gdp(self):
        country_with_gdp, _ = self.get_no_medal_countries_by_soceconomics()

        result_df = pd.DataFrame(columns=['gdp avg (2014-2016)'])
        for country in country_with_gdp:
            print(country)

            result_df.loc[country[0]] = country[1]

        return result_df
