import pyhop_anytime.pyhop
from pyhop_anytime import *


# operator
def move(state, entity, start, end):
    if state.loc[entity] == start and end in state.connected[start] and end not in state.visited[entity]:
        state.loc[entity] = end
        state.visited[entity].append(end)
        return state


def start_up(state, a, x):
    if state.loc[a] == x:
        state.speed[a] = 'Increasing'
        return state
    else:
        return False


def accelerate_on_lane(state, a, x):
    if state.speed[a] != 'High':
        state.speed[a] = 'High'
        return state
    else:
        return False


def continue_acceleration(state, a, x):
    if state.speed[a] != 'High':
        state.speed[a] = 'High'
        return state
    else:
        return False


def accelerate_till_pedestrian(state, a, x):
    if state.speed[a] != 'High':
        state.speed[a] = 'High'
        return state
    else:
        return False


def decelerate_in_zone(state, a):
    if state.speed[a] != 'Low':
        state.speed[a] = 'Low'
        return state
    else:
        return False


def dodge_obstacle(state, a):
    if state.speed[a] != 'Low':
        state.speed[a] = 'Low'
        return state
    else:
        return False


def dodge_pedestrian(state, a):
    if state.speed[a] != 'Low':
        state.speed[a] = 'Low'
        return state
    else:
        return False


def dodge_animal(state, a):
    if state.speed[a] != 'Low':
        state.speed[a] = 'Low'
        return state
    else:
        return False


def activate_esp(state, a):
    if not state.esp[a]:
        state.esp[a] = True
        return state
    return False


def stop(state, a, y):
    if state.loc[a] != y:
        state.loc[a] = y
        state.speed[a] = 'Zero'
        return state
    else:
        return False


def reach(state, a, y):
    if state.loc[a] != y:
        state.loc[a] = y
        state.speed[a] = 'Low'
        return state
    else:
        return False


# method
def long_route(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'lr':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList([('start_up', entity, start), ('accelerate_on_lane', entity, start),
                             ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def truck_crossing(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'tc':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList([('start_up', entity, start), ('accelerate_on_lane', entity, start),
                             ('dodge_obstacle', entity), ('continue_acceleration', entity, cc_nbor),
                             ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def pedestrian_crossing(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'pc':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList([('start_up', entity, start), ('accelerate_on_lane', entity, start),
                             ('dodge_pedestrian', entity), ('continue_acceleration', entity, cc_nbor),
                             ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def animal_crossing(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'ac':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList([('start_up', entity, start), ('accelerate_on_lane', entity, start),
                             ('dodge_animal', entity), ('continue_acceleration', entity, cc_nbor),
                             ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def hospital_zone(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'hz':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList([('start_up', entity, start), ('accelerate_on_lane', entity, start),
                             ('decelerate_in_zone', entity), ('continue_acceleration', entity, cc_nbor),
                             ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def school_zone(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'sz':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList([('start_up', entity, start), ('accelerate_on_lane', entity, start),
                             ('decelerate_in_zone', entity), ('continue_acceleration', entity, cc_nbor),
                             ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def icy_road(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'ir':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList(
                [('start_up', entity, start), ('activate_esp', entity), ('accelerate_on_lane', entity, start),
                 ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def under_construction(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'uc':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList(
                [('start_up', entity, start), ('activate_esp', entity), ('accelerate_on_lane', entity, start),
                 ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def loose_gravel(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'lg':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList(
                [('start_up', entity, start), ('activate_esp', entity), ('accelerate_on_lane', entity, start),
                 ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def slippery_road(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'sr':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList(
                [('start_up', entity, start), ('activate_esp', entity), ('accelerate_on_lane', entity, start),
                 ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


def lane_visible(state, entity, start, end):
    if start == end:
        return TaskList(completed=True)
    else:
        weight, cc_nbor = method_options(start, end, state.connected)
        if weight == 'lv':
            c_nbor.append(cc_nbor)
            c_neighbor.append(cc_nbor)
            return TaskList([('start_up', entity, start), ('accelerate_on_lane', entity, start),
                             ('reach', entity, cc_nbor), ('travel', entity, cc_nbor, end)])


# declaration of method and operator
def make_travel_planner():
    planner = pyhop.Planner()
    planner.declare_operators(move, start_up, accelerate_on_lane, continue_acceleration, accelerate_till_pedestrian,
                              decelerate_in_zone, dodge_obstacle, dodge_pedestrian, dodge_animal, activate_esp, stop,
                              reach)
    planner.declare_methods('travel', long_route, truck_crossing, pedestrian_crossing, animal_crossing, hospital_zone,
                            school_zone, icy_road, under_construction, loose_gravel, slippery_road, lane_visible)
    return planner
