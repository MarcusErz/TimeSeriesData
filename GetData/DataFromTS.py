import math
import numpy as np
from sklearn.manifold import Isomap
from sklearn.preprocessing import StandardScaler


def data_from_ts(ts_values, window_size):
    len_ts = len(ts_values)
    len_networks = math.ceil(len_ts / window_size)
    networks = []
    print(len_networks)
    for i in range(0, len_ts, window_size):
        window = ts_values[i:i + window_size]
        new_network = compute_network(window)
        networks.append(new_network)
    return networks


def compute_network(window):
    len_window = len(window)
    network = np.zeros((len_window, len_window))
    for i in range(len_window):
        network[:, i] = np.sqrt(np.array(abs(window[i] - window) ** 2, dtype=np.float64))
    return network


def reduce_networks(networks):
    sparsifyed_networks = []
    for i in range(len(networks)):
        net = networks[i]
        iso_net = get_iso_net(net, 4, 2)
        reduced_net = compute_multi_net(iso_net)

        # normalize
        # TODO Die Elemente auf der Hauptdiagonalen sollten eigentlich gleich sein sind sie aber nicht
        scaler = StandardScaler()
        scaler.fit(net)
        a1 = scaler.transform(net)

        scaler2 = StandardScaler()
        scaler2.fit(reduced_net)
        a2 = scaler2.transform(reduced_net)

        difference = a1 - a2
        sparsify_net = spar_net(reduced_net, difference)
        # print('sparsify net: {}'.format(sparsify_net))
        sparsifyed_networks.append(sparsify_net)
    return sparsifyed_networks


def compute_multi_net(iso_net):
    len_ts = iso_net.shape[0]
    distance_matrix = np.zeros((len_ts, len_ts))
    dim_ts = iso_net.ndim

    for x in range(len_ts):
        distance = np.zeros(len_ts)
        for y in range(dim_ts):
            distance = np.power(abs(iso_net[x, y] - iso_net[:, y]), 2) + distance
        distance_matrix[x, :] = np.sqrt(distance)
    return distance_matrix


def get_iso_net(net, neighbours, comps):
    embedding = Isomap(n_neighbors=neighbours, n_components=comps)
    net_transformed = embedding.fit_transform(net)
    return net_transformed


def spar_net(reduced_net, difference):
    len_ts = reduced_net.shape[0]
    width_ts = reduced_net.shape[1]

    sparsified_net = reduced_net.copy()
    # TODO is std a good solution
    std_diff = np.std(difference)

    for i in range(len_ts):
        for z in range(width_ts):
            if -std_diff < difference[i, z] < std_diff:
                sparsified_net[i, z] = 0

    return sparsified_net
