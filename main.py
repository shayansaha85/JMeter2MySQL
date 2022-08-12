import JTL2HTML as j2h
import insertDB as idb
import dataFileForDB as dfdb

# jtlFilePath = "C:\\Users\\shaya\\Desktop\\push_results\\TestAPI_120822.jtl"
# jmeterBinLocation = "F:\\Tools\\apache-jmeter-5.4.3\\apache-jmeter-5.4.3\\bin"


def insertResults(jtlFilePath, jmeterBinLocation):
    j2h.jtl2html(jtlFilePath, jmeterBinLocation)
    o = dfdb.getDBData()
    idb.insert_data(o)