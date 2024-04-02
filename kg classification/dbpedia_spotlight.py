import requests
import urllib
import datetime


def annotate_text(text, confidence=0.9):
    result = {}

    if not text:
        return []

    cutLength = 4000
    count = len(text) / cutLength + 1
    for i in range(int(count)):
        to = len(text) if len(text) < i * cutLength + cutLength - 1 else i * cutLength + cutLength - 1
        cut = text if len(text) < cutLength else text[i * cutLength: to]

        # if i == 20:
        #     break

        # print(cut)
        cut = cut.replace("\\{", "[")
        cut = cut.replace("\\}", "]")

        responsePlain = requests.get("http://api.dbpedia-spotlight.org/en/annotate?text=" +
                                urllib.parse.quote(cut) +
                                "&confidence=" + str(confidence) + "&support=0&spotter=Default&disambiguator=Default&policy=whitelist&types=&sparql=",
                                headers={'Accept':'application/json'})
        if responsePlain.status_code != 200:
            # print("ERROR : Status Code " + str(responsePlain.status_code) + " for Dbpedia Spotlight Request")
            continue

        response = responsePlain.json()

        for r in response['Resources'] if 'Resources' in response else []:
            offset =  int(r['@offset']) + i * cutLength
            item = {'offset': offset, 'uri': r['@URI'], 'surfaceForm': r['@surfaceForm'],
                    'types': r['@types']}

            result[item['uri']] = item


    return list(result.values())
