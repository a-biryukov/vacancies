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

    # Получение данных из базы данных

    # companies = db.get_companies_and_vacancies_count()
    # print(companies)

    # all_vacancies = db.get_all_vacancies()
    # print(all_vacancies)

    # avg_salary = db.get_avg_salary()
    # print(avg_salary)

    # with_higher_salary = db.get_vacancies_with_higher_salary()
    # print(with_higher_salary)

    # words = input("Напишите слова по которым хотите произвести поиск \n"
    #               "(для поиска по отдельным словам - нужно писать их через запятую,\n"
    #               "для поиска по словосочетаниям - писать через пробел,\n"
    #               "пример: Младший менеджер, python, менеджер по продажам): ")
    # with_words = db.get_vacancies_with_keyword(words)
    # print(with_words)


if __name__ == '__main__':
    main()
