import os, sys
import json
import nltk
import collections
import code #DEBUG code.interact(local=locals())

#Returns map from recipeIDs -> imperatives -> counts
def get_imperatives(jsonDir):

	imperative_map = {}

	for filename in os.listdir(jsonDir):
		if filename.endswith('.json'):
			data = json.load(open(os.path.join(jsonDir, filename)))

			for recipe_id, recipe in data.iteritems():
				instructions_lg = ' '.join(recipe['instructions'])

				sentences = nltk.sent_tokenize(instructions_lg)

				imperatives = collections.Counter()

				#Iterate through sentences
				for s in sentences:
					for raw_clause in s.split('; '):

						clause = 'They {}'.format(raw_clause.rstrip('.'))
						words = nltk.word_tokenize(clause)
						words[1] = words[1].lower()
						pos_labels = nltk.pos_tag(words)
						
						for label in pos_labels:
							if label[1] == 'VBP':
								imperatives[label[0].lower()] += 1
						
						
						#TODO: Strictly pick verbs related to 'They' as the subject

				imperative_map[recipe_id] = imperatives

	return imperative_map

#map uniqueid -> cooktime
#def get_labels(jsonDir):

if __name__ == '__main__':
	inDir = sys.argv[1]
	out = get_imperatives(inDir)