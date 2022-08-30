from venv import create
from flask import *
import pymysql.cursors
import os
from jproperties import Properties
import uuid
import shutil

app = Flask(__name__)

html_folder_name = {
    "htmlReport" : ""
}

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


def insertResults(jtlFilePath, jmeterBinLocation, htmlreport_folder):
    jtl2html(jtlFilePath, jmeterBinLocation, htmlreport_folder)
    o = getDBData(htmlreport_folder)
    insert_data(o)


def getDBData(htmlreport_folder):
    d = get_statistics_data(htmlreport_folder)
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


def insert_data(d):
    creds = getCreds()
    connection = pymysql.connect(
        host=creds["host"],
        user=creds["user"],
        password=creds["password"],
        database=creds["database"]
    )

    cursor = connection.cursor()
    try:
        sqlForCreatingTable = """
        create table results (totalSamples int,minResTime decimal(6,2),avgResTime decimal(6,2),maxResTime decimal(6,2),90pct decimal(6,2),95pct decimal(6,2),99pct decimal(6,2),throughput decimal(6,2))
        """
        cursor.execute(sqlForCreatingTable)
        print("TABLE CREATED")
    except:
        print("TABLE ALREADY EXISTED")

    sql = "insert into results(totalSamples, minResTime, avgResTime, maxResTime, 90pct, 95pct, 99pct, throughput) values (%s, %s, %s, %s,%s, %s, %s, %s)"

    cursor.execute(sql, (d["totalSamples"], d["minResTime"], d["avgResTime"],
                   d["maxResTime"], d["90pct"], d["95pct"], d["99pct"], d["throughput"]))

    connection.commit()
    
    print("DATA INSERTED")

def create_dir():
    folder_name = str(uuid.uuid4())
    os.mkdir(folder_name)
    return folder_name



def jtl2html(jtlFilePath, jmeterBinLocation, htmlreport_folder):
    binPath = str(os.path.join(jmeterBinLocation, "jmeter.bat"))
    print(binPath)
    command = binPath + " -g " + jtlFilePath + " -o " + htmlreport_folder
    try:
        os.system(command)
        print("HTML Report Created")
    except:
        print("HTML Report Creation Failed")


def get_statistics_data(htmlreport_folder):
    statistics_path = os.path.join(htmlreport_folder, "statistics.json")
    file = open(statistics_path, "r")
    s = str(file.read())
    file.close()
    d = json.loads(s)
    return d


@app.route("/insert", methods=["POST"])
def insert():
    msg = ""
    html_folder_name["htmlReport"] = create_dir()
    try:
        payload = request.get_json()
        jtlFilePath = str(payload["jtl_path"])
        jmeterBinPath = str(payload["jmeter_bin"])
        insertResults(jtlFilePath, jmeterBinPath, html_folder_name["htmlReport"])
        msg = {"message": "results inserted successfully"}
        shutil.rmtree(html_folder_name["htmlReport"])
    except:
        msg = {"message": "error in inserting data"}

    return msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7171)
