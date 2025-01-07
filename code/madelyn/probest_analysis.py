import numpy as np
import matplotlib.pyplot as plt


def create_plot(x, y, title, label):
    plt.title(title)
    plt.plot(x, y, label=label)
    plt.legend()
    plt.savefig(f"./previews/probest_times_{title}")
    plt.clf()

def growth_list(power_est, x_list, times_list):
    growth=[(times_list[i]/(x_list[i]**power_est)) for i in range(0, len(x_list))]
    return growth



p_tag = "high"
iter= "1000"
times = np.load(f"./cache/timing_probest/times_{p_tag}_{iter}.npz", allow_pickle=True)

plt.figure(figsize=(6, 3))

n_list = times['inline_n']
m_list = times['inline_m']
times_list = times['inline_times']
plt.ylabel("Runtime")

#nodes
plt.xlabel("Number of Nodes")
create_plot(n_list, times_list, "Nodes", "Runtime")
#nodes growth analysis
growth_1 = growth_list(1, n_list, times_list)
plt.plot(n_list, growth_1, label="Runtime/n")

growth_2 = growth_list(2, n_list, times_list)
plt.plot(n_list, growth_2, label="Runtime/n^2")

growth_3 = growth_list(3, n_list, times_list)
create_plot(n_list, growth_3, "Nodes_Growth", "Runtime/n^3")



#edges
plt.xlabel("Number of Edges")
create_plot(m_list, times_list, "Edges", "Runtime")
#edges growth analysis
growth_1 = growth_list(1, m_list, times_list)
plt.plot(m_list, growth_1, label="Runtime/n")

growth_2 = growth_list(2, m_list, times_list)
plt.plot(m_list, growth_2, label="Runtime/n^2")

growth_3 = growth_list(3, m_list, times_list)
create_plot(m_list, growth_3, "Edges_Growth", "Runtime/n^3")
