# My implementation of Ledger CLI
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
                amount = float(line.split("$")[1].strip().replace(",",""))
            else:
                amount = -float(amount)

            # Appending the account name and amount to the last entry
            data[entries]["transactions"].append({
                "account": account,
                "amount": amount
            })
    return data

############### Defining the "sort" function ###############
def sortData(data):
    ...

############### Defining the "prices-db" function ###############
def pricesDatabase(data):
    ...

############### Defining the "balance" function ###############
def balanceReport(data, sorted = False, prices = None):
    balanceBook = {}
    for i in range(len(data)):
        for j in range(len(data[i]["transactions"])):
            if data[i]["transactions"][j]["account"] in balanceBook:
                balanceBook[data[i]["transactions"][j]["account"]] += data[i]["transactions"][j]["amount"]
            else:
                balanceBook[data[i]["transactions"][j]["account"]] = data[i]["transactions"][j]["amount"]
    # Variable to store the total balance
    sum = 0
    # List to store the names of the main accounts
    listOfAccounts = []

    for entry in balanceBook:
        if entry.split(":")[0] in listOfAccounts:
            continue
        else:
            listOfAccounts.append(entry.split(":")[0])
    
    # Create a dictionary (res) to store all the subaccounts tied to a main account and print them with each amount
    for element in listOfAccounts:
        res = dict(filter(lambda item: element in item[0], balanceBook.items()))
        for acc in res:
            sum += res[acc]
            print("\t{:^10.2f}\t{}".format(res[acc],acc))
    # Final line to print the total balance
    print("------------------------\n","\t{:^10.2f}".format(sum))

############### Defining the "register" function ###############
def registerReport(data, sorted = False, prices = None):
    ...

############### Defining the "print" function ###############
def printReport(data, sorted = False, prices = None):
    # Main loop to print every main entry from the journal
    for i in range(len(data)):
        print(data[i]["entry"])
        # Secondary loop to print all the transactions for each entry
        for j in range(len(data[i]["transactions"])):
            print("\t{:<40}${:^10.2f}\n".format(data[i]["transactions"][j]["account"], data[i]["transactions"][j]["amount"]))

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
        readData(parsed_args.file[0])
        balanceReport(data, parsed_args.sort, parsed_args.priceDatabase)

    # Calling the "register" function
    elif parsed_args.command == "reg":
        readData(parsed_args.file[0])
        registerReport(data, parsed_args.sort, parsed_args.priceDatabase)

    # Calling the "print" function
    elif parsed_args.command == "print":
        readData(parsed_args.file[0])
        printReport(data, parsed_args.sort, parsed_args.priceDatabase)
    