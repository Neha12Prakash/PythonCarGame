import pyhop_anytime.pyhop
from pyhop_anytime import *
from Domain_file import *
from Problem_file import *
#from Problem_file_GenericMap import *

state = setup_state('state', [('car', source)], initial_state)
planner = make_travel_planner()
plans = planner.anyhop(state, [('travel', 'car', source, destination)])
path, trust, route = pyhop_anytime.pyhop.print_route()
print('The path taken is: ', path)
print('The respective route: ', route)
print('The average trust value of the route is: ', trust, '%')
for plan, elapsed_time in plans:
    print('Time taken to generate the plan: ', elapsed_time, 's')
    print('Generated Plan: ', plan)

# save plan in a txt file

textfile = open('Plan.txt', 'w')

textfile.write("""
********************************************************************************
Trust based HTN Planning for Automated Vehicles 
********************************************************************************

""")
textfile.write('The path taken is: \n')
for i in path:
    textfile.write(i + '. ')

textfile.write('\n\nTime taken to generate the plan: ' + str(elapsed_time) + ' s')

textfile.write('\n\nThe respective route: \n')
for i in route:
    textfile.write(i + '. ')

textfile.write('\n\nThe average trust value of the route is: ' + str(trust) + '%')

textfile.write('\n\nGenerated Plan: \n')
if plan:
    for i in plan:
        textfile.write(str(i) + '\n')
textfile.close()
