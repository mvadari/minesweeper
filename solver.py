from minesweeper import *

DEBUG = True

def solve(w, h, num_mines, get_first = False):
    m = gen_minesweeper(w, h, num_mines)
    r,c = m.get_first()
    m.uncover(r,c)
    if get_first:
        return m,(r,c)
    else:
        return m

def solve_cheat(w, h, mines, first):
    m = Minesweeper(w, h, mines)
    m.uncover(first[0], first[1])
    return m



def exhaustive_check(m):
    changed = True
    while changed and m.state=="ongoing":
        changed = False
        for r in range(m.w):
            for c in range(m.h):
                value = m.get(r,c)
                if isinstance(value, int) and value!=0:
                    if DEBUG:
                        print("ex check ({},{}), value {}".format(r,c,value))
                    if recursive_check(m,r,c):
                        changed = True
        if not changed:
            for r1 in range(m.w):
                for c1 in range(m.h):
                    value1 = get_effective_value(m, r1, c1)
                    if isinstance(value1, int) and value1!=0:
                        for r2,c2 in get_uncovered_neighbors(m, r1, c1):
                            value2 = get_effective_value(m, r2, c2)
                            if isinstance(value2, int) and value2!=0:
                                if DEBUG:
                                    print("ex check 2 ({},{}), ({},{}), value {}".format(r1,c1,r2,c2,value))
                                if get_pair_info(m, (r1,c1), (r2,c2)):
                                    changed = True
                                    break
        if DEBUG:
            print("END OF LOOP", changed)
            m.view()


def recursive_check(m, row, col):
    check_set = {(row,col)}
    loop_count = 0
    while len(check_set)>0:
        if m.state == "victory":
            break
        new_check_set = set()
        loop_count += 1
        for r,c in check_set:
            if DEBUG:
                print("Checking ({},{}), value {}".format(r,c, m.get(r,c)))

            for fr,fc in check_same_value_around(m,r,c):
                new_check_set.update(m.get_neighbors(fr,fc))
            new_check_set.update(check_flag_count_around(m,r,c))
            # if DEBUG:
            #     m.view()
            check_set = new_check_set

    return loop_count > 1

def check_same_value_around(m, r, c):
    ret = set()
    value = m.get(r, c)
    if isinstance(value, int) and value!=0:
        if neighbor_covered(m, r, c) and count_uncovered_around(m, r, c)==value:
            for nr,nc in m.get_neighbors(r, c):
                if m.get(nr,nc) == "*":
                    if DEBUG:
                        print("flagged ({},{})".format(nr,nc))
                    m.flag(nr, nc)
                    ret.add((nr,nc))
    return ret

def check_flag_count_around(m, r, c):
    ret = set()
    value = m.get(r, c)
    if isinstance(value, int) and value!=0:
        if neighbor_covered(m, r, c) and count_flags_around(m, r, c)==value:
            for nr,nc in m.get_neighbors(r, c):
                if m.get(nr,nc) == "*":
                    if DEBUG:
                        print("uncovered ({},{})".format(nr,nc))
                    m.uncover(nr, nc)
    return ret

def get_pair_info(m, p1, p2):
    r1,c1 = p1
    r2,c2 = p2
    neighbors1 = get_covered_neighbors(m, r1, c1)
    neighbors2 = get_covered_neighbors(m, r2, c2)
    combined_neighbors = neighbors1.intersection(neighbors2)
    neighbors1 = neighbors1 - combined_neighbors
    neighbors2 = neighbors2 - combined_neighbors

    value1 = get_effective_value(m, r1, c1)
    value2 = get_effective_value(m, r2, c2)

    if value1 == 0 or value2 == 0:
        return False

    if DEBUG:
        print(neighbors1, neighbors2, combined_neighbors)
        print(p1, p2, value1, value2)

    if value1-value2 == 0:
        if DEBUG:
            print("same")
        if len(neighbors1) == 0 and len(neighbors2) == 0:
            if DEBUG:
                print("invalid0")
            return False
        elif len(neighbors1) == 0:
            if DEBUG:
                print("valid01")
            for nr,nc in neighbors2:
                m.uncover(nr,nc)
            return True
        elif len(neighbors2) == 0:
            if DEBUG:
                print("valid02")
            for nr,nc in neighbors1:
                m.uncover(nr,nc)
            return True
    elif len(neighbors1) == value1-value2:
        if DEBUG:
            print("valid1")
        for nr,nc in neighbors1:
            m.flag(nr,nc)
        return True
    elif len(neighbors2) == value2-value1:
        if DEBUG:
            print("valid2")
        for nr,nc in neighbors2:
            m.flag(nr,nc)
        return True

    return False


def get_effective_value(m, r, c):
    try:
        return m.get(r, c) - count_flags_around(m, r, c)
    except TypeError:
        return 0

def count_uncovered_around(m, r, c):
    return len([(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if m.get(nr,nc)=="*" or m.get(nr,nc)=="f"])

def get_covered_neighbors(m, r, c):
    return {(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if m.get(nr,nc)=="*" and not (nr==r and nc==c)}

def get_uncovered_neighbors(m, r, c):
    return {(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if isinstance(m.get(nr,nc), int) and not (nr==r and nc==c)}

def neighbor_covered(m, r, c):
    return len(get_covered_neighbors(m, r, c)) > 0

def count_flags_around(m, r, c):
    return len([(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if m.get(nr,nc)=="f"])

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


print(get_easy_stats(1000))
# mines = {(6, 9), (4, 8), (6, 6), (0, 14), (13, 4), (12, 12), (3, 0), (12, 5), (10, 15), (4, 12), (15, 8), (3, 14), (6, 14), (10, 8), (12, 2), (8, 14), (0, 15), (12, 13), (15, 9), (15, 11), (9, 11), (11, 1), (12, 3), (6, 4), (10, 4), (6, 11), (4, 5), (8, 11), (9, 3), (4, 14), (14, 6), (10, 1), (6, 12), (0, 8), (3, 5), (5, 10), (14, 7), (2, 0), (10, 14), (1, 7)}
# first = (7, 1)
# m = solve_cheat(16, 16, mines, first)
# m = solve(7, 7, 7)
# # m.print()
# # m.view()
# exhaustive_check(m)
# m.print()
# m.view()
# print(m.mines)
# check_one_mine_two_options(m, 4, 0)

#other ideas
#figure out 50-50s
#to make this more efficient, can keep track of 