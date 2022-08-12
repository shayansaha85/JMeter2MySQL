from flask import *
import main as m

app = Flask(__name__)

@app.route("/insert", methods = ["POST"])
def insert():
    msg = ""
    try:
        payload = request.get_json()
        jtlFilePath = str(payload["jtl_path"])
        jmeterBinPath = str(payload["jmeter_bin"])
        m.insertResults(jtlFilePath, jmeterBinPath)
        msg = {"message" : "results inserted successfully"}
    except:
        msg = {"message" : "error in inserting data"}

    return msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    


