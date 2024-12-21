from matplotlib import pyplot as plt
from collections import defaultdict
import numpy as np


class Graphics:
    def __init__(self, levels, balances, survival_data, max_level, auction_data, colonies):
        """
        Инициализация графического модуля.

        :param levels: Список уровней колоний
        :param balances: Список балансов колоний
        :param survival_data: Список выживших колоний по циклам
        :param max_level: Максимальный уровень колоний
        :param auction_data: Данные аукционов (опционально)
        :param colonies: Список колоний
        """
        self.levels = levels
        self.colonies = colonies
        self.balances = balances
        self.survival_data = survival_data
        self.max_level = max_level
        self.auction_data = auction_data or []
        print(f"Graphics initialized with max_level = {max_level}")

    def plot_average_balance_by_level(self):
        """Средний баланс по уровням."""
        balance_by_level = defaultdict(list)
        for level, balance in zip(self.levels, self.balances):
            balance_by_level[level].append(balance)

        avg_balance = {level: np.mean(values) for level, values in balance_by_level.items()}
        plt.bar(avg_balance.keys(), avg_balance.values(), color="gold", alpha=0.7)
        plt.title("Средний баланс по уровням")
        plt.xlabel("Уровень")
        plt.ylabel("Средний баланс")
        plt.show()

    def plot_auction_winning_bids(self):
        """Распределение победных ставок в аукционах."""
        if not self.auction_data:
            print("Нет данных об аукционах для графика.")
            return

        winning_bids = [data["winning_bid"] for data in self.auction_data]
        plt.hist(winning_bids, bins=20, alpha=0.7, color="teal")
        plt.title("Распределение победных ставок")
        plt.xlabel("Ставка")
        plt.ylabel("Количество")
        plt.show()

    def plot_survival_vs_defeat_ratio(self):
        """Процентное соотношение выживших и побежденных."""
        # Фильтруем активные колонии (выжившие) и выбывшие
        active_colonies = [colony for colony in self.colonies if colony.alive]
        defeated_colonies = [colony for colony in self.colonies if not colony.alive]

        survival_count = len(active_colonies)
        defeat_count = len(defeated_colonies)

        labels = ["Выжившие", "Побежденные"]
        sizes = [survival_count, defeat_count]
        colors = ["blue", "red"]

        plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
        plt.title("Соотношение выживших и побежденных")
        plt.show()

    def plot_auction_win_probability_by_level(self):
        """Вероятность победы в аукционах по уровням."""
        if not self.auction_data:
            print("Нет данных об аукционах для графика.")
            return

        wins_by_level = defaultdict(int)
        participation_by_level = defaultdict(int)

        for data in self.auction_data:
            level = data["winner_level"]
            wins_by_level[level] += 1
            for participant in data["participants"]:
                participation_by_level[participant] += 1

        probabilities = {
            level: wins_by_level[level] / participation_by_level[level]
            for level in participation_by_level if participation_by_level[level] > 0
        }

        plt.bar(probabilities.keys(), probabilities.values(), alpha=0.7, color="purple")
        plt.title("Вероятность победы в аукционах по уровням")
        plt.xlabel("Уровень")
        plt.ylabel("Вероятность")
        plt.show()

    def plot_level_distribution(self):
        """Гистограмма распределения уровней колоний."""
        plt.hist(self.levels, bins=range(1, self.max_level + 2), alpha=0.7, color="blue")
        plt.title("Распределение уровней колоний")
        plt.xlabel("Уровень")
        plt.ylabel("Количество")
        plt.show()

    def plot_balance_distribution(self):
        """Гистограмма распределения балансов колоний."""
        plt.hist(self.balances, bins=20, alpha=0.7, color="orange")
        plt.title("Распределение балансов колоний")
        plt.xlabel("Баланс")
        plt.ylabel("Количество")
        plt.show()

    def plot_survival_curve(self):
        """График выживаемости колоний по циклам."""
        plt.plot(self.survival_data, label="Выживаемость", color="green")
        plt.title("График выживаемости колоний")
        plt.xlabel("Цикл")
        plt.ylabel("Количество выживших")
        plt.legend()
        plt.show()

    def plot_average_survival_by_level(self):
        """График средней выживаемости по уровням."""
        survival_by_level = defaultdict(list)

        for level, survival in zip(self.levels, self.survival_data):
            survival_by_level[level].append(survival)

        avg_survival = {level: np.mean(values) for level, values in survival_by_level.items()}

        plt.bar(avg_survival.keys(), avg_survival.values(), alpha=0.7, color="purple")
        plt.title("Средняя выживаемость по уровням")
        plt.xlabel("Уровень")
        plt.ylabel("Средняя выживаемость")
        plt.show()

    def plot_max_level_progression(self, level_progression):
        """График прогресса максимального уровня по циклам."""
        plt.plot(level_progression, label="Максимальный уровень", color="red")
        plt.title("Прогресс максимального уровня")
        plt.xlabel("Цикл")
        plt.ylabel("Максимальный уровень")
        plt.legend()
        plt.show()

    def plot_level_growth_distribution(self, levels_growth):
        """График распределения прироста уровня."""
        plt.hist(levels_growth, bins=20, alpha=0.7, color="cyan")
        plt.title("Распределение прироста уровня")
        plt.xlabel("Прирост уровня")
        plt.ylabel("Количество")
        plt.show()

    def plot_balance_change(self, balances_by_cycle):
        """График изменения балансов колоний по циклам."""
        for i, balances in enumerate(balances_by_cycle):
            plt.plot(balances, label=f"Цикл {i + 1}")

        plt.title("Изменение балансов колоний")
        plt.xlabel("Цикл")
        plt.ylabel("Баланс")
        plt.legend()
        plt.show()

    def plot_survival_and_levels(self, level_progression):
        """Сводный график выживаемости и роста максимального уровня."""
        plt.plot(self.survival_data, label="Выживаемость", color="blue")
        plt.plot(level_progression, label="Максимальный уровень", color="green")
        plt.title("Выживаемость и максимальный уровень")
        plt.xlabel("Цикл")
        plt.ylabel("Значения")
        plt.legend()
        plt.show()