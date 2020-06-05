import pickle
import re
import csv
import random

if __name__ == '__main__':
    input_paths = {
        'kaczmarski': 'jacek_kaczmarski.pickle',
        'krawczyk': 'krzysztof_krawczyk.pickle',
    }
    output_path = '_vs_'.join(sorted(input_paths.keys())) + '.csv'
    rows = set()

    for artist, input_path in input_paths.items():
        with open(input_path, 'rb') as f_in:
            songs = pickle.load(f_in)

        for song in songs:
            song = re.sub(r'\[.*\]', '', song)
            verses = song.split('\n\n')

            for verse in verses:
                verse = verse.replace('\n', ' ')\
                    .replace('REF.', '')\
                    .replace('Ref.', '')\
                    .replace('Refren', '')\
                    .replace('x2', '')\
                    .strip()

                if len(verse) > 40 and 'a' in verse and "'" not in verse:
                    rows.add((artist, verse))

    rows = list(rows)
    random.shuffle(rows)        

    with open(output_path, 'w', encoding='utf-8', newline='') as f_out:
        writer = csv.writer(f_out)
        writer.writerow(('artist', 'text'))
        writer.writerows(rows)

    for artist in input_paths.keys():
        count = sum(1 for a, _ in rows if a == artist)
        print(f'{artist}: {count}')
