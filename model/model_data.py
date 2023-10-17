import itertools


def generate_model_data(city_list):
    depot = 'depot'
    node_list = city_list + [depot]
    city_index_dict = {city: idx for idx, city in enumerate(node_list)}
    depot_index = city_index_dict[depot]

    arc_list, in_nodes, out_nodes = _generate_graph(city_list, city_index_dict, depot_index)
    return arc_list, in_nodes, out_nodes, depot_index, city_index_dict


def transform_index_to_city_name(sols, city_list):
    city_name_sols = list()
    for sol in sols:
        city_name_sol = [city_list[idx] for (_, idx) in sol[:-1]]
        city_name_sols.append(city_name_sol)
    return city_name_sols


def get_character_arcs(arc_list, city_list, depot_index):
    character_arcs = dict()
    for arc in arc_list:
        if arc[0] == depot_index:
            character = city_list[arc[1]][0]
        else:
            character = city_list[arc[0]][-1]
        character_arcs.setdefault(character, list()).append(arc)
    return character_arcs


def _generate_graph(city_list, city_index_dict, depot_index):
    prefix_dict = dict()
    suffix_dict = dict()
    arc_list = list()

    for city in city_list:
        prefix = city[0]
        suffix = city[-1]
        prefix_dict.setdefault(prefix, list()).append(city)
        suffix_dict.setdefault(suffix, list()).append(city)

    intersect_characters = set(prefix_dict.keys()).intersection(list(suffix_dict.keys()))

    for character in intersect_characters:
        from_nodes = suffix_dict[character]
        to_nodes = prefix_dict[character]

        for (from_node, to_node) in itertools.product(from_nodes, to_nodes):
            if from_node == to_node:
                continue
            arc_list.append((city_index_dict[from_node], city_index_dict[to_node]))

    for city in city_list:
        city_index = city_index_dict[city]
        arc_list.append((depot_index, city_index))
        arc_list.append((city_index, depot_index))

    in_nodes = dict()
    out_nodes = dict()
    for (i, j) in arc_list:
        in_nodes.setdefault(j, list()).append(i)
        out_nodes.setdefault(i, list()).append(j)
    return arc_list, in_nodes, out_nodes
