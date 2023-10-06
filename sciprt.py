import os
import re
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import time

# Ваши входные слова
input_words = [ "Слава", "Украине", "Украина", "вторжение", "война", "Россия", "Независимость", "Герои", "Майдан", "Киев",
                "Донецк", "Луганск", "Крым", "Аннексия", "Оккупация", "Агрессия", "Санкции", "Конфликт", "Миротворцы", "Сепаратисты", "Российская",
                "НАТО", "Украинская", "армия", "Евромайдан", "Путин",
                "Украинский", "Конфликт", "Военные", "силы", "Беженцы", "санкции", "Территория","Армия", "Ракеты","Оружие", "Военные", "Протесты", "Демонстрации", "Пропаганда",
                "война", "Блокада", "Конфликта",
                "Миротворцы", "Политический", "кризис", "Террористы", "Борьба", "Вооруженные", "силы", "Терроризм", "Военное", "сражение", "Войска", "Бронетехника", "Захват", "территории",
                "Агрессор", "Внутренний", "конфликт", "национальная", "Враг",
                "Суверенитет", "Оружейный", "конфликт", "Угроза",
                "Glory", "Ukraine", "Ukraina", "invasion", "Russia", "Independence", "Heroes", "Maidan", "Kyiv",
                "Donetsk", "Luhansk", "Crimea", "Annexation", "Occupation", "Aggression", "Peaceful",
                "Sanctions", "Peacekeepers", "Separatists", "Russian",
                "Ukrainian", "army", "Euromaidan", "Putin",
                "Ukrainian", "Military",
                "Humanitarian", "Refugees", "sanctions", "Territory",
                "Army", "Missiles", "Weapons", "Military", "Protests", "Demonstrations", "Propaganda",
                "Blockade", "Humanitarian",
                "organizations", "Peacekeepers", "crisis", "Terrorists", "Struggle", "Constitution", "Armed",
                "Judicial", "Terrorism", "Military", "battle", "Territory",
                "Aggressor", "Enemy",
                "Sovereignty", "Armed",
                "Слава", "Україна", "Україна", "вторгнення", "війна", "Росія", "Незалежність", "Герої", "Майдан", "Київ",
                "Донецьк", "Луганськ", "Крим", "Аннексія", "Окупація", "Агресія", "Санкції", "Конфлікт", "Миротворці", "Сепаратисти", "Російська",
                "НАТО", "Українська", "Армія", "Євромайдан", "Путін",
                "Український", "Конфлікт", "Військові", "сили", "Біженці", "санкції", "Територія", "Армія", "Ракети", "Зброя", "Військові", "Протести", "Демонстрації ", "Пропаганда",
                "війна", "Блокада", "Конфлікту",
                "Миротворці", "Політична", "криза", "Терористи", "Боротьба", "Збройні", "сили", "Тероризм", "Військове", "битва", "Війська", "Бронетехніка", "Захоплення ", "території",
                "Агресор", "Внутрішній", "конфлікт", "національна", "Ворог",
                "Суверенітет", "Збройовий", "конфлікт", "Загроза",
]

# Функция для поиска вхождений слов в файле
def search_words_in_file(file_path):
    found_words = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        for word in input_words:
            matches = re.findall(r'\w*{}\w*'.format(re.escape(word.lower())), content.lower())
            found_words.extend(matches)
    return found_words, file_path

# Функция для обработки файлов с использованием multiprocessing
def process_files(root, files):
    found_files = []
    num_processes = cpu_count()

    with Pool(num_processes) as pool:
        file_paths = [os.path.join(root, file_name) for file_name in files]
        results = list(tqdm(pool.imap(search_words_in_file, file_paths), total=len(files), desc="Обработка в процессе"))

        for found_words, file_path in results:
            if found_words:
                found_files.append((file_path, found_words))

    return found_files
def print_folder_change(root, dirs, files):
    for dir_name in dirs:
        next_folder = os.path.join(root, dir_name)
        if len(os.listdir(next_folder)) != 0:
            print(f"Исследуем код в рамках директории: {next_folder}")
if __name__ == '__main__':
    start_time = time.time()
    found_files = []
    count = 0
    count_file_path = []
    dir_now = 0
    for root,dirs, files in os.walk(os.getcwd()):
        if files:
            if not files[0].startswith("pack", 0, 4):
                if dirs != dir_now:
                    dir_now = dirs
                    print_folder_change(root, dirs, files)
                    found_files.extend(process_files(root, files))
                else:
                    found_files.extend(process_files(root, files))


    for file_path, found_words in found_files:
        count += len(found_words)
        count_file_path.append(file_path)
        print(f'В файле {file_path} найдены следующие слова: {", ".join(found_words)}')
        end_time = time.time()
        print(end_time - start_time)



