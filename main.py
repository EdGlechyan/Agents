import random
import pandas as pd
from Graphics import Graphics
from const import *
from Effect import Effect
from Colony import Colony
from Artifact import Artifact
from Environment import dust_storm, renaissance

# Функции симуляции
def run_cycle(active_colonies, winners, losers, cycle_number, log):
    log.append(f"\nЦикл {cycle_number}: Начало.")

    for i, colony in enumerate(active_colonies[:]):
        if colony.is_winner:
            winners.append(colony)
            active_colonies.remove(colony)
            continue

        colony.rounds_played += 1
        colony.apply_effects(log, cycle_number, i)
        colony.update_balance(log)
        colony.check_level_up(log, cycle_number)

        if not colony.alive:
            if colony.is_winner:
                winners.append(colony)
            else:
                losers.append(colony)
            active_colonies.remove(colony)


    if cycle_number % EVENT_INTERVAL == 0:
        event = random.choice([dust_storm, renaissance])
        log.append("\nСобытие среды:")
        for colony in active_colonies:
            event(colony, log)

    if cycle_number % AUCTION_INTERVAL == 0:
        run_auction(active_colonies, log, auction_data)

def choose_opponent(colony):
    opponents = [c for c in active_colonies if c != colony]
    if opponents:
        strongest_opponent = max(opponents, key=lambda c: c.level)
        return strongest_opponent
    else:
        return None



artifact_pool = [
    # Артефакт 16:
    Artifact("Артефакт 16", [
        Effect('experience', 20, 3, "+20% к опыту", duration_type='rounds', experience_base=EXPERIENCE_THRESHOLD),
        Effect('income', 20, 1, "Увеличение дохода на 20%", duration_type='once'),
        Effect('balance_multiply', 2, 1, "Умножение баланса х2", duration_type='until_next_event')
    ]),

    # Артефакт 42:
    Artifact("Артефакт 42", [
        Effect('balance_fixed', 100, 1, "Баланс +100", duration_type='until_next_auction'),
        Effect('expenses_fixed', 10, 3, "Расходы -10", duration_type='rounds'),
        Effect('zero_experience', 0, 1, "Обнуление опыта соперника", duration_type='once', target_colony_func=choose_opponent)
    ]),

    # Артефакт 63:
    Artifact("Артефакт 63", [
        Effect('income_fixed', 50, 5, "Доход +50", duration_type='rounds'),
        Effect('experience_fixed', 50, 5, "+50 опыта", duration_type='iterations')
    ]),

    # Артефакт 62:
    Artifact("Артефакт 62", [
        Effect('expenses_fixed', 10, 1, "Расходы -10", duration_type='until_next_event')
    ]),

    # Артефакт 38:
    Artifact("Артефакт 38", [
        Effect('balance_multiply', 2, 1, "Умножение баланса х2", duration_type='once')
    ]),
]



def run_auction(active_colonies, log, auction_data):
    log.append("\nАукцион начинается.")
    active_bidders = [c for c in active_colonies if c.balance > 5]
    if not active_bidders:
        log.append("Нет доступных колоний для участия в аукционе.")
        return

    for artifact in artifact_pool:
        if not active_bidders:
            break

        log.append(f"Лот: {artifact.name} ({len(active_bidders)} участников)")
        bids = {}

        for colony in active_bidders:
            utility = 0
            for effect in artifact.effects:
                if effect.effect_type == 'income' or effect.effect_type == 'income_fixed':
                    value = colony.income * (effect.value / 100) if effect.effect_type == 'income' else effect.value
                    utility += value * INCOME_WEIGHT * (
                        effect.duration)
                elif effect.effect_type == 'expenses' or effect.effect_type == 'expenses_fixed':
                    value = colony.expenses * (effect.value / 100) if effect.effect_type == 'expenses' else effect.value
                    utility -= value * EXPENSES_WEIGHT * (effect.duration)
                elif effect.effect_type == 'balance' or effect.effect_type == 'balance_fixed' or effect.effect_type == 'balance_multiply':
                    value = colony.balance * effect.value if effect.effect_type == 'balance_multiply' else (
                        colony.balance * (effect.value / 100) if effect.effect_type == 'balance' else effect.value)
                    utility += value * BALANCE_WEIGHT * (effect.duration)
                elif effect.effect_type == 'experience' or effect.effect_type == 'experience_fixed':
                    remaining_exp = EXPERIENCE_THRESHOLD - colony.experience
                    experience_gain = effect.experience_base * (
                                effect.value / 100) if effect.effect_type == 'experience' else effect.value
                    utility += max(0, min(1, experience_gain / max(1,
                                                                   remaining_exp))) * EXPERIENCE_WEIGHT * colony.income * (
                                   effect.duration)
                elif effect.effect_type == 'zero_experience':
                    opponent = choose_opponent(colony)
                    if opponent:
                        utility += opponent.experience * ZERO_EXPERIENCE_WEIGHT * (
                            effect.duration)

            total_weighted_value = sum(effect.value * effect.duration for effect in artifact.effects)
            duration_sum = sum(effect.duration for effect in artifact.effects)
            cost_estimate = total_weighted_value / (duration_sum if duration_sum > 0 else 1)

            if utility > cost_estimate * BID_THRESHOLD:
                max_bid = int(colony.balance * MAX_BET)
                bid = (int(utility * BID_PERCENTAGE), max_bid)
                bids[colony] = bid
                log.append(f"{colony.name} предложила {bid} единиц.")

        if not bids:
            log.append("Ни одна колония не сделала ставку на текущем аукционе.")
            return

        winner = max(bids, key=bids.get)
        winning_bid = bids[winner]

        auction_data.append({
            "artifact": artifact.name,
            "winning_bid": winning_bid,
            "winner_name": winner.name,
            "winner_level": winner.level,
            "participants": [c.level for c in active_bidders],
        })

        log.append(f"{winner.name} выигрывает лот с ставкой {winning_bid} единиц!")
        winner.balance -= winning_bid[1]
        artifact.apply_artifact(winner, log)


    log.append("Аукцион завершён.")


# Инициализация колоний
colonies = [
    Colony(f"Колония {i + 1}", INITIAL_BALANCE, random.randint(10, 50), random.randint(5, 30))
    for i in range(COLONY_COUNT)
]

log = []
active_colonies = colonies[:]
winners = []
losers = []

survival_data = []
level_progression = []
levels_growth = []
balances_by_cycle = []
victory_levels = []
defeat_levels = []

auction_data = []
previous_total_level = sum(colony.level for colony in colonies)

for cycle in range(1, SIMULATION_TIME + 1):
    if not active_colonies:
        break

    run_cycle(active_colonies, winners, losers, cycle, log)

    # Обновление данных для графиков
    # 1. Прогресс уровней (средний уровень)
    avg_level = sum(colony.level for colony in active_colonies) / max(1, len(active_colonies))
    level_progression.append(avg_level)

    # 2. Прирост уровней
    current_total_level = sum(colony.level for colony in active_colonies)
    levels_growth.append(current_total_level - previous_total_level)
    previous_total_level = current_total_level

    # 3. Балансы по циклам
    balances_by_cycle.append([colony.balance for colony in active_colonies])

    # 4. Уровни победителей
    for winner in winners:
        if winner.level not in victory_levels:
            victory_levels.append(winner.level)

    # 5. Уровни выбывших
    for loser in losers:
        if loser.level not in defeat_levels:
            defeat_levels.append(loser.level)

    # Сохраняем количество выживших для графика выживаемости
    survival_data.append(len(active_colonies))

# Сохранение лога в файл
with open(FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

# Построение графиков

levels = [c.level for c in colonies]
balances = [c.balance for c in colonies]

graphics = Graphics(levels=levels, balances=balances, survival_data=survival_data, max_level=MAX_LEVEL, auction_data=auction_data, colonies=colonies)
graphics.plot_level_distribution()
graphics.plot_balance_distribution()
graphics.plot_survival_curve()

# Дополнительные графики с динамически посчитанными данными
graphics.plot_average_survival_by_level()
graphics.plot_max_level_progression(level_progression)
graphics.plot_level_growth_distribution(levels_growth)
graphics.plot_balance_change(balances_by_cycle)

graphics.plot_survival_and_levels(level_progression)
graphics.plot_average_balance_by_level()
graphics.plot_auction_winning_bids()
graphics.plot_survival_vs_defeat_ratio()
graphics.plot_auction_win_probability_by_level()


# Сбор итоговой таблицы
colony_info = [
    {
        "Название": c.name,
        "Уровень": c.level,
        "Баланс": c.balance,
        "Статус": "Победитель" if c in winners else ("Выбыла" if c in losers else "Активна"),
        "Раунды сыграно": c.rounds_played,
        "Итерация достижения максимального уровня": c.level_up_iteration if c.is_winner else "Не достиг",
        "Причина выбытия": "Баланс отрицателен" if c in losers else "Не выбыла",
    } for c in colonies
]

pd.set_option('display.max_rows', None)  # Показывать все строки
pd.set_option('display.max_columns', None)  # Показывать все столбцы
df = pd.DataFrame(colony_info)
print(df)