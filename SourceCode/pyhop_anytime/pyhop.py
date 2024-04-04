"""
This is a derived work of the Pyhop planner written by Dana Nau.


This software is adapted from:

Pyhop, version 1.2.2 -- a simple SHOP-like planner written in Python.
Author: Dana S. Nau, 2013.05.31

Copyright 2013 Dana S. Nau - http://www.cs.umd.edu/~nau

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import copy
import time
from ResearchProject_V1.Problem_file import *
#from ResearchProject_V1.Problem_file_GenericMap import *

c_neighbor = [source]
c_nbor = [source]


class State:
    def __init__(self, name):
        self.__name__ = name

    def __repr__(self):
        return '\n'.join(
            [f"{self.__name__}.{name} = {val}" for (name, val) in vars(self).items() if name != "__name__"])


class TaskList:
    def __init__(self, options=None, completed=False):
        self.completed = completed
        if options and len(options) > 0:
            self.options = options if type(options[0]) == list else [options]
        else:
            self.options = [[]] if completed else []

    def __repr__(self):
        return f"TaskList(options={self.options},completed={self.completed})"

    def complete(self):
        return self.completed

    def failed(self):
        return len(self.options) == 0 and not self.completed

    def in_progress(self):
        return not self.complete() and not self.failed()


class Planner:
    def __init__(self, verbose=0):
        self.operators = {}
        self.methods = {}
        self.verbose = verbose

    def declare_operators(self, *op_list):
        self.operators.update({op.__name__: op for op in op_list})

    def declare_methods(self, task_name, *method_list):
        self.methods.update({task_name: list(method_list)})
        print(self.methods)

    def print_operators(self):
        print(f'OPERATORS: {", ".join(self.operators)}')

    def print_methods(self):
        print(f'METHODS: {", ".join(self.methods)}')

    def log(self, min_verbose, msg):
        if self.verbose >= min_verbose:
            print(msg)

    def log_state(self, min_verbose, msg, state):
        if self.verbose >= min_verbose:
            print(msg)
            print(state)

    def pyhop(self, state, tasks, verbose=0):
        for plan in self.pyhop_generator(state, tasks, verbose):
            if plan:
                return plan

    def anyhop(self, state, tasks, max_seconds=1000, verbose=0, disable_branch_bound=False):
        start_time = time.time()
        plan_times = []
        for plan in self.pyhop_generator(state, tasks, verbose, disable_branch_bound):
            elapsed_time = time.time() - start_time
            if max_seconds and elapsed_time > max_seconds:
                break
            if plan:
                plan_times.append((plan, elapsed_time))
        return plan_times
        # back to your program****

    def pyhop_generator(self, state, tasks, verbose=0, disable_branch_bound=False):
        self.verbose = verbose
        self.log(1, f"** anyhop, verbose={self.verbose}: **\n   state = {state.__name__}\n   tasks = {tasks}")
        options = [PlanStep([], tasks, state)]
        shortest_length = None
        while len(options) > 0:
            candidate = options.pop()
            if shortest_length is None or (not disable_branch_bound and len(candidate.plan) < shortest_length):
                self.log(2, f"depth {candidate.depth()} tasks {candidate.tasks}")
                self.log(3, f"plan: {candidate.plan}")
                if candidate.complete():
                    self.log(3, f"depth {candidate.depth()} returns plan {candidate.plan}")
                    self.log(1, f"** result = {candidate.plan}\n")
                    shortest_length = len(candidate.plan)
                    yield candidate.plan
                else:
                    options.extend(candidate.successors(self))
                    yield None
            else:
                yield None

    def anyhop_best(self, state, tasks, max_seconds=None, verbose=0):
        plans = self.anyhop(state, tasks, max_seconds, verbose)
        return plans[-1][0]

    def anyhop_stats(self, state, tasks, max_seconds=None, verbose=0):
        plans = self.anyhop(state, tasks, max_seconds, verbose)
        return [(len(plan), time) for (plan, time) in plans]


class PlanStep:
    def __init__(self, plan, tasks, state):
        self.plan = plan
        self.tasks = tasks
        self.state = state

    def depth(self):
        return len(self.plan)

    def complete(self):
        return len(self.tasks) == 0

    def successors(self, planner):
        options = []
        self.add_operator_options(options, planner)
        self.add_method_options(options, planner)
        if len(options) == 0:
            planner.log(3, f"depth {self.depth()} returns failure")
        return options

    def add_operator_options(self, options, planner):
        next_task = self.next_task()
        if type(next_task[0]) == list:
            print(f"next_task: {next_task}")
        if next_task[0] in planner.operators:
            planner.log(3, f"depth {self.depth()} action {next_task}")
            operator = planner.operators[next_task[0]]
            newstate = operator(copy.deepcopy(self.state), *next_task[1:])
            planner.log_state(3, f"depth {self.depth()} new state:", newstate)
            if newstate:
                options.append(PlanStep(self.plan + [next_task], self.tasks[1:], newstate))

    def add_method_options(self, options, planner):
        con = dict_form(initial_state)
        route, cor = method_options(c_nbor[-1], destination, con)
        next_task = self.next_task()
        if next_task[0] in planner.methods:
            planner.log(3, f"depth {self.depth()} method instance {next_task}")
            method = planner.methods[next_task[0]]
            for met in method:
                if route == 'lr' and (str(met).find('function long_route')) == 1:
                    break
                elif route == 'tc' and (str(met).find('function truck_crossing')) == 1:
                    break
                elif route == 'pc' and (str(met).find('function pedestrian_crossing')) == 1:
                    break
                elif route == 'ac' and (str(met).find('function animal_crossing')) == 1:
                    break
                elif route == 'hz' and (str(met).find('function hospital_zone')) == 1:
                    break
                elif route == 'sz' and (str(met).find('function school_zone')) == 1:
                    break
                elif route == 'ir' and (str(met).find('function icy_road')) == 1:
                    break
                elif route == 'uc' and (str(met).find('function under_construction')) == 1:
                    break
                elif route == 'lg' and (str(met).find('function loose_gravel')) == 1:
                    break
                elif route == 'sr' and (str(met).find('function slippery_road')) == 1:
                    break
                elif route == 'lv' and (str(met).find('function lane_visible')) == 1:
                    break
            subtask_options = met(self.state, *next_task[1:])
            if subtask_options is not None:
                for subtasks in subtask_options.options:
                    planner.log(3, f"depth {self.depth()} new tasks: {subtasks}")
                    options.append(PlanStep(self.plan, subtasks + self.tasks[1:], self.state))

    def next_task(self):
        result = self.tasks[0]
        if type(result) is tuple:
            return result
        else:
            return tuple([result])


############################################################
# Helper functions that may be useful in domain models

def dict_form(connections=initial_state):
    conn = {}
    for (loc1, loc2, val) in connections:
        if loc1 not in conn:
            conn[loc1] = []
        if loc2 not in conn:
            conn[loc2] = []
        conn[loc1].append(loc2)
        conn[loc2].append(loc1)

    return conn


def setup_state(title, people, connections):
    state = State(title)
    state.visited = {person: [] for (person, location) in people}
    state.loc = {person: location for (person, location) in people}
    state.connected = {}
    state.speed = {'car': 'Zero'}
    state.esp = {'car': False}
    for (loc1, loc2, val) in connections:
        if loc1 not in state.connected:
            state.connected[loc1] = []
        if loc2 not in state.connected:
            state.connected[loc2] = []
        state.connected[loc1].append(loc2)
        state.connected[loc2].append(loc1)

    return state


def forall(seq, cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True


def find_if(cond, seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x):
            return x


def method_options(start, end, connected):
    global c_nbor
    wt = 0
    if end in connected[start]:
        cc_nbor = end
        nbor = cc_nbor
        node = [start, nbor]
        for i in initial_state:
            if set(node).issubset(i) and nbor not in c_nbor:
                route = i[2]
                route = [i for i, a in globals().items() if a == route][0]
    else:
        method_option = []
        for nbor in connected[start]:
            node = [start, nbor]
            for i in initial_state:
                if set(node).issubset(i) and nbor not in c_nbor:
                    method_option.append(i[2])
                    if i[2] > wt:
                        cc_nbor = nbor
                        wt = i[2]
        method_option.sort(reverse=True)
        route = [i for i, a in globals().items() if a == method_option[0]][0]

    return route, cc_nbor


def print_route():
    trust = 0
    route = []
    route_exp = []
    num = len(c_neighbor)
    for i in range(num - 1):
        nod = tuple([c_neighbor[i], c_neighbor[i + 1]])
        for ii in initial_state:
            if set(nod).issubset(ii):
                trust = trust + ii[2]
                route1 = [i for i, a in globals().items() if a == ii[2]][0]
                route.append(route1)
    if num > 1:
        trust = int(trust / (num - 1))
    for i in route:
        if i == 'lr':
            route_exp.append('Long route')
        elif i == 'tc':
            route_exp.append('Truck crossing')
        elif i == 'pc':
            route_exp.append('Pedestrian crossing')
        elif i == 'sr':
            route_exp.append('Slippery route')
        elif i == 'nsr':
            route_exp.append('Non slippery route')
        elif i == 'lg':
            route_exp.append('Loose gravel route')
        elif i == 'uc':
            route_exp.append('Route under construction')
        elif i == 'lv':
            route_exp.append('Route with lane visibility')
        elif i == 'lnv':
            route_exp.append('Route with no lane visibility')
        elif i == 'ir':
            route_exp.append('Icy road')
        elif i == 'ac':
            route_exp.append('Animal crossing')
        elif i == 'ps':
            route_exp.append('Play street')
        elif i == 'sz':
            route_exp.append('School zone')
        elif i == 'hz':
            route_exp.append('Hospital zone')
    return c_neighbor, trust, route_exp
