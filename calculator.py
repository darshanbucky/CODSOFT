def calculator():
    print("Select an operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")

    choice = input("Enter the number for the operation you want to perform : ")

    if choice in ['1', '2', '3', '4']:
        n1 = float(input("Enter first number: "))
        n2 = float(input("Enter second number: "))

        if choice == '1':
            result = n1 + n2
        elif choice == '2':
            result = n1 - n2
        elif choice == '3':
            result = n1 * n2
        elif choice == '4':
            if n2 != 0:
                result = n1 / n2
            else:
                print("Error! Division by zero.")
                return
            
        print(f"Result: {int(result)}")
    else:
        print("Invalid choice! Please select a valid option.")
        
if __name__=="__main__":
    calculator()

