# Задание 1. Копирование содержимого одного файла в другой
# Создайте программу, которая копирует содержимое файла source.txt в новый файл destination.txt.
def task1():
    read_file_path = "./data/source.txt"
    write_file_path = "./data/destination.txt"
    with open(read_file_path, "r") as f_read, open(write_file_path, "w") as f_write:
        f_write.write(f_read.read())


# Задание 2. Подсчёт стоимости заказа из файла
# Напишите программу, которая считывает файл prices.txt, содержащий информацию о товарах: название, количество и цену, и подсчитывает общую стоимость заказа.
def task2():
    read_file_path = "./data/prices.txt"
    total = 0
    with open(read_file_path, "r") as f_read:
        for row in f_read.readlines():
            _name, _cnt, price = row.split()
            total += int(price)
    print(total)


# Задание 3. Подсчёт количества слов в файле
# Напишите программу, которая подсчитывает количество слов в текстовом файле text_file.txt и выводит результат на экран.
def task3():
    read_file_path = "./data/text_file.txt"
    with open(read_file_path, "r") as f_read:
        print(len(f_read.read().split()))


# Задание 4. Копирование уникального содержимого одного файла в другой
# Создайте программу, которая считывает строки из файла input.txt, сохраняет только уникальные строки и записывает их в новый файл unique_output.txt.
def task4():
    read_file_path = "./data/input.txt"
    write_file_path = "./unique_output.txt"
    added_lines: set[str] = set()
    with open(read_file_path, "r") as f_read, open(write_file_path, "w") as f_write:
        for line in f_read.readlines():
            if line in added_lines:
                continue
            f_write.write(line)
            added_lines.add(line)

