"""Small educational models. SI units unless a function explicitly says otherwise."""
import math
from collections import deque


def parallel(a, b):
    if a <= 0 or b <= 0:
        raise ValueError('Resistances must be positive')
    return a*b/(a+b)


def divider(v, top, bottom, load=None):
    if top <= 0 or bottom <= 0:
        raise ValueError('Resistances must be positive')
    lower = bottom if load is None else parallel(bottom, load)
    return v*lower/(top+lower)


def rc(t, r, c, final=1, initial=0):
    if r <= 0 or c <= 0 or t < 0:
        raise ValueError('Require R,C > 0 and t >= 0')
    return final+(initial-final)*math.exp(-t/(r*c))


def adc(v, ref=3.3, bits=12):
    if ref <= 0 or not isinstance(bits, int) or not 1 <= bits <= 32:
        raise ValueError('Require positive reference and 1–32 bits')
    return max(0, min(2**bits-1, math.floor(v/ref*2**bits)))


def full_adder(a,b,carry=0):
    if any(x not in (0,1) for x in (a,b,carry)):
        raise ValueError('Inputs must be bits')
    total=a+b+carry
    return total & 1, total >> 1


def cache_trace(addresses, sets=4, block=4):
    if sets <= 0 or block <= 0:
        raise ValueError('Cache dimensions must be positive')
    tags=[None]*sets
    result=[]
    for address in addresses:
        if address < 0:
            raise ValueError('Address cannot be negative')
        number=address//block
        index=number % sets
        tag=number//sets
        result.append(tags[index] == tag)
        tags[index]=tag
    return result


def fir(x,h):
    if not x or not h:
        return []
    out=[0.0]*(len(x)+len(h)-1)
    for i,v in enumerate(x):
        for j,c in enumerate(h):
            out[i+j]+=v*c
    return out


def reflection(load, line=50):
    if line <= 0 or load < 0:
        raise ValueError('Require line > 0 and load >= 0')
    return (load-line)/(load+line)


def proportional(k=2, dt=0.01, steps=500):
    """Forward Euler, plant dx/dt = -x + u, u=k*(1-x), no saturation."""
    if k < 0 or dt <= 0 or dt*(1+k) >= 2 or steps < 0:
        raise ValueError('Require nonnegative gain and stable Euler step')
    x=0.0
    values=[x]
    for _ in range(steps):
        x+=dt*(-x+k*(1-x))
        values.append(x)
    return values


def arm(theta1,theta2,l1=1,l2=1):
    if l1 <= 0 or l2 <= 0:
        raise ValueError('Lengths must be positive')
    return (l1*math.cos(theta1)+l2*math.cos(theta1+theta2),
            l1*math.sin(theta1)+l2*math.sin(theta1+theta2))


class FIFO:
    """Bounded FIFO; rejected pushes and empty pops do not alter state."""
    def __init__(self, depth=4):
        if depth <= 0:
            raise ValueError('Depth must be positive')
        self.depth=depth
        self.data=deque()
    def push(self,value):
        if len(self.data)==self.depth:
            return False
        self.data.append(value)
        return True
    def pop(self):
        if not self.data:
            raise IndexError('FIFO empty')
        return self.data.popleft()
    def reset(self):
        self.data.clear()


def decode_region(address, base=0x40000000, size=4096):
    return base <= address < base+size


def frame(payload):
    if len(payload)>512:
        raise ValueError('Payload exceeds 512-byte policy')
    return len(payload).to_bytes(2,'big')+payload


def parse_frame(data):
    """One complete frame only. No checksum; this lab teaches bounded framing."""
    if len(data)<2:
        raise ValueError('Truncated header')
    length=int.from_bytes(data[:2],'big')
    if length>512:
        raise ValueError('Payload exceeds policy')
    if len(data)!=length+2:
        raise ValueError('Incomplete frame or trailing bytes')
    return data[2:]


def quantize(x, scale=0.1, zero=0, low=-128, high=127):
    """Python ties-to-even rounding, then integer saturation."""
    if scale <= 0 or low > high:
        raise ValueError('Invalid quantizer parameters')
    q=max(low,min(high,round(x/scale)+zero))
    return q,scale*(q-zero)
