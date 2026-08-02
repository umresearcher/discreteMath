import streamlit as st
import graphviz
import pandas as pd
from Chapter_6_utils import *

RECOMMENDED_SET_SIZE = 10
MAX_SET_SIZE = 20

st.title(
    "Module 4: Paths, Reachability, and Transitive Closure"
)

st.markdown("""
A relation describes direct connections between elements.

In this module, we study paths, reachability,
graph powers, and transitive closure, which
capture indirect connections.
""")

st.header(
    "Reachability in Directed Graphs"
)

#Initialize to None (if not already defined)
if "validated_AB" not in st.session_state:
    st.session_state.validated_AB = None

if "last_relation_mode" not in st.session_state:
    st.session_state.last_relation_mode = None

if "last_predefined_relation" not in st.session_state:
    st.session_state.last_predefined_relation = None

if "validated_relation_code" not in st.session_state:
    st.session_state.validated_relation_code = None

if "relation_function" not in st.session_state:
    st.session_state.relation_function = None

if "relation_instance" not in st.session_state:
    st.session_state.relation_instance = None

# --------------------------------------------------
# Step 1: Define a Relation on A
# --------------------------------------------------

st.subheader(
    "Step 1: Define a Set and Relation"
)

st.markdown("""
Define a finite set **A** and a binary relation **R**
on **A**.

The relation consists of all pairs (a,b) in A × A
for which relationDef(a,b) returns True.
""")

if "set_ab" not in st.session_state:
    st.session_state.set_ab = "1,2,3,4"

set_ab_text = st.text_input(
    "Enter elements separated by commas",
    key="set_ab"
)

st.caption(
    f"Recommended: {RECOMMENDED_SET_SIZE} or fewer elements. "
    f"Maximum allowed: {MAX_SET_SIZE} elements."
)

def clear_set():
    st.session_state.set_ab = ""
    st.session_state.validated_AB = None
    st.session_state.last_relation_mode = None
    st.session_state.last_predefined_relation = None
    st.session_state.validated_relation_code = None
    st.session_state.relation_function = None
    st.session_state.relation_instance = None

col1, col2 = st.columns(2)

with col1:
    validate_ab = st.button("Validate Set")

with col2:
    st.button(
        "Clear Set",
        on_click=clear_set
    )

if validate_ab:
    try:
        AB = parse_set(set_ab_text)

        if len(AB) > MAX_SET_SIZE:
            st.session_state.validated_AB = None
            raise ValueError(
                f"Maximum allowed set size is {MAX_SET_SIZE} elements."
            )

        st.session_state.validated_AB = AB

        if len(AB) > RECOMMENDED_SET_SIZE:
            st.warning(
                f"Sets larger than {RECOMMENDED_SET_SIZE} elements may "
                "produce graphs and matrices that are difficult to read."
            )

        # Clear everything downstream
        st.session_state.validated_relation_code = None
        st.session_state.relation_function = None
        st.session_state.relation_instance = None       
        st.success(
            f"Set is valid ({len(AB)} elements)"
        )
    except Exception as e:
        st.error(str(e))

if st.session_state.validated_AB is not None:
    AB = st.session_state.validated_AB
    st.markdown(
        f"**A =** "
        f"{{{', '.join(map(str, AB))}}}"
    )

    st.markdown(
        f"**|A| = {len(AB)}**"
    )

# --------------------------------------------------
# Relation Definition
# --------------------------------------------------

if st.session_state.validated_AB is not None:
    st.markdown(
        "#### Define the Relation"
    )
    st.markdown("""
    We now define a binary relation on set A.

    A binary relation is a subset of:

    **A × A**

    Choose a predefined relation or define your own relation
    using the function:

    ```python
    relationDef(a, b)
    ```

    For each pair (a, b) in A × A, the function is evaluated.

    The function should return:

    - `True` if `(a, b)` belongs to the relation.
    - `False` if `(a, b)` does not belong to the relation.""")

    with st.expander("Allowed Python features"): 
        st.markdown(""" You may use: 

        - Variables
        - Arithmetic operations (`+`, `-`, `*`, `/`, `%`)
        - Comparisons (`<`, `<=`, `>`, `>=`, `==`, `!=`)
        - Boolean operators (`and`, `or`, `not`)
        - `if` / `else` statements
        - The functions `abs()`, `min()`, `max()`, `int()`, and `float()`

        The following constructs are not allowed:

        - `import`
        - `for` loops
        - `while` loops
        - File operations
        - Network operations
        - Recursion
        """)

    relation_mode = st.radio(
        "Choose Relation Definition",
        [
            "Predefined Relation",
            "Custom Relation"
        ]
    )

    if relation_mode != st.session_state.last_relation_mode:
        st.session_state.validated_relation_code = None
        st.session_state.relation_instance = None
        st.session_state.last_relation_mode = relation_mode

    PREDEFINED_RELATIONS = {
        "Equality":
    """def relationDef(a, b):
        return a == b
    """,

        "Different":
    """def relationDef(a, b):
        return a != b
    """,

        "Less Than":
    """def relationDef(a, b):
        return a < b
    """,

        "Less Than or Equal":
    """def relationDef(a, b):
        return a <= b
    """,

        "Same Parity":
    """def relationDef(a, b):
        return (a % 2) == (b % 2)
    """,

        "Divides":
    """def relationDef(a, b):
        if a == 0:
            return False
        return b % a == 0
    """,

        "Immediate Successor":
    """def relationDef(a, b):
        return b == a + 1
    """,

        "Empty Relation":
    """def relationDef(a, b):
        return False
    """
    }

    if relation_mode == "Predefined Relation":

        relation_names = list(PREDEFINED_RELATIONS.keys())

        chosen_relation = st.selectbox(
            "Select a Relation",
            relation_names,
            index=relation_names.index("Immediate Successor")
        )

        if (
            chosen_relation
            != st.session_state.last_predefined_relation
        ):
            st.session_state.relation_instance = None
            st.session_state.last_predefined_relation = (
                chosen_relation
            )

        relation_code = PREDEFINED_RELATIONS[
            chosen_relation
        ]
        st.code(
            relation_code,
            language="python"
        )
        st.session_state.validated_relation_code = relation_code
        st.session_state.relation_function = (
            build_relation_function(relation_code)
        )
    else:
        relation_code = st.text_area(
            "Enter relationDef(a, b)",
            value="""def relationDef(a, b):
        return a == b
    """,
            height=200
        )
        if st.button(
            "Validate Relation Definition"
        ):
            is_valid, message = validate_relation(
                relation_code,
                AB,
                AB
            )
            if is_valid:
                st.session_state.validated_relation_code = relation_code

                st.session_state.relation_function = (
                    build_relation_function(relation_code)
                )
                st.session_state.relation_instance = None
                st.success(message)
            else:
                st.error(message)

if (
    st.session_state.validated_AB is not None
    and
    st.session_state.validated_relation_code is not None
):

    if st.button(
        "Build Relation"
    ):

        rel_func = (
            st.session_state.relation_function
        )

        relation = build_relation_instance(
            AB,
            AB,
            rel_func
        )

        st.session_state.relation_instance = (
            relation
        )

if st.session_state.relation_instance is not None:
    relation = st.session_state.relation_instance
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Possible Pairs",
            len(AB) * len(AB)
        )
    with col2:
        st.metric(
            "|R|",
            len(relation)
        )

if (st.session_state.validated_AB is not None
    and st.session_state.validated_relation_code is not None
    and st.session_state.relation_instance is not None):

    st.info("""
    Next, we will use the graph and matrix
    representations to study reachability.
    """)

    st.subheader(
        "Step 2: Explore the Relation"
    )
    st.markdown("""
    The relation can be viewed in several equivalent
    representations.

    For a pair `(a,b)`:

    - `(a,b)` is an ordered pair in the relation.
    - There is an arrow from `a` to `b` in the graph.
    - The matrix entry `M[a,b]` is `1`.
    """)

    relation_instance = (
        st.session_state.relation_instance
    )

    st.markdown("### Ordered Pairs")
    ordered_pairs_text = (
        "{" +
        ", ".join(
            f"({a},{b})"
            for a, b in relation_instance
        ) +
        "}"
    )

    st.code(ordered_pairs_text)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "### Directed Graph"
        )

        st.caption(
            "There is an arrow from a to b whenever "
            "(a,b) belongs to the relation."
        )

        try:

            g = graphviz.Digraph(
                format="png"
            )

            g.attr(rankdir="LR")

            g.attr(
                nodesep="0.3"
            )

            g.attr(
                ranksep="0.4"
            )

            g.attr(
                "node",
                shape="circle",
                fontsize="12"
            )

            for n in AB:

                g.node(str(n))

            # Encourage a compact layout
            for i in range(
                len(AB) - 1
            ):
                g.edge(
                    str(AB[i]),
                    str(AB[i + 1]),
                    style="invis"
                )

            for u, v in relation_instance:

                g.edge(
                    str(u),
                    str(v)
                )

            st.graphviz_chart(
                g,
                use_container_width=True
            )

        except Exception:

            st.error(
                "Unable to display graph."
            )

    with col2:

        st.markdown(
            "### Adjacency Matrix"
        )

        st.caption(
            "M[a,b] = 1 iff "
            "(a,b) belongs to the relation."
        )

        matrix_df = (
            adjacency_matrix_dataframe(
                AB,
                relation_instance
            )
        )

        st.dataframe(
            matrix_df,
            use_container_width=True
        )

    st.info("""
A path from a to b corresponds to a sequence of edges in the directed graph.

In the next step, we will determine which pairs of 
elements are reachable by paths of a given length.
""")    

if (st.session_state.validated_AB is not None
    and st.session_state.validated_relation_code is not None
    and st.session_state.relation_instance is not None):
    st.subheader(
        "Step 3: Explore Reachability"
    )

    st.markdown("""
    A pair `(a,b)` in the relation represents a
    direct connection from `a` to `b`.

    Sometimes an element can reach another element indirectly
    by following a sequence of edges in the directed graph.

    Such a sequence of edges is called a path.
    """)

    if len(AB) > 5:
        st.info(
            """
            To keep the examples manageable,
            reachability is currently displayed
            for paths up to 5 hops.

            Longer paths can be explored later
            through graph powers and transitive
            closure.
            """
        )

    k = st.slider(
        "Path Length (Number of Edges)",
        min_value=1,
        max_value=min(len(AB), 5),
        value=2
    )

    st.markdown(
        f"### Reachable by a Path of Length {k}"
    )

    relation_instance = (
        st.session_state.relation_instance
    )

    reachability_relation, witness_paths = (
        relation_power_with_paths(
            AB,
            relation_instance,
            k
        )
    )

    if len(reachability_relation) == 0:

        st.info(
            f"No pairs are reachable by a path of length {k}."
        )

    else:

        best_pair = max(
            witness_paths,
            key=lambda pair: (
                len(set(witness_paths[pair])),
                -sum(
                    1
                    for i in range(
                        len(witness_paths[pair]) - 1
                    )
                    if witness_paths[pair][i]
                    == witness_paths[pair][i + 1]
                )
            )
        )

        best_path = witness_paths[best_pair]

        st.markdown(
            f"**Pairs reachable by a path of length {k}:**"
        )

        pairs_text = (
            "{"
            + ", ".join(
                f"({a},{b})"
                for a, b in sorted(
                    reachability_relation
                )
            )
            + "}"
        )

        st.code(pairs_text)

        st.markdown(
            "### Illustrative Example"
        )

        st.markdown(
            f"""
The pair **{best_pair}** is reachable by a path of length **{k}**.
"""
        )

        path_text = " → ".join(
            str(v)
            for v in best_path
        )

        st.markdown(
            f"""
One path is:

**{path_text}**
"""
        )

        path_pairs = [
            (
                best_path[i],
                best_path[i + 1]
            )
            for i in range(
                len(best_path) - 1
            )
        ]

        relation_pairs_text = ", ".join(
            f"({u},{v})"
            for u, v in path_pairs
        )

        st.markdown(
            f"""
**Corresponding relation pairs:**

{relation_pairs_text}
"""
        )

        st.caption(
            "Each edge in the path corresponds to a pair in the relation."
        )

        st.caption(
            f"This is one illustrative example chosen "
            f"from the {len(reachability_relation)} "
            f"pairs reachable by a path of length {k}."
        )

        st.markdown(
            "### Illustrative Example in the Directed Graph"
        )

        st.caption(
            "The green edges show the path used in the example."
        )

        path_edges = set(
            (best_path[i], best_path[i + 1])
            for i in range(len(best_path) - 1)
        )

        g = graphviz.Digraph(format="png")

        g.attr(rankdir="LR")

        g.attr(
            "node",
            shape="circle",
            fontsize="12"
        )

        for n in AB:
            g.node(str(n))

        # Encourage a compact layout
        for i in range(
            len(AB) - 1
        ):
            g.edge(
                str(AB[i]),
                str(AB[i + 1]),
                style="invis"
            )

        for u, v in relation_instance:

            if (u, v) in path_edges:

                g.edge(
                    str(u),
                    str(v),
                    color="green",
                    penwidth="3"
                )

            else:

                g.edge(
                    str(u),
                    str(v),
                    color="gray"
                )

        st.graphviz_chart(
            g,
            use_container_width=True
        )

def superscript(n):
    mapping = {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹"
    }

    return "".join(
        mapping[d]
        for d in str(n)
    )

if (st.session_state.validated_AB is not None
    and st.session_state.validated_relation_code is not None
    and st.session_state.relation_instance is not None):

    st.subheader(
        "Step 4: Relation Powers"
    )

    st.markdown("""
    In Step 3, we explored pairs that are reachable
    by paths of a given length.

    The relation consisting of all pairs reachable by a path of length k is denoted by Rᵏ.
    """)    

    st.markdown("""
    - **R¹** consists of all pairs in the original relation R.
    - **R²** consists of all pairs connected by a path of length 2.
    - **R³** consists of all pairs connected by a path of length 3.
    - More generally, **Rᵏ** consists of all pairs connected by a path of length k.
    """)

    power_k = st.slider(
        "Select k for Rᵏ",
        min_value=1,
        max_value=min(len(AB), 5),
        value=2,
        key="relation_power_slider"
    )

    power_relation, witness_paths = (
        relation_power_with_paths(
            AB,
            relation_instance,
            power_k
        )
    )

    st.markdown(
        f"### Relation R{superscript(power_k)}"
    )

    pairs_text = (
        "{"
        + ", ".join(
            f"({a},{b})"
            for a, b in sorted(power_relation)
        )
        + "}"
    )

    st.code(pairs_text)

    if len(power_relation) > 0:
        st.info(
            f"R{superscript(power_k)} is itself a relation on A.\n\n"
            f"Each pair in R{superscript(power_k)} represents two vertices "
            f"that are reachable by a path of length {power_k} in the original graph."
        )
    else:
        st.info(
            f"R{superscript(power_k)} is itself a relation on A.\n\n"
            f"In this case, R{superscript(power_k)} is the empty relation."
        )

    st.markdown(
        f"### Directed Graph of R{superscript(power_k)}"
    )

    st.caption(
        f"There is an edge from a to b whenever "
        f"(a,b) belongs to R{superscript(power_k)}."
    )

    g = graphviz.Digraph(format="png")
    g.attr(rankdir="LR")

    g.attr(
        "node",
        shape="circle",
        fontsize="12"
    )

    for n in AB:
        g.node(str(n))

    # Encourage a compact layout
    for i in range(
        len(AB) - 1
    ):
        g.edge(
            str(AB[i]),
            str(AB[i + 1]),
            style="invis"
        )

    for u, v in power_relation:
        g.edge(
            str(u),
            str(v)
        )

    st.graphviz_chart(
        g,
        use_container_width=True
    )

    st.markdown(
        f"### Adjacency Matrix of R{superscript(power_k)}"
    )

    st.caption(
        f"""
    Rows correspond to a and columns correspond to b.

    M[a,b] = 1 iff (a,b) belongs to R{superscript(power_k)}.
    """
    )

    matrix_df = (
        adjacency_matrix_dataframe(
            AB,
            power_relation
        )
    )

    st.dataframe(
        matrix_df,
        use_container_width=True
    )


