import statistics_readable as sr


def getDBData():
    d = sr.get_statistics_data()
    
    output = {
        "totalSamples": d["Total"]["sampleCount"],
        "minResTime" : round(d["Total"]["minResTime"],2),
        "avgResTime" : round(d["Total"]["meanResTime"],2),
        "maxResTime" : round(d["Total"]["maxResTime"],2),
        "90pct" : round(d["Total"]["pct1ResTime"],2),
        "95pct" : round(d["Total"]["pct2ResTime"],2),
        "99pct" : round(d["Total"]["pct3ResTime"],2),
        "throughput" : round(d["Total"]["throughput"],2)
    }

    return output