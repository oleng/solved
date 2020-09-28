"""
    Use codewar API to retrieve completed katas and create individual notebooks from them
"""
from loguru import logger as log
import sys
import requests
import json
from pathlib import Path
import nbformat.v4 as nbformat
from time import sleep
log.add(sys.stderr, colorize=True, format="{time} - {name} - <level>{message}</level>", level="DEBUG")

page = 0
api = 'https://www.codewars.com/api/v1'
user = '/users/deadvoid'
katas = '/code-challenges'
nb_ext = 'ipynb'


def get(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        log.debug(f'{r.status_code}: {r.reason}\n{r.content}')
        return False

def get_katas(kata_id):
    return get(f"{api}{katas}/{kata_id}")

def create_notebook(markdown=None, code=None):
    nb = nbformat.new_notebook()
    if markdown:
        if isinstance(markdown, list):
            for each in markdown:
                md = nbformat.new_markdown_cell(source=each)
                nb['cells'].append(md)
    if code:
        nb['cells'].append(nbformat.new_code_cell(source=code))

    return nb


def main(data):
    notebooks = {}
    for i, k in enumerate(data):
        details = get_katas(k['id'])

        name                            = k['name']
        filename                        = k['slug']
        datetime                        = k['completedAt']
        k['url'] = link                 = details['url']
        k['category'] = category        = details['category']
        k['rank'] = rank                = details['rank']['name']
        k['tags'] = tags                = details['tags']
        k['description'] = md_challenge = details['description']

        md_meta = f'Title: {name}    \n' + \
                    f'Rank: {rank}    \n' + \
                    f'Link: {link}    \n' + \
                    f'Datetime: {datetime}     \n' + \
                    f'Category: {category}     \n' + \
                    f'Tags: {tags}'

        md = [md_meta, md_challenge]

        nb = create_notebook(markdown=md, code='# Solution')

        notebooks[f'codewar.{rank}.{filename}'] = nb

    return notebooks


if __name__ == '__main__':
    completed = get(f'{api}{user}{katas}/completed')
    data = completed['data']

    notebooks = main(data)

    for each, nb in notebooks.items():
        filename = Path(f'{each}.{nb_ext}')
        if not filename.exists() and filename.absolute().parent.name == 'codewar':
            with open(filename, 'w') as fh:
                fh.write(json.dumps(nb, indent=4))
        else:
            print(f'Youre in {filename.cwd()}. Aborting.')
            break
