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
                unit = "$"
            elif any(char.isdigit() for char in line):#len(line.split()) > 1:
                for i in range(len(line.split())):
                    if line.split()[i].isnumeric():
                        amount = float(line.split()[i])
                        unit = line.split()[i+1]
            else:
                amount = -float(amount)

            # Appending the account name and amount to the last entry
            data[entries]["transactions"].append({
                "account": account,
                "amount": amount,
                "unit": unit
            })
    return data

############### Defining the "sort" function ###############
def sortData(data, sorted):
    # New list to save the data
    sortedData = [None]*len(data)

    if sorted == "date":
        
        dateList = []
        for i in range(len(data)):
            dateList.append(data[i]["date"])

        for i in range(len(data)):
            maxDateind = dateList.index(max(dateList))
            dateList.pop(maxDateind)
            sortedData[i] = data.pop(maxDateind)
        
        return sortedData

    elif sorted == "amount":

        amountList = {}
        amounts = []
        for i in range(len(data)):
            for j in range(len(data[i]["transactions"])):
                amounts.append(data[i]["transactions"][j]["amount"])
                amountList[i] = amounts
            amounts = []

        for i in range(len(data)):
            maxAmountind = list(filter(lambda x: amountList[x] == max(amountList.values()), amountList))[0]
            amountList.pop(maxAmountind)
            sortedData[i] = data[maxAmountind]

        return sortedData

    else: 
        return data

############### Defining the "prices-db" function ###############
def pricesDatabase(data, pricesFile):
    priceList = {}
    with open(pricesFile, "r") as prices:
        for line in prices:
            if len(line.split()) > 2:
                priceList[line.split()[-2]] = float(line.split()[-1].replace("$","").replace(",",""))
    
    for i in range(len(data)):
        for j in range(len(data[i]["transactions"])):
            if data[i]["transactions"][j]["unit"] in priceList:
                data[i]["transactions"][j]["amount"] = data[i]["transactions"][j]["amount"] * priceList[data[i]["transactions"][j]["unit"]]
                data[i]["transactions"][j]["unit"] = "$"
    
    return data
                    


############### Defining the "balance" function ###############
def balanceReport(data):
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
def registerReport(data):

    sum = 0
    for i in range(len(data)):
        temp = data[i]["entry"].strip()
        for j in range(len(data[i]["transactions"])):
            sum += data[i]["transactions"][j]["amount"]
            if data[i]["transactions"][j]["unit"] == "$":
                print("{:<40}\t{:<25}\t${:^20.2f}\t{:^20.2f}".format(temp,data[i]["transactions"][j]["account"],data[i]["transactions"][j]["amount"],sum))
            else:
                print("{:<40}\t{:<25}\t{:^20.2f}{:<}\t{:^20.2f}".format(temp,data[i]["transactions"][j]["account"],data[i]["transactions"][j]["amount"],data[i]["transactions"][j]["unit"],sum))

            temp = ""

############### Defining the "print" function ###############
def printReport(data):
    # Main loop to print every main entry from the journal
    for i in range(len(data)):
        print(data[i]["entry"])
        # Secondary loop to print all the transactions for each entry
        for j in range(len(data[i]["transactions"])):
            if data[i]["transactions"][j]["unit"] == "$":
                print("\t{:<40}{}{:^10.2f}\n".format(data[i]["transactions"][j]["account"],data[i]["transactions"][j]["unit"], data[i]["transactions"][j]["amount"]))
            elif data[i]["transactions"][j]["unit"] != "$":
                print("\t{:<40}{:^10.2f}{}\n".format(data[i]["transactions"][j]["account"],data[i]["transactions"][j]["amount"], data[i]["transactions"][j]["unit"]))
    

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
        dest = "sort",
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

    # Reading data
    data = readData(parsed_args.file[0])

    # Modifying data if sort and price-db flag is used 
    if parsed_args.sort != None and parsed_args.priceDatabase != None:
        data = pricesDatabase(data, parsed_args.priceDatabase[0])
        data = sortData(data, parsed_args.sort)
    # Modifying data if only sort flag is used
    elif parsed_args.sort != None and parsed_args.priceDatabase == None:
        data = sortData(data, parsed_args.sort)
    # Modifying data if only price-db flag is used
    elif parsed_args.priceDatabase != None and parsed_args.sort == None:
        data = pricesDatabase(data, parsed_args.priceDatabase[0])

    # Executing functions depending on the command
    # Calling the "balance" function
    if parsed_args.command == "bal":
        balanceReport(data)

    # Calling the "register" function
    elif parsed_args.command == "reg":
        registerReport(data)

    # Calling the "print" function
    elif parsed_args.command == "print":
        printReport(data)