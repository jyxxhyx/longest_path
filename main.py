import datetime

from output_handler.drawer import draw_map
from util.util import add_output_cwd, add_input_cwd
from input_handler import reader
from model.longest_path_model import LongestPathModel
from model.model_data import generate_model_data, transform_index_to_city_name
from output_handler.wirter import write_result


def main():
    all_sols = list()
    must_select_cities = list()
    file_name = 'city_list.csv'
    max_iteration = 20

    city_list = reader.read(add_input_cwd(file_name))
    arc_list, in_nodes, out_nodes, depot_index, city_index_dict = generate_model_data(
        city_list)
    node_list = list(city_index_dict.values())
    must_select_city_indices = [
        city_index_dict[city] for city in must_select_cities
    ]

    for idx in range(max_iteration):
        model = LongestPathModel(node_list, arc_list, in_nodes, out_nodes,
                                 depot_index, all_sols,
                                 must_select_city_indices)
        result = model.solve()
        if len(all_sols) > 0 and len(result) < len(all_sols[0]):
            break
        all_sols.append(result)

    all_sols = transform_index_to_city_name(all_sols, city_list)

    file_name = f'result_{datetime.datetime.now()}.csv'
    write_result(all_sols, add_output_cwd(file_name))
    file_name = file_name.replace('.csv', '.html')
    draw_map(all_sols, add_output_cwd(file_name))
    return


if __name__ == '__main__':
    main()
