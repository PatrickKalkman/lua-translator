from googletrans import Translator
import time

input_file = 'en_test2.lua'
output_file = input_file.replace('.lua', '.translated.lua')

translator = Translator()

with open(input_file) as f:
    content = f.readlines()

source_language = 'de'
for line in content:
    if 'Locales' in line:
        tokens = line.split('[')
        language = tokens[1].split(']')
        source_language = language[0].replace('\'', '')

print(f'Source language = {source_language}')

to_file = []
for line in content:
    if 'Locales' not in line and line.strip() and '}' not in line and '--' not in line:
        tokens = line.split('=')
        to_translate = tokens[1].replace('\'', '').replace('\n', '').replace(',','').strip()
        result = translator.translate(to_translate, src=source_language, dest='nl')
        translated = result.text.replace('% ', '%').replace('\'', '').replace('~ Input_pickUp ~', '~INPUT_PICKUP~').replace('~ Input_pickup ~', '~INPUT_PICKUP~').replace('~ y ~', '~y~').replace('~ r ~','~r~')
        if ' | ' in line and ' | ' not in translated:
            translated = translated.replace(' |', ' | ')
        
        print(f'Translated "{to_translate}" to "{translated}"')
        time.sleep(0.5)
        to_file.append(f'{tokens[0]} = \'{translated}\',\n')
    else:
        to_file.append(line)

with open(output_file, 'w') as f:
    for line in to_file:
        f.write(f'{line}')

