import json
import pprint
import random

pp = pprint.PrettyPrinter(indent=2)

FILE_JSON_UNPROCESSED = "inspire_data_random.json"
LIST_SECTORS = ['Education', 'Environment and Sustainability', 'Science and Technology', 'Health', 'Entrepreneurship and Business', 'Others']

def read_data():
	with open(FILE_JSON_UNPROCESSED) as data_file:    
		return json.load(data_file)

def generate_random_whole_number_upto_and_including_limit(limit):
	return random.randint(0, limit)

def get_random_combination_of_elements_from_list(l):
	num_elements_in_random_list = generate_random_whole_number_upto_and_including_limit(len(l))
	return random.sample(l, num_elements_in_random_list)

#Note: The following function is not stateless, it modifies the object passed in as parameters
def get_json_data_with_sector_field_converted_to_list_form(data_json):
	for i in range(len(data_json)):
		sectors_list = get_random_combination_of_elements_from_list(LIST_SECTORS)
		data_json[i]['sectors'] = sectors_list
	return data_json

def write_data(data):
	with open('inspire_data_random_processed.json', 'w') as outfile:
		json.dump(data, outfile)

if __name__ == '__main__':
	data_random_json = read_data()
	data_random_json_processed = get_json_data_with_sector_field_converted_to_list_form(data_random_json)
	write_data(data_random_json_processed)