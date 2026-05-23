def lemonade_change(bills: list) -> bool:
    five = 0
    ten = 0
    for i in range(len(bills)):
        if bills[i] == 5:
            five += 1
        elif bills[i] == 10:
            if five:
                five -= 1
                ten += 1
            else:
                return False
        else:
            if five and ten:
                five -= 1
                ten -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True

bills = [5,5,5,10,20]
# bills = [5,5,10,10,20]

print(lemonade_change(bills))