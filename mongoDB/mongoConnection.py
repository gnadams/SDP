from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId, Decimal128


uri = "mongodb+srv://gna5:mLlcsUw7PwPefhHH@cluster08.d5vve.mongodb.net/?retryWrites=true&w=majority&appName=Cluster08"
CLIENT = MongoClient(uri, server_api=ServerApi('1'))
DATABASE = CLIENT["ConcussionData"]
COLLECTION = DATABASE["impacts"]
DOCUMENTS = COLLECTION.find()

def add_impact_record(collection, date, gyroscope_data, accelerometer_data, concussion_detected):
    """
    Adds a new document to the MongoDB collection with the specified values.
    
    :param date: String (e.g., "3/4/2025")
    :param gyroscope_data: List of integers [x, y, z]
    :param accelerometer_data: List of floats [x, y, z]
    :param concussion_detected: Boolean (True/False)
    """
    document = {
        "_id": ObjectId(),  # Generate a new MongoDB ObjectId
        "date": date,
        "gyroscopeData": [float(val) for val in gyroscope_data],  # Ensure float values
        "AccelerometerData": [float(val) for val in accelerometer_data],  # Ensure float values
        "ConcussionDetected": concussion_detected
    }


    try:
        collection.insert_one(document)
        print("Document added successfully:", document)
    except:
        print("error adding document")

# prints out all documents for 'Impact'
def printDocuments():
    for doc in DOCUMENTS:
        print(doc)

def verifyConnection(client):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def main():
    client = MongoClient(uri, server_api=ServerApi('1'))
    verifyConnection(client)
    database = client["ConcussionData"]
    collection = database["impacts"]
    documents = collection.find()
    # returns all documents
    printDocuments()
    add_impact_record(collection, "3/11/2025", [50.0, 30.5, 45.2], [424.5124, 43.0, 54.52], False)



if __name__=="__main__":
    main()
