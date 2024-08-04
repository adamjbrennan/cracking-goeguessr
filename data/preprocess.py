import json
from pathlib import Path

from datasets import load_dataset

DATASET_DIR = Path('crackinggeoguessr_ds')
IMAGE_DIR = DATASET_DIR / 'images'
TRAIN_JSON_FILE = DATASET_DIR / 'train_crackinggeoguessr_finetune_data.json'
TEST_JSON_FILE = DATASET_DIR / 'test_crackinggeoguessr_finetune_data.json'

USER_PROMPT = '''
Given the provided picture, give the location where it was taken.
Provide your best guess.
Keep your answer brief.
'''.strip()

def parse_city_and_country_from_prompt(prompt):
	city_and_rest: str = prompt[45:]
	city, rest = city_and_rest.split('(')
	country = rest.split(')')[0]
	return city, country

def load_dataset_1():
	dataset = load_dataset("louistichelman/streetview", split='train')
	return dataset

def load_dataset_2():
	dataset = load_dataset('stochastic/random_streetview_images_pano_v0.0.2', split='train')
	return dataset

def main():
	ds1 = load_dataset_1().shuffle(seed=31)
	ds2 = load_dataset_2().shuffle(seed=31)

	ds1_split = int(len(ds1) * .8)
	ds2_split = int(len(ds2) * .8)
	ds1_train = ds1[:ds1_split]
	ds1_test = ds1[ds1_split:]
	ds2_train = ds2[:ds2_split]
	ds2_test = ds2[ds2_split:]

	train_entries = list()
	test_entries = list()

	next_id = 0
	def write_image_and_add_to_json(entries, image, label):
		nonlocal next_id
		image_save_path = str(IMAGE_DIR / f'image_{next_id}.png')
		image.save(str(image_save_path))
		json_entry = json.dumps({
			'id': f'{next_id}',
			'image': image_save_path,
			"conversations": [
				{
					'role': 'user',
					'content': USER_PROMPT
				},
				{
					'role': 'assistant',
					'content': f'{label}'
				}
			]
		})
		entries.append(json_entry)
		next_id += 1

	for example in ds1_train:
		img = example['image']
		city, country = parse_city_and_country_from_prompt(example['prompt'])
		label = f'{city}, {country}'
		write_image_and_add_to_json(train_entries, img, label)

	for example in ds1_test:
		img = example['image']
		city, country = parse_city_and_country_from_prompt(example['prompt'])
		label = f'{city}, {country}'
		write_image_and_add_to_json(test_entries, img, label)

	for example in ds2_train:
		img = example['image']
		label = example['address']
		write_image_and_add_to_json(train_entries, img, label)

	for example in ds2_test:
		img = example['image']
		label = example['address']
		write_image_and_add_to_json(test_entries, img, label)

	TRAIN_JSON_FILE.write_text(json.dumps(train_entries))
	TEST_JSON_FILE.write_text(json.dumps(test_entries))

main()