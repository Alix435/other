import os
import csv
from datetime import datetime

constanta = [
            ('', ''),
        ]

class Work:
    def __init__(self):
        self.conf = "ActiveUsers_Export.csv"

        self.data = []

    def command_center(self):
        if self.check_config():
            self.read_config()
            self.sort_data()
            self.index_data()
            self.print_data()
            self.save_csv()
        else:
            print('The file does not exist!')
            exit()

    def check_config(self):
        if os.path.exists(self.conf):
            print('The file exists')
            return True
        else:
            return False


    def read_config(self):
        with open(self.conf, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            const_lines = [f'"{name}", "{email}"\n' for name, email in constanta]

            all_lines = [lines[0]] + lines[1:] + const_lines

            for line in all_lines[1:]:
                line = line.strip()
                if not line:
                    continue
                line = line.replace('"', '')
                parts = [part.strip() for part in line.split(',', 1)]

                if len(parts) == 2:
                    fio, email = parts
                    fio_parts = fio.split()

                    surname_name = f"{fio_parts[0]} {fio_parts[1]}"
                    short_name = f"{fio_parts[0]} {fio_parts[1][0]}"

                    entry = {
                        'number': 0,
                        'atype': 'A',
                        'full_name': surname_name,
                        'short_name': short_name,
                        'empty': '[1]',
                        'title': '',
                        'email': email
                    }
                    self.data.append(entry)


    def sort_data(self):
        self.data.sort(key=lambda x: x['full_name'])

    def index_data(self):
        nn = ["ab", "cd", "ef", "gh", "ijk", "lmn", "opq", "rst", "uvw", "xyz"]
        count = 1
        for inf in self.data:
            index = -1
            character = 0

            for i in range(len(inf['email'])):
                if inf['email'][i] == ".":
                    character = inf['email'][i + 1]
                    break

            for i, chars in enumerate(nn):
                if character in chars:
                    index = i + 1
                    break

            if index == -1:
                index = 111111111111111111111

            inf['title'] = f'[{index}]'
            inf['number'] = count

            count += 1


    def save_csv(self):
            name_file = f'FromPrintersPSCM_{datetime.now().strftime("%d.%m.%Y_%H")}.csv'

            # Сохраняем в кодировке Windows-cp1251 или utf-8
            with open(name_file, 'w', encoding='cp1251') as file:
                writer = csv.writer(file)

                for inform in self.data:
                    writer.writerow([inform['number'], inform['atype'], inform['full_name'], inform['short_name'], inform['empty'], inform['title'], inform['email']])


    def print_data(self):
        for i in self.data:
            print(i)

if __name__ == "__main__":
    work = Work()
    work.command_center()
