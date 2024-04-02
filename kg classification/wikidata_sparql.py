# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import os, csv

endpoint_url = "https://query.wikidata.org/sparql"
MAX_LEVEL = 2


def query(id):
    return """
SELECT ?item ?itemLabel 
WHERE 
{ 
  ?item wdt:P31|wdt:P279 wd:""" + id + """. 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
}"""


def query_path(id):
    return """
SELECT ?item ?itemLabel 
WHERE 
{ 
  ?item wdt:P31*|wdt:P279* wd:""" + id + """. 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
} LIMIT 5000"""


def query_prop(prop, id):
    return """
SELECT ?item ?itemLabel 
WHERE 
{ 
  ?item wdt:P31|wdt:""" + prop + """ wd:""" + id + """. 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
}"""


def query_general(id):
    return """
SELECT ?item ?itemLabel ?prop 
WHERE 
{
  ?item ?prop wd:""" + id + """.
  filter  (?prop != wdt:P101 && ?prop != wdt:P921 && ?prop != ps:P101 && ?prop != ps:P921 && ?prop != schema:about && ?prop != pq:P812 && ?prop != pq:P101
   && ?prop != ps:P509 && ?prop != pq:P509)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } 
# Helps get the label in your language, if not, then en language
} LIMIT 10000
    """

def query_disseminate(id):
    return """
SELECT ?item ?itemLabel  ?prop ?object ?objectLabel ?prop2 ?object2 ?object2Label
WHERE 
{
  VALUES (?item) { (wd:""" + id + """)}
  ?item ?prop ?object.
  ?object ?prop2 ?object2
          filter(strstarts(str(?prop), str(wdt:)) && strstarts(str(?object2), str(wd:)))
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
}
    """


def get_results(endpoint_url, query):
    try:
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()
    except:
        return {'results': {'bindings': []}}


def parse_results(results):
    response = []
    for result in results['results']['bindings']:
        tmp = result['item']['value'].replace('http://www.wikidata.org/entity/', '')
        response.append(
            {'wikidata_id': tmp, 'label': result['itemLabel']['value'].capitalize()}) if len(
            [r for r in response if r['wikidata_id'] == tmp]) == 0 else None

    return response


def parse_results_general(results):
    response = []
    for result in results['results']['bindings']:
        if 'http://www.wikidata.org/entity/statement/' in result['item']['value']:
            tmp = result['item']['value'].replace('http://www.wikidata.org/entity/statement/', '')
            tmp = tmp[:tmp.index('-')]

            response.append({'wikidata_id': tmp, 'label': result['itemLabel']['value'].capitalize()}) if len(
                [r for r in response if r['wikidata_id'] == tmp]) == 0 else None
        else:
            response.append(
                {'wikidata_id': result['item']['value'], 'label': result['itemLabel']['value'].capitalize()}) if len(
                [r for r in response if r['wikidata_id'] == result['item']['value']]) == 0 else None

    return response


def fetch_subclasses(wikidata_id, label, level):
    if level > MAX_LEVEL:
        return []

    childs = []
    results = get_results(endpoint_url, query(wikidata_id))
    print('Fetched {} subclasses for {}-{} - LEVEL {}'.format(len(results['results']['bindings']), label, wikidata_id,
                                                              level))
    for result in results["results"]["bindings"]:
        node = {}
        node['wikidata_id'] = result['item']['value'].replace('http://www.wikidata.org/entity/', '')
        node['label'] = result['itemLabel']['value']
        if len(results["results"]["bindings"]) < 10:
            node['childs'] = fetch_subclasses(node['wikidata_id'], node['label'], level + 1)
            node['child_count'] = len(node['childs'])
        else:
            node['childs'] = []

        childs.append(node)

    return childs


def write_to_file(writer, node, level):
    if level > MAX_LEVEL:
        return []

    for child in node['childs']:
        row = ['' for i in range(0, (level - 1) * 2)]
        row.extend([child['label'], child['wikidata_id']])
        writer.writerow(row)

        write_to_file(writer, child, level + 1)


def run():
    os.system("mkdir wikidata_results_metaclass; cd wikidata_results;")
    metaclass_id = 'Q19478619'  # Q19361238
    results = get_results(endpoint_url, query(metaclass_id))

    for result in results["results"]["bindings"]:
        node = {}
        node['wikidata_id'] = result['item']['value'].replace('http://www.wikidata.org/entity/', '')
        node['label'] = result['itemLabel']['value']

        node['childs'] = fetch_subclasses(node['wikidata_id'], node['label'], 1)
        node['child_count'] = len(node['childs'])

        file_name = node['label'] + '-' + node['wikidata_id'] + '.csv'
        print('Writing to file {}'.format(file_name))

        file = open("wikidata_results_metaclass/{}".format(file_name.replace("/", "_")), 'w', encoding='UTF8')
        writer = csv.writer(file)
        header = ['Label', 'Wikidata Id', 'Child Count']
        writer.writerow(header)
        for child in node['childs']:
            writer.writerow([child['label'], child['wikidata_id'], node['child_count']])

        file.close()

        print('Finished.')


if __name__ == '__main__':
    run()
