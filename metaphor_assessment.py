from metaphor_python import Metaphor
import spacy
import re

# Location recommendations (for corresponding space NE, "GPE") and bypass clicking through all the URLs
# Gather titles and content with Metaphor, plug into Spacy to find all places, and sort by greatest number of mentions
# Can also replace with other prompts and corresponding spacy tag (but the NE-recognition is not as great)
# Ex. "this is my favorite organization", "ORG"
# Need to install spacy

prompts = ["this is my favorite place to visit for vacation", "this is my favorite city", "this is my favorite island"]
n = 5 # Top n ...

metaphor = Metaphor(api_key="b3e4bc03-9846-421b-94cf-2b668ab154ec") # API key
ner = spacy.load("en_core_web_sm")

query = prompts[0] # Pick any prompt from the above
search_response = metaphor.search(
    query, use_autoprompt=True, num_results=5,
)

# Remove all the html tags so spacy can recognize entities and compile all text to find all named entities
pattern = re.compile('<.*?>')
ids=[result.id for result in search_response.results]
responses = [ re.sub('[ \t\n\r]+', ' ',re.sub(pattern, ' ', metaphor.get_contents(i).contents[0].extract))\
             + ' ' + metaphor.get_contents(i).contents[0].title
              for i in ids]
compiled_responses = ' '.join(responses)
keywords = ner(compiled_responses)

# Go through all NEs and filter for location-related keywords
count = dict()
for k in keywords.ents:
    if k.label_=="GPE":
        count[k.text] = count.get(k.text,0) +1

# Output NEs by most mentioned 
print(sorted(count.keys(), key=count.get)[:n])