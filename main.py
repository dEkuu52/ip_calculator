import sqlite3
import ipaddress

USER = 'user_v2.db'

def db_user_save():
    with sqlite3.connect(USER) as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE ,
            password TEXT NOT NULL)
            ''')
        conn.commit()

def reg_user_save():
    print('======= Введите ваши данные =======')
    username = input('Введите юзернейм: ')
    login = input('Введите логин: ')
    password = input('Введите пароль: ')

    try:
        with sqlite3.connect(USER) as conn:
            cur = conn.cursor()
            cur.execute(
                'INSERT INTO users (username, login, password) VALUES (?, ?, ?)',
                (username, login, password),
            )
            conn.commit()
            print('Вы успешно зарегистрировались')
            print(f'Приветствуем, {username} ({login})!')
            IpCalculatorRun().run_calculator()
    except sqlite3.IntegrityError:
        print('Такой пользователь уже есть')

def auth_user_save():
    print('======= Введите ваши данные =======')
    login = input('Введите логин: ')
    password = input('Введите пароль: ')

    with sqlite3.connect(USER) as conn:
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM users WHERE login = ? AND password = ?',
            (login, password),
        )

        user = cur.fetchone()

        if user:
            print(f'Приветсвуем {login}')
            IpCalculatorRun().run_calculator()

        else:
            print('Неверный логин или пароль')


class IpCalculatorRun:
    def __init__(self):
        self.ip_address = None
        self.mask = None
        self.ip_class = None
        self.default_mask = None
        self.prefix = None

    def class_network(self, ip_address: str):
        first_byte = ip_address.split('.')[0]

        if 1 <= int(first_byte) <= 126:
            return 'A', '255.0.0.0', 8
        elif int(first_byte) == 127:
            return 'Loopback(Локальный)', '255.0.0.0', 8
        elif 128 <= int(first_byte) <= 191:
            return 'class B', '255.255.0.0', 16
        elif 192 <= int(first_byte) <= 223:
            return 'class C', '255.255.255.0', 24
        elif 224 <= int(first_byte) <= 239:
            return 'class D (Multicast)', None, None
        elif 240 <= int(first_byte) <= 255:
            return 'class E (Reserved)', None, None

    def address_network(self):
        network = ipaddress.IPv4Network(f'{self.ip_address}/{self.prefix}', strict=False)
        print(f'Адресс сети: {network.network_address}')


    def run_calculator(self):
        while True:
            print('''
                === Рады что вы авторизировались, выберите действие ===
                1. - Класс сети
                2. - Адрес сети
                3. - Выход
            ''')

            choice_user = int(input('Введите число нужной вам функции: '))

            if choice_user == 1:
                self.ip_address = input('Введите IP-адрес (например, 192.168.1.1): ')

                self.ip_class, self.default_mask, self.prefix = self.class_network(self.ip_address)
                print(f'\nРезультат для IP {self.ip_address}:')
                print(f'Класс сети: {self.ip_class}')
                print(f'Маска по умолчанию: {self.default_mask}')
                print(f'Префикс: /{self.prefix}\n')
            elif choice_user == 2:
                self.ip_address = input('Введите IP-адрес (например, 192.168.1.1): ')
                self.ip_class, self.default_mask, self.prefix = self.class_network(self.ip_address)

                if self.prefix and isinstance(self.prefix, int):
                    self.address_network()
                else:
                    print('Error')
            elif choice_user == 3:
                exit()

            else:
                exit()


def main():
    db_user_save()
    while True:
        print('''
            ===== Привет, это IP-калькулятор Зарегистрируйтесь/Авторизуйтесь для начала работы =====
                  1. Зарегистрироваться
                  2. Авторизоваться
                  3. Выход
        ''')

        choice_user = int(input('Выберите действие: '))

        if choice_user == 1:
            reg_user_save()
        elif choice_user == 2:
            auth_user_save()
        elif choice_user == 3:
            exit()
        else:
            print('ошибка ввода')



if __name__ == '__main__':
    main()



