site_structure = {
    "Home": ["Welcome", "Featured Products", "Best Sellers", "New Arrivals"],
    "Products": {
        "Electronics": ["Laptops", "Phones", "Tablets", "Accessories"],
        "Fashion": ["Men's Clothing", "Women's Clothing", "Shoes", "Bags"],
        "Home & Living": ["Furniture", "Kitchen", "Decor", "Appliances"],
        "Sports & Outdoors": ["Fitness", "Cycling", "Camping", "Running"],
        "Beauty & Health": ["Skincare", "Makeup", "Supplements", "Personal Care"]
    },
    "Cart": ["View Cart", "Checkout", "Payment Options"],
    "About": ["Company Info", "Team", "Careers", "Contact Us"],
    "Blog": ["Tech", "Lifestyle", "Tutorials", "Trends"]
}

account_email = None
account_password = None
account_username = None

def show_menu():
    print("\n=== Navigation Menu ===")
    for page in site_structure.keys():
        print("-", page)
    print("- Exit (type 'Exit' to quit)\n")

def navigate_site():
    while True:
        show_menu()
        choice = input("Type page name or 'Exit': ").strip()

        if choice.lower() == "exit":
            print("\nThank you for exploring the system. Goodbye!")
            break

        matched = None
        for page in site_structure:
            if choice.lower() == page.lower():
                matched = page
                break

        if matched:
            print(f"\n=== {matched} ===")
            categories = site_structure[matched]

            if isinstance(categories, dict):
                for subcat, items in categories.items():
                    print(f"{subcat}: {', '.join(items)}")
            else:
                print(", ".join(categories))
        else:
            print("\nPage not found. Please choose a valid page from the menu.\n")

user = input("Login or Sign up: ").lower()

if user == "sign up":
    account_username = input("Enter Username: ")
    account_email = input("Enter Email: ")

    while True:
        password = input("Enter your password: ")
        password2 = input("Enter your password again: ")

        if password != password2:
            print("Password doesn't match")
            continue
        else:
            account_password = password
            print("Account created successfully!")
            print("============================================")
            print("            Please Login ")
            print("============================================")

            while True:
                login_username = input("Enter Username: ")
                login_password = input("Enter Password: ")

                if login_username == account_username and login_password == account_password:
                    print("Login successful! Welcome back.")
                    navigate_site()
                    break
                else:
                    print("Invalid username or password. Try again.")
            break

elif user == "login":
    if account_email is None or account_password is None:
        print("No account found. Please sign up first.")
    else:
        while True:
            login_username = input("Enter Username: ")
            login_password = input("Enter Password: ")

            if login_username == account_username and login_password == account_password:
                print("Login successful! Welcome back.")
                navigate_site()
                break
            else:
                print("Invalid username or password.")
                continue
