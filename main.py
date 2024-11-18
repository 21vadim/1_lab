import requests
import xml.etree.ElementTree as ET


def get_usd_exchange_rate():
    """
    Получает актуальный курс доллара США (USD) к рублю (RUB) из API Центрального Банка России.

    Возвращает:
        float: Курс USD к RUB
    """
    url = "http://www.cbr.ru/scripts/XML_daily.asp"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешность запроса
    except requests.RequestException as e:
        print(f"Ошибка при получении данных с ЦБ РФ: {e}")
        return None

    try:
        # Парсинг XML
        root = ET.fromstring(response.content)
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            if char_code == 'USD':
                value = valute.find('Value').text
                nominal = valute.find('Nominal').text
                # Преобразование строки с запятой на точку и вычисление курса за 1 USD
                rate = float(value.replace(',', '.')) / int(nominal)
                return rate
        print("Доллар США (USD) не найден в данных ЦБ РФ.")
        return None
    except ET.ParseError as e:
        print(f"Ошибка при парсинге XML: {e}")
        return None
    except (AttributeError, ValueError) as e:
        print(f"Ошибка при обработке данных курса: {e}")
        return None


def convert_rub_to_usd(amount_rub, exchange_rate):
    """
    Конвертирует сумму из рублей в доллары по заданному курсу.

    Аргументы:
        amount_rub (float): Сумма в рублях
        exchange_rate (float): Курс USD к RUB

    Возвращает:
        float: Сумма в долларах
    """
    return amount_rub / exchange_rate


def main():
    print("=== Конвертер Валют: RUB -> USD ===\n")

    # Получение актуального курса USD к RUB
    rate = get_usd_exchange_rate()
    if rate is None:
        print("Не удалось получить актуальный курс доллара. Попробуйте позже.")
        return

    print(f"Актуальный курс USD к RUB: 1 USD = {rate:.2f} RUB\n")

    while True:
        user_input = input("Введите сумму в рублях для конвертации (или 'exit' для выхода): ").strip()

        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Спасибо за использование конвертера! До свидания.")
            break

        try:
            amount_rub = float(user_input.replace(',', '.'))
            if amount_rub < 0:
                print("Пожалуйста, введите неотрицательное число.\n")
                continue
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите числовое значение.\n")
            continue

        amount_usd = convert_rub_to_usd(amount_rub, rate)
        print(f"{amount_rub:.2f} RUB = {amount_usd:.2f} USD\n")


if __name__ == "__main__":
    main()
    