"""Executable capstone reference models; not hardware implementations."""
import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'labs'))
from models import FIFO, adc, fir, frame, parse_frame
from run import experiment


def sensor_pipeline(values):
    codes=[adc(v) for v in values]
    smooth=fir(codes,[1/8]*8)[:len(codes)]  # zero-filled startup history
    payload=b''.join(code.to_bytes(2,'big') for code in codes)
    return codes,smooth,parse_frame(frame(payload))


def robot(vr,vl,width=0.5,dt=0.001,seconds=1):
    if width<=0 or dt<=0 or seconds<0:
        raise ValueError('Invalid geometry or time')
    x=y=theta=0.0
    for _ in range(round(seconds/dt)):
        v=(vr+vl)/2
        x+=dt*v*math.cos(theta)
        y+=dt*v*math.sin(theta)
        theta+=dt*(vr-vl)/width
    return x,y,theta


def cpu(program,limit=100):
    """Teaching ISA: ('imm',rd,value), ('add',rd,ra,rb), ('halt',). 4×8-bit registers."""
    r=[0]*4
    def register(index):
        if not isinstance(index,int) or not 0<=index<4:
            raise ValueError('Invalid register')
        return index
    for cycles,ins in enumerate(program,1):
        if cycles>limit:
            raise ValueError('Instruction budget exhausted')
        if not ins:
            raise ValueError('Empty instruction')
        op=ins[0]
        if op=='halt' and len(ins)==1:
            return r,cycles
        if op=='imm' and len(ins)==3:
            r[register(ins[1])]=ins[2]&255
        elif op=='add' and len(ins)==4:
            r[register(ins[1])]=(r[register(ins[2])]+r[register(ins[3])])&255
        else:
            raise ValueError('Unsupported instruction')
    raise ValueError('Program did not halt')


class Peripheral:
    """Offsets: 0=data (R/W), 4=count (R), 8=reset (W, value 1)."""
    def __init__(self):
        self.fifo=FIFO(4)
    def write(self,offset,value):
        if offset==0:
            return self.fifo.push(value & 255)
        if offset==8 and value==1:
            self.fifo.reset()
            return True
        raise ValueError('Invalid write')
    def read(self,offset):
        if offset==0:
            return self.fifo.pop()
        if offset==4:
            return len(self.fifo.data)
        raise ValueError('Invalid read')


def demo(name):
    if name=='sensor-node':
        c,s,p=sensor_pipeline([1.65]*16)
        return {'codes':c,'filtered':s,'payload_hex':p.hex()}
    if name=='robot-controller':
        return {'pose_x_y_theta':robot(0.6,0.4),'units':'m, m, rad'}
    if name=='tiny-cpu':
        r,cycles=cpu([('imm',0,7),('imm',1,5),('add',2,0,1),('halt',)])
        return {'registers':r,'cycles':cycles,'ISA':'Teaching ISA; not RISC-V'}
    if name=='digital-link':
        return experiment('bpsk')
    if name=='soc-peripheral':
        device=Peripheral()
        accepted=[device.write(0,i) for i in range(5)]
        return {'accepted':accepted,'count':device.read(4),'readback':[device.read(0) for _ in range(4)]}
    raise ValueError(name)

if __name__=='__main__':
    import argparse,json
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project',choices=['sensor-node','robot-controller','tiny-cpu','digital-link','soc-peripheral'])
    print(json.dumps(demo(parser.parse_args().project),indent=2))
