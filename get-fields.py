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

def main(deck, output, fields):
	query = 'deck:{}'.format(deck)
	note_ids = invoke('findNotes', query = query)

	count = 0
	array = []
	for note in invoke('notesInfo', notes = note_ids):
		count += 1
		print('\n{}/{}\nGathered fields on note [{}]'.format(count, len(note_ids), note['noteId']))
		object = {}
		for field in fields:
			object[field] = note['fields'][field]['value']
			print('\tSaved |{}| as "{}"'.format(field, object[field]))
		array.append(object)

	with open(output, 'w') as file:
		file.write(json.dumps(array))

############################
######### Settings #########
############################

# The name of the deck to query
deck = '日本語'

# The file to output the fields to
output = 'data.json'

# The list of fields to get
fields = ['Word', 'WordAudio', 'Sentence']

main(deck, output, fields)
