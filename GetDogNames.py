import requests
import time
import random
import json

# Constant set to generate a list of all dogs, as they're all taller than min_height.
min_height = 1

# Pagination offset is set to 20 as the API only returns a max of 20 results
breeds = []


#This is the function that allows the program to stay constantly running.
#It awaits the file "call_check.json" to be written to 1.
#After it is written to, the program will open and begin asking for input

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


def resetCallFile():
    call_check = open("call_check.json", "w")
    call_check.write("0")
    call_check.close()
    keepFileOpen()

def generateDogApi():
    name = getUserInput()
    if name != None:

        api_url = 'https://api.api-ninjas.com/v1/dogs?name={}'.format(name)
        response = requests.get(api_url, headers={'X-Api-Key': ''})
        #         print(response.text)

        with open("random_dog.json", "w", encoding='utf8') as generated:
            generated.write(json.dumps(response.json(), ensure_ascii=False))

        return resetCallFile()

    else:
        return generateDogApi()

def getUserInput():
    prompt = input("Would you like to generate a random dog? (Y/N) ").upper()
    while True:
        if prompt == "N":
            print("Okay, goodbye.")
            with open('call_check.json', "w") as call_write:
                call_write.write("0")

            return keepFileOpen()

        elif prompt == "Y":
            check_generated = input("Have you generated the list of dogs? (Y/N) ").upper()

            if check_generated == "Y":
                return getRandomBreed()

            elif check_generated == "N":
                print("Okay let's retrieve the list of dogs now.")
                return getDogNamesFile()

            else:
                print("Input out of range, let's try again.")
                getUserInput()
        else:
            print("Input out of range, let's try again.")
            getUserInput()


def getDogNamesFile():
    offset = -20
    for i in range(15):
        offset = offset + 20
        time.sleep(0.5)
        api_url = 'https://api.api-ninjas.com/v1/dogs?offset={}&min_height={}'.format(offset, min_height)
        response = requests.get(api_url, headers={'X-Api-Key': ''})
        data = response.json()
        for i in range(len(data)):
            names = data[i]['name']
            breeds.append(names)
            save_file = open("dog_names.json", "w", encoding='utf8')
            json.dump(breeds, save_file, indent=4, ensure_ascii=False)
            save_file.close()
        print("Generating dog list. Please wait.")
    print("Dog list has been generated. Generating your random dog now!")
    return getRandomBreed()


def getRandomBreed():
    with open('dog_names.json', 'r') as user_file:
        file_contents = json.load(user_file)

        if len(file_contents) >= 10:
            random_choice = (random.choice(file_contents))
            print("Your random dog is: " + random_choice)

        else:
            print("Dog list not generated...")

    return random_choice



keepFileOpen()

