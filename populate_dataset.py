import ujson
import pymongo
import argparse

def populate(args):
    with open(args.olympics_json_pth, 'r') as file:
        olympics_data = ujson.load(file)
    
    with pymongo.MongoClient() as client:
        db = client[args.mongo_db_name]
        for collection_key in list(olympics_data):
            print("inserting {} collection".format(collection_key))
            for element_key in list(olympics_data[collection_key]):
                if str(type(olympics_data[collection_key][element_key])) == '<class \'bson.objectid.ObjectId\'>':
                    continue
                db[collection_key].insert_one(olympics_data[collection_key][element_key])
    
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--olympics_json_pth',
                        help='path to .json file containing olympics dataset'
                        type=str,
                        required=True)
    parser.add_argument('--mongo_db_name'
                        help='name of the mongo db where data will be stored'
                        type=str,
                        required=True)

    return parser.parse_args()

if __name__=='__main__':
    args = parse_opt()
    populate(args)

