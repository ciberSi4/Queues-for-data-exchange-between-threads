# Домашнее задание по теме "Очереди для обмена данными между потоками."

import threading
from random import randint
from queue import Queue


# Класс Table представляет собой стол в кафе
class Table:
    def __init__(self, number):
        # Номер стола
        self.number = number
        # Гость, сидящий за столом (изначально никто)
        self.guest = None


# Класс Guest представляет посетителя кафе, является потоком
class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        # Имя гостя
        self.name = name

    # Метод run выполняется при старте потока
    def run(self):
        # Задержка от 3 до 10 секунд, имитирующая время приёма пищи
        delay = randint(3, 10)
        print(f"{self.name} кушает {delay} секунд...")
        # Ждём указанное количество времени
        threading.Event().wait(delay)


# Класс Cafe управляет работой кафе, включая очереди и обслуживание посетителей
class Cafe:
    def __init__(self, *tables):
        # Очередь для ожидания гостей
        self.queue = Queue()
        # Список столов в кафе
        self.tables = list(tables)

    # Метод для прибытия новых гостей
    def guest_arrival(self, *guests):
        for guest in guests:
            # Проверяем наличие свободного стола
            free_table = next((t for t in self.tables if t.guest is None), None)
            if free_table:
                # Если найден свободный стол, сажаем гостя за него
                free_table.guest = guest
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
                # Запускаем поток гостя
                guest.start()
            else:
                # Если все столы заняты, добавляем гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    # Метод для обслуживания гостей
    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest for table in self.tables):
            # Проходим по всем столам
            for table in self.tables:
                # Если за столом кто-то сидит и этот гость уже закончил прием пищи
                if table.guest and not table.guest.is_alive():
                    # Освобождаем стол
                    guest_name = table.guest.name
                    table.guest = None
                    print(f"{guest_name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    # Если очередь еще не пуста, берем следующего гостя из очереди
                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                        new_guest.start()


# Пример использования классов

if __name__ == "__main__":
    # Создаём список столов
    tables = [Table(number) for number in range(1, 6)]

    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Victoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    # Создаём гостей
    guests = [Guest(name) for name in guests_names]

    # Создаём объект кафе
    cafe = Cafe(*tables)

    # Принимаем гостей
    cafe.guest_arrival(*guests)

    # Начинаем обслуживать гостей
    cafe.discuss_guests()