# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime


def mask_card_number(card_number):
    return f'{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}'


def mask_account_number(account_number):
    return f"**{account_number[-4:]}"


def last_five_orders(json_file_name):
    with open(json_file_name, 'r') as file:
        file = file.read()
        operations = json.loads(file)
    operations_ex = []
    for operation in operations:
        if operation.get('state'):
            if operation['state'] == 'EXECUTED':
                operation['date'] = datetime.fromisoformat(operation['date'])

                operations_ex.append(operation)

    operations_ex = sorted(operations_ex, key=lambda x: x['date'])

    for operation_ex in operations_ex[-5:][::-1]:
        operation_ex_date = operation_ex['date'].strftime('%d.%m.%Y')

        if operation_ex.get('from'):
            operation_ex_from_split = operation_ex['from'].split()
            operation_ex_from_number = operation_ex_from_split[-1]

            if re.search(r".* \d{16}\b", operation_ex['from']):
                operation_ex_from_number = mask_card_number(
                    operation_ex_from_number)

            elif re.search(r".* \d{20}\b", operation_ex['from']):
                operation_ex_from_number = mask_account_number(
                    operation_ex_from_number)
            operation_ex_from = ' '.join(
                operation_ex_from_split[:-1] + [operation_ex_from_number])
        else:
            operation_ex_from = ''

        if operation_ex.get('to'):
            operation_ex_to_split = operation_ex['to'].split()
            operation_ex_to_number = operation_ex_to_split[-1]

            if re.search(r".* \d{16}\b", operation_ex['to']):
                operation_ex_to_number = mask_card_number(
                    operation_ex_to_number)

            elif re.search(r".* \d{20}\b", operation_ex['to']):
                operation_ex_to_number = mask_account_number(
                    operation_ex_to_number)
            operation_ex_to = ' '.join(
                operation_ex_to_split[:-1] + [operation_ex_to_number])
        else:
            operation_ex_to = ''
        result_string = f'''{operation_ex_date} {operation_ex["description"]}
{operation_ex_from} -> {operation_ex_to}
{operation_ex['operationAmount']['amount']} {operation_ex['operationAmount']['currency']['name'].replace('.', '')}.\n'''
        print(result_string)


if __name__ == "__main__":
    last_five_orders('operations.json')
