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

    def add_race(self):
        # Создаем новое окно для добавления расы
        add_race_window = tk.Toplevel(self)
        add_race_window.title("Добавить расу")
        add_race_window.geometry("400x500")

        # Поля для ввода основных характеристик
        ttk.Label(add_race_window, text="Имя расы:").pack(pady=5)
        name_entry = ttk.Entry(add_race_window)
        name_entry.pack(pady=5)

        ttk.Label(add_race_window, text="Скорость:").pack(pady=5)
        speed_entry = ttk.Entry(add_race_window)
        speed_entry.pack(pady=5)

        ttk.Label(add_race_window, text="Размер:").pack(pady=5)
        size_entry = ttk.Entry(add_race_window)
        size_entry.pack(pady=5)

        ttk.Label(add_race_window, text="Темное зрение:").pack(pady=5)
        dark_vision_entry = ttk.Entry(add_race_window)
        dark_vision_entry.pack(pady=5)

        # Секция для навыков
        ttk.Label(add_race_window, text="Навыки:").pack(pady=5)
        skills_frame = ttk.Frame(add_race_window)
        skills_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        skills_listbox = tk.Listbox(skills_frame)
        skills_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        skills_scrollbar = ttk.Scrollbar(skills_frame, orient="vertical", command=skills_listbox.yview)
        skills_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        skills_listbox.config(yscrollcommand=skills_scrollbar.set)

        # Кнопки управления навыками
        skill_buttons_frame = ttk.Frame(add_race_window)
        skill_buttons_frame.pack(pady=5)

        def add_skill():
            skill_data = self.get_skill_data_dialog()
            if skill_data:
                skills_listbox.insert(tk.END, skill_data['Название'])
                skills_listbox.skills.append(skill_data)

        def edit_skill():
            selected_index = skills_listbox.curselection()
            if selected_index:
                index = selected_index[0]
                skill_data = skills_listbox.skills[index]
                updated_skill = self.get_skill_data_dialog(skill_data)
                if updated_skill:
                    skills_listbox.delete(index)
                    skills_listbox.insert(index, updated_skill['Название'])
                    skills_listbox.skills[index] = updated_skill

        def delete_skill():
            selected_index = skills_listbox.curselection()
            if selected_index:
                index = selected_index[0]
                del skills_listbox.skills[index]
                skills_listbox.delete(index)

        skills_listbox.skills = []

        add_skill_button = ttk.Button(skill_buttons_frame, text="Добавить навык", command=add_skill)
        add_skill_button.pack(side=tk.LEFT, padx=5)

        edit_skill_button = ttk.Button(skill_buttons_frame, text="Редактировать навык", command=edit_skill)
        edit_skill_button.pack(side=tk.LEFT, padx=5)

        delete_skill_button = ttk.Button(skill_buttons_frame, text="Удалить навык", command=delete_skill)
        delete_skill_button.pack(side=tk.LEFT, padx=5)

        def save_race():
            name = name_entry.get().strip()
            speed = speed_entry.get().strip()
            size = size_entry.get().strip()
            dark_vision = dark_vision_entry.get().strip()

            if not name:
                messagebox.showerror("Ошибка", "Введите имя расы.")
                return
            if not speed.isdigit():
                messagebox.showerror("Ошибка", "Скорость должна быть числом.")
                return

            race = {
                "Имя": name,
                "Скорость": speed,
                "Размер": size,
                "Темное зрение": dark_vision,
                "Навыки": skills_listbox.skills
            }

            self.races.append(race)
            self.update_race_list()
            messagebox.showinfo("Успех", "Раса добавлена.")
            add_race_window.destroy()

        save_button = ttk.Button(add_race_window, text="Сохранить расу", command=save_race)
        save_button.pack(pady=10)

    def get_skill_data_dialog(self, skill=None):
        skill_window = tk.Toplevel(self)
        skill_window.title("Добавить навык" if skill is None else "Редактировать навык")
        skill_window.geometry("400x400")

        ttk.Label(skill_window, text="Название навыка:").pack(pady=5)
        name_entry = ttk.Entry(skill_window)
        name_entry.pack(pady=5)

        ttk.Label(skill_window, text="Описание:").pack(pady=5)
        description_text = tk.Text(skill_window, height=5)
        description_text.pack(pady=5)

        is_important_var = tk.BooleanVar()
        is_important_check = ttk.Checkbutton(skill_window, text="Важный навык", variable=is_important_var)
        is_important_check.pack(pady=5)

        # Секция для опций навыка
        ttk.Label(skill_window, text="Опции:").pack(pady=5)
        options_frame = ttk.Frame(skill_window)
        options_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        options_listbox = tk.Listbox(options_frame)
        options_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        options_scrollbar = ttk.Scrollbar(options_frame, orient="vertical", command=options_listbox.yview)
        options_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        options_listbox.config(yscrollcommand=options_scrollbar.set)

        options_listbox.options = []

        # Кнопки управления опциями
        options_buttons_frame = ttk.Frame(skill_window)
        options_buttons_frame.pack(pady=5)

        def add_option():
            option_data = self.get_option_data_dialog()
            if option_data:
                options_listbox.insert(tk.END, option_data['Название'])
                options_listbox.options.append(option_data)

        def edit_option():
            selected_index = options_listbox.curselection()
            if selected_index:
                index = selected_index[0]
                option_data = options_listbox.options[index]
                updated_option = self.get_option_data_dialog(option_data)
                if updated_option:
                    options_listbox.delete(index)
                    options_listbox.insert(index, updated_option['Название'])
                    options_listbox.options[index] = updated_option

        def delete_option():
            selected_index = options_listbox.curselection()
            if selected_index:
                index = selected_index[0]
                del options_listbox.options[index]
                options_listbox.delete(index)

        add_option_button = ttk.Button(options_buttons_frame, text="Добавить опцию", command=add_option)
        add_option_button.pack(side=tk.LEFT, padx=5)

        edit_option_button = ttk.Button(options_buttons_frame, text="Редактировать опцию", command=edit_option)
        edit_option_button.pack(side=tk.LEFT, padx=5)

        delete_option_button = ttk.Button(options_buttons_frame, text="Удалить опцию", command=delete_option)
        delete_option_button.pack(side=tk.LEFT, padx=5)

        ttk.Label(skill_window, text="Дополнительная информация:").pack(pady=5)
        additional_text = tk.Text(skill_window, height=3)
        additional_text.pack(pady=5)

        if skill:
            name_entry.insert(0, skill.get('Название', ''))
            description_text.insert(tk.END, skill.get('Описание', ''))
            is_important_var.set(skill.get('Важный', 'Нет') == 'Да')
            additional_text.insert(tk.END, skill.get('Дополнительно', ''))
            options_listbox.options = skill.get('Опции', [])
            for option in options_listbox.options:
                options_listbox.insert(tk.END, option['Название'])

        def save_skill():
            name = name_entry.get().strip()
            description = description_text.get(1.0, tk.END).strip()
            is_important = 'Да' if is_important_var.get() else 'Нет'
            additional = additional_text.get(1.0, tk.END).strip()

            if not name:
                messagebox.showerror("Ошибка", "Введите название навыка.")
                return

            skill_data = {
                "Название": name,
                "Описание": description,
                "Важный": is_important,
                "Опции": options_listbox.options,
                "Дополнительно": additional
            }

            skill_window.skill_data = skill_data
            skill_window.destroy()

        save_button = ttk.Button(skill_window, text="Сохранить навык", command=save_skill)
        save_button.pack(pady=10)

        skill_window.skill_data = None
        self.wait_window(skill_window)
        return skill_window.skill_data

    def get_option_data_dialog(self, option=None):
        option_window = tk.Toplevel(self)
        option_window.title("Добавить опцию" if option is None else "Редактировать опцию")
        option_window.geometry("300x200")

        ttk.Label(option_window, text="Название опции:").pack(pady=5)
        name_entry = ttk.Entry(option_window)
        name_entry.pack(pady=5)

        ttk.Label(option_window, text="Описание опции:").pack(pady=5)
        description_text = tk.Text(option_window, height=5)
        description_text.pack(pady=5)

        if option:
            name_entry.insert(0, option.get('Название', ''))
            description_text.insert(tk.END, option.get('Описание', ''))

        def save_option():
            name = name_entry.get().strip()
            description = description_text.get(1.0, tk.END).strip()

            if not name:
                messagebox.showerror("Ошибка", "Введите название опции.")
                return

            option_data = {
                "Название": name,
                "Описание": description
            }

            option_window.option_data = option_data
            option_window.destroy()

        save_button = ttk.Button(option_window, text="Сохранить опцию", command=save_option)
        save_button.pack(pady=10)

        option_window.option_data = None
        self.wait_window(option_window)
        return option_window.option_data

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
