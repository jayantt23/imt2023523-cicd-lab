tasks = []

def main():
    while True:
        print("1. Add task  2. View tasks  3. Exit")
        choice = input("Choose: ")
        if choice == '1':
            tasks.append(input("Enter task: "))
        elif choice == '2':
            print(tasks)
        else:
            break

if __name__ == "__main__":
    main()
