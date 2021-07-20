# -*- coding: utf-8 -*-

import casperfpga
import time
import matplotlib.pyplot as plt
import struct
import numpy as np

katcp_port=7147
roach = '192.168.40.79'
#firmware_fpg = 'lock_in_v2_2021_Apr_29_1629.fpg'
firmware_fpg = 'test_v4_2021_May_20_1557.fpg'
fpga = casperfpga.katcp_fpga.KatcpFpga(roach, timeout = 3.)
time.sleep(1)
if (fpga.is_connected() == True):
    print 'Connected to the FPGA '
else:
    print 'Not connected to the FPGA'

if (fpga.upload_to_ram_and_program(firmware_fpg) == True):
    print 'Uploaded firmware'
else:
    print 'Failed to upload firmware or already uploaded'
    
fpga.listdev()
