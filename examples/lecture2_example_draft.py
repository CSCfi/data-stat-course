import json
import requests
import pandas as pd
import matplotlib.pylab as plt
from bs4 import BeautifulSoup

API_BASE_URL = 'http://localhost:5000/api/'

print
print "Reading and writing in JSON, 101"
# Reading and writing in JSON, 101
# In Python JSON values are mapped as follows:
# true -> True
# false -> False
# number -> int / float
# string -> str
# object -> dict
# array -> list

# Collection of book records
books = [
    {
        "title": "Wuthering Heights",
        "author": "Emily Bronte"
    },
    {
        "title": "Anna Karenina",
        "author": "Leo Tolstoi"
    }
]

# Open file, serialize the list of book records to JSON and write to file
with open("file.json", "w") as f:
    json.dump(books, f)

# Open the file we just wrote, pass the file handle to json.load which deserializes the JSON content in the file
data_from_file = json.load(open("file.json"))

# Print book objects one by one
for book in data_from_file:
    print "Book record:", book

# print a list of titles
print "Titles", [book['title'] for book in data_from_file]

# json.dumps serializes Python values to JSON string, json.loads deserializes from JSON string to Python values
print "Serialize back to JSON: ", json.dumps(data_from_file)

# Retrieving data from APIs
print
print "Retrieving data from APIs"
response = requests.get(API_BASE_URL)
print "Status code: ", response.status_code
print "Content", response.text

print
print "Parse response content as JSON",
response = requests.get(API_BASE_URL).json()
print "and read parameters from it"
min_round = response['/api/round/<round>']['param_min']
max_round = response['/api/round/<round>']['param_max']
print "min_round: %s max_round: %s" % (min_round, max_round)

print
print "Retrieve the results for one round:",
response = requests.get(API_BASE_URL + 'round/%s' % min_round).json()
result = response.get('result')
print result

print
print "Retrieve all results between from round %s to ronud %s" % (min_round, max_round)
print "Visualize distribution of numbers with histogram"
results = []
for i in range(min_round, max_round + 1):
    response = requests.get(API_BASE_URL + 'round/%s' % (min_round + i)).json()
    result = response.get('result')
    if result:
        results.extend(result)

plt.figure()
numbers = pd.Series(results)
numbers.hist(bins=39, normed=True)
plt.savefig('out.png')
plt.show()


# Scraping
html_doc = open("perustilastot.html")
soup = BeautifulSoup(html_doc)
