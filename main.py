import json
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class RaceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Менеджер Рас")
        self.geometry("900x600")
        self.filename = "races.json"
        self.races = self.load_races()

        # Устанавливаем тему
        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # Вы можете выбрать 'default', 'clam', 'alt', 'classic'

        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        self.style.configure('TButton', font=('Helvetica', 10))
        self.style.configure('TLabel', font=('Helvetica', 10))
        self.style.configure('Treeview', font=('Helvetica', 10))
        self.style.configure('Treeview.Heading', font=('Helvetica', 11, 'bold'))
        self.style.configure('TEntry', font=('Helvetica', 10))
        self.style.configure('TNotebook', font=('Helvetica', 10))
        self.style.configure('TNotebook.Tab', font=('Helvetica', 10))

    def create_widgets(self):
        self.create_menu()

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_race_list(main_frame)
        self.create_details_area(main_frame)

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Загрузить", command=self.load_races)
        file_menu.add_command(label="Сохранить", command=self.save_races)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        self.config(menu=menubar)

    def create_race_list(self, parent):
        left_frame = ttk.Frame(parent)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Добавляем поиск
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(search_frame, text="Поиск:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_var.trace_add('write', self.update_race_list)

        # Используем Treeview для списка рас
        columns = ('Имя',)
        self.race_tree = ttk.Treeview(left_frame, columns=columns, show='headings')
        self.race_tree.heading('Имя', text='Имя')
        self.race_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5)

        self.update_race_list()

        self.race_tree.bind('<<TreeviewSelect>>', self.on_race_select)

        self.create_buttons(left_frame)

    def update_race_list(self, *args):
        search_text = self.search_var.get().lower()
        for item in self.race_tree.get_children():
            self.race_tree.delete(item)
        for idx, race in enumerate(self.races):
            race_name = race.get('Имя', 'Безымянная раса')
            if search_text in race_name.lower():
                self.race_tree.insert('', 'end', iid=idx, values=(race_name,))

    def on_race_select(self, event):
        selected_item = self.race_tree.focus()
        if selected_item:
            index = int(selected_item)
            race = self.races[index]
            self.show_race_details(race)

    def show_race_details(self, race):
        self.details_text.configure(state='normal')
        self.details_text.delete(1.0, tk.END)
        details = f"Имя: {race.get('Имя', '')}\n"
        details += f"Скорость: {race.get('Скорость', '')}\n"
        details += f"Размер: {race.get('Размер', '')}\n"
        details += f"Темное зрение: {race.get('Темное зрение', '')}\n"
        details += "\nНавыки:\n"
        for skill in race.get("Навыки", []):
            details += f"- {skill.get('Название', '')}\n"
            details += f"  Важный: {skill.get('Важный', 'Нет')}\n"
            details += f"  Описание: {skill.get('Описание', '')}\n"
            if "Опции" in skill:
                details += "  Опции:\n"
                for option in skill["Опции"]:
                    details += f"    • {option.get('Название', '')}: {option.get('Описание', '')}\n"
            if "Дополнительно" in skill:
                details += f"  Дополнительно: {skill.get('Дополнительно', '')}\n"
            details += "\n"
        self.details_text.insert(tk.END, details)
        self.details_text.configure(state='disabled')

    def create_buttons(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        add_button = ttk.Button(button_frame, text="Добавить расу", command=self.add_race)
        add_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(button_frame, text="Удалить расу", command=self.delete_race)
        delete_button.pack(side=tk.LEFT, padx=5)

        half_race_button = ttk.Button(button_frame, text="Отобразить полурасу", command=self.display_half_race)
        half_race_button.pack(side=tk.LEFT, padx=5)

    def create_details_area(self, parent):
        right_frame = ttk.Frame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка с деталями расы
        details_frame = ttk.Frame(notebook)
        notebook.add(details_frame, text='Детали')

        self.details_text = tk.Text(details_frame, wrap=tk.WORD, state='disabled')
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вы можете добавить дополнительные вкладки при необходимости

    def add_race(self):
        race = self.get_race_data()
        if race:
            self.races.append(race)
            self.update_race_list()
            messagebox.showinfo("Успех", "Раса добавлена.")

    def get_race_data(self):
        name = simpledialog.askstring("Название расы", "Введите название расы:")
        if not name:
            return None
        speed = simpledialog.askstring("Скорость", "Введите скорость расы (число):")
        if not speed or not speed.isdigit():
            messagebox.showerror("Ошибка", "Скорость должна быть числом.")
            return None
        size = simpledialog.askstring("Размер", "Введите размер расы:")
        dark_vision = simpledialog.askstring("Темное зрение", "Введите дальность темного зрения или 'Нет':")
        num_skills = simpledialog.askinteger("Навыки", "Сколько навыков вы хотите добавить?")
        if num_skills is None or num_skills < 0:
            messagebox.showerror("Ошибка", "Некорректное количество навыков.")
            return None
        race = {
            "Имя": name,
            "Скорость": speed,
            "Размер": size,
            "Темное зрение": dark_vision,
            "Навыки": []
        }
        for i in range(num_skills):
            skill = self.get_skill_data(i+1)
            if skill:
                race["Навыки"].append(skill)
        return race

    def get_skill_data(self, skill_number):
        name = simpledialog.askstring(f"Навык {skill_number}", "Введите название навыка:")
        if not name:
            return None
        description = simpledialog.askstring(f"Навык {skill_number}", "Введите описание навыка:")
        is_important = messagebox.askyesno(f"Навык {skill_number}", "Является ли навык важным?")
        skill = {
            "Название": name,
            "Описание": description,
            "Важный": "Да" if is_important else "Нет"
        }
        has_options = messagebox.askyesno(f"Навык {skill_number}", "Есть ли у навыка опции?")
        if has_options:
            num_options = simpledialog.askinteger(f"Навык {skill_number}", "Сколько опций у навыка?")
            skill["Опции"] = []
            for j in range(num_options):
                option_name = simpledialog.askstring(f"Опция {j+1} для навыка {name}", "Введите название опции:")
                option_description = simpledialog.askstring(f"Опция {j+1} для навыка {name}", "Введите описание опции:")
                option = {
                    "Название": option_name,
                    "Описание": option_description
                }
                skill["Опции"].append(option)
        has_additional = messagebox.askyesno(f"Навык {skill_number}", "Есть ли дополнительная информация?")
        if has_additional:
            additional = simpledialog.askstring(f"Навык {skill_number}", "Введите дополнительную информацию:")
            skill["Дополнительно"] = additional
        return skill

    def delete_race(self):
        selected_item = self.race_tree.focus()
        if selected_item:
            index = int(selected_item)
            race_name = self.races[index].get('Имя', 'Безымянная раса')
            confirm = messagebox.askyesno("Удалить расу", f"Вы уверены, что хотите удалить расу '{race_name}'?")
            if confirm:
                del self.races[index]
                self.update_race_list()
                self.details_text.configure(state='normal')
                self.details_text.delete(1.0, tk.END)
                self.details_text.configure(state='disabled')
                messagebox.showinfo("Успех", "Раса удалена.")
        else:
            messagebox.showwarning("Предупреждение", "Сначала выберите расу для удаления.")

    def display_half_race(self):
        if len(self.races) < 2:
            messagebox.showwarning("Предупреждение", "Недостаточно рас для создания полурасы.")
            return
        selection_window = tk.Toplevel(self)
        selection_window.title("Выбор рас для полурасы")
        selection_window.geometry("300x200")

        ttk.Label(selection_window, text="Выберите первую расу:").pack(pady=5)
        race1_var = tk.StringVar()
        race1_combobox = ttk.Combobox(selection_window, textvariable=race1_var)
        race1_combobox['values'] = [race.get('Имя', 'Безымянная раса') for race in self.races]
        race1_combobox.pack()

        ttk.Label(selection_window, text="Выберите вторую расу:").pack(pady=5)
        race2_var = tk.StringVar()
        race2_combobox = ttk.Combobox(selection_window, textvariable=race2_var)
        race2_combobox['values'] = [race.get('Имя', 'Безымянная раса') for race in self.races]
        race2_combobox.pack()

        def create_half_race():
            race1_name = race1_var.get()
            race2_name = race2_var.get()
            if race1_name == race2_name or not race1_name or not race2_name:
                messagebox.showerror("Ошибка", "Выберите две разные расы.")
                return
            race1 = next((race for race in self.races if race.get('Имя') == race1_name), None)
            race2 = next((race for race in self.races if race.get('Имя') == race2_name), None)
            if not race1 or not race2:
                messagebox.showerror("Ошибка", "Ошибка выбора рас.")
                return
            half_race = self.generate_half_race(race1, race2)
            self.show_race_details(half_race)
            selection_window.destroy()

        ttk.Button(selection_window, text="Создать полурасу", command=create_half_race).pack(pady=10)

    def generate_half_race(self, race1, race2):
        half_race = {}
        half_race_name = f"Полураса: {race1['Имя']}/{race2['Имя']}"
        half_race["Имя"] = half_race_name

        # Случайный выбор скорости
        speed1 = race1.get("Скорость", "0")
        speed2 = race2.get("Скорость", "0")
        half_race["Скорость"] = random.choice([speed1, speed2])

        # Случайный выбор размера
        size1 = race1.get("Размер", "")
        size2 = race2.get("Размер", "")
        half_race["Размер"] = random.choice([size1, size2])

        # Случайный выбор темного зрения
        dark_vision1 = race1.get("Темное зрение", "Нет")
        dark_vision2 = race2.get("Темное зрение", "Нет")
        half_race["Темное зрение"] = random.choice([dark_vision1, dark_vision2])

        # Объединение навыков
        skills1 = race1.get("Навыки", [])
        skills2 = race2.get("Навыки", [])
        all_skills = skills1 + skills2

        # Определение максимального количества навыков
        num_skills1 = len(skills1)
        num_skills2 = len(skills2)
        max_skills = int((num_skills1 + num_skills2) / 2)

        # Случайный выбор навыков
        if max_skills > 0:
            unique_skills = {skill['Название']: skill for skill in all_skills}
            skill_list = list(unique_skills.values())
            selected_skills = random.sample(skill_list, min(max_skills, len(skill_list)))
        else:
            selected_skills = []

        half_race["Навыки"] = selected_skills

        return half_race

    def load_races(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                races = json.load(f)
            return races
        except FileNotFoundError:
            messagebox.showwarning("Предупреждение", "Файл не найден. Будет создан новый при сохранении.")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Ошибка чтения данных из файла. Начинаем с пустого списка.")
            return []

    def save_races(self):
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.races, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные успешно сохранены.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении данных: {e}")

if __name__ == "__main__":
    app = RaceApp()
    app.mainloop()
