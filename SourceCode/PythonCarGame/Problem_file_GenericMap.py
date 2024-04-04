lr = 98  # long route
tc = 95  # truck crossing
pc = 80  # pedestrian crossing
sr = 88  # slippery route
nsr = 97  # non-slippery route
lg = 89  # loose gravel
uc = 83  # under construction
lv = 99  # lane visible
lnv = 12  # lane not visible
ir = 89  # icy road
ac = 82  # animal crossing
cs = 1  # charging station
gs = 1  # gas station
ps = 75  # play street
sz = 76  # school zone
hz = 78  # hospital zone

# initial state
source = 'A'
initial_state = [('A', 'B', hz), ('A', 'C', lr), ('B', 'D', ac), ('B', 'C', pc),
                 ('C', 'D', ir), ('C', 'E', tc), ('D', 'E', lv), ('D', 'F', sz), ('E', 'F', hz), ('F', 'Z', sz)]

# initial task network
destination = 'F'
