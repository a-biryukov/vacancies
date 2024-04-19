from src.class_headhunter_api import HeadHunterAPI
from src.class_db_manager import DBManager
from src.config import config


def main():

    employers_ids = [
        "1740",   # Яндекс
        "64174",  # 2ГИС
        "3529",   # СБЕР
        "2748",   # Ростелеком
        "2180",   # Ozon
        "78638",  # Тинькофф
        "84585",  # Авито
        "87021",  # WILDBERRIES
        "3127",   # МегаФон
        "780654"  # Lamoda
    ]

    # Получение данных с hh.ru
    hh = HeadHunterAPI(employers_ids)
    vacancy_data = hh.get_data()

    # Получение параметров для подключения к базе данных
    params = config()

    # Создание базы данных
    db_postgres = DBManager(params, dbname="postgres")
    try:
        db_postgres.create_database()
    finally:
        db_postgres.connection.close()
        db_postgres.connection.close()

    # Cоздание таблиц и их заполнение
    db_hh = DBManager(params)
    try:
        db_hh.create_tables()
        db_hh.save_data_to_database(vacancy_data)

        # Интерактив с пользователем
        while True:
            user_query = input("\n1 - Показать список компаний и количество вакансий\n"
                               "2 - Показать все вакансии\n"
                               "3 - Показать среднюю зарплату по вакансиям\n"
                               "4 - Показать список вакансий с зарплатой выше средней\n"
                               "5 - Поиск вакансий по ключевым словам\n"
                               "exit - выход из программы\n"
                               "Для получения данных введите соответствующую цифру: ").strip().lower()

            # Вывод данных
            if user_query == "1":
                companies = db_hh.get_companies_and_vacancies_count()
                print("")
                for company in companies:
                    print(f"{company[0]} - {company[1]} вакансий")
                continue

            elif user_query == "2":
                all_vacancies = db_hh.get_all_vacancies()
                print("")
                db_hh.printing(all_vacancies)
                continue

            elif user_query == "3":
                avg_salary = db_hh.get_avg_salary()
                print("")
                print(f"Средняя зарплата по всем вакансиям составляет: {avg_salary} рублей")
                continue

            elif user_query == "4":
                with_higher_salary = db_hh.get_vacancies_with_higher_salary()
                print("")
                db_hh.printing(with_higher_salary)
                continue

            elif user_query == "5":
                while True:
                    words = input("\nНапишите слова по которым хотите произвести поиск \n"
                                  "(для поиска по отдельным словам - нужно писать их через запятую,\n"
                                  "для поиска по словосочетаниям - писать через пробел,\n"
                                  "пример: Младший менеджер, python, менеджер по продажам)\n"
                                  "1 - выйти в основное меню.\n"
                                  "Ввод: ")

                    if words.strip() == "1":
                        break
                    else:
                        try:
                            with_keywords = db_hh.get_vacancies_with_keyword(words)
                        except AttributeError as ae:
                            print(f"\n{ae}")
                            continue
                        else:
                            print("")
                            db_hh.printing(with_keywords)
                            continue
                continue

            elif user_query == "exit":
                break

            else:
                print("Некорректный ввод. попробуйте еще раз.")
                continue
    finally:
        db_hh.cur.close()
        db_hh.connection.close()


if __name__ == '__main__':
    main()
