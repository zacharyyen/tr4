import numpy as np
import matplotlib.pyplot as plt

# time
t = np.linspace(0, 20, 400)

# parameters
k = 1.0              # signal input rate
alpha = 0.15         # feedback strength
threshold = 7

tau_fast = 2
tau_mid = 5
tau_slow = 8

# delayed feedback function (smooth)
def feedback(t, tau, sharpness=4):
    return 1 / (1 + np.exp(-sharpness * (t - tau)))

# simulate S(t)
def simulate(tau):
    S = np.zeros_like(t)
    dt = t[1] - t[0]

    for i in range(1, len(t)):
        F = feedback(t[i], tau)
        dS = k - alpha * F * S[i-1]
        S[i] = max(S[i-1] + dS * dt, 0)

    return S

# run simulations
S_fast = simulate(tau_fast)
S_mid = simulate(tau_mid)
S_slow = simulate(tau_slow)

# plot
plt.figure()
plt.plot(t, S_fast, label="fast feedback (low τ)")
plt.plot(t, S_mid, label="moderate feedback (mid τ)")
plt.plot(t, S_slow, label="delayed feedback (high τ)")
plt.axhline(threshold, linestyle="--", label="activation threshold")
plt.xlabel("time")
plt.ylabel("immune signal S(t)")
plt.legend()
plt.show()
