from configparser import ConfigParser


def config(filename="database.ini", section="postgresql") -> dict:
    """
    Получает параметры для подключения к базе данных из файла
    :param filename: Имя файла
    :param section: Раздел откуда парсим данные
    :return: Словарь с параметрами
    """
    parser = ConfigParser()
    parser.read(filename)
    params = {}
    if parser.has_section(section):
        lines = parser.items(section)
        for line in lines:
            params[line[0]] = line[1]

    return params
