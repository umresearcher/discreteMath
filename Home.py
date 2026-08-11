import streamlit as st

st.set_page_config(
    page_title="Discrete Math Bridge",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Discrete Math Learning System")
st.markdown("### Bridging Mathematics & Computer Science")

st.info("👈 Please select a Chapter from the sidebar to begin.")

st.markdown("""
### Course Roadmap

##### 🟢 **Chapter 6: Relations (Available Now)**

We have transformed textbook concepts into interactive modules:

1. **Binary Relations ↔ Tables**
   - Define sets and relations.
   - View relations as ordered pairs and tables.

2. **Binary Relations on the Same Set**
   - Explore reflexivity, symmetry,
     antisymmetry, and transitivity.

3. **Binary Relations ↔ Directed Graphs**
   - Visualize relations as digraphs.

4. **Binary Relations ↔ Matrices**
   - Represent relations using adjacency matrices.

5. **Reachability & Transitive Closure**
   - Paths, matrix powers, and closure.

6. **N-ary Relations ↔ Database Tables**
   - Connect mathematical relations to SQL tables.
   
#### 🚧 **Chapter 1: Logic (Coming Soon)**
* Logic Gates & Circuits.
* Truth Tables as Data Validation.
""")