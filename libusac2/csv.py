def parse_csv(f, headers, skip_lines=1):
    """
    Parse a CSV file into a dictionary with type conversions
    :param f: the path of the file to use
    :param headers: an ``OrderedDict`` mapping field names to conversions in the order they appear in the file
    :return: a list of dictionaries, each representing a row of data
    """
    output = []
    with open(f) as fl:
        data = fl.readlines()[skip_lines:]
        keys = headers.keys()
        for d in data:
            rider = {}
            d.replace(', TN', ' TN')
            d = d.split(',')
            for i in range(len(keys)):
                rider[keys[i]] = headers[keys[i]](d[i])
            output.append(rider)
    return output