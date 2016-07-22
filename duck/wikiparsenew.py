import requests
from SPARQLWrapper.SPARQLUtils import deprecated
from bs4 import BeautifulSoup


def states_death_ratio(wiki_url):
    mymap = {}

    if wiki_url:
        source_code = requests.get(wiki_url)
    else:
        # source_code = requests.get('https://en.wikipedia.org/wiki/Hurricane_Wilma')
        source_code = requests.get('https://en.wikipedia.org/wiki/Hurricane_Katrina')
    soup = BeautifulSoup(source_code.content, "lxml")

    tables = soup.find_all('table', attrs={'class':'wikitable'})
    table = tables[1]
    rows = table.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values


    print(data)
    for d in data:
        if len(d) > 1:
            mymap[d[0]] = d[1]

    if mymap:
        return mymap


def us_states_population():
    mymap = {}
    source_code = requests.get('http://state.1keydata.com/state-population-2005.php')
    soup = BeautifulSoup(source_code.content, "lxml")

    table = soup.find('table', attrs={'class':'content3'})
    rows = table.find_all('tr')

    data_new = []
    for row in rows:
        cols = row.find_all('td')
        # print(cols)
        cols = [ele.text.strip() for ele in cols]
        data_new.append([ele for ele in cols if ele]) # Get rid of empty values

    state_pop_list = []

    for d in data_new[1:]:
        mymap[d[0]] = d[1]
        state_pop_list.append((d[0], d[1]))

    if mymap:
        return mymap


@deprecated
def total_casualties():
    source_code = requests.get('https://en.wikipedia.org/wiki/Hurricane_Wilma')
    soup = BeautifulSoup(source_code.content, "lxml")
    table = soup.find('table', attrs={'class':'infobox vevent'})
    rows = table.find_all('tr')

    data_new2 = []
    for row in rows:
        cols_h = row.find_all('th')
        cols_d = row.find_all('td')
        # print(cols)
        cols_h = [ele.text.strip() for ele in cols_h]
        cols_d = [ele.text.strip() for ele in cols_d]

        if "Fatalities" in cols_h:
            print(cols_d)
            data_new2.append([ele for ele in cols_d if ele]) # Get rid of empty values

    # for d in data_new2:
    #     print (d)


mapa1 = states_death_ratio("https://en.wikipedia.org/wiki/Hurricane_Katrina")
mapa2 = us_states_population()

for key in mapa1:
    print key, 'has deaths ', mapa1[key]

for key in mapa2:
    print key, 'has population of', mapa2[key]