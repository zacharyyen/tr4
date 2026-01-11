import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# page config
# ----------------------------
st.set_page_config(page_title="banana immunity timing", layout="wide")

st.title("Immune timing determines banana resistance to tr4")
st.caption(
    "An interactive model showing how delayed negative feedback enables early immune activation"
)

# ----------------------------
# layout
# ----------------------------
col_controls, col_plot = st.columns([1, 2])

# ----------------------------
# controls
# ----------------------------
with col_controls:
    st.subheader("Model controls")

    tau = st.slider(
        "Feedback delay (τ)",
        min_value=0.0,
        max_value=10.0,
        value=5.0,
        help="how long immune brakes wait before turning on"
    )

    k = st.slider(
        "Pathogen pressure (k)",
        min_value=0.3,
        max_value=2.0,
        value=1.0,
        help="how strongly tr4 drives immune signaling"
    )

    alpha = st.slider(
        "Feedback strength (α)",
        min_value=0.05,
        max_value=0.3,
        value=0.15,
        help="how strongly feedback suppresses signaling once active"
    )

# ----------------------------
# model setup
# ----------------------------
t = np.linspace(0, 20, 400)
dt = t[1] - t[0]
threshold = 7
tau_baseline = 2.0  # fast feedback baseline (wild-type proxy)

def feedback(t, tau, sharpness=4):
    return 1 / (1 + np.exp(-sharpness * (t - tau)))

def simulate(tau, k, alpha):
    S = np.zeros_like(t)

    for i in range(1, len(t)):
        F = feedback(t[i], tau)
        dS = k - alpha * F * S[i - 1]
        S[i] = max(S[i - 1] + dS * dt, 0)

    return S

# ----------------------------
# run simulations
# ----------------------------
S_baseline = simulate(tau_baseline, k, alpha)
S_current = simulate(tau, k, alpha)

commits = np.any(S_current > threshold)

# ----------------------------
# plot
# ----------------------------
with col_plot:
    fig, ax = plt.subplots()

    ax.plot(
        t,
        S_baseline,
        linestyle="--",
        color="gray",
        label="baseline (fast feedback)"
    )

    ax.plot(
        t,
        S_current,
        label="current setting"
    )

    ax.axhline(
        threshold,
        linestyle=":",
        color="black",
        label="activation threshold"
    )

    # stabilize y-axis
    y_max = max(S_baseline.max(), S_current.max())
    ax.set_ylim(0, y_max * 1.1)

    ax.set_xlabel("time")
    ax.set_ylabel("immune signal S(t)")
    ax.legend()

    st.pyplot(fig)
    plt.close(fig)

    # ----------------------------
    # interpretation
    # ----------------------------
    if commits:
        st.success("Immune activation precedes feedback → defense commits")
    else:
        st.warning("Feedback suppresses signaling before activation → immune failure")

    st.markdown(
        "Immune outcome depends on whether signaling crosses an activation threshold "
        "before inducible negative feedback suppresses it. the dashed curve shows a "
        "baseline fast-feedback response, while the solid curve shows the effect of "
        "altering feedback timing."
    )

st.caption(
    "This model is conceptual and intended to explore timing effects in banana–tr4 interactions."
)



