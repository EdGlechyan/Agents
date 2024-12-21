def dust_storm(colony, log, income_reduction=20, expense_increase=10):
    colony.income -= colony.income * (income_reduction / 100)
    colony.expenses += colony.expenses * (expense_increase / 100)
    log.append(
        f"{colony.name}: Пыльная буря! Доход уменьшен на {income_reduction}%, расходы увеличены на {expense_increase}%.")


def renaissance(colony, log, income_increase=20, expense_reduction=10):
    colony.income += colony.income * (income_increase / 100)
    colony.expenses -= colony.expenses * (expense_reduction / 100)
    colony.expenses = max(1, colony.expenses)
    log.append(
        f"{colony.name}: Ренессанс! Доход увеличен на {income_increase}%, расходы уменьшены на {expense_reduction}%.")