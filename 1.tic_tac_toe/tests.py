unit1 = input("Which unit would you like to convert from: ")
unit2 = input("Which unit would you like to convert to: ")
num1 = input("Enter your value: " )
if unit1 == "cm" and unit2 == "m":
    ans = float(num1) / 100
    print(ans)
if unit1 == "m" and unit2 == "km":
    ans = float(num1) / 1000
    print(ans)
if unit1 == "m" and unit2 == "cm":
    ans = float(num1) * 1000
    print(ans)
if unit1 == "M" and unit2 == "Mm":
    ans = float(num1) * 1000
    print(ans)
if unit1 == "Hour" and unit2 == "second":
    ans = float(num1) * 3600
    print(ans)