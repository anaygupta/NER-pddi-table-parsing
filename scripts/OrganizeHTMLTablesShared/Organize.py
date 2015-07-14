# Goals for this .py file
#   1. List number of rows and columns for each table
#   2. Append all headings of each table into a list without duplication
#   3. Find the total number of tables [DONE]
#   4. Find the distribution of rows and columns between tables
#   5. Find how many times each heading is stated in HTML document
#   6. Find how many headers each group contains

import re
from bs4 import BeautifulSoup

def generate():
    # [WORKING] Section fixes broken HTML before processing
    fileName = "/Users/Josh/Documents/NER-pddi-table-parsing/scripts/OrganizeHTMLTablesShared/tables.html"
    file = open(fileName, "rb")
    html = file.read()

    ## TODO: fix the script that pulls tables from Linked SPLs so that
    ## encoding and "prettify" are done at the time of extraction.
    soupTemp = BeautifulSoup(html)

    output = open("/Users/Josh/Documents/NER-pddi-table-parsing/scripts/OrganizeHTMLTablesShared/output.html", "w")
    output.write(soupTemp.prettify().encode("utf-8"))
    output.close()

def organize():
    categories = {"SetID": [],
                  "Interacting Substance": (),
                  "Interacting Substance Properties": (),
                  "Interaction Properties": (),
                  "Drug Name or Drug Class": (),
                  "Drug Effect": (),
                  "Drug Dose Recommendation": (),
                  "Effect on Drug": (),
                  "Clinical Comment": (),
                  "Sample Size": (),
                  "Misc.": ()}
    tableInfo = {"Name": [("Table ID", "Row", "Col")]}
    headers = []
    tableStatsCols = []
    tableStatsRows = []
    colsTot = 0
    colsTotTemp = 0
    rowsTot = 0

    input = open("output.txt", "r") 
    htmlParse = input.read().decode("utf-8")

    # Section prepares each part for addition to tableInfo dictionary
    soup = BeautifulSoup(htmlParse)
    tables = soup.findChildren("table") # (ResultSet)

    tableIDs = [(n["value"]) for n in soup.findChildren("input")] # Creates a list of table names (List)

    for c in range(0, len(tableIDs)): # Goes through all tables
        tableNo = tables[c].findChildren(["tr"]) # Finds all rows in a table (ResultSet)

        for line in tableNo:
            dataCellsCols = len(line.findChildren(["td", "th"])) # The amount of cells per row (columns)
            colsTotTemp += dataCellsCols

            if tableNo.index(line) == 0 and line.findChildren(["th"]):
                headers.append(line.findChildren(["th"]))

            elif tableNo.index(line) == 0 and line.findChildren(["td"]):
                headers.append(line.findChildren(["td"]))

        colsTot += colsTotTemp/len(tableNo)
        colsTotTemp = 0

        dataCellsRows = len(tableNo)
        rowsTot += dataCellsRows

        tableStatsCols.append(dataCellsCols)
        tableStatsRows.append(len(tableNo))

    for n in range (0, len(headers)):
        print headers[n]

    print len(headers)

    print "Total Columns: " + str(colsTot)
    print "Minimum Columns: " + str(min(tableStatsCols))
    print "Maximum Columns: " + str(max(tableStatsCols))
    print "Average Columns: " + str(sum(tableStatsCols)/len(tableStatsCols)) + "\n\n"

    print "Total Rows: " + str(rowsTot)
    print "Minimum Rows: " + str(min(tableStatsRows))
    print "Maximum Rows: " + str(max(tableStatsRows))
    print "Average Rows: " + str(sum(tableStatsRows)/len(tableStatsRows)) + "\n\n"

    """
        for i in range(0, len(trList)): # Goes through each table for row, col, and data information
            tdList.append(trList[i][0].findChildren(["td", "th"]))
    """

    # print trList

        # print("Table ID: "+ tableIDs[c] + "\t\tNumber: " + str(c + 1))

def dbToDict():
    connect = {}

    # [WORKING] Section takes txt database and categorizes everything into a dictionary
    db = "/Users/Josh/Documents/Python Projects/ParseTableInfo/Categories.txt" ## get the Categories.txt into the code repository and adjust like above to not care about local configuration (relative path)
    data = open(db, "rb")

    with data as txtData:
        for line in txtData:
            line = re.split(r"\t+", line.strip("\n"))

            if line[1] in connect:
                if line[0] not in connect.values():
                    connect[line[1]].append(line[0])

                else:
                    break

            else:
                connect.update({line[1]: [line[0]]})

    print connect