import glob
import json
import argparse
import os

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('-l', '--language', type=str, required=True,
                        help="Language to convert")
arg_parser.add_argument('-m', '--mode', type=str, required=True,
                        help="Converting mode")
arg_parser.add_argument('-t', '--text', type=str, required=True,
                        help="Text to convert")
arg_parser.add_argument('--reverse', dest='reverse', action='store_true', default=False,
                        help="Replace in the reverse order")

args = arg_parser.parse_args()

paths = glob.glob(os.path.join('data', '*.json'))
if len(paths) == 0:
    print('No data files found!')
    exit()

dataset = []
for path in paths:
    with open(path, encoding='utf-8') as file:
        try:
            json_content = json.load(file)
        except json.decoder.JSONDecodeError:
            print(f'Error while decoding a file "{path}"')
            raise
        language_name = json_content['language']
        mode_name = json_content['mode']
        if language_name == args.language and mode_name == args.mode:
            dataset.append(json_content)

if len(dataset) == 0:
    print(f'A file with the values l="{args.language}" and m="{args.mode}" not found in the dataset.')
    exit()


def run_tasks(text_input, data_object):
    tasks = data_object['tasks']
    text_output = text_input
    for task in tasks:
        task_type = task['type']
        if task_type == 'replace_all':
            for item in task['items']:
                replace_from = item[0]
                replace_to = item[1]
                if args.reverse:
                    replace_from, replace_to = replace_to, replace_from
                text_output = text_output.replace(replace_from, replace_to)
        else:
            print(f'An unsupported task type "{task_type}".')
    return text_output


for d in dataset:
    result = run_tasks(args.text, d)
    if 'description' in d:
        print(d['description'] + ':')
    print(result)
