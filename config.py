import pymongo
import certifi

me = {
    'name': 'Jason',
    'last_name': 'Ramirez',
    'email': '12ramirezjasons@gmail.com',
    'GitHub': 'https://github.com/JasonRamz'
}


con_str = "mongodb+srv://JasonRamz:158964Jrz@cluster0.abqgxy0.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database("bodega")
