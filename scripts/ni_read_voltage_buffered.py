#!/usr/bin/env python
# coding: utf-8

# In[1]:


##############################################
# Hardware
#    - Windows 11 
#    - NI USB-6008
#    Erst NI-DAQmx 19.5 installiert 
#          (aktuelle Version 2023 Q2 zeigt die Karte nicht an)
#          (Die Unterstützung für Net Framework und C++ nicht installieren wenn kein Compiler auf dem Rechner)
#    Dann nidaqmax installieren: "pip install nidaqmx" in Anaconda Prompt

import time as t
import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType
import pprint

fSampling = 10000 #Hz
nSamples = 1000 #samples
pp = pprint.PrettyPrinter(indent=4)
dtMax = 1 #sec

###############################################
# DAQ

data = []
t_insgesamt = 0

# config
with nidaqmx.Task() as task:
    t_vorher = t.time()    
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(fSampling, sample_mode=AcquisitionType.CONTINUOUS)

    t_nachher = t.time()    
    while t_insgesamt < dtMax:
        value = task.read(number_of_samples_per_channel=nSamples)
        #t.sleep(1)
        data.extend(value)
        t_nachher = t.time()
        dt_buffer = t_nachher-t_vorher
        t_insgesamt += dt_buffer
        t_vorher = t_nachher
        #Verzögerungen haben keinen Einfluss auf die Messung! Super, hier der Beweis:        
        #print(dt_buffer)
        #pp.pprint(data)
###############################################
# output to file


# In[2]:


print("Gesamte Messzeit [s]: " + str(t_insgesamt))
print("Anzahl aufgenommener Werte: " + str(len(data)))
print("Abtastfrequenz [Hz]: " + str(len(data) / t_insgesamt))


# In[3]:


import matplotlib.pyplot as plt
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

fig = plt.figure()
plt.plot(data)
plt.tight_layout()
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.show()
fig.savefig('..\output_bilder\output_voltage.png', dpi=fig.dpi)


# In[4]:


f = open("..\output_csv\output_voltage.txt", "w")
f.write("t,U")
for i in range(len(data)):
    f.write(str(i/len(data)*t_insgesamt) + ',' + str(data[i]) + '\n')
f.close()


# In[ ]:




