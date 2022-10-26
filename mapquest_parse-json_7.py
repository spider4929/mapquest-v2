from contextlib import redirect_stdout
import urllib.parse
import requests
import sys

from termcolor import colored, cprint
from prettytable import PrettyTable

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "AYkoyibLjuWaN0x49w1AcXGyA20orQPG"
dividerError = colored("****************************","red")
dividerSuccess = colored("============================================","green")

def grey(word):
    return colored(word,"grey")
def red(word):
    return colored(word,"red")
def green(word):
    return colored(word,"green")
def yellow(word):
    return colored(word,"yellow")
def blue(word):
    return colored(word,"blue")
def magenta(word):
    return colored(word,"magenta")
def cyan(word):
    return colored(word,"cyan")
def white(word):
    return colored(word,"white")

while True:
    counter = 0
    orig = input("Starting Location: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination: ")
    if dest == "quit" or dest == "q":
        break
    
    user_input = input("Imperial or Metric\n")
    if user_input.lower() == 'imperial':
        unit = 0
    elif user_input.lower() == 'metric':
        unit = 1
    else:
        print(red("Invalid Input!"))
        break
    url = main_api + urllib.parse.urlencode({"key":key, "from":orig, "to":dest})
    print("URL: " + (url))
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    if json_status == 0:
        print("API Status: " + green(str(json_status)) + " = A successful route call.\n")
        print(dividerSuccess)
        print("Directions from " + yellow((orig)) + " to " + magenta((dest)))
        print("Trip Duration: " + blue((json_data["route"]["formattedTime"])))
        if unit == 0:
            print("Miles: " + blue("{:.2f}".format((json_data["route"]["distance"])*1)))
            print("Fuel Used (Gal): " + blue("{:.2f}".format((json_data["route"]["fuelUsed"])*1)))
            t = PrettyTable(['Direction','Distance (mi)'])
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                counter += 1
                if counter % 2 == 0:
                    t.add_row([(grey(each["narrative"])), grey(str("{:.2f}".format((each["distance"])*1)))])
                else:
                    t.add_row([(each["narrative"]), str("{:.2f}".format((each["distance"])*1))])
        else:
            print("Kilometers: " + blue("{:.2f}".format((json_data["route"]["distance"])*1.61)))
            print("Fuel Used (Ltr): " + blue("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)))
            t = PrettyTable(['Direction','Distance (km)'])
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                counter += 1
                if counter % 2 == 0:
                    t.add_row([(grey(each["narrative"])), grey(str("{:.2f}".format((each["distance"])*1.61)))])
                else:
                    t.add_row([(each["narrative"]), str("{:.2f}".format((each["distance"])*1))])
        print(t)
        print(dividerSuccess)
    elif json_status == 402:
        print(dividerError)
        print("Status Code: " + red(str(json_status)) + "; Invalid user inputs for one or both locations.")
        print(dividerError)
    elif json_status == 611:
        print(dividerError)
        print("Status Code: " + red(str(json_status)) + "; Missing an entry for one or both locations.")
        print(dividerError)
    else:
        print(dividerError)
        print("Status Code: " + red(str(json_status)) + "; Refer to: ")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print(dividerError)
