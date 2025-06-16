def generate_mealplan(kcal):
    breakfast = round(kcal * 0.25)
    lunch = round(kcal * 0.35)
    dinner = round(kcal * 0.25)
    snacks = kcal - (breakfast + lunch + dinner)

    return {
        "Завтрак": f"Овсянка с фруктами (~{breakfast} ккал)",
        "Обед": f"Курица с рисом и салатом (~{lunch} ккал)",
        "Ужин": f"Рыба с овощами (~{dinner} ккал)",
        "Перекусы": f"Орехи, йогурт (~{snacks} ккал)"
    }
