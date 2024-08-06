import json
from pathlib import Path

from datasets import load_dataset

DATASET_DIR = Path('crackinggeoguessr_ds')
DATASET_DIR.mkdir(exist_ok=True)
IMAGE_DIR = DATASET_DIR / 'images'
IMAGE_DIR.mkdir(exist_ok=True)
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
	print('loading dataset 1')
	ds1 = load_dataset_1().shuffle(seed=31)
	print('loading dataset 2')
	ds2 = load_dataset_2().shuffle(seed=31)

	print('Starting preprocess now...')

	ds1_split = int(len(ds1) * .8)
	ds2_split = int(len(ds2) * .8)

	train_entries = list()
	test_entries = list()

	def write_image_and_add_to_json(entries, image, label, train_or_test):
		id = len(entries)
		image_save_path = (IMAGE_DIR / f'image_{id}_{train_or_test}.png').as_posix()
		image.save(str(image_save_path))
		entry = {
			'id': f'{id}',
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
		}
		entries.append(entry)

	next_train_id = 0
	next_test_id = 0

	for example in ds1:
		img = example['image']
		city, country = parse_city_and_country_from_prompt(example['prompt'])
		label = f'{city}, {country}'
		print(label)
		if next_train_id < ds1_split:
			write_image_and_add_to_json(train_entries, img, label, 'train')
			next_train_id += 1
		else:
			write_image_and_add_to_json(test_entries, img, label, 'test')
			next_test_id += 1

	for example in ds2:
		img = example['image']
		label = example['address']
		print(label)
		if (next_train_id - ds1_split) < ds2_split:
			write_image_and_add_to_json(train_entries, img, label, 'train')
			next_train_id += 1
		else:
			write_image_and_add_to_json(test_entries, img, label, 'test')
			next_test_id += 1

	TRAIN_JSON_FILE.write_text(json.dumps(train_entries, indent=4))
	TEST_JSON_FILE.write_text(json.dumps(test_entries, indent=4))

main()