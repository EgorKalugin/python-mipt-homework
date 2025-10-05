# Задание 1. Обработка деления на ноль
#
# Напишите программу, которая принимает два числа от пользователя и выводит результат их деления.
# Используйте обработку исключений, чтобы корректно обработать ситуацию, когда пользователь вводит 0 в качестве второго числа.
def task1():
    try:
        print(
            int(input("Введите первое число: ")) / int(input("Введите второе число: "))
        )
    except ZeroDivisionError:
        print("На ноль делить нельзя!")


# Задание 2. Обработка некорректного ввода
#
# Расширьте предыдущую программу, чтобы она также обрабатывала ситуацию, когда пользователь вводит строку вместо числа.
# Используйте несколько блоков except для обработки разных типов исключений.
def task2():
    try:
        print(
            int(input("Введите первое число: ")) / int(input("Введите второе число: "))
        )
    except ValueError:
        print("Нужно ввести число!")
    except ZeroDivisionError:
        print("На ноль делить нельзя!")


# Задание 3. Создание собственных исключений
#
# Напишите программу, которая вычисляет сумму списка целых чисел.
# Создайте свои собственные классы исключений для обработки ситуаций, когда в списке есть хотя бы одно чётное или отрицательное число.
# Используйте оператор raise для генерации исключений.
class NumberBaseError(Exception):
    def __init__(self, number: int) -> None:
        self.number = number


class EvenNumberError(NumberBaseError):
    def __str__(self) -> str:
        return f"Ошибка: число {self.number} четное!"


class NegativeNumberError(NumberBaseError):
    def __str__(self) -> str:
        return f"Ошибка: число {self.number} отрицательное!"


def calculate_list_of_numbers_sum(numbers: list[int]) -> int:
    result = 0
    for number in numbers:
        if number < 0:
            raise NegativeNumberError(number)
        elif number % 2 == 0:
            raise EvenNumberError(number)
        else:
            result += number
    return result


def get_list_of_ints_from_input() -> list[int]:
    numbers: list[int] = []
    print("Введите элементы списка. Нажмите ENTER чтобы завершить ввод.")
    while True:
        new_input = input("Введите число: ")
        if new_input == "":
            break
        numbers.append(int(new_input))
    return numbers


def task3():
    numbers = get_list_of_ints_from_input()
    res = calculate_list_of_numbers_sum(numbers)
    print(f"Сумма элементов списка равна: {res}")


# Задание 4. Обработка ошибок индексации
#
# Напишите программу, которая принимает от пользователя индекс элемента списка и выводит значение этого элемента.
# Используйте обработку исключений для корректной обработки ситуаций, когда пользователь вводит индекс, выходящий за пределы списка.
def task4():
    numbers = get_list_of_ints_from_input()
    ind = int(input("Введите индекс: "))
    try:
        print(numbers[ind])
    except IndexError:
        print("Индекс вышел за пределы списка!")


# Задание 5. Обработка ошибок преобразования типов
#
# Напишите программу, которая принимает от пользователя строку и преобразует её в число с плавающей точкой.
# Используйте обработку исключений для корректной обработки ситуаций, когда пользователь вводит строку, которую невозможно преобразовать в число.
def task5():
    try:
        float(input("Введите число с плавающей точкой: "))
    except ValueError:
        print(
            "Введенное значение не может быть преобразовано в число с плавающей точкой!"
        )


# Задание 6. Обработка ошибок импорта модулей
#
# Напишите программу, которая импортирует модуль math и использует функцию sqrt() для вычисления квадратного корня числа, введённого пользователем.
# Используйте обработку исключений для корректной обработки ситуаций, когда модуль math не может быть импортирован или функция sqrt() не может быть вызвана для отрицательного числа.
def task6():
    try:
        import math

        input_number = int(input("Введите число: "))
        math.sqrt(input_number)
    except ModuleNotFoundError:
        print("Модуль не может быть импортирован!")
    except ValueError:
        print("Корень не может быть вычислен для отрицательного числа!")
