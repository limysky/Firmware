"""
Copyright (c) 2017, Sensirion AG
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of Sensirion AG nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""



import numpy as np
import matplotlib.pyplot as plt



## differential pressure, sensor values in Pascal
dp_SDP33=np.linspace(0,800,100)



## total length tube in mm = length dynamic port+ length static port; compensation only valid for inner diameter of 1.5mm
l_tube=400

## densitiy air in kg/m3
rho_air=1.29


## flow through sensor
flow_SDP33=(300.805 - 300.878/(0.00344205*dp_SDP33**0.68698 + 1))*1.29/rho_air

## additional dp through pitot tube
dp_Pitot=28557670. - 28557670./(1 + (flow_SDP33/5027611)**1.227924)


## pressure drop through tube
dp_Tube=flow_SDP33*0.000746124*l_tube*rho_air

## speed at pitot-tube tip due to flow through sensor
dv=0.0331582*flow_SDP33

## sum of all pressure drops
dp_tot=dp_SDP33+dp_Tube+dp_Pitot

## computed airspeed without correction for inflow-speed at tip of pitot-tube
airspeed_uncorrected=np.sqrt(2*dp_tot/rho_air)

## corrected airspeed
airspeed_corrected=airspeed_uncorrected+dv


## just to compare to value without compensation
airspeed_raw=np.sqrt(2*dp_SDP33/rho_air)




plt.figure()
plt.plot(dp_SDP33,airspeed_corrected/airspeed_raw)
plt.xlabel('differential pressure raw value [Pa]')
plt.ylabel('correction factor [-]')
plt.show()



plt.figure()
plt.plot(airspeed_corrected,(airspeed_corrected-airspeed_raw)/airspeed_corrected)
plt.xlabel('airspeed [m/s]')
plt.ylabel('relative error [-]')
plt.show()
