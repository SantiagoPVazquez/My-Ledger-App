# Ledger CLI
# Santiago Pereyra Vázquez - Dec 2022

import argparse

# Availabe commands 
COMMANDS = {
    "register": "",
    "balance": "",
    "print": ""
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Welcome to your accounting tool")
    parser.add_argument(
        "command",
        type = str,
        choices = COMMANDS.keys(),
        help = "Which report you want to see"
    )
    parser.add_argument(
        "--sort", "-S",
        choices = ["date", "amount"],
        help = "Sort report by date or amount"
    )
    parser.add_argument(
        "--price-db", "-pdb",
        nargs = 1,
        help = "Price history"

    )
    parser.add_argument(
        "--file", "-f",
        nargs = 1,
        help = "File name"
    )
    parsed_args = parser.parse_args()
    print(parsed_args)