from solver import *

def get_easy_stats(it):
    return get_stats(it, 8, 8, 10)

def get_medium_stats(it):
    return get_stats(it, 16, 16, 40)

def get_hard_stats(it):
    return get_stats(it, 24, 24, 99)

def get_stats(it, w, h, mines):
    global DEBUG
    DEBUG = False
    count = 0
    for _ in range(it):
        m,first = solve(w, h, mines, get_first=True)
        # print(m.mines, first)
        exhaustive_check(m)
        if (m.state == "victory"):
            count+=1
        elif m.state == "defeat":
            m.view()
            print(m.mines)
            DEBUG = True
            return
        else:
            m.view()
            print(m.mines, first)
            DEBUG = True
            return
    DEBUG = True
    return count/it

def test():
    print(get_easy_stats(1000))
    print(get_medium_stats(1000))
    print(get_hard_stats(1000))

def to_failure(w, h, num_mines):
    '''
    Keep running simulations of wxh board with num_mines mines until it fails
    '''
    while True:
        m = solve(w, h, num_mines)
        exhaustive_check(m)
        if m.state != "victory":
            return m


if __name__ == '__main__':
    result = to_failure(16, 16, 40)
    result.view()
    result.print()