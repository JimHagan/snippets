"""
export AWS_ACCESS_KEY_ID=KEY_ID_GOES_HERE
export AWS_SECRET_ACCESS_KEY=KEY_GOES_HERE
"""

from dynamodb_mapper.model import DynamoDBModel
from boto.dynamodb.condition import GT
from dynamodb_mapper.model import ConnectionBorg

class DoomMap(DynamoDBModel):
	__table__=u"doom_map"
	__hash_key__=u"episode"
	__range_key__=u"map"
	__schema__={
		u"episode": int,
		u"map": int,
		u"name"ll
        : unicode,
		u"cheats": set,
		}
	__defaults__={
		"cheats": set([u"Konami"]),
		}


if __name__ == "__main__":
    conn = ConnectionBorg()
    conn.create_table(DoomMap, 10, 10, wait_for_active=True)
    
    e1m1 = DoomMap()

    e1m1.episode = 1
    e1m1.map = 1
    e1m1.name = u"Hangar"
    e1m1.cheats = set([u"idkfa", u"iddqd", u"idclip"])
    e1m1.save()

    # Later on, retrieve that same object from the DB...
    e1m1 = DoomMap.get(1, 1)    
    
    # query all maps of episode 1
    e1_maps = DoomMap.query(1)

    for m in e1_maps:
        print m.to_json_dict()
        
    
    e1_maps_after_1 = DoomMap.query(1, range_key_condition=GT(1))
    
    for m in e1_maps_after_1:
        print m.to_json_dict()
        
        
    #access data without ORM
    table=conn.get_table("doom_map")
    for row in table.query(1):
        print row
        
    for row in table.query(1, GT(1)):
        print row
        
    for t in tbl.query(1, None, attributes_to_get=["episode", "map", "name"]):
        print t