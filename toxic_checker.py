import requests
import json
import subprocess

class ToxicChecker:
    def __init__(self):
        self.names_toxic_repos = []

    def get_bd(self):
        """Получение json с toxic repos"""
        toxic_repos = 'https://raw.githubusercontent.com/toxic-repos/toxic-repos/main/data/json/toxic-repos.json'
        try:
            response = requests.get(toxic_repos)
            if response.status_code == 200:
                bd = json.loads(response.content)
                self.names_toxic_repos = [entry['name'] for entry in bd]
            else:
                print(f"Ошибка получения базы данных ({response.status_code})")
        except Exception as e:
            print("Проверьте интернет-соединение")

    def installation(self):
        """Установка необходимых пакетов"""
        subprocess.run('sudo apt-get update', shell=True)
        subprocess.run('sudo apt-get install -y npm python3-pip', shell=True)
        subprocess.run('echo "y" | sudo -H pip3 install fuzzywuzzy python-Levenshtein', shell=True)
        subprocess.run("sudo npm config set strict-ssl false", shell=True)
        subprocess.run('echo "y" | sudo npm install -g @cyclonedx/cdxgen@8.6.0', shell=True)

    def sbom_generation(self):
        """Генерация SBOM"""
        type_of_project = input("Укажите язык(-и) проекта: ").split()

        name_for_sbom_s = []
        for lang in type_of_project:
            name_for_sbom = input(f"Укажите название/ПОЛНЫЙ путь для SBOM проекта на {lang}: ")
            name_for_sbom_s.append(name_for_sbom)

        self.conformity = dict(zip(type_of_project, name_for_sbom_s))

        for lang, sbom_path in self.conformity.items():
            generate_sbom = f"sudo cdxgen -t {lang} -o {sbom_path}.json"
            subprocess.run(generate_sbom, shell=True, check=True)

    def extract_names_from_sbom_s(self):
        """Извлекает названия библиотек из SBOM-ов"""
        self.dictionaries = {}
        for lang, file_path in self.conformity.items():
            try:
                with open(f"{file_path}.json", 'r') as file:
                    json_data = json.load(file)
                    names = [component['name'] for component in json_data.get("components", []) if 'name' in component]
                    self.dictionaries[lang] = names
            except FileNotFoundError:
                print(f"Файл не найден по пути: {file_path}")
            except json.JSONDecodeError:
                print(f"Неверный формат JSON в файле: {file_path}")

    def check_toxic_of_project(self):
        """Поиск вхождений токсичных библиотек"""
        from fuzzywuzzy import fuzz

        similarity_list = []  # Сохранение информации о сходстве

        for lang, sbom_value in self.dictionaries.items():
            a = sbom_value
            b = self.names_toxic_repos

            for a_word in a:
                for b_word in b:
                    similarity_ratio = fuzz.ratio(a_word.lower(), b_word.lower())
                    if similarity_ratio > 60:  # При необходимости отрегулируйте этот порог
                        similarity_list.append((lang, a_word, b_word, similarity_ratio))

        # Сортировка списка сходства в порядке убывания на основе коэффициента сходства
        similarity_list.sort(key=lambda x: x[3], reverse=True)

        for similarity_info in similarity_list:
            lang, a_word, b_word, similarity_ratio = similarity_info
            print(f"Для проекта на {lang} найдено сходство между: {a_word} и {b_word}, Сходство: {similarity_ratio}%")

    def run_toxic_checker(self):
        self.get_bd()
        self.installation()
        self.sbom_generation()
        self.extract_names_from_sbom_s()
        self.check_toxic_of_project()

if __name__ == "__main__":
    toxic_checker = ToxicChecker()
    toxic_checker.run_toxic_checker()
