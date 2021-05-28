"""
Demeter example run.

Copyright (c) 2017, Battelle Memorial Institute

Open source under license BSD 2-Clause - see LICENSE and DISCLAIMER

@author:  Chris R. Vernon (chris.vernon@pnnl.gov)
"""

import os
import glob
from configobj import ConfigObj
import ntpath

from demeter.model import Demeter


if __name__ == "__main__":

    # config file in example directory
    ini = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config_LAC.ini')

    # The short names of all the gcms to run
    # GCMS = ["IPSL-CM5A-LR", "MIROC-ESM-CHEM", 'NorESM1-M', 'HadGEM2-ES', 'GFDL-ESM2M']
    # RCPS = ['rcp2p6', 'rcp6p0', 'rcp4p5', 'rcp8p5']
    GCMS = ['GFDL-ESM2M']
    RCPS = ['rcp2p6']
    SCENARIOS = ['Reference', 'Impacts', 'Policy']

    projected_dir = r'E:/NEXO-UA/Demeter/example/inputs/projected/'
    projected_files = glob.glob(projected_dir + '*.csv')
    for gcm in GCMS:
        for rcp in RCPS:
            for scn in SCENARIOS:
                projected_lu_data = [cf for cf in projected_files if 'DemeterDownscaled_33Regions_gcam5p3-stash' in cf and gcm in cf
                                     and rcp in cf and scn in cf]

                scenario = 'gcam5p3-stash_' + gcm + '_' + rcp + '_' + scn
                run_desc = 'demeter_' + scn

                args = {
                    'scenario': scenario,
                    'run_desc': run_desc,
                    'projected_lu_data': ntpath.basename(projected_lu_data[0])
                }

                config = ConfigObj(ini)
                config['PARAMS']['scenario'] = args['scenario']
                config['PARAMS']['run_desc'] = args['run_desc']
                config['INPUTS']['PROJECTED']['projected_lu_data'] = args['projected_lu_data']
                config.write()


                # instantiate Demeter
                dm = Demeter(config=ini)

                # run all time steps as set in config file
                dm.execute()

                # run a random ensemble of parameters
                # dm.ensemble()

                # clean up
                del dm
