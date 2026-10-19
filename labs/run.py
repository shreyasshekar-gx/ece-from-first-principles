"""Run a numerical experiment: python3 labs/run.py rc --sweep 2."""
import argparse
import json
import math
import random
from models import *


def experiment(name, s=1.0):
    if s <= 0 or not math.isfinite(s):
        raise ValueError('Sweep multiplier must be finite and positive')
    if name=='measurement':
        readings=[3.29,3.31,3.30,3.28,3.32]
        return {'readings_V':readings,'mean_V':sum(readings)/len(readings),'loaded_V':divider(5,10000,10000,1e6/s)}
    if name=='math':
        dt=0.1/s
        if dt >= 2:
            raise ValueError('Euler step must be < 2')
        steps=round(1/dt)
        return {'dt_s':dt,'time_s':steps*dt,'Euler':(1-dt)**steps,'exact':math.exp(-steps*dt)}
    if name=='divider':
        return {'load_ohm':10000*s,'unloaded_V':divider(5,10000,10000),'loaded_V':divider(5,10000,10000,10000*s)}
    if name=='rc':
        return {'R_ohm':1000*s,'C_F':1e-6,'time_ms':[0,1,2,3,4,5],'voltage_V':[rc(i/1000,1000*s,1e-6,3.3) for i in range(6)]}
    if name=='diode':
        # This experiment varies ideality factor, not voltage, to avoid unbounded exponentials.
        return {'ideality_factor':s,'voltage_V':[0.1,0.2,0.3],'current_A':[1e-12*math.expm1(v/(s*0.0259)) for v in [0.1,0.2,0.3]]}
    if name=='adc':
        return {'input_V':1.65*s,'code':adc(1.65*s),'step_V':3.3/4096}
    if name=='logic':
        return {'rows':[{'a':a,'b':b,'cin':c,'sum_carry':full_adder(a,b,c)} for a in (0,1) for b in (0,1) for c in (0,1)]}
    if name=='bits':
        x=int(0x11*s)&255
        return {'input':hex(x),'set_bit3_clear_bit0':hex((x|8)&~1&255)}
    if name=='cache':
        addresses=[0,4,0,16,0,4]
        return {'addresses':addresses,'sets':max(1,int(4*s)),'hits':cache_trace(addresses,sets=max(1,int(4*s)))}
    if name=='uart':
        return {'baud':9600*s,'bytes':50,'time_s':50*10/(9600*s)}
    if name=='schedule':
        u=2*s/10+3*s/20
        return {'utilization':u,'ideal_EDF_feasible':u<=1,'assumptions':'Independent preemptible periodic tasks, D=T, no overhead or blocking.'}
    if name=='fir':
        return {'input':[1,2,0,0],'coefficients':[0.5*s,0.5*s],'full_output':fir([1,2,0,0],[0.5*s,0.5*s])}
    if name=='bpsk':
        rng=random.Random(7)
        n=10000
        bits=[rng.randrange(2) for _ in range(n)]
        sigma=0.5*s
        errors=sum((int((2*b-1)+rng.gauss(0,sigma)>=0)!=b) for b in bits)
        return {'samples':n,'noise_sigma':sigma,'errors':errors,'BER':errors/n,'theoretical_BER':0.5*math.erfc(1/(sigma*math.sqrt(2))),'assumptions':'Unit symbols; independent Gaussian noise; perfect synchronization.'}
    if name=='reflection':
        g=reflection(50*s)
        return {'load_ohm':50*s,'gamma':g,'reflected_power_fraction':g*g}
    if name=='control':
        k=2*s
        values=proportional(k,dt=min(0.01,0.5/(1+k)),steps=2000)
        return {'Kp':k,'final_state':values[-1],'analytic_equilibrium':k/(1+k),'assumptions':'First-order plant, no delay, no saturation.'}
    if name=='robot':
        return {'joint_angles_rad':[0,math.pi/2*s],'end_effector_m':arm(0,math.pi/2*s)}
    if name=='counter':
        bits=max(1,min(16,int(3*s)))
        return {'bits':bits,'start':2**bits-2,'next_values':[(2**bits-2+i)%2**bits for i in range(1,6)]}
    if name=='power':
        return {'voltage_V':s,'dynamic_W':0.1*10e-12*s*s*100e6,'assumptions':'Activity=0.1 charging events/cycle; C=10 pF; f=100 MHz; excludes leakage.'}
    if name=='fifo':
        q=FIFO(max(1,int(4*s)))
        accepted=[q.push(i) for i in range(q.depth+1)]
        return {'depth':q.depth,'accepted':accepted,'readback':[q.pop() for _ in range(q.depth)]}
    if name=='timing':
        actual=0.4+5*s+0.6
        return {'period_ns':8,'arrival_ns':actual,'setup_slack_ns':8-actual,'assumptions':'Simplified path; no skew or uncertainty; not sign-off STA.'}
    if name=='soc':
        base=0x40000000
        addresses=[base-1,base,base+4095,base+4096]
        return {'addresses':[hex(a) for a in addresses],'decoded':[decode_region(a) for a in addresses]}
    if name=='packet':
        payload=b'ECE'*max(1,min(170,int(3*s)))
        encoded=frame(payload)
        return {'frame_hex':encoded.hex(),'roundtrip':parse_frame(encoded).decode()}
    if name=='thermal':
        power=(5-3.3)*0.2*s
        return {'current_A':0.2*s,'dissipation_W':power,'estimated_junction_C':40+power*100,'assumptions':'Steady state; effective thermal resistance 100 C/W.'}
    if name=='quantize':
        return {'scale':0.1*s,'samples':[{'input':v,'code':quantize(v,0.1*s)[0],'reconstructed':quantize(v,0.1*s)[1]} for v in [-0.37,0,0.26,20]]}
    raise ValueError('Unknown lab: '+name)

NAMES='measurement math divider rc diode adc logic bits cache uart schedule fir bpsk reflection control robot counter power fifo timing soc packet thermal quantize'.split()
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('lab',choices=NAMES+['all'])
    parser.add_argument('--sweep',type=float,default=1,help='Multiplier for the lab-specific input; see labs/README.md')
    args=parser.parse_args()
    try:
        output={name:experiment(name,args.sweep) for name in (NAMES if args.lab=='all' else [args.lab])}
        print(json.dumps(output,indent=2,allow_nan=False))
    except (ValueError,OverflowError) as exc:
        parser.error(str(exc))
