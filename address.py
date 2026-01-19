# -*- coding: utf-8 -*-
import os
import re
from datetime import datetime


class DataConfig:
    def __init__(self):
        self.number = 0
        self.atype = "A"
        self.name = ""
        self.name2 = ""
        self.empty1 = "[1]"
        self.title = ""
        self.email = ""


class Work:
    def __init__(self):
        self.text = "#Один пользователь, одна строчка.\n#Перечисление данных запятой.\n#Фамилия Имя, электронная почта."
        self.conf = "address_printers.txt"
        self.data_config = []
        self.count = 1

    def command_center(self):
        if self.check_config():
            self.read_config()
            self.sort_by_name()
            self.data_numbering()
            self.save_csv()
        else:
            self.create_config()
            print("Create config")
            self.command_center()

    def check_config(self):
        return os.path.exists(self.conf)

    def create_config(self):
        with open(self.conf, 'w', encoding='utf-8') as f:
            f.write(self.text)
        return True

    def read_config(self):
        try:
            with open(self.conf, 'r', encoding='utf-8') as f:
                content = f.readlines()

            for line in content:
                line = line.strip()
                if not line or line[0] == '#':
                    continue

                parts = line.split(',', 1)
                if len(parts) == 2:
                    var1 = parts[0].strip()
                    var2 = parts[1].strip()

                    pair = DataConfig()
                    pair.name = var1
                    pair.name2 = self.check_len_name(var1)
                    pair.title = self.name_number(var2)
                    pair.email = var2

                    self.data_config.append(pair)
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")

    def sort_by_name(self):
        self.data_config.sort(key=lambda x: x.name)

    def data_numbering(self):
        for i, item in enumerate(self.data_config):
            item.number = i + 1


    def save_csv(self):
        try:
            output = []
            # output.append("Номер,Тип,Имя,КороткоеИмя,Пусто,Заголовок,Email")

            for row in self.data_config:
                output.append(f"{row.number},{row.atype},{row.name},{row.name2},{row.empty1},{row.title},{row.email}")

            name_file = f'FromPrintersPSCM_{datetime.now().strftime("%d.%m.%Y_%H")}.csv'

            # Сохраняем в кодировке Windows-1251
            with open(name_file, 'w', encoding='cp1251') as f:
                f.write('\n'.join(output))
        except Exception as e:
            print(f"Ошибка сохранения CSV: {e}")

    def name_number(self, email):
        nn = ["ab", "cd", "ef", "gh", "ijk", "lmn", "opq", "rst", "uvw", "xyz"]

        if len(email) < 3:
            return "not found"

        character = None
        for i in range(len(email)):
            if email[i] == ".":
                character = email[i+1]
                break

        # character = email[2]
        index = -1

        for i, chars in enumerate(nn):
            if character in chars:
                index = i + 1
                break

        if index == -1:
            return "not found"

        return f"[{index}]"

    def check_len_name(self, full_name):
        # Подсчет длины строки в байтах для UTF-8
        length = len(full_name.encode('utf-8'))

        if length <= 15:
            return full_name

        pos = full_name.find(' ')
        if pos <= 0:
            return full_name[:15]

        surname = full_name[:pos]
        name = full_name[pos + 1:]

        if name:
            first_letter = name[0]
            return f"{surname} {first_letter}."

        return surname

    def print_data(self):
        for row in self.data_config:
            print(f"Number: {row.number}")
            print(f"Type: {row.atype}")
            print(f"Name: {row.name}")
            print(f"Name2: {row.name2}")
            print(f"Empty: {row.empty1}")
            print(f"Title: {row.title}")
            print(f"E-mail: {row.email}\n")


if __name__ == "__main__":
    work = Work()
    work.command_center()
