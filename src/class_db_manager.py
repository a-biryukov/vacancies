import psycopg2
from typing import Any


class DBManager:
    """ Класс для работы с базой данных """

    params: dict

    def __init__(self, params: dict[str: str]) -> None:
        """
        Конструктор класса. Задаем значения атрибутам экземпляра класса.
        :param params: Параметры для подключения к базе данных (host, user, password, port)
        """
        self.__params = params

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """ Получает список всех компаний и количество вакансий у каждой компании """
        result = self.__execute("""
            SELECT employer_name, number_of_vacancies
            FROM employers
        """)

        return result

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """ Получает список всех вакансий """
        result = self.__execute("""
            SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url
            FROM vacancies
            JOIN employers USING (employer_id)
        """)

        return result

    def get_avg_salary(self) -> int:
        """ Получает среднюю зарплату по вакансиям """

        result = int(self.__execute("""
            SELECT (AVG(salary_from) + AVG(salary_to)) / 2
            FROM vacancies
        """)[0][0])

        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """ Получает список вакансий с зарплатой выше средней по всем вакансий """

        result = self.__execute("""
            SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url FROM vacancies
            JOIN employers USING (employer_id)
            WHERE salary_from > (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 FROM vacancies) 
            OR salary_to > (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 FROM vacancies)
        """)

        return result

    def get_vacancies_with_keyword(self, words: str) -> list[tuple[Any, ...]]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        Для поиска отдельно по нескольким словам - слова нужно писать через запятую.
        При написании слов через пробел - поиск будет производиться по словосочетаниям.
        :param words: Строка из слов по которым будет производиться поиск
        :return: Список с вакансиями отобранными по указанным словам
        """
        words_list = words.lower().split(",")
        query = f"""
        SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url FROM vacancies
        JOIN employers USING (employer_id) 
        WHERE LOWER(vacancy_name) LIKE '%{words_list[0].strip()}%' 
        """
        for i in range(1, len(words_list)):
            query += f"OR LOWER(vacancy_name) LIKE '%{words_list[i].strip()}%'"

        result = self.__execute(query)

        if len(result) == 0:
            raise AttributeError("По вашему запросу вакансий не найдено.")

        return result

    def create_database(self) -> None:
        """ Создает базу данных 'headhunter' и таблицы 'employers' и 'vacancies' """

        try:
            self.__execute("CREATE DATABASE headhunter", dbname="postgres")
        except psycopg2.errors.DuplicateDatabase:
            self.__execute("DROP DATABASE headhunter", dbname="postgres")
            self.__execute("CREATE DATABASE headhunter", dbname="postgres")

        self.__execute("""
            CREATE TABLE employers 
            (
                employer_id INTEGER PRIMARY KEY,
                employer_name varchar(100) NOT NULL,
                number_of_vacancies SMALLINT NOT NULL
            );

            CREATE TABLE vacancies 
            (
                vacancy_id SERIAL PRIMARY KEY,
                vacancy_name varchar(100) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER, 
                vacancy_url varchar(100) NOT NULL,
                employer_id INTEGER REFERENCES employers(employer_id) NOT NULL
            );
        """)

    def save_data_to_database(self, data: list[dict[str: Any]]) -> None:
        """
        Заполняет таблицы 'employers' и 'vacancies' данными
        :param data: Список с данными полученными с hh.ru
        """
        conn = psycopg2.connect(**self.__params, dbname="headhunter")
        conn.autocommit = True
        try:
            with conn.cursor() as cur:
                for employer in data:
                    vacancy_list = employer.get("items")

                    employer_id = vacancy_list[0].get("employer").get("id")
                    employer_name = vacancy_list[0].get("employer").get("name")
                    number_of_vacancies = 0
                    for vacancy in vacancy_list:
                        if vacancy.get("salary").get("currency") == "RUR":
                            number_of_vacancies += 1

                    cur.execute(
                        """
                        INSERT INTO employers (employer_id, employer_name, number_of_vacancies)
                        VALUES (%s, %s, %s)
                        """,
                        (employer_id, employer_name, number_of_vacancies)
                    )

                    for vacancy in vacancy_list:
                        if vacancy.get("salary").get("currency") != "RUR":
                            continue
                        vacancy_name = vacancy.get("name")
                        salary_from = vacancy.get("salary").get("from")
                        salary_to = vacancy.get("salary").get("to")
                        vacancy_url = vacancy.get("alternate_url")
                        cur.execute(
                            """
                            INSERT INTO vacancies (vacancy_name, salary_from, salary_to, vacancy_url, employer_id)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (vacancy_name, salary_from, salary_to, vacancy_url, employer_id)
                        )
        finally:
            conn.close()

    def __execute(self, query, dbname="headhunter"):
        """ Подключение к базе данных """

        conn = psycopg2.connect(**self.__params, dbname=dbname)
        conn.autocommit = True
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                if "SELECT" in query:
                    results = cur.fetchall()
                    return results
        finally:
            conn.close()

    @staticmethod
    def printing(vacancies: list[tuple[Any, ...]]) -> None:
        """
        Выводит данные в фермате: название компании, название вакансии, закрплата, ссылка на вакансию
        :param vacancies: список с данными о вакансиях
        """
        for vacancy in vacancies:
            vacancy_info = f"{vacancy[0]}, {vacancy[1]}, зарплата "

            if vacancy[2] is not None:
                vacancy_info += f"от {vacancy[2]} "

            if vacancy[3] is not None:
                vacancy_info += f"до {vacancy[3]} "

            vacancy_info += vacancy[4]

            print(vacancy_info)
