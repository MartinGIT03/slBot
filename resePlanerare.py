# Detta program raknar ut om taget kommer att komma itid nasta dag

import requests
import datetime 
import json

API_NYCKEL_RESEPLANERARE = ""
API_NYCKEL_PLATSUPPSLAG = "" # Skriv in din nyckel från trafiklab.se

def fetchUserProfile():
    with open("userProfile.json", "r") as file:
        data = json.load(file)
    return data

def getReseURL(datum):
    auto = str(input("Vill du kora auto? ja eller nej? Andra bara tid? Skriv bara tid "))
    auto = auto.lower()
    if auto == 'ja':
        data = fetchUserProfile()
        orginHallplats = data["orginHallplats"]
        destinationHallplats = data["destinationHallplats"]
        TID = data["TID"]

    if auto == 'nej':
        orginHallplats = str(input("Vilken hallplats aker du ifran? "))
        destinationHallplats = str(input("Vilken hallplats vill du komma till? "))
        TID = str(input("Nar ska du komma fram? "))

    if auto == 'tid':
        data = fetchUserProfile()
        orginHallplats = data["orginHallplats"]
        print(orginHallplats)
        destinationHallplats = data["destinationHallplats"]
        TID = str(input("Nar ska du komma fram? "))
 
# Sen hämtar vi ID-numret för den hållplatsen från Platsuppslag
    orginURL = "https://api.sl.se/api2/typeahead.json?key=" + API_NYCKEL_PLATSUPPSLAG + "&searchstring=" + orginHallplats +"&stationsonly=True&maxresults=1"

    destinationURL = "https://api.sl.se/api2/typeahead.json?key=" + API_NYCKEL_PLATSUPPSLAG + "&searchstring=" + destinationHallplats +"&stationsonly=True&maxresults=1"

    response = requests.get(orginURL)
    response_dictionary = response.json()["ResponseData"]
    ORGIN_ID = response_dictionary[0]["SiteId"] # ID:t som vi nu kan använda i nästa API-request

    response = requests.get(destinationURL)
    response_dictionary = response.json()["ResponseData"]
    DESTINATION_ID = response_dictionary[0]["SiteId"] # ID:t som vi nu kan använda i nästa API-request

    reseURL = "http://api.sl.se/api2/TravelPlannerV3_1/trip.json?key=" + API_NYCKEL_RESEPLANERARE + "&originId=" + ORGIN_ID + "&destId=" + DESTINATION_ID + "&searchForArrival=1&date=" + datum[:10] + "&time=" + TID 
    print(reseURL)
    reseFile = requests.get(reseURL)
   
    writeTrainLog(reseFile.json()) # Used for debugging fault in the train records  
    getTrainTime(reseFile.json())

def getTrainTime(data):
    print("Train arrives at starting destination at:\n") 
    
    for key in range(0, len(data["Trip"])):
        print(data["Trip"][key]["LegList"]["Leg"][0]["Origin"]["time"])

    print("----------------------------------------") 
    print("Train arrives at final destination at:\n") 
    for key in range(0, len(data["Trip"])):
        print(data["Trip"][key]["LegList"]["Leg"][0]["Destination"]["time"])

def getTime():
    data = fetchUserProfile()
    nextDay = data["nextDay"]
    if nextDay == 'ja' or nextDay == 'Ja':
        idagDatum = datetime.datetime.now()
        imorgonDatum = str(idagDatum + datetime.timedelta(days=1))
        getReseURL(imorgonDatum)
    if nextDay == 'nej' or nextDay == 'Nej':
        idagDatum = datetime.datetime.now()
        print(idagDatum)
        getReseURL(idagDatum)
    
def writeTrainLog(data):
    with open("log.json", "w") as file:
        json.dump(data, file, indent=6)




