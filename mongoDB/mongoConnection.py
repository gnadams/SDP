from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId, Decimal128


uri = "mongodb+srv://gna5:mLlcsUw7PwPefhHH@cluster08.d5vve.mongodb.net/?retryWrites=true&w=majority&appName=Cluster08"
CLIENT = MongoClient(uri, server_api=ServerApi('1'))
DATABASE = CLIENT["ConcussionData"]
COLLECTION = DATABASE["impacts"]
DOCUMENTS = COLLECTION.find()

def add_impact_record(collection, date, gyroscope_data, accelerometer_data, concussion_detected, force):
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
        "force": force,
        "ConcussionDetected": concussion_detected
    }


    try:
        collection.insert_one(document)
        print("Document added successfully:", document)
    except:
        print("error adding document")

def retrieveImpactData():
        uri = "mongodb+srv://gna5:mLlcsUw7PwPefhHH@cluster08.d5vve.mongodb.net/?retryWrites=true&w=majority&appName=Cluster08"
        client = MongoClient(uri, server_api=ServerApi('1'))
        database = client["ConcussionData"]
        collection = database["impacts"]
        documents = collection.find()
        #print("Documents: ", documents)
        results = []
        for doc in documents:
            #print(doc)
            try:
                processed_doc = {
            "date": str(doc["date"]),
            "gyroscope1": {
                "x": float(doc["gyroscopeData1"]["x"]),
                "y": float(doc["gyroscopeData1"]["y"]),
                "z": float(doc["gyroscopeData1"]["z"])
            },
            "gyroscope2": {
                "x": float(doc["gyroscopeData2"]["x"]),
                "y": float(doc["gyroscopeData2"]["y"]),
                "z": float(doc["gyroscopeData2"]["z"])
            },
            "gyroscope3": {
                "x": float(doc["gyroscopeData3"]["x"]),
                "y": float(doc["gyroscopeData3"]["y"]),
                "z": float(doc["gyroscopeData3"]["z"])
            },
            "accelerometer1": {
                "x": float(doc["AccelerometerData1"]["x"]),
                "y": float(doc["AccelerometerData1"]["y"]),
                "z": float(doc["AccelerometerData1"]["z"])
            },
            "accelerometer2": {
                "x": float(doc["AccelerometerData2"]["x"]),
                "y": float(doc["AccelerometerData2"]["y"]),
                "z": float(doc["AccelerometerData2"]["z"])
            },
            "accelerometer3": {
                "x": float(doc["AccelerometerData3"]["x"]),
                "y": float(doc["AccelerometerData3"]["y"]),
                "z": float(doc["AccelerometerData3"]["z"])
            },
            "force": float(doc["force"]),
            "helmetID": int(doc["helmetID"]),
            "ConcussionDetected": doc["ConcussionDetected"]
                }
                results.append(processed_doc)

            except Exception as e:
                print(f"Error processing document: {e}")
                print(f"The document with the error: {doc}")
                print("\0")
        return results


def calculateAverages(impacts):
    try:
        if impacts[0]["date"] == None:
            print("impacts[0] is null")
            return None
    except:
        print("impacts[0] is null")
        return None
    data = {
        "latestImpact": impacts[0]["date"],
        "AverageForce": 0.0,
        "totalConcussions": 0,
        "totalImpacts": 0,
        "timestamps" : [],
    }
    impactCount = 0
    impactSum = 0
    
    print("impacts in calculateAverages: ", impacts)
    print("latest_impact in calculateAverages: ", data["latestImpact"])
    print("impacts[0] in calculateAverages: ", impacts[0])
    for impact in impacts:
        impactCount += 1
        impactSum += impact["force"]
        data["timestamps"].append(impact["date"])
        if impact["date"] > data["latestImpact"]:
            data["latestImpact"] = impact["date"]
        if impact["ConcussionDetected"]:
            data["totalConcussions"] += 1
    data["AverageForce"] = impactSum / impactCount if impactCount > 0 else 0.0
    data["totalImpacts"] = impactCount
    return data

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
    results = retrieveImpactData()
    print(results)
        # returns all documents
    #printDocuments()
    #add_impact_record(collection, "3/11/2025", [50.0, 30.5, 45.2], [424.5124, 43.0, 54.52], False)



if __name__=="__main__":
    main()
