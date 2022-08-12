import os

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
