# -*- coding: utf-8 -*-

import casperfpga
import time
import matplotlib.pyplot as plt
import struct
import numpy as np

katcp_port=7147
roach = '192.168.40.79'
#firmware_fpg = 'lock_in_v2_2021_Apr_29_1629.fpg'
firmware_fpg = 'snap_test_v2_golden_shower_2021_Jun_01_1606.fpg'
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


def getADCvals():
	fpga.write_int('adc_snap_ctrl', 0)
	time.sleep(0.1)
	fpga.write_int('adc_snap_ctrl', 1)
	time.sleep(0.1)
	fpga.write_int('adc_snap_ctrl', 0)
	time.sleep(0.1)
	fpga.write_int('adc_snap_trig', 1)
	time.sleep(0.1)
	fpga.write_int('adc_snap_trig', 0)
	time.sleep(0.1)
	adc = fpga.read('adc_snap_bram',(2**10)*8)
	return adc[7::8]

def plotADC():
        # Plots the ADC timestream
        fig = plt.figure(figsize=(10.24,7.68))
        plot1 = fig.add_subplot(211)
        line1, = plot1.plot(np.arange(0,1024), np.zeros(1024), 'r-', linewidth = 2)
        plot1.set_title('I', size = 20)
        plot1.set_ylabel('mV', size = 20)
        plt.xlim(0,1024)
        plt.ylim(-600,600)
        plt.yticks(np.arange(-600, 600, 100))
        plt.grid()
        plot2 = fig.add_subplot(212)
        line2, = plot2.plot(np.arange(0,2048), np.zeros(2048), 'b-', linewidth = 2)
        plot2.set_title('Q', size = 20)
        plot2.set_ylabel('mV', size = 20)
        plt.xlim(0,1024)
        plt.ylim(-600,600)
        plt.yticks(np.arange(-600, 600, 100))
        plt.grid()
        plt.tight_layout()
        plt.show(block = False)
        count = 0
        stop = 1.0e8
        while count < stop:
            time.sleep(0.1)
            fpga.write_int('adc_snap_ctrl', 0)
            time.sleep(0.1)
            fpga.write_int('adc_snap_ctrl', 1)
            time.sleep(0.1)
            fpga.write_int('adc_snap_ctrl', 0)
            time.sleep(0.1)
            fpga.write_int('adc_snap_trig', 1)
            time.sleep(0.1)
            fpga.write_int('adc_snap_trig', 0)
            time.sleep(0.1)
            adc = (np.fromstring(fpga.read('adc_snap_bram',(2**10)*8))).astype('float')
            print(adc)
            #adc /= (2**15)
            #adc *= 550.
            #I1 = np.hstack(adc[0::8])
            #I2 = np.hstack(adc[1::8])
            I = np.hstack(zip(adc[::]))
            
            line1.set_ydata(I)
            print(np.shape(I))
            #line2.set_ydata(I2)
            fig.canvas.draw()
            count += 1
        return
        
        
