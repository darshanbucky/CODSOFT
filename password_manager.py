import random
import string

def generate_password(length, complexity):
    if complexity == "weak":
        characters = string.ascii_lowercase
    elif complexity == "medium":
        characters = string.ascii_letters + string.digits
    elif complexity == "strong":
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        print("Invalid complexity choice.")
        return None

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    try:
        length = int(input("Enter the length of the password: "))
        if length <= 0:
            print("Length should be greater than zero.")
            return
        
        print("\nSelect Password Complexity:")
        print("1. Only Alphabets ")
        print("2. Alphabets and Number")
        print("3. Alphabets and Number Special Character ")
        
        choice = input("Enter your choice : ")
        
        complexity_map = {"1": "weak", "2": "medium", "3": "strong"}
        complexity = complexity_map.get(choice)

        if not complexity:
            print("Invalid choice. Please select 1, 2, or 3.")
            return

        password = generate_password(length, complexity)
        if password:
            print(f"\nGenerated {complexity.capitalize()} Password: {password}")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
