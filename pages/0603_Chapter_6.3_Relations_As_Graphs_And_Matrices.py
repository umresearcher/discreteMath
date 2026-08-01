import streamlit as st
import graphviz
from Chapter_6_utils import *

RECOMMENDED_SET_SIZE = 10
MAX_SET_SIZE = 20

# --------------------------------------------------
# Module 3: Binary Relations As Graphs and Matrices
# --------------------------------------------------

st.title("Module 3: Binary Relations As Graphs and Matrices")


st.markdown("""
In Module 1, we saw that a binary relation can be represented as
a collection of ordered pairs or as a 2-column table.

In this module, we focus on binary relations on a single set
(A = B) and introduce two additional representations:

* Directed Graphs
* Adjacency Matrices

All three representations describe the same relation:

* Ordered Pairs / Table
* Directed Graph
* Adjacency Matrix
""")

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
# Step 1: Define the Set
# --------------------------------------------------

st.subheader("Step 1: Define the Set")

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
# Step 2: Define the Relation
# --------------------------------------------------

if st.session_state.validated_AB is None:
    st.info(
        "Complete Step 1 by validating the set."
    )
else:
    st.subheader("Step 2: Define the Relation")
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
        chosen_relation = st.selectbox(
            "Select a Relation",
            list(PREDEFINED_RELATIONS.keys())
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

# --------------------------------------------------
# Step 3: Build the Relation
# --------------------------------------------------

if (
    st.session_state.validated_AB is not None
    and st.session_state.validated_relation_code is not None
):
    st.subheader("Step 3: Build the Relation")

    st.markdown("""
    The relation is obtained by evaluating `relationDef(a, b)`
    for every pair in **A × A**.
    """)

    if st.button("Build the Relation"):
        rel_func = st.session_state.relation_function
        relation = build_relation_instance(
            AB,
            AB,
            rel_func
        )
        st.session_state.relation_instance = relation

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Possible Pairs in A × A",
                len(AB) * len(AB)
            )

        with col2:
            st.metric(
                "Relation Size (|R|)",
                len(relation)
            )

if (st.session_state.validated_AB is not None
    and st.session_state.validated_relation_code is not None
    and st.session_state.relation_instance is not None):

    st.subheader(
        "Step 4: View the Relation in Different Representations"
    )
    relation_instance = st.session_state.relation_instance
    st.markdown("""
    The four views below all represent the same relation.

    For a pair `(a, b)`, the following statements are equivalent:

    - `(a, b)` appears in the ordered-pair representation.
    - `(a, b)` appears in the relation table.
    - There is an arrow from `a` to `b` in the directed graph.
    - The matrix entry `M[a,b]` is `1`.
    """)

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("### Relation as Ordered Pairs")
        if len(relation_instance) == 0:
            st.write("∅")
        else:
            pairs_text = "\n".join(
                f"({a}, {b})"
                for a, b in relation_instance
            )

            st.text_area(
                "",
                value=pairs_text,
                height=250,
                disabled=True
            )

    with row1_col2:
        st.markdown("### Relation as a Table")
        df = relation_dataframe(
            relation_instance
        )
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("### Relation as a Directed Graph")
        st.caption(
            "There is an arrow from a to b whenever "
            "(a, b) belongs to the relation."
        )
        try:
            g = graphviz.Digraph(format="png")
            g.attr(rankdir="LR")

            g.attr(nodesep="0.3")
            g.attr(ranksep="0.4")
            g.attr(
                "node",
                shape="circle",
                fontsize="12"
            )

            for n in AB:
                g.node(str(n))

            # Invisible edges to encourage a compact layout
            for i in range(len(AB)-1):
                g.edge(
                    str(AB[i]),
                    str(AB[i+1]),
                    style="invis"
                )

            for u, v in relation_instance:
                g.edge(str(u), str(v))
            st.graphviz_chart(
                g,
                use_container_width=True
            )
        except Exception:
            st.error("Unable to display graph.")

    with row2_col2:
        st.markdown("### Relation as an Adjacency Matrix")

        st.caption(
            "Rows correspond to a and columns correspond to b. "
            "M[a,b] = 1 iff (a,b) belongs to the relation."
        )

        matrix_df = adjacency_matrix_dataframe(
            AB,
            relation_instance
        )

        st.dataframe(
            matrix_df,
            use_container_width=True
        )
