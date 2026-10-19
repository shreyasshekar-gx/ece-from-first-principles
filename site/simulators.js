/* Pure numerical models shared by the workbench and node tests. */
(function(root){
  const models={
    rc(t,r,c,v=3.3){if(r<=0||c<=0||t<0)throw Error('Invalid RC parameters');return v*(1-Math.exp(-t/(r*c)));},
    alias(f,fs){if(fs<=0)throw Error('Invalid sample rate');return Math.abs(((f+fs/2)%fs+fs)%fs-fs/2);},
    reflection(load,line=50){if(load<0||line<=0)throw Error('Invalid impedance');return (load-line)/(load+line);},
    power(v,c=10e-12,f=100e6,a=0.1){return a*c*v*v*f;},
    pwm(t,frequency,duty){return ((t*frequency)%1)<duty?1:0;},
    control(t,k){return k/(1+k)*(1-Math.exp(-(1+k)*t));}
  };
  if(typeof module!=='undefined')module.exports=models;else root.ECE_MODELS=models;
})(typeof window==='undefined'?globalThis:window);
