import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

# Фон приложения
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# Инициализация базы
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS operations (
                    id INTEGER PRIMARY KEY, 
                    type TEXT, 
                    amount REAL, 
                    category TEXT)""")
conn.commit()


# Красивые кнопки
def styled_button(text, color=(0.2, 0.6, 0.9, 1)):
    return Button(
        text=text,
        size_hint=(1, 0.2),
        background_normal='',
        background_color=color,
        color=(1, 1, 1, 1),
        font_size=18
    )


# Экран главного меню
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=15, padding=25)

        btn_income = styled_button("Добавить доход", (0.2, 0.7, 0.3, 1))
        btn_income.bind(on_press=lambda x: setattr(self.manager, 'current', "add_income"))

        btn_expense = styled_button("Добавить расход", (0.9, 0.3, 0.3, 1))
        btn_expense.bind(on_press=lambda x: setattr(self.manager, 'current', "add_expense"))

        btn_stats = styled_button("Показать статистику", (0.3, 0.5, 0.9, 1))
        btn_stats.bind(on_press=lambda x: self.manager.get_screen("statistics").show_chart())

        btn_clear = styled_button("Очистить статистику", (0.5, 0.5, 0.5, 1))
        btn_clear.bind(on_press=self.clear_data)

        layout.add_widget(Label(text="УЧЁТ ФИНАНСОВ", font_size=28, bold=True, size_hint=(1, 0.2), color=(0, 0, 0, 1)))
        layout.add_widget(btn_income)
        layout.add_widget(btn_expense)
        layout.add_widget(btn_stats)
        layout.add_widget(btn_clear)
        self.add_widget(layout)

    def clear_data(self, instance):
        cursor.execute("DELETE FROM operations")
        conn.commit()
        print("Статистика очищена")


# Экран добавления дохода
class AddIncomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=15, padding=25)

        self.amount = TextInput(hint_text="Введите сумму", multiline=False, input_filter='float', font_size=18)
        self.category = TextInput(hint_text="Категория", multiline=False, font_size=18)
        save_btn = styled_button("💾 Сохранить", (0.2, 0.7, 0.3, 1))
        save_btn.bind(on_press=self.save_income)
        back_btn = styled_button("⬅ Назад", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', "menu"))

        layout.add_widget(Label(text="Добавить доход", font_size=24, size_hint=(1, 0.2), color=(0, 0, 0, 1)))
        layout.add_widget(self.amount)
        layout.add_widget(self.category)
        layout.add_widget(save_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def save_income(self, instance):
        if self.amount.text and self.category.text:
            cursor.execute("INSERT INTO operations (type, amount, category) VALUES (?, ?, ?)",
                           ("income", float(self.amount.text), self.category.text))
            conn.commit()
            self.manager.current = "menu"
            self.amount.text = ""
            self.category.text = ""


# Экран добавления расхода
class AddExpenseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=15, padding=25)

        self.amount = TextInput(hint_text="Введите сумму", multiline=False, input_filter='float', font_size=18)
        self.category = TextInput(hint_text="Категория", multiline=False, font_size=18)
        save_btn = styled_button("💾 Сохранить", (0.9, 0.3, 0.3, 1))
        save_btn.bind(on_press=self.save_expense)
        back_btn = styled_button("⬅ Назад", (0.5, 0.5, 0.5, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', "menu"))

        layout.add_widget(Label(text="Добавить расход", font_size=24, size_hint=(1, 0.2), color=(0, 0, 0, 1)))
        layout.add_widget(self.amount)
        layout.add_widget(self.category)
        layout.add_widget(save_btn)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def save_expense(self, instance):
        if self.amount.text and self.category.text:
            cursor.execute("INSERT INTO operations (type, amount, category) VALUES (?, ?, ?)",
                           ("expense", float(self.amount.text), self.category.text))
            conn.commit()
            self.manager.current = "menu"
            self.amount.text = ""
            self.category.text = ""


# Экран статистики
class StatisticsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def show_chart(self):
        cursor.execute("SELECT category, SUM(amount) FROM operations WHERE type='income' GROUP BY category")
        income_data = cursor.fetchall()
        cursor.execute("SELECT category, SUM(amount) FROM operations WHERE type='expense' GROUP BY category")
        expense_data = cursor.fetchall()

        income_values = [c[1] for c in income_data]
        income_categories = [c[0] for c in income_data]
        expense_values = [c[1] for c in expense_data]
        expense_categories = [c[0] for c in expense_data]

        positions = [0, 1]  # 0 = доходы, 1 = расходы
        bottom = [0, 0]

        plt.figure(figsize=(7, 6))
        colors_list = [cm.viridis, cm.plasma]

        # Рисуем столбцы
        for col in range(2):
            values = income_values if col == 0 else expense_values
            labels = income_categories if col == 0 else expense_categories
            colors = colors_list[col](np.linspace(0, 1, len(values))) if values else []
            for i, val in enumerate(values):
                plt.bar(positions[col], val, bottom=bottom[col], color=colors[i])
                plt.text(positions[col], bottom[col] + val / 2,
                         f"{labels[i]}: {val:.2f}",
                         ha='center', va='center',
                         color='black', fontsize=9, fontweight='bold')
                bottom[col] += val

        plt.xticks(positions, ['Доходы', 'Расходы'], fontsize=12)
        plt.ylabel("Сумма", fontsize=12)
        plt.title("Финансовая статистика", fontsize=14, fontweight="bold")

        # Итоговые суммы
        total_income = sum(income_values)
        total_expense = sum(expense_values)
        plt.text(0, bottom[0] + max(bottom)*0.05, f"Всего: {total_income:.2f}", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')
        plt.text(1, bottom[1] + max(bottom)*0.05, f"Всего: {total_expense:.2f}", ha='center', va='bottom', fontsize=10, color='black', fontweight='bold')

        plt.tight_layout()
        plt.show()



# Основное приложение
class FinanceApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(AddIncomeScreen(name="add_income"))
        sm.add_widget(AddExpenseScreen(name="add_expense"))
        sm.add_widget(StatisticsScreen(name="statistics"))
        return sm


if __name__ == "__main__":
    FinanceApp().run()
