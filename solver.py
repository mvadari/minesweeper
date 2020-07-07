from minesweeper import gen_minesweeper

DEBUG = False

def debug(*args):
    if DEBUG:
        if args[0]=="view":
            m.view()
        else:
            print(*args)

def solve(w, h, num_mines, get_first = False):
    '''
    Solve a Minesweeper puzzle dimensions wxh, 
    with num_mines mines
    get_first: whether to get the first square uncovered
    '''
    m = gen_minesweeper(w, h, num_mines)
    r,c = m.get_first()
    m.uncover(r,c)
    if get_first:
        return m,(r,c)
    else:
        return m

def solve_cheat(w, h, mines, first):
    '''
    Solve a Minesweeper puzzle knowing where the mines are and choosing where to start
    '''
    m = Minesweeper(w, h, mines)
    m.uncover(first[0], first[1])
    return m


def exhaustive_check(m):
    '''
    The main function used to solve a board
    Iterates through all the squares on the board
    TODO finish this docstring
    '''
    changed = True
    while changed and m.state=="ongoing":
        changed = False
        # iterate through all squares on the board
        for r in range(m.w):
            for c in range(m.h):
                value = m.get(r,c)
                if isinstance(value, int) and value!=0: # uncovered, not flagged -> has a number value
                    debug("ex check ({},{}), value {}".format(r,c,value))
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
                                debug("ex check 2 ({},{}), ({},{}), value {}".format(r1,c1,r2,c2,value))
                                if get_pair_info(m, (r1,c1), (r2,c2)):
                                    changed = True
                                    break
        debug("END OF LOOP", changed)
        debug("view")


def recursive_check(m, row, col):
    '''

    '''
    check_set = {(row,col)}
    loop_count = 0
    while len(check_set)>0:
        if m.state == "victory": # nothing more to check
            break
        new_check_set = set()
        loop_count += 1
        for r,c in check_set:
            debug("rec checking ({},{}), value {}".format(r,c, m.get(r,c)))

            for fr,fc in check_same_value_around(m,r,c):
                new_check_set.update(m.get_neighbors(fr,fc))

            new_check_set.update(check_flag_count_around(m,r,c))
            check_set = new_check_set

    return loop_count > 1

def check_same_value_around(m, r, c):
    '''
    '''
    ret = set()
    value = m.get(r, c)
    if isinstance(value, int) and value!=0:
        if neighbor_covered(m, r, c) and count_uncovered_around(m, r, c)==value:
            for nr,nc in m.get_neighbors(r, c):
                if m.get(nr,nc) == "*":
                    debug("flagged ({},{})".format(nr,nc))
                    m.flag(nr, nc)
                    ret.add((nr,nc))
    return ret

def check_flag_count_around(m, r, c):
    '''
    '''
    ret = set()
    value = m.get(r, c)
    if isinstance(value, int) and value!=0:
        if neighbor_covered(m, r, c) and count_flags_around(m, r, c)==value:
            for nr,nc in m.get_neighbors(r, c):
                if m.get(nr,nc) == "*":
                    debug("uncovered ({},{})".format(nr,nc))
                    m.uncover(nr, nc)
    return ret

def get_pair_info(m, p1, p2):
    '''
    
    '''
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

    debug(neighbors1, neighbors2, combined_neighbors)
    debug(p1, p2, value1, value2)

    if value1-value2 == 0:
        debug("same")
        if len(neighbors1) == 0 and len(neighbors2) == 0:
            debug("invalid0")
            return False
        elif len(neighbors1) == 0:
            debug("valid01")
            for nr,nc in neighbors2:
                m.uncover(nr,nc)
            return True
        elif len(neighbors2) == 0:
            debug("valid02")
            for nr,nc in neighbors1:
                m.uncover(nr,nc)
            return True
    elif len(neighbors1) == value1-value2:
        debug("valid1")
        for nr,nc in neighbors1:
            m.flag(nr,nc)
        return True
    elif len(neighbors2) == value2-value1:
        debug("valid2")
        for nr,nc in neighbors2:
            m.flag(nr,nc)
        return True

    return False


def get_effective_value(m, r, c):
    '''
    How many mine neighbors does (r, c) have for which we don't know the location?
    '''
    try:
        return m.get(r, c) - count_flags_around(m, r, c)
    except TypeError: # if (r, c) has already been flagged or isn't uncovered
        return 0

def count_uncovered_around(m, r, c):
    '''
    How many uncovered squares does (r, c) have around it?
    '''
    return len([(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if m.get(nr,nc)=="*" or m.get(nr,nc)=="f"])

def get_covered_neighbors(m, r, c):
    '''
    What not-revealed neighbors does (r, c) have?
    '''
    return {(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if m.get(nr,nc)=="*" and not (nr==r and nc==c)}

def get_uncovered_neighbors(m, r, c):
    '''
    What revealed neighbors does (r, c) have?
    '''
    return {(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if isinstance(m.get(nr,nc), int) and not (nr==r and nc==c)}

def neighbor_covered(m, r, c):
    '''
    Does (r, c) have any covered neighbors?
    '''
    return len(get_covered_neighbors(m, r, c)) > 0

def count_flags_around(m, r, c):
    '''
    Count the flags around (r, c)
    '''
    return len([(nr,nc) for (nr,nc) in m.get_neighbors(r,c) if m.get(nr,nc)=="f"])