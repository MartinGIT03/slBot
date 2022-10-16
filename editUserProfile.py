import json


editHallplats = str(input("Andra hallplatser? ja eller nej "))

if editHallplats == "ja" or editHallplats == "Ja":
    orginHallplats = str(input("Vilken hallplats aker du ifran? "))
    destinationHallplats = str(input("Vilken hallplats vill du komma till? "))

if editHallplats == "nej" or editHallplats == "Nej":
    with open("userProfile.json", "r") as file:
        data = json.load(file)
        orginHallplats = data["orginHallplats"]
        destinationHallplats = data["destinationHallplats"]

TID = str(input("Nar ska du komma fram? "))
nextDay = str(input("Next day or not? ja eller nej? "))

with open("userProfile.json", "w") as file:
    userProfile = {"orginHallplats": orginHallplats, "destinationHallplats": destinationHallplats, "TID": TID, "nextDay": nextDay}

    json.dump(userProfile, file, indent=6)


