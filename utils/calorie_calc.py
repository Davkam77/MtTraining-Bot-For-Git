def calc_calories(weight, height, age, gender, activity, goal):
    if gender == "m":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    tdee = bmr * activity
    deficit = 500 if goal < weight else 0
    return tdee - deficit
