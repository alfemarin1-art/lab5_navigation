
print("Welcome to Human-Computer Interaction!")
print("Exploring Information Architecture with Python")

website_name = "HCI Demo Site"
author = "Allfe Marin"
print("Website:", website_name)
print("Author:", author)

sections = {
    "Home": "Welcome to the Homepage. This is where users first arrive.",
    "About": "About Page: Mission, Team, and Background Information.",
    "Services": "Services Page: See the list of services we provide.",
    "Contact": "Contact Page: Email and Phone Details",
}

services = ["Web Design", "App Development", "Data Analysis"]


def show_menu():
    print("\n=== Navigation Menu ===")
    for key in sections.keys():
        print("-", key)
    print("- Exit (type 'Exit' to quit)\n")


while True:
    show_menu()
    choice = input("Type page name or 'Exit': ").strip()

    if choice.lower() == "exit":
        print("\nThank you for exploring the system. Goodbye!")
        break

    matched = None
    for page in sections:
        if choice.lower() == page.lower():
            matched = page
            break

    if matched:
        print(f"\nYou are now on the {matched} page.")
        print("Content:", sections[matched])

        if matched == "Services":
            print("\nOur Services:")
            for s in services:
                print("-", s)

        go_back = input("\nDo you want to visit another page? (y/n): ").strip().lower()
        if go_back == "n":
            print("\nEnding Session. Thank You!")
            break
        else:
            print("")

    else:
        print("\nPage not found. Please choose a valid page from the menu.\n")