# generate a dataset

from datasets import Dataset
from SPARQLWrapper import SPARQLWrapper, JSON
import re
import random


sparql = SPARQLWrapper("https://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery("""
SELECT ?song
WHERE{
?song dbo:artist ?person.
?song a dbo:Song.
}
GROUP BY ?song 
HAVING (COUNT(?person) = 1 )
LIMIT 20
""")

# get DBpedia song URIs
dbpedia_songs = [r['song']['value'] for r in sparql.queryAndConvert()["results"]["bindings"]]


# get corresponding labels for each song and artist

def remove_everyting_between_paraenthesis(text):
    return re.sub(r'\([^)]*\)', '', text).strip()

songs = []
artists = []
for song in dbpedia_songs:
    sparql.setQuery(f"""
    SELECT ?songLabel ?personLabel
    WHERE{{
        <{song}> dbo:artist ?person.
        <{song}> rdfs:label ?songLabel.
        ?person rdfs:label ?personLabel.
        FILTER (lang(?personLabel) = 'en' && lang(?songLabel) = 'en')
    }}
    """)
    sparql.setReturnFormat(JSON)
    for r in sparql.queryAndConvert()["results"]["bindings"]:
        songs.append(remove_everyting_between_paraenthesis(r['songLabel']['value']))
        artists.append(remove_everyting_between_paraenthesis(r['personLabel']['value']))

print(songs)
print(artists)

# create questions
query = []
choices = []
label = []
for song, artist in zip(songs, artists):
    query.append(f"The artist of the song {song} is ") # more like sentence completion...
    #query.append(f"Who is the artist of the song {song}?")

    # get 3 random artists as distractors from answers list and make sure they are not the same as the correct answer
    distractors = []
    while len(distractors) < 3:
        distractor = random.choice(artists)
        if distractor != artist and distractor not in distractors:
            distractors.append(distractor)
    #add the correct answer to the list of distractors
    distractors.append(artist)
    random.shuffle(distractors)
    # get the index of the correct answer
    correct_index = distractors.index(artist)

    choices.append(distractors)
    label.append(correct_index)

ds = Dataset.from_dict({"query": query, "choices": choices, "label": label})
ds_dict = ds.train_test_split(test_size=0.2)

ds_dict['train'].to_json("./kb_train.json") # do not use to_csv because it will not save the list of lists in the choices column
ds_dict['test'].to_json("./kb_test.json")