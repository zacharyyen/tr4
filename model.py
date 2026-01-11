import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# page config
# ----------------------------
st.set_page_config(page_title="banana immunity timing", layout="wide")

st.title("immune timing determines banana resistance to tr4")
st.caption(
    "an interactive model showing how delayed negative feedback enables early immune activation"
)

# ----------------------------
# layout
# ----------------------------
col_controls, col_plot = st.columns([1, 2])

# ----------------------------
# controls
# ----------------------------
with col_controls:
    st.subheader("model controls")

    tau = st.slider(
        "feedback delay (τ)",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        help="how long immune brakes wait before turning on"
    )

    k = st.slider(
        "pathogen pressure (k)",
        min_value=0.3,
        max_value=2.0,
        value=1.0,
        help="how strongly tr4 drives immune signaling"
    )

    alpha = st.slider(
        "feedback strength (α)",
        min_value=0.05,
        max_value=0.3,
        value=0.15,
        help="how strongly feedback suppresses signaling once active"
    )

# ----------------------------
# model components (UNCHANGED logic)
# ----------------------------
t = np.linspace(0, 20, 400)
dt = t[1] - t[0]
threshold = 7

def feedback(t, tau, sharpness=4):
    return 1 / (1 + np.exp(-sharpness * (t - tau)))

def simulate(tau, k, alpha):
    S = np.zeros_like(t)

    for i in range(1, len(t)):
        F = feedback(t[i], tau)
        dS = k - alpha * F * S[i-1]
        S[i] = max(S[i-1] + dS * dt, 0)

    return S

# ----------------------------
# run model
# ----------------------------
S = simulate(tau, k, alpha)
commits = np.any(S > threshold)

# ----------------------------
# plot + interpretation
# ----------------------------
with col_plot:
    fig, ax = plt.subplots()
    ax.plot(t, S, label="immune signal S(t)")
    ax.axhline(threshold, linestyle="--", label="activation threshold")
    ax.set_xlabel("time")
    ax.set_ylabel("immune signal")
    ax.legend()

    st.pyplot(fig)

    if commits:
        st.success("immune activation precedes feedback → defense commits")
    else:
        st.warning("feedback suppresses signaling before activation → immune failure")

    st.markdown(
        "immune outcome depends on whether signaling crosses an activation threshold "
        "before inducible negative feedback suppresses it. delaying feedback shifts this "
        "balance without requiring stronger signaling."
    )

st.caption(
    "this model is conceptual and intended to explore timing effects in banana–tr4 interactions."
)
