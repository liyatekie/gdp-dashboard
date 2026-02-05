import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# ---------------- Page setup ----------------
st.set_page_config(page_title="4D Hypercube Explorer", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title(" Interactive 4D Hypercube")
st.markdown("""
This visualization shows a **4-dimensional hypercube (tesseract)** projected into **3D space**.
Rotate with your mouse and explore how higher dimensions behave.
""")

# ---------------- Controls ----------------
dimension = st.selectbox(
    "Select which dimension to explore",
    ["w", "x", "y", "z"]
)

animate = st.checkbox("Animate through 4D")

slider = st.slider(
    "Dimension value",
    -2.0,
    2.0,
    1.2,
    0.01
)

if animate:
    slider = np.sin(time.time()) * 1.5

# ---------------- Build 4D hypercube ----------------
vertices = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for w in [-1, 1]:
                vertices.append({"x": x, "y": y, "z": z, "w": w})

# Generate edges (differ in exactly one dimension)
edges = []
keys = ["x", "y", "z", "w"]
for i in range(len(vertices)):
    for j in range(i + 1, len(vertices)):
        diff = sum(vertices[i][k] != vertices[j][k] for k in keys)
        if diff == 1:
            edges.append((vertices[i], vertices[j]))

# ---------------- Projection function ----------------
def project(v, dim, offset):
    d = offset - v[dim]
    if abs(d) < 0.1:
        d = 0.1  # prevent explosion
    scale = 1 / d
    return (
        v["x"] * scale,
        v["y"] * scale,
        v["z"] * scale,
        v[dim]
    )

# ---------------- Project points ----------------
xs, ys, zs, colors = [], [], [], []
for v in vertices:
    x, y, z, c = project(v, dimension, slider)
    xs.append(x)
    ys.append(y)
    zs.append(z)
    colors.append(c)

# ---------------- Plot ----------------
fig = go.Figure()

# Edges
for v1, v2 in edges:
    p1 = project(v1, dimension, slider)
    p2 = project(v2, dimension, slider)

    fig.add_trace(
        go.Scatter3d(
            x=[p1[0], p2[0]],
            y=[p1[1], p2[1]],
            z=[p1[2], p2[2]],
            mode="lines",
            line=dict(color="white", width=2),
            showlegend=False
        )
    )

# Vertices
fig.add_trace(
    go.Scatter3d(
        x=xs,
        y=ys,
        z=zs,
        mode="markers",
        marker=dict(
            size=7,
            color=colors,
            colorscale="Turbo",
            opacity=0.95
        ),
        showlegend=False
    )
)

fig.update_layout(
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
        bgcolor="#0e1117"
    ),
    paper_bgcolor="#0e1117",
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Explanation ----------------
st.markdown("""
### How to use
- **Rotate** with your mouse  
- **Zoom** with scroll  
- Select a dimension (X, Y, Z, or W)  
- Slide to move through **4D space**  
- Turn on animation to see the hypercube pulse  

""")
