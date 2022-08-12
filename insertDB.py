import pymysql.cursors

def insert_data(d):
    connection= pymysql.connect(
        host="localhost",
        user="root",
        password="shayan",
        database="jmeterresults"
    )


    cursor= connection.cursor()

    sql="insert into resuts(totalSamples, minResTime, avgResTime, maxResTime, 90pct, 95pct, 99pct, throughput) values (%s, %s, %s, %s,%s, %s, %s, %s)"

    cursor.execute(sql, (d["totalSamples"],d["minResTime"],d["avgResTime"],d["maxResTime"],d["90pct"],d["95pct"],d["99pct"],d["throughput"]))

    connection.commit()
    print("DATA INSERTED")