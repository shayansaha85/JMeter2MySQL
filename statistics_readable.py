import json

def get_statistics_data():
    file = open("./htmlReport/statistics.json", "r")
    s = str(file.read())
    file.close()

    d = json.loads(s)
    return d

