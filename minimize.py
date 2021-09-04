
ite = "ite({}, {}, {})"


def without(bdd, tbl, f, g):
    if f == bdd.false: return bdd.false
    if g == bdd.true: return bdd.false
    if g == bdd.false: return f
    if f == bdd.true: return bdd.true

    x, f1, f2 = f.var, f.high, f.low
    y, g1, g2 = g.var, g.high, g.low

    r = tbl.get(("without", str(f), str(g)), None)
    if r is not None:
        return r

    if bdd.var_levels[x] < bdd.var_levels[y]:
        u = without(bdd, tbl, f1, g)
        v = without(bdd, tbl, f2, g)

        r_expr = ite.format(x, u, v)
        r = bdd.add_expr(r_expr)

        tbl[("without", str(f), str(g))] = r
        return r

    elif bdd.var_levels[x] > bdd.var_levels[y]:
        return without(bdd, tbl, f, g2)

    else:
        u = without(bdd, tbl, f1, g1)
        v = without(bdd, tbl, f2, g2)

        r_expr = ite.format(x, u, v)
        r = bdd.add_expr(r_expr)

        tbl[("without", str(f), str(g))] = r
        return r


def minimize(bdd, tbl, f, indent=0):
    if (f == bdd.true) or (f == bdd.false):
        return f
    print(("\t"*indent) + "Minimizing: {}".format(bdd.to_expr(f)))

    r = tbl.get(("min", str(f)), None)
    if r is not None:
        return r

    x, g, h = f.var, f.high, f.low

    k = minimize(bdd, tbl, g, indent+1)
    u = without(bdd, tbl, k, h)
    v = minimize(bdd, tbl, h, indent+1)

    r_expr = ite.format(x, u, v)
    r = bdd.add_expr(r_expr)

    tbl[("min", str(f))] = r

    print(("\t"*indent) + "r_expr: {}".format(r_expr))
    print(("\t"*indent) + "r after add_expr: {}".format(bdd.to_expr(r)))
    return r


def bdd_paths(bdd, u, cut, complements=0):
    if u == bdd.true and (complements%2==0):
        return [frozenset(cut)]
    elif u == bdd.true and (complements%2==1):
        return None
    elif u == bdd.false and (complements%2==0):
        print("even complemenets in false")
        return None
    elif u == bdd.false and (complements%2==1):
        return None

    n = int(u.low.negated)

    low = bdd_paths(bdd, u.low, cut, complements + n)
    cut.add(u.var)
    high = bdd_paths(bdd, u.high, cut, complements)
    cut.remove(u.var)

    results = low if low is not None else []
    results.extend(high if high is not None else [])

    return results


def bdd_prob(bdd, f, p, memo):
    if f == bdd.false: return 0
    if f == bdd.true: return 1

    if f.negated:
        print("{} negated".format(f.var))
    r = memo.get(("prob", str(f)), None)
    if r is not None:
        return 1-r if f.negated else r

    x, g, h = f.var, f.high, f.low
    r = ((p[f.var] * bdd_prob(bdd, g, p, memo)) + ((1-p[f.var]) * bdd_prob(bdd, h, p, memo)))
    memo[("prob", str(f))] = r

    return 1-r if f.negated else r