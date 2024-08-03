import re

from datasets import load_dataset


def parse_city_and_country_from_prompt(prompt):
	city_and_rest: str = prompt[45:]
	city, rest = city_and_rest.split('(')
	country = rest.split(')')[0]
	return city, country

def load_dataset_1():
	ds = load_dataset("louistichelman/streetview")
	return ds
	pattern = re.compile(r'A realistic google streetview image taken in (.+) \((.+)\)')

	cities = set()
	countries = set()

	for row in ds['train']:
		prompt = row['prompt']
		city_and_rest: str = prompt[45:]
		city, rest = city_and_rest.split('(')
		country = rest.split(')')[0]
		cities.add(city.strip())
		countries.add(country)


	print('CITIES')
	print(cities)

	print()

	print('COUNTRIES')
	print(countries)

def load_dataset_2():
	dataset = load_dataset('stochastic/random_streetview_images_pano_v0.0.2', split='train')
	return dataset

	countries = set()
	def func(rows):
		for c in rows['address']:
			countries.add(c)
	
	dataset.map(func, batched=True, remove_columns=['image', 'latitude', 'longitude', 'address'])

	print(len(countries))
	print(countries)

def load_datasets():
	ds1 = load_dataset_1()
	ds2 = load_dataset_2()

	places = list()
	images = list()

	def ds1_handler(batch):
		for prompt in batch['prompt']:
			city, country = parse_city_and_country_from_prompt(prompt)
			places.append(f'{city}, {country}')
		for image in batch['image']:
			images.append(image)

	def ds2_handler(batch):
		for address in batch['address']:
			places.append(address)
		for image in batch['image']:
			images.append(image)

	ds1.map(ds1_handler, batched=True)
	ds2.map(ds2_handler, batched=True)

	print('Len images:', len(images))
	print('Len places', len(places))

load_datasets()