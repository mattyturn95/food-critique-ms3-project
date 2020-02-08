# function for pagination
def paginate(data, count, page=None):
    next = True
    if page is None:
        page = 1
    try:
        page = int(page)
    except ValueError:
        page = 1
    if page < 1:
        page = 1
    start = int(count * (page - 1))
    stop = int(count * page)
    data = [x for x in data]
    if stop >= len(data):
        next = False
    return data[start:stop], page, next
