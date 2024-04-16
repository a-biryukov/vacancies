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

    # Создание базы данных, создание таблиц и их заполнение
    db = DBManager(params)
    db.create_database()
    db.save_data_to_database(vacancy_data)

    while True:
        print("")
        user_query = input("1 - Показать список компаний и количество вакансий\n"
                           "2 - Показать все вакансии\n"
                           "3 - Показать среднюю зарплату по вакансиям\n"
                           "4 - Показать список вакансий с зарплатой выше средней\n"
                           "5 - Поиск вакансий по ключевым словам\n"
                           "exit - выход из программы\n"
                           "Для получения данных введите соответствующую цифру: ").strip().lower()
        print("")

        if user_query == "1":
            companies = db.get_companies_and_vacancies_count()
            for company in companies:
                print(f"{company[0]} - {company[1]} вакансий")
            continue

        elif user_query == "2":
            all_vacancies = db.get_all_vacancies()
            db.printing(all_vacancies)
            continue

        elif user_query == "3":
            avg_salary = db.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям составляет: {avg_salary} рублей")
            continue

        elif user_query == "4":
            with_higher_salary = db.get_vacancies_with_higher_salary()
            db.printing(with_higher_salary)
            continue

        elif user_query == "5":
            while True:
                words = input("Напишите слова по которым хотите произвести поиск \n"
                              "(для поиска по отдельным словам - нужно писать их через запятую,\n"
                              "для поиска по словосочетаниям - писать через пробел,\n"
                              "пример: Младший менеджер, python, менеджер по продажам): ")
                try:
                    with_keywords = db.get_vacancies_with_keyword(words)
                except AttributeError as ae:
                    print(f"\n{ae}")
                    user_input = input("1 - продолжить поиск по словам\n"
                                       "2 - выйти в основное меню\n"
                                       "Введите цифру: ").strip()
                    if user_input == "1":
                        print("")
                        continue
                    else:
                        break
                else:
                    print("")
                    db.printing(with_keywords)
                    user_input = input("\n1 - продолжить поиск по словам\n"
                                       "2 - выйти в основное меню\n"
                                       "Введите цифру: ").strip()
                    if user_input == "1":
                        print("")
                        continue
                    else:
                        break
            continue

        elif user_query == "exit":
            break

        else:
            print("Некорректный ввод. попробуйте еще раз.")
            continue


if __name__ == '__main__':
    main()
