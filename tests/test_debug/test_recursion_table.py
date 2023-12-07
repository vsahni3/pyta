"""
Test suite for the RecursionTable class on different
types of recursive functions.
"""
from python_ta.debug import RecursionTable
from python_ta.util.tree import Tree


def test_base_case_call() -> None:
    with RecursionTable("fact") as table:

        def fact(n):
            if n == 0:
                return 1
            else:
                return n * fact(n - 1)

        fact(0)

    recursive_dict = table.get_recursive_dict()
    assert len(list(recursive_dict.keys())) == 3
    assert recursive_dict["n"] == [0]
    assert recursive_dict["called by"] == ["N/A"]
    assert recursive_dict["return value"] == [1]


def test_one_parameter_one_call() -> None:
    with RecursionTable("fact") as table:

        def fact(n):
            if n == 0:
                return 1
            else:
                return n * fact(n - 1)

        fact(3)

    recursive_dict = table.get_recursive_dict()
    assert len(list(recursive_dict.keys())) == 3
    assert recursive_dict["n"] == [3, 2, 1, 0]
    assert recursive_dict["called by"] == ["N/A", "fact(3)", "fact(2)", "fact(1)"]
    assert recursive_dict["return value"] == [6, 2, 1, 1]


def test_one_parameter_multiple_calls() -> None:
    with RecursionTable("fib") as table:

        def fib(n):
            if n in [0, 1]:
                return 1
            else:
                return fib(n - 2) + fib(n - 1)

        fib(3)

    recursive_dict = table.get_recursive_dict()
    assert len(list(recursive_dict.keys())) == 3
    assert recursive_dict["n"] == [3, 1, 2, 0, 1]
    assert recursive_dict["called by"] == ["N/A", "fib(3)", "fib(3)", "fib(2)", "fib(2)"]
    assert recursive_dict["return value"] == [3, 1, 2, 1, 1]


def test_multiple_parameters_one_call() -> None:
    with RecursionTable("fact_with_state") as table:

        def fact_with_state(n, prod):
            if n == 1:
                return prod
            else:
                return fact_with_state(n - 1, prod * n)

        fact_with_state(3, 1)

    recursive_dict = table.get_recursive_dict()
    assert len(list(recursive_dict.keys())) == 4
    assert recursive_dict["n"] == [3, 2, 1]
    assert recursive_dict["prod"] == [1, 3, 6]
    assert recursive_dict["called by"] == ["N/A", "fact_with_state(3, 1)", "fact_with_state(2, 3)"]
    assert recursive_dict["return value"] == [6, 6, 6]


def test_multiple_parameters_multiple_calls() -> None:
    with RecursionTable("sum_prod_lists") as table:

        def sum_prod_lists(lst, multiplier):
            if len(lst) == 1:
                return lst[0] * multiplier
            else:
                mid = len(lst) // 2
                return sum_prod_lists(lst[:mid], multiplier + 1) + sum_prod_lists(
                    lst[mid:], multiplier + 1
                )

        sum_prod_lists([1, 2, 3, 4], 1)

    recursive_dict = table.get_recursive_dict()
    assert len(list(recursive_dict.keys())) == 4
    assert recursive_dict["lst"] == [[1, 2, 3, 4], [1, 2], [1], [2], [3, 4], [3], [4]]
    assert recursive_dict["multiplier"] == [1, 2, 3, 3, 2, 3, 3]
    assert recursive_dict["called by"] == [
        "N/A",
        "sum_prod_lists([1, 2, 3, 4], 1)",
        "sum_prod_lists([1, 2], 2)",
        "sum_prod_lists([1, 2], 2)",
        "sum_prod_lists([1, 2, 3, 4], 1)",
        "sum_prod_lists([3, 4], 2)",
        "sum_prod_lists([3, 4], 2)",
    ]
    assert recursive_dict["return value"] == [30, 9, 3, 6, 21, 9, 12]


def test_with_static_method():
    class Testing:
        @staticmethod
        def fact(n):
            if n == 0:
                return 1
            return n * Testing.fact(n - 1)

    with RecursionTable("fact") as table:
        Testing.fact(3)

    recursive_dict = table.get_recursive_dict()
    assert len(list(recursive_dict.keys())) == 3
    assert recursive_dict["n"] == [3, 2, 1, 0]
    assert recursive_dict["called by"] == ["N/A", "fact(3)", "fact(2)", "fact(1)"]
    assert recursive_dict["return value"] == [6, 2, 1, 1]


def test_invalid_function_name() -> None:
    with RecursionTable("invalid") as table:

        def fact(n):
            if n == 0:
                return 1
            else:
                return n * fact(n - 1)

        fact(3)
    recursive_dict = table.get_recursive_dict()
    assert recursive_dict == {}


def test_different_initial_function_call() -> None:
    with RecursionTable("fact") as table:

        def wrapper_func():
            def fact(n):
                if n == 0:
                    return 1
                else:
                    return n * fact(n - 1)

            fact(3)

        wrapper_func()

    recursive_dict = table.get_recursive_dict()
    assert len(list(recursive_dict.keys())) == 3
    assert recursive_dict["n"] == [3, 2, 1, 0]
    assert recursive_dict["called by"] == ["N/A", "fact(3)", "fact(2)", "fact(1)"]
    assert recursive_dict["return value"] == [6, 2, 1, 1]


def test_one_parameter_one_call_tree() -> None:
    with RecursionTable("fact") as table:

        def fact(n):
            if n == 0:
                return 1
            else:
                return n * fact(n - 1)

        fact(3)

    actual_tree = table._get_root()
    expected_tree = Tree(["fact(3)", 6])

    node1 = Tree(["fact(2)", 2])
    node2 = Tree(["fact(1)", 1])
    node3 = Tree(["fact(0)", 1])

    expected_tree.add_child(node1)
    node1.add_child(node2)
    node2.add_child(node3)
    assert actual_tree == expected_tree


def test_one_parameter_multiple_calls_tree() -> None:
    with RecursionTable("fib") as table:

        def fib(n):
            if n in [0, 1]:
                return 1
            else:
                return fib(n - 2) + fib(n - 1)

        fib(3)

    actual_tree = table._get_root()
    expected_tree = Tree(["fib(3)", 3])

    node1 = Tree(["fib(1)", 1])
    node2 = Tree(["fib(2)", 2])
    node3 = Tree(["fib(0)", 1])
    node4 = Tree(["fib(1)", 1])

    expected_tree.add_child(node1)
    expected_tree.add_child(node2)
    node2.add_child(node3)
    node2.add_child(node4)

    assert actual_tree == expected_tree


def test_multiple_parameters_one_call_tree() -> None:
    with RecursionTable("fact_with_state") as table:

        def fact_with_state(n, prod):
            if n == 1:
                return prod
            else:
                return fact_with_state(n - 1, prod * n)

        fact_with_state(3, 1)

    actual_tree = table._get_root()
    expected_tree = Tree(["fact_with_state(3, 1)", 6])

    node1 = Tree(["fact_with_state(2, 3)", 6])
    node2 = Tree(["fact_with_state(1, 6)", 6])

    expected_tree.add_child(node1)
    node1.add_child(node2)

    assert actual_tree == expected_tree


def test_multiple_parameters_multiple_calls_tree() -> None:
    with RecursionTable("sum_prod_lists") as table:

        def sum_prod_lists(lst, multiplier):
            if len(lst) == 1:
                return lst[0] * multiplier
            else:
                mid = len(lst) // 2
                return sum_prod_lists(lst[:mid], multiplier + 1) + sum_prod_lists(
                    lst[mid:], multiplier + 1
                )

        sum_prod_lists([1, 2, 3, 4], 1)

    actual_tree = table._get_root()
    expected_tree = Tree(["sum_prod_lists([1, 2, 3, 4], 1)", 30])

    node1 = Tree(["sum_prod_lists([1, 2], 2)", 9])
    node2 = Tree(["sum_prod_lists([1], 3)", 3])
    node3 = Tree(["sum_prod_lists([2], 3)", 6])
    node4 = Tree(["sum_prod_lists([3, 4], 2)", 21])
    node5 = Tree(["sum_prod_lists([3], 3)", 9])
    node6 = Tree(["sum_prod_lists([4], 3)", 12])

    expected_tree.add_child(node1)
    expected_tree.add_child(node4)
    node1.add_child(node2)
    node1.add_child(node3)
    node4.add_child(node5)
    node4.add_child(node6)

    assert actual_tree == expected_tree
