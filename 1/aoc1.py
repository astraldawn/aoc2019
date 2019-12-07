with open('aoc1', 'rb') as f:
    res = 0
    for line in f:
        f_req = int(line)
        while(f_req > 0):
            next_req = f_req // 3 - 2
            if next_req > 0:
                res += next_req
            f_req = next_req

    print(res)
