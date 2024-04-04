lr = 98  # long route
tc = 95  # truck crossing
pc = 80  # pedestrian crossing
sr = 88  # slippery route
nsr = 97  # non-slippery route
lg = 89  # loose gravel
uc = 83  # under construction
lv = 99  # lane visible
lnv = 70  # lane not visible
ir = 89  # icy road
ac = 82  # animal crossing
ps = 75  # play street
sz = 76  # school zone
hz = 78  # hospital zone

# initial state
source = 'Osterreichischer_Platz'

initial_state = [('Osterreichischer_Platz', 'StadtPalais', hz), ('Osterreichischer_Platz', 'Pursuits', lr),
                 ('StadtPalais', 'Gewerschaftshaus', sz), ('StadtPalais', 'Staatsgalerie', lr),
                 ('Pursuits', 'Gewerschaftshaus', pc), ('Staatsgalerie', 'Stuttgart_hbf', lv),
                 ('Stuttgart_hbf', 'Gewerschaftshaus', uc)]

# initial task network
destination = 'Staatsgalerie'
