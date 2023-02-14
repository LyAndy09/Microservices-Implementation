import requests
import time
import json
import random

# Constant set to generate a list of all dogs, as they're all taller than min_height.
min_height = 1

# Pagination offset is set to 20 as the API only returns a max of 20 results
# In file list to save values loop and send to dog_names.json
breeds = []


# This is the function that allows the program to stay constantly running.
# It awaits the file "call_check.json" to be written to 1.
# After it is written to, the program will open and begin asking for input
def keepFileOpen():
    while True:
        try:
            call_check = open("call_check.json", "r")
            call_read = json.loads(call_check.read())
            call_check.close()
            if call_read == 1:
                return generateDogApi()
            else:
                print("Awaiting for call_check.json to be written")
                time.sleep(10)
                return keepFileOpen()
        except FileNotFoundError:
            print("Communication file not created. Creating one now.")
            return resetCallFile()


# This function sets the program back into an awaiting state.
def resetCallFile():
    call_check = open("call_check.json", "w")
    call_check.write("0")
    call_check.close()
    keepFileOpen()

# Initial call of this program uses the function getRandomBreed().
# The return of getRandomBreed is then sent to the api ninja API
# And generates the final file containing the returned API.
def generateDogApi():
    name = getRandomBreed()
    if name != None:

        api_url = 'https://api.api-ninjas.com/v1/dogs?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': 'REPLACE HERE'})
        #         print(response.text)

        with open("random_dog.json", "w", encoding='utf8') as generated:
            generated.write(json.dumps(response.json(), ensure_ascii=False))

        return resetCallFile()

    else:
        return generateDogApi()

# The purpose of this function is to check if the dog breed file has been generated.
# If the file is found, then the function will continue and return a random breed from the list.

def getRandomBreed():
    try:
        with open('dog_names.json', 'r') as user_file:
            file_contents = json.load(user_file)

            if len(file_contents) >= 10:
                random_choice = (random.choice(file_contents))
                print("Your random dog is: " + random_choice)
                time.sleep(3)

            else:
                print("Dog list not correctly generated...")

    except FileNotFoundError:
        return getDogNamesFile()

    return random_choice

# This function is how we generate the list of all breed names from API Ninjas.
# Because API Ninjas does not disclose all available breeds, we need to manually request
# All breeds and then save them to a file.
def getDogNamesFile():
    offset = -20
    for i in range(15):
        offset = offset + 20
        time.sleep(0.5)
        api_url = 'https://api.api-ninjas.com/v1/dogs?offset={}&min_height={}'.format(offset, min_height)
        response = requests.get(api_url, headers={'X-Api-Key': 'REPLACE HERE'})
        data = response.json()
        for i in range(len(data)):
            names = data[i]['name']
            breeds.append(names)
            save_file = open("dog_names.json", "w", encoding='utf8')
            json.dump(breeds, save_file, indent=4, ensure_ascii=False)
            save_file.close()
        print("Generating dog list. Please wait.")
    print("Dog list detected. Generating random dog now!")
    return getRandomBreed()

# Initial call of the program to begin.
keepFileOpen()

