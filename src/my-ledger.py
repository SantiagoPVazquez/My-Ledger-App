# Ledger CLI
# Santiago Pereyra Vázquez - Dec 2022

import argparse
import re, datetime

# Availabe commands 
COMMANDS = {
    "reg": "",
    "bal": "",
    "print": ""
}

# List to save every line from the text file
lines = []
# List to save every entry with the corresponding transactions
data = []


############### Defining the function to read the data ###############
def readData(filePath):
    entries = -1
    with open(filePath, "r") as journal:
        for line in journal:
            if line.lstrip().startswith(";"):
                continue
            elif line.startswith("\n"):
                continue
            elif ";" in line:
                lines.append(line.split(";")[0])
            else:
                lines.append(line)

    for line in lines:
        # If a line starts with another character that is not a space it is a new entry of the journal
        if line.startswith(" ") == False:
            entries += 1
            # Extracting the date from the string
            day = re.search("\d{4}/\d{2}/\d{2}", line)
            date = datetime.datetime.strptime(day.group(), "%Y/%m/%d").date()

            # Appending the date, entry text and opening transactions list
            data.append({
                "date": date,
                "entry": line,
                "transactions": []
            })

        # If a line starts with a space it is a transaction for last entry in the journal
        elif line.startswith(" ") == True:
            account = line.split()[0]
            if "$" in line:
                amount = line.split("$")[1]
            else:
                amount = 0

            # Appending the account name and amount to the last entry
            data[entries]["transactions"].append({
                "account": account,
                "amount": amount
            })
    ...

############### Defining the "balance" function ###############
def balanceReport(filePath = "test.txt", sorted = False, prices = None):
    ...

############### Defining the "register" function ###############
def registerReport(filePath = "test.txt", sorted = False, prices = None):
    ...

############### Defining the "print" function ###############
def printReport(filePath = "test.txt", sorted = False, prices = None):
    ...

############### Main ###############
if __name__ == "__main__":
    # Defining the recieved commands and options
    parser = argparse.ArgumentParser(description="Welcome to your accounting tool")
    parser.add_argument(
        "command",
        type = str,
        choices = COMMANDS.keys(),
        help = "Which report you want to see"
    )
    parser.add_argument(
        "--sort", "-S",
        type = str,
        choices = ["date", "amount"],
        help = "Sort report by date or amount"
    )
    parser.add_argument(
        "--price-db", "-pdb",
        type = str,
        nargs = 1,
        dest = "priceDatabase",
        help = "Price history"

    )
    parser.add_argument(
        "--file", "-f",
        type = str,
        nargs = 1,
        required = True,
        help = "File name"
    )

    # Saved arguments
    parsed_args = parser.parse_args()

    # Executing functions depending on the command
    # Calling the "balance" function
    if parsed_args.command == "bal":
        balanceReport(parsed_args.file, parsed_args.sort, parsed_args.priceDatabase);
        readData(parsed_args.file[0])
    # Calling the "register" function
    elif parsed_args.command == "reg":
        registerReport(parsed_args.file, parsed_args.sort, parsed_args.priceDatabase);
    # Calling the "print" function
    elif parsed_args.command == "print":
        printReport(parsed_args.file, parsed_args.sort, parsed_args.priceDatabase);
    