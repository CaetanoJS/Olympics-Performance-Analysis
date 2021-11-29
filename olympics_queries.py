import pymongo

class OlympicsQueries:
    def __init__(self, db_name):
        self.db_name = db_name

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
        pass

    
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