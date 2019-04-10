import re
import csv
import argparse


def get_cell_code_mapping(cell_codes_filename):
    mapping = {}
    with open(cell_codes_filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            cell_code = re.sub('[ x]+', '', line['number_pattern'])
            mapping[cell_code] = line['provider']
    return mapping


def write_phones(phone_provider_list, output_filename):
    with open(output_filename, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(('phone', 'provider'))
        writer.writerows(phone_provider_list)


def main(input_file_name, cell_codes_filename, provider_list, output_file_name):
    cell_code_mapping = get_cell_code_mapping(cell_codes_filename)

    with open(input_file_name) as input_file:
        input_text = input_file.read()
    list_phones = []
    for phone_number in re.findall('[+0-9 ()-]{9,}', input_text):
        cleaned_phone_number = re.sub('[+ ()-]', '', phone_number)
        if cleaned_phone_number.startswith('380'):
            provider_code_1 = cleaned_phone_number[3:5]
            provider_code_2 = cleaned_phone_number[3:6]
            tail = cleaned_phone_number[5:]
        elif cleaned_phone_number.startswith('0'):
            provider_code_1 = cleaned_phone_number[1:3]
            provider_code_2 = cleaned_phone_number[1:4]
            tail = cleaned_phone_number[3:]
        formatted_phone_number = (f'+380{provider_code_1} ' f'{tail[:3]}-{tail[3:5]}-{tail[5:]}')
        if cell_code_mapping.get(provider_code_1) in provider_list:
            list_phones.append((formatted_phone_number, cell_code_mapping.get(provider_code_1)))
        elif cell_code_mapping.get(provider_code_2) in provider_list:
            list_phones.append(formatted_phone_number, cell_code_mapping.get(provider_code_2))
    write_phones(list_phones, output_file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract phone numbers.')
    parser.add_argument('-i', '--input_file', required=True, help='input text file')
    parser.add_argument('-c', '--cell_codes', required=True, help='cell codes csv file')
    parser.add_argument('-p', '--provider', action='append', required=True, help='cell code provider (repeatable)')
    parser.add_argument('-o', '--output_file', required=True, help='output report csv file')

    args = parser.parse_args()
    main(args.input_file, args.cell_codes, args.provider, args.output_file)


