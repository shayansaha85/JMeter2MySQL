from flask import *
import pymysql.cursors
import os
from jproperties import Properties


app = Flask(__name__)


def getCreds():
    configs = Properties()

    with open('connection.properties', 'rb') as config_file:
        configs.load(config_file)

    host = str(configs.get("host").data)
    user = str(configs.get("user").data)
    password = str(configs.get("password").data)
    database = str(configs.get("database").data)

    creds = {
        "host": "",
        "user": "",
        "password": "",
        "database": ""
    }

    creds["host"] = host
    creds["user"] = user
    creds["password"] = password
    creds["database"] = database

    return creds


def insertResults(jtlFilePath, jmeterBinLocation):
    jtl2html(jtlFilePath, jmeterBinLocation)
    o = getDBData()
    insert_data(o)


def getDBData():
    d = get_statistics_data()

    output = {
        "totalSamples": d["Total"]["sampleCount"],
        "minResTime": round(d["Total"]["minResTime"], 2),
        "avgResTime": round(d["Total"]["meanResTime"], 2),
        "maxResTime": round(d["Total"]["maxResTime"], 2),
        "90pct": round(d["Total"]["pct1ResTime"], 2),
        "95pct": round(d["Total"]["pct2ResTime"], 2),
        "99pct": round(d["Total"]["pct3ResTime"], 2),
        "throughput": round(d["Total"]["throughput"], 2)
    }

    return output


def insert_data(d):
    creds = getCreds()
    connection = pymysql.connect(
        host=creds["host"],
        user=creds["user"],
        password=creds["password"],
        database=creds["database"]
    )

    cursor = connection.cursor()
    sqlForCreatingTable = """
    create table results (
	totalSamples int,
	minResTime decimal(6,2),
	avgResTime decimal(6,2),
	maxResTime decimal(6,2),
	'90pct' decimal(6,2),
	'95pct' decimal(6,2),
	'99pct' decimal(6,2),
	throughput decimal(6,2)
    )
    """
    cursor.execute(sqlForCreatingTable)

    print("TABLE CREATED")

    sql = "insert into resuts(totalSamples, minResTime, avgResTime, maxResTime, 90pct, 95pct, 99pct, throughput) values (%s, %s, %s, %s,%s, %s, %s, %s)"

    cursor.execute(sql, (d["totalSamples"], d["minResTime"], d["avgResTime"],
                   d["maxResTime"], d["90pct"], d["95pct"], d["99pct"], d["throughput"]))

    connection.commit()
    
    print("DATA INSERTED")


def jtl2html(jtlFilePath, jmeterBinLocation):
    os.system("mkdir htmlReport")
    binPath = str(os.path.join(jmeterBinLocation, "jmeter.bat"))
    print(binPath)
    command = binPath + " -g " + jtlFilePath + " -o htmlReport"
    try:
        os.system(command)
        print("HTML Report Created")
    except:
        print("HTML Report Creation Failed")


def get_statistics_data():
    file = open("./htmlReport/statistics.json", "r")
    s = str(file.read())
    file.close()

    d = json.loads(s)
    return d


@app.route("/insert", methods=["POST"])
def insert():
    msg = ""
    try:
        payload = request.get_json()
        jtlFilePath = str(payload["jtl_path"])
        jmeterBinPath = str(payload["jmeter_bin"])
        insertResults(jtlFilePath, jmeterBinPath)
        msg = {"message": "results inserted successfully"}
    except:
        msg = {"message": "error in inserting data"}

    return msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7171)
