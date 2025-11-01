import threading
import time


def sum_of_cubes(i: int) -> int:
    print(f"sum_of_cubes start with {i=}")
    res = 0
    for el in range(i):
        res += el**3
    print(f"sum_of_cubes finish with {res=}")
    return res


def sum_of_squares(i: int) -> int:
    print(f"sum_of_squares start with {i=}")
    res = 0
    for el in range(i):
        res += el**2
    print(f"sum_of_squares finish with {res=}")
    return res


def task1():
    sum_of_cubes_thread = threading.Thread(target=sum_of_cubes, args=(100,))
    sum_of_squares_thread = threading.Thread(target=sum_of_squares, args=(100,))

    sum_of_cubes_thread.start()
    sum_of_squares_thread.start()


def print_numbers(thread_name: str):
    for i in range(1, 11):
        print(f"{thread_name}: {i}")
        time.sleep(1)


def task2():
    threads: list[threading.Thread] = []

    for n in range(3):
        thread = threading.Thread(target=print_numbers, args=(f"Поток-{n + 1}",))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
