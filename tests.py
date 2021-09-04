import dd.cudd as _bdd
import random

import pytest
from minimize import *

def test_cutsets_rauzy_simple_example():
    bdd = _bdd.BDD()
    bdd.declare("a", "b", "c")
    r_expr = "(a | c) & (b | c)"
    root = bdd.add_expr(r_expr)
    x = { "a": 0.5, "b": 0.5, "c": 0.5}

    print(bdd_prob(bdd, root, x, dict()))
    tbl = {}
    root = minimize(bdd, tbl, root)
    tbl.clear()

    cutsets = frozenset(bdd_paths(bdd, root, set()))

    assert cutsets == frozenset([frozenset(["c"]), frozenset(["a", "b"])])

    bdd.dump("abc-after-minimize.pdf", [root])
    print(bdd_prob(bdd, root, x, dict()))

def test_minimize_bdd():
    bdd = _bdd.BDD()
    bdd.configure(reordering=False)
    bdd.declare( "b", "c", "a")
    r = bdd.add_expr("(a | c) & (b | c)")

    r_expr = bdd.to_expr(r)
    r = minimize(bdd, dict(), r)


def test_funky():
    expr = "x1 | ((x2 | x3 | x4 | (x8 & x9)) & (x5 | x6 | x7))"
    bdd = _bdd.BDD()
    bdd.configure(reordering=False)
    bdd.declare("x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9")
    r = bdd.add_expr(expr)
    o_sol = bdd_sol(bdd, r)

    
    # o_order = dict.copy(bdd.var_levels)
    # rand_order = list(bdd.vars)
    # random.shuffle(rand_order)
    # rand_order = {u: idx for idx, u in enumerate(rand_order)}

    # assert rand_order != o_order
    #bdd.reorder(rand_order)

    bad_order = {
      "x5" : 0,
      "x8" : 1,
      "x2" : 2,
      "x6" : 3,
      "x9" : 4,
      "x7" : 5,
      "x4" : 6,
      "x3" : 7,
      "x1" : 8,
    }

    bdd.dump("good-order-pre-minimize.pdf", [r])

    bdd.reorder(bad_order)

    reordered_sol = bdd_sol(bdd, r)
    assert reordered_sol == o_sol

    bdd.dump("bad-order-pre-minimize.pdf", [r])

    tbl = {}
    r = minimize(bdd, tbl, r, 0)
    tbl.clear()

    bdd.dump("bad-order-post-minimize.pdf", [r])

    cutsets = frozenset(bdd_paths(bdd, r, set(), int(r.negated)))

    expected = frozenset([frozenset(["x1"]),
                          frozenset(["x2", "x5"]),
                          frozenset(["x3", "x5"]),
                          frozenset(["x4", "x5"]),
                          frozenset(["x8", "x9", "x5"]),
                          frozenset(["x2", "x6"]),
                          frozenset(["x3", "x6"]),
                          frozenset(["x4", "x6"]),
                          frozenset(["x8", "x9", "x6"]),
                          frozenset(["x2", "x7"]),
                          frozenset(["x3", "x7"]),
                          frozenset(["x4", "x7"]),
                          frozenset(["x8", "x9", "x7"])])
    print("MCS Accurate? {}".format(cutsets==expected))




def bdd_sol(bdd, r):
    sol = []
    for s in bdd.pick_iter(r):
        sol.append(frozenset(filter(lambda u: s[u], s)))

    return frozenset(sol)



def test_negated_edge():
  r_expr = "a & ~b"
  bdd = _bdd.BDD()
  bdd.declare('a', 'b')
  r = bdd.add_expr(r_expr)

  x = {"a" :0.5, "b": 0.25}
  bdd.dump("negated.pdf", [r])
  print(bdd_prob(bdd, r, x, dict()))


def test_negated_edge_2():

    r_expr = "a & ~(b | ~c)"
    bdd = _bdd.BDD()
    bdd.declare('a', 'b', 'c')
    r = bdd.add_expr(r_expr)

    bdd.dump("negated.pdf", [r])
    x = {"a": 0.5, "b": 0.25, "c" : 0.125}
    print (bdd_prob(bdd, r, x, dict()))

def test_negated_funky():
  r_expr = "a & (b | c & ~(d & (e | f))) | (d & (e | f))"

  bdd = _bdd.BDD()
  bdd.declare('a', 'b', 'c', 'd', 'e', 'f')

  r = bdd.add_expr(r_expr)
  bdd.dump("negated.pdf", [r])

if __name__ == "__main__":
  test_negated_edge_2()