import os
import csv
import typing

from bs4 import BeautifulSoup

FIELD_NAMES = [
    'name',
    'Energy',
    'Protein-to-Fat',
    'Fat',
    'of which saturates',
    'Carbohydrates',
    'of which sugars',
    'Fibre',
    'Protein',
    'Salt',
    'Iron',
    'Calcium',
    'Vitamin C',
    'Omega 3'
]

def parse_quantity(quantity: str) -> float:
    if quantity.endswith('g'):
        return float(quantity.replace('g', ''))
    
    if quantity.endswith('mg'):
        return float(quantity.replace('mg', '') / 1000.0)

    raise ValueError(f'Unknown quantity type: {quantity}')

def protein_to_fat(row: typing.List[str]) -> float:
    return parse_quantity(row['Protein']) / parse_quantity(row['Fat'])

with open('uncommitted/nutrition.csv', 'w') as out:
    csv_writer = csv.DictWriter(out, fieldnames=FIELD_NAMES, extrasaction='ignore')
    csv_writer.writeheader()

    for html_file in os.listdir('uncommitted'):
        with open(f'uncommitted/{html_file}') as html_fh:

            soup = BeautifulSoup(html_fh, 'html.parser')

            tables = soup.find_all('table')
            for table in tables:
                headers = [header.text for header in table.find_all('th')]
                results = [{headers[i]: cell.text for i, cell in enumerate(row.find_all('td'))}
                    for row in table.find_all('tr')]

                normalised = {row['Typical Values']: row['Per 100g'] for row in results if 'Typical Values' in row}
                normalised['Protein-to-Fat'] = f'{protein_to_fat(normalised):.1f}'
                normalised['name'] = html_file.replace('.html', '')

                csv_writer.writerow(normalised)

            
        
