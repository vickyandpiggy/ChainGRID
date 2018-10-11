import json
import random
import mosaik
from mosaik.util import connect_randomly, connect_many_to_one
import sawtooth_client_interact
import run_mosaik_demo
import read_mosaik_hdf5

sim_config = {
    'CSV': {
        'python': 'mosaik_csv:CSV',
    },
    'DB': {
        'cmd': 'mosaik-hdf5 %(addr)s',
    },
    'HouseholdSim': {
        'python': 'householdsim.mosaik:HouseholdSim',
        # 'cmd': 'mosaik-householdsim %(addr)s',
    },
    'PyPower': {
        'python': 'mosaik_pypower.mosaik:PyPower',
        # 'cmd': 'mosaik-pypower %(addr)s',
    },
}

# start time, duration, config file
START = '2014-01-01 00:00:00'
DUR = 24 * 3600  # 1 day
PERIOD = 900 # 15 mins
NUM_OF_SIM = DUR / PERIOD
PV_DATA = 'data/pv_10kw.csv'
PROFILE_FILE = 'data/profiles.data.gz'
GRID_NAME = 'demo_lv_grid'
GRID_FILE = 'data/%s.json' % GRID_NAME
PRICE_RATIO = 1

def register_nodes(test_id):
    with open(GRID_FILE, 'r') as f:
        grid_config = json.load(f)
        print(json.dumps(grid_config))
    bus_info = grid_config['bus']
    print(bus_info)
    bus_ids = [bus[0] for bus in bus_info]
    print(bus_ids)
    for bus_id in bus_ids:
        usr_name = bus_id + '_' + test_id
        sawtooth_client_interact.key_gen(usr_name)
        p = sawtooth_client_interact.open_cli(usr_name)
        sawtooth_client_interact.register_participant_account(p, usr_name)
        sawtooth_client_interact.close_cli(p, usr_name)

def read_config_file():
    with open(GRID_FILE, 'r') as f:
        grid_config = json.load(f)
        print(json.dumps(grid_config))
    # bus
    bus_info = grid_config['bus']
    bus_ids = [bus[0] for bus in bus_info]
    # branch
    branch_info = grid_config['branch']
    branch_link_info = {}
    for branch in branch_info:
        branch_link_info[branch[0]] = (branch[1], branch[2])
    return bus_ids, branch_link_info

def transactions_between_nodes():
    create_exchange_offer('test_8', 10, 0.5, 'test_7', 2)

if __name__ == '__main__':
    register_nodes('0')
#    bus_ids, branch_link_info = read_config_file()
#    run_mosaik_demo.main(sim_config, START, PERIOD, PV_DATA, PROFILE_FILE, GRID_NAME, GRID_FILE)
#    branch_flow = read_mosaik_hdf5.read('branch')
#    print(branch_flow)
#    for branch in branch_flow.keys():
#        print(branch)
#        sawtooth_client_interact.create_exchange_offer(branch_link_info[branch][0], int(branch_flow[branch][0]), PRICE_RATIO, 
#                branch_link_info[branch][1], int(-branch_flow[branch][1]))
