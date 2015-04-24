from bs4 import BeautifulSoup
import requests

base_url = 'http://tilastot.kirjastot.fi/fi-fi/perustilastot.aspx?AreaKey='
libraries = {
    'helsinki': 'Y2014T2N91',
    'vantaa': 'Y2014T2N92',
    'espoo': 'Y2014T2N49',
    'kauniainen': 'Y2014T2N235'
}

headers = {
    'Accept': 'text/html',
    'Accept-encoding': ''
}

# Scraping
for library, search_id in libraries.items():
    html_doc = requests.get(base_url + search_id, headers=headers).text
    soup = BeautifulSoup(html_doc)
    import pdb; pdb.Pdb().set_trace()
    for x in [[y.text for y in x.findAll('td') if y.text][:2] for x in soup.body.findAll('table')[5].findAll('tr')]:
        if x:
            a, b = x
            if "Kirja-aine" in a:
                print "%s: %s" % (library, int(b.replace(u"\xa0", "")))
