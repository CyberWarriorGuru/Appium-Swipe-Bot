from config import *
def fnReadJsonData():
    with open(ELEMENT_JSON, "r") as fp:
        data = json.load(fp=fp)
    return data

def fnCreateBotInstance(desired_cap, server_url):

    driver = webdriver.Remote(
        command_executor = server_url, 
        desired_capabilities = desired_cap
    )
    print(server_url, desired_cap)
    return driver

def fnGenerateNonRepeatNumber():
    randomList=[]
    while True:
        r=random.randint(0, 3)
        if r not in randomList:
            randomList.append(r)
            if len(randomList) == 2:
                break
    return randomList

