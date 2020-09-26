#!/usr/bin/env python
# -*- coding: utf-8 -*-

def markdown_table_to_dict(strip_data=False, path=None, _str=None, io_txt=None, json_path=False):
    '''
    Convert markdown table to dict

    :strip_data: `bool`
        `True` will strip any markdown string formats in the table data that use these characters,
            including anchor id links: `\`*_#~`.
        Blockquotes, images, external links, and horizontal rule formatting will be left intact `⋅.:>[]-()!`
    :path: `str` object, should contain valid POSIX path
    :_str: `str` object
    :io_txt: `str` text IO (`io.TextIOBase`)

    Output:
        {
        'column_labels': ['No.', 'Title', 'Acceptance', 'Difficulty'],
        'column_alignments': ['left', 'left', 'right', 'left'],
        'table_body': [
                        ['1', '[Two Sum](https://leetcode.com/problems/two-sum)', '45.8%', 'Easy'],
                        ['2', '[Add Two Numbers](https://leetcode.com/problems/add-two-numbers)', '34.2%', 'Medium'],
                        ['3', '[Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters)', '30.6%', 'Medium'],
                        ['4', '[Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays)', '30.0%', 'Hard']
                      ]
        }
    '''
    if path:
        with open(path, 'r', encoding='utf8') as fh:
            lines_list = fh.read().splitlines()
    elif _str:
        lines_list = _str.splitlines()
    elif io_txt:
        lines_list = io_txt.read().splitlines()
    else:
        print('Please provide a path to markdown file / string input / IO text object to continue')
        return

    def remove_md_formats(s):
        return s.strip().replace('`', '').replace('*', '').replace('_', '')\
                .replace('#', '').replace('~','').strip()

    # parse markdown lines
    ## pre-process removing markdown markups
    header = remove_md_formats(lines_list[0].strip().replace('|', '')).split()
    alignments = lines_list[1].strip()\
                            .replace('|-',',|-')\
                            .replace(':|',':|,')\
                            .replace('-|','-|,')\
                            .replace('|:',',|:')\
                            .split(',')
    md = {}
    aligned = {
        'left': ':-',
        'right': '-:',
        'default': '|---|'
    }
    md['column_labels'] = header
    md['column_alignments'] = col_a = []
    for idx, x in enumerate(alignments):
        if idx == 0 and (not x or x == ' '):
            # remove empty space in list's first element produced from splitting the markdown table markups
            continue
        elif aligned['left'] in x:
            col_a.append('left')
        elif aligned['right'] in x:
            col_a.append('right')
        else:
            col_a.append('default')

    if strip_data:
        md['table_body'] = [ remove_md_formats(l)\
                                  .lstrip('|').rstrip('|').strip().split(' | ')
                                  for l in lines_list[2:]
                                 ]
    else:
        md['table_body'] = [ l.lstrip('|').rstrip('|').strip().split(' | ')
                                  for l in lines_list[2:]
                                 ]

    if json_path:
        with open(json_path, 'w', encoding='utf8') as j:
            j.write(json.dumps(md, indent=4))
        return True

    return md
