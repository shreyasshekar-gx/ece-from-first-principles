import math
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'labs'),str(ROOT/'projects')]
from models import *
from run import NAMES, experiment
from reference import sensor_pipeline,robot,cpu,Peripheral

class Models(unittest.TestCase):
    def test_divider_loading(self):
        self.assertEqual(divider(5,10000,10000),2.5)
        self.assertAlmostEqual(divider(5,10000,10000,10000),5/3)
        with self.assertRaises(ValueError): divider(5,0,10)
    def test_rc_limits(self):
        self.assertEqual(rc(0,1,1,5,2),2)
        self.assertAlmostEqual(rc(1,1,1),1-math.exp(-1))
        self.assertAlmostEqual(rc(100,1,1),1)
        with self.assertRaises(ValueError): rc(-1,1,1)
    def test_adc_clamps_and_boundaries(self):
        self.assertEqual(adc(-1),0)
        self.assertEqual(adc(3.3),4095)
        self.assertEqual(adc(1.65),2048)
        self.assertEqual(adc(1,2.56,8),100)
    def test_full_adder_exhaustive(self):
        for a in [0,1]:
            for b in [0,1]:
                for c in [0,1]:
                    s,carry=full_adder(a,b,c)
                    self.assertEqual(s+2*carry,a+b+c)
    def test_cache_conflicts_and_blocks(self):
        self.assertEqual(cache_trace([0,1,16,0,4,4]),[False,True,False,False,False,True])
        self.assertEqual(cache_trace([0,16,0],sets=8),[False,False,True])
    def test_convolution(self):
        self.assertEqual(fir([1,2],[1,-1]),[1,1,-2])
        self.assertEqual(fir([1,0],[0.5,0.5]),[0.5,0.5,0])
        self.assertEqual(fir([],[]),[])
    def test_reflections(self):
        self.assertEqual(reflection(50),0)
        self.assertEqual(reflection(0),-1)
        self.assertAlmostEqual(reflection(100),1/3)
    def test_control_against_equilibrium(self):
        self.assertAlmostEqual(proportional()[-1],2/3,places=6)
        self.assertEqual(proportional(0)[-1],0)
        with self.assertRaises(ValueError): proportional(2,dt=1)
    def test_arm_geometry(self):
        self.assertEqual(arm(0,0),(2,0))
        x,y=arm(0,math.pi/2)
        self.assertAlmostEqual(x,1); self.assertAlmostEqual(y,1)
    def test_fifo_rejection_preserves_order(self):
        q=FIFO(2)
        with self.assertRaises(IndexError): q.pop()
        self.assertTrue(q.push(10)); self.assertTrue(q.push(20))
        self.assertFalse(q.push(30)); self.assertEqual(q.pop(),10)
        self.assertTrue(q.push(40)); self.assertEqual(q.pop(),20)
        self.assertEqual(q.pop(),40)
    def test_fifo_reset(self):
        q=FIFO(); q.push(9); q.reset()
        with self.assertRaises(IndexError): q.pop()
    def test_address_edges(self):
        self.assertFalse(decode_region(0x3fffffff))
        self.assertTrue(decode_region(0x40000000))
        self.assertTrue(decode_region(0x40000fff))
        self.assertFalse(decode_region(0x40001000))
    def test_frame_roundtrip(self):
        for p in [b'',b'hello',bytes(range(256))*2]:
            self.assertEqual(parse_frame(frame(p)),p)
    def test_frame_rejects_malformed(self):
        for data in [b'',b'\x00',b'\x00\x02a',b'\xff\xff',b'\x00\x00x']:
            with self.assertRaises(ValueError): parse_frame(data)
        with self.assertRaises(ValueError): frame(b'x'*513)
    def test_quantization_and_clipping(self):
        self.assertEqual(quantize(0.26)[0],3)
        self.assertEqual(quantize(-0.37)[0],-4)
        self.assertEqual(quantize(100)[0],127)
        self.assertEqual(quantize(-100)[0],-128)
        with self.assertRaises(ValueError): quantize(1,0)
    def test_all_experiments_run(self):
        for name in NAMES:
            with self.subTest(lab=name): self.assertTrue(experiment(name))
    def test_bpsk_theory(self):
        data=experiment('bpsk')
        self.assertLess(abs(data['BER']-data['theoretical_BER']),0.01)
        self.assertEqual(data,experiment('bpsk'))
        self.assertGreater(experiment('bpsk',2)['BER'],data['BER'])

class Capstones(unittest.TestCase):
    def test_sensor_chain(self):
        codes,smooth,payload=sensor_pipeline([1.65]*16)
        self.assertEqual(codes,[2048]*16)
        self.assertEqual(smooth[7:],[2048]*9)
        self.assertEqual(payload,b'\x08\x00'*16)
    def test_robot_straight_and_rotate(self):
        x,y,t=robot(0.5,0.5)
        self.assertAlmostEqual(x,0.5); self.assertEqual(y,0); self.assertEqual(t,0)
        x,y,t=robot(0.2,-0.2,width=0.4)
        self.assertEqual(x,0); self.assertEqual(y,0); self.assertAlmostEqual(t,1)
    def test_robot_curve_analytic(self):
        x,y,t=robot(0.6,0.4)
        self.assertLess(math.hypot(x-1.25*math.sin(0.4),y-1.25*(1-math.cos(0.4))),0.01)
    def test_cpu_semantics(self):
        r,n=cpu([('imm',0,7),('imm',1,5),('add',2,0,1),('halt',)])
        self.assertEqual(r,[7,5,12,0]); self.assertEqual(n,4)
        self.assertEqual(cpu([('imm',0,255),('imm',1,1),('add',2,0,1),('halt',)])[0][2],0)
    def test_cpu_rejects_invalid(self):
        for code in [[('bad',)],[('imm',0,3)],[('imm',4,3),('halt',)]]:
            with self.assertRaises(ValueError): cpu(code)
        with self.assertRaises(ValueError): cpu([('halt',)],limit=0)
    def test_peripheral_contract(self):
        p=Peripheral()
        for i in range(4): self.assertTrue(p.write(0,i))
        self.assertFalse(p.write(0,99)); self.assertEqual(p.read(4),4)
        self.assertEqual([p.read(0) for _ in range(4)],[0,1,2,3])
        p.write(0,42); p.write(8,1); self.assertEqual(p.read(4),0)
        with self.assertRaises(IndexError): p.read(0)
        for addr in [1,3,12,4096]:
            with self.assertRaises(ValueError): p.read(addr)

if __name__=='__main__': unittest.main()
