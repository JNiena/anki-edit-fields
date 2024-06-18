import json
import re
import requests
import urllib.request

def request(action, **params):
  return { 'action': action, 'params': params, 'version': 6 }

def invoke(action, **params):
	requestJson = json.dumps(request(action, **params)).encode('utf-8')
	response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))

	if len(response) != 2:
		raise Exception('The response has an unexpected number of fields.')

	if 'error' not in response:
		raise Exception('The response is missing a required error field.')

	if 'result' not in response:
		raise Exception('The response is missing a required result field.')

	if response['error'] is not None:
		raise Exception(response['error'])

	return response['result']

def main(deck, input, fields, match, overwrite, dry_run):
	query = 'deck:{}'.format(deck)
	note_ids = invoke('findNotes', query = query)
	notes = invoke('notesInfo', notes = note_ids)

	with open(input, 'r') as file:
		input_fields = json.loads(file.read())

	matched = 0
	for input_field in input_fields:
		for note in notes:
			if note['fields'][match]['value'] == input_field[match]:
				matched += 1
				print('\n{}/{}\nMatched "{}" from |{}| on note [{}]'.format(matched, len(notes), input_field[match], match, note['noteId']))
				for field in fields:
					if not overwrite and not note['fields'][field]['value'] == '':
						continue
					if not dry_run:
						invoke('updateNote', note = {
							'id': note['noteId'],
							'fields': {
								field: input_field[field]
							}
						})
					print('\tUpdated |{}| to "{}"'.format(field, input_field[field]))
				break

############################
######### Settings #########
############################

# The name of the deck to query
deck = '日本語'

# The file to input the fields from
input = 'data.json'

# The list of fields to set
fields = ['WordAudio', 'Sentence']

# The field used to match 
match = 'Word'

# Overwrite empty fields
overwrite = True

# Whether or not to do a dry run
dry_run = True

main(deck, input, fields, match, overwrite, dry_run)
