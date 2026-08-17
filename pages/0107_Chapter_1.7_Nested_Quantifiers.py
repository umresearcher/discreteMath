import streamlit as st
import pandas as pd

st.title("Module 7: Nested Quantifiers")

st.markdown("""
In Module 6, we learned how to negate quantified statements.

In this module, we study nested quantifiers and see how the order of quantifiers affects meaning.
""")

st.subheader("Nested Quantifiers")

st.markdown("""
A nested quantifier occurs when a quantified statement contains more than one quantifier.
""")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
∀x ∃y P(x,y)
""")

with col2:
    st.markdown("""
∃y ∀x P(x,y)
""")

st.info(""" Changing the order of quantifiers may change the meaning of a statement. """)

st.info("""
Quantifiers of the same type can be reordered without changing meaning.

For example,

∀x ∀y P(x,y) ≡ ∀y ∀x P(x,y)

and

∃x ∃y P(x,y) ≡ ∃y ∃x P(x,y)
""")

st.subheader("Example")

col1, col2 = st.columns(2)

with col1:

    col3, col4 = st.columns([1,2])

    with col3:
        st.markdown("""""")

        st.markdown("""
        **Predicate**
        """)

    with col4:
        st.markdown("""
        ```text
        Enrolled(student, course)
        ```

        which is True when the student is enrolled in the course.""")

    col3, col4 = st.columns([1,2])

    with col3:
        st.markdown("""""")
        st.markdown("""**Domain of students**""")

    with col4:
        st.markdown("""
        ```text
        {Alice, Bob, Carol}
        ```
        """)


    col3, col4 = st.columns([1,2])

    with col3:
        st.markdown("""""")
        st.markdown("""**Domain of courses**""")

    with col4:
        st.markdown("""
        ```text
        {CSC375, CSC384}
        ```
        """)

with col2:
    st.markdown("""
    The table contains the combinations of values for which the predicate is True.
    """)

    enrolled_df = pd.DataFrame( { 
        "Student": [ "Alice", "Alice", "Bob", "Carol" ], 
        "Course": [ "CSC375", "CSC384", "CSC375", "CSC384" ] } )

    st.markdown("""**Enrolled**""")
    st.dataframe( enrolled_df, hide_index=True, width="content" )

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
```text
∀student ∃course
Enrolled(student, course)
```

means

```text
Every student is enrolled
in at least one course.
```
""")

with col2:
    st.markdown("""
    ```text
    ∃course ∀student
    Enrolled(student, course)
    ```
    means

    ```text
    There exists a course
    in which every student is enrolled.
    ```
    """)

st.markdown("""For the given table:""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ```text
    ∀student ∃course Enrolled(student, course)
    ```

    is **True** because every student appears in at least one row.
    """)

with col2:
    st.markdown("""
    ```text
    ∃course ∀student Enrolled(student, course)
    ```

    is **False** because no single course contains every student.
    """)

st.warning(""" These two statements are not equivalent. """)

st.subheader("Explore Nested Quantifiers")

st.markdown("""
Select the rows that belong to the relation

```text
Enrolled(student, course)
```
""")

col1, col2, col3 = st.columns(3) 

with col1: 
    alice_375 = st.checkbox( "Enrolled(Alice, CSC375)", value=True ) 
    alice_384 = st.checkbox( "Enrolled(Alice, CSC384)", value=True ) 

with col2:
    bob_375 = st.checkbox( "Enrolled(Bob, CSC375)", value=True ) 
    bob_384 = st.checkbox( "Enrolled(Bob, CSC384)", value=False ) 

with col3: 
    carol_375 = st.checkbox( "Enrolled(Carol, CSC375)", value=False ) 
    carol_384 = st.checkbox( "Enrolled(Carol, CSC384)", value=True )

enrolled = {
    ("Alice", "CSC375"): alice_375,
    ("Alice", "CSC384"): alice_384,
    ("Bob", "CSC375"): bob_375,
    ("Bob", "CSC384"): bob_384,
    ("Carol", "CSC375"): carol_375,
    ("Carol", "CSC384"): carol_384,
}

students = ["Alice", "Bob", "Carol"]
courses = ["CSC375", "CSC384"]

forall_exists = all(
    any(
        enrolled[(student, course)]
        for course in courses
    )
    for student in students
)

exists_forall = any(
    all(
        enrolled[(student, course)]
        for student in students
    )
    for course in courses
)

results_df = pd.DataFrame(
    {
        "Statement": [
            "∀student ∃course Enrolled(student, course)",
            "∃course ∀student Enrolled(student, course)",
        ],
        "Truth Value": [
            "T" if forall_exists else "F",
            "T" if exists_forall else "F",
        ],
    }
)

forall_exists2 = all(
    any(
        enrolled[(student, course)]
        for student in students
    )
    for course in courses
)

exists_forall2 = any(
    all(
        enrolled[(student, course)]
        for course in courses
    )
    for student in students
)

results_df2 = pd.DataFrame(
    {
        "Statement": [
            "∀course ∃student Enrolled(student, course)",
            "∃student ∀course Enrolled(student, course)",
        ],
        "Truth Value": [
            "T" if forall_exists2 else "F",
            "T" if exists_forall2 else "F",
        ],
    }
)

col1, col2 = st.columns(2)

with col1:
    st.dataframe(
        results_df,
        hide_index=True,
        width="stretch",
    )

with col2:
    st.dataframe(
        results_df2,
        hide_index=True,
        width="stretch",
    )


st.info("""
Experiment with the rows.

Notice that changing the order of the quantifiers can change the truth value of the statement.
""")

st.subheader("Summary")

summary_df = pd.DataFrame(
    {
        "Statement": [
            "∀x ∀y P(x,y)",
            "∃x ∃y P(x,y)",
            "∀x ∃y P(x,y)",
            "∃y ∀x P(x,y)",
        ],
        "Observation": [
            "Order may be swapped",
            "Order may be swapped",
            "Order may matter",
            "Order may matter",
        ],
    }
)

st.dataframe(
    summary_df,
    hide_index=True,
    width="content",
)

st.warning("""
Quantifiers of the same type can be reordered.

When different quantifiers are nested, the order of the quantifiers may change the meaning of the statement.
""")

with st.expander("Additional Observation"):

    st.markdown("""
Consider a binary relation

```text
R(x,y)
```

Then

```text
∃y ∀x R(x,y) implies ∀x ∃y R(x,y)
```

Why is this true?

If there exists a value of y for which R(x,y) is true for every x, 
then for every x there certainly exists a y (namely the same y) 
for which R(x,y) is true.

However, the converse is not always true. In other words,

```text
∀x ∃y R(x,y) does not imply ∃y ∀x R(x,y) 
```

In our example,

```text
∃course ∀student Enrolled(student, course) implies ∀student ∃course Enrolled(student, course)
∀student ∃course Enrolled(student, course) does not imply ∃course ∀student Enrolled(student, course)
```

By the same reasoning,

```text
∃student ∀course Enrolled(student, course) implies ∀course ∃student Enrolled(student, course)
∀course ∃student Enrolled(student, course) does not imply ∃student ∀course Enrolled(student, course)
```
""")

