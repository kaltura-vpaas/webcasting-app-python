from prettytable import PrettyTable


def printTable(stats, name):
    print(name)
    table = PrettyTable(stats['header'].split(","))
    if stats['data'] == '':
        print("no data. try adjusting the time frame.")

    else:
        data = stats['data'].rstrip(';').split(";")
        for x in data:
            table.add_row(x.split(','))

        print(table)
        if ('totalCount' in stats): print(stats['totalCount'])