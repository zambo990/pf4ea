if __name__ == '__main__':
    cell = "(11, 13)"
    cell = cell.replace("(", "")
    cell = cell.replace(")", "")
    index = cell.find(",")
    int(cell[0:(index)])
    int(cell[(index + 1):len(cell)])