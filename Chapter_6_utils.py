import pandas as pd
import ast
import random

def parse_set(text):
    items = [
        x.strip()
        for x in text.split(",")
        if x.strip()
    ]
    if len(items) == 0:
        raise ValueError("Set cannot be empty.")
    if len(items) > 100:
        raise ValueError("Maximum size is 100 elements.")
    try:
        items = [int(x) for x in items]
    except ValueError:
        pass
    return sorted(list(set(items)))

ALLOWED_FUNCTIONS = {
    "abs": abs,
    "int": int,
    "float": float,
    "max": max,
    "min": min,
}

def build_relation_function(code_text):
    scope = {}
    exec(
        code_text,
        {"__builtins__": {}, **ALLOWED_FUNCTIONS},
        scope
    )
    return scope["relationDef"]

def validate_relation(code_text, A, B):

    try:
        tree = ast.parse(code_text)

        funcs = [
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
        ]

        if len(funcs) != 1:
            return False, "Provide exactly one function."

        func = funcs[0]

        if func.name != "relationDef":
            return (
                False,
                "Function must be named relationDef."
            )

        if len(func.args.args) != 2:
            return (
                False,
                "Function must have exactly two parameters."
            )

        forbidden = (
            ast.Import,
            ast.ImportFrom,
            ast.For,
            ast.While,
            ast.With,
            ast.Try,
            ast.ClassDef,
            ast.Lambda,
        )

        for node in ast.walk(tree):

            if isinstance(node, forbidden):
                return (
                    False,
                    f"{type(node).__name__} is not allowed."
                )

            if isinstance(node, ast.Call):

                if (
                    isinstance(node.func, ast.Name)
                    and node.func.id == "relationDef"
                ):
                    return (
                        False,
                        "Recursion is not allowed."
                    )

        if not any(
            isinstance(node, ast.Return)
            for node in ast.walk(func)
        ):
            return (
                False,
                "Function must contain a return statement."
            )

        rel_func = build_relation_function(
            code_text
        )

        # ----------------------------------
        # Validate on the actual domain
        # ----------------------------------

        for a in A:
            for b in B:

                try:
                    result = rel_func(a, b)

                except Exception as e:

                    return (
                        False,
                        f"Function failed for "
                        f"({a}, {b}): {e}"
                    )

                if not isinstance(result, bool):

                    return (
                        False,
                        f"relationDef({a}, {b}) "
                        f"returned "
                        f"{type(result).__name__}. "
                        "Every pair must return "
                        "True or False."
                    )

        return True, "Function is valid."

    except SyntaxError as e:

        return False, f"Syntax error: {e}"

def preview_relation(A, B, rel_func, sample_size=50):
    pairs = [
        (a, b)
        for a in A
        for b in B
    ]
    random.shuffle(pairs)
    rows = []
    for a, b in pairs[:sample_size]:
        try:
            result = rel_func(a, b)
            if result:
                result = "✅   Belongs"
            else:
                result = "❌   Does Not Belong"
        except Exception as e:
            result = f"ERROR: {e}"
        rows.append(
            {
                "a": str(a),
                "b": str(b),
                "Result": result
            }
        )
    return pd.DataFrame(rows)

def build_relation_instance(A, B, rel_func):
    tuples = []
    for a in A:
        for b in B:
            try:
                if rel_func(a, b):
                    tuples.append((a, b))
            except Exception:
                pass
    return tuples

def relation_dataframe(relation):
    df = pd.DataFrame(
        relation,
        columns=["A", "B"]
    )
    df["A"] = df["A"].astype(str)
    df["B"] = df["B"].astype(str)
    return df

def relation_properties(A, relation):
    R = set(relation)
    reflexive = all(
        (a, a) in R
        for a in A
    )
    anti_reflexive = all(
        (a, a) not in R
        for a in A
    )
    symmetric = all(
        (b, a) in R
        for (a, b) in R
    )
    antisymmetric = all(
        a == b or (b, a) not in R
        for (a, b) in R
    )
    transitive = True
    for (a, b) in R:
        for (c, d) in R:
            if b == c and (a, d) not in R:
                transitive = False
                break
        if not transitive:
            break
    return {
        "Reflexive": reflexive,
        "AntiReflexive": anti_reflexive,
        "Symmetric": symmetric,
        "Antisymmetric": antisymmetric,
        "Transitive": transitive,
    }

def reflexive_counterexample(A, relation):

    R = set(relation)

    for a in A:
        if (a, a) not in R:
            return a

    return None

def anti_reflexive_counterexample(A, relation):

    R = set(relation)

    for a in A:
        if (a, a) in R:
            return a

    return None

def symmetric_counterexample(relation):

    R = set(relation)

    for a, b in R:

        if (b, a) not in R:
            return (a, b)

    return None

def antisymmetric_counterexample(relation):

    R = set(relation)

    for a, b in R:

        if a != b and (b, a) in R:
            return (a, b)

    return None

def transitive_counterexample(relation):

    R = set(relation)

    for a, b in R:
        for c, d in R:

            if b == c and (a, d) not in R:

                return (
                    (a, b),
                    (c, d),
                    (a, d)
                )

    return None

def adjacency_matrix_dataframe(nodes, relation):

    R = set(relation)

    matrix = []

    for a in nodes:

        row = []

        for b in nodes:

            row.append(
                1 if (a, b) in R else 0
            )

        matrix.append(row)

    return pd.DataFrame(
        matrix,
        index=nodes,
        columns=nodes
    )