import pulp

from model.abstract_model import AbstractModel


class LongestPathModel(AbstractModel):
    def __init__(self,
                 node_list,
                 arc_list,
                 in_nodes,
                 out_nodes,
                 depot,
                 previous_sols: list = None,
                 must_select_cities: list = None):
        self.m = pulp.LpProblem('Longest Path', pulp.LpMaximize)
        self.node_list = node_list
        self.arc_list = arc_list
        self.in_nodes = in_nodes
        self.out_nodes = out_nodes
        self.depot = depot
        self.previous_sols = previous_sols
        self.must_select_cities = must_select_cities
        self.big_m = len(node_list)
        return

    def _set_iterables(self):
        return

    def _set_variables(self):
        self.y = pulp.LpVariable.dicts('y', self.node_list, cat=pulp.LpBinary)
        self.x = pulp.LpVariable.dicts('x', self.arc_list, cat=pulp.LpBinary)
        self.n = pulp.LpVariable.dicts('n',
                                       self.node_list,
                                       cat=pulp.LpContinuous)
        return

    def _set_objective(self):
        self.m += pulp.lpSum(self.x[arc] for arc in self.arc_list)
        return

    def _set_constraints(self):
        self._set_flow_balance_constraints()
        self._set_mtz_constraints()
        self._set_selection_constraints()
        return

    def _post_process(self):
        result = list()
        current_node = self.depot
        flag = True
        while flag:
            for node in self.out_nodes[current_node]:
                if self.x[current_node, node].value() > 0.9:
                    result.append((current_node, node))
                    current_node = node
                    break
            if current_node == self.depot:
                flag = False
        return result

    def _process_infeasible_case(self):
        return list()

    def _optimize(self):
        self.m.solve()
        return

    def _is_feasible(self):
        return True

    def _set_flow_balance_constraints(self):
        self.m += (pulp.lpSum(self.x[self.depot, j]
                              for j in self.out_nodes[self.depot]) == 1,
                   'depot-out')
        self.m += (pulp.lpSum(self.x[i, self.depot]
                              for i in self.in_nodes[self.depot]) == 1,
                   'depot-in')
        for j in self.node_list:
            if j == self.depot:
                continue
            self.m += (pulp.lpSum(self.x[i, j]
                                  for i in self.in_nodes[j]) == pulp.lpSum(
                                      self.x[j, k] for k in self.out_nodes[j]),
                       f'flow-balance-{j}')
        return

    def _set_mtz_constraints(self):
        for (i, j) in self.arc_list:
            if j == self.depot:
                continue
            self.m += (self.n[j] - self.n[i] - 1 >= self.big_m *
                       (self.x[i, j] - 1), f'mtz-{i}-{j}')
        return

    def _set_selection_constraints(self):
        for i in self.node_list:
            if i == self.depot:
                continue
            self.m += (pulp.lpSum(self.x[i, j]
                                  for j in self.out_nodes[i]) == self.y[i],
                       f'x-y-1-{i}')
        for idx, sol in enumerate(self.previous_sols):
            temp_sol = sol[:-1]
            self.m += (pulp.lpSum(self.y[item[1]]
                                  for item in temp_sol) <= len(temp_sol) - 1,
                       f'cutoff-{idx}')
        for i in self.must_select_cities:
            self.m += (self.y[i] == 1, f'must-select-{i}')
        self.m += (self.y[self.depot] == 0, 'depot')
        return
