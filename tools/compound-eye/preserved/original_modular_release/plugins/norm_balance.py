"""An extensible eye for the user's scalar phase/decay hypothesis."""
import math
def run(inputs,context,dependencies,spec,runtime):
    F=inputs['scalar_factor'];psi=inputs['amplitude'];h=inputs['hbar']
    if len(F)!=2 or len(psi)!=2 or any(type(x) not in (float,int) or not math.isfinite(x) for x in F+psi+[h]) or h<=0:
        raise ValueError('Finite real/imaginary pairs and positive hbar required.')
    f=complex(*F);a=complex(*psi);da=-1j*f*a/h
    derivative=2*(a.conjugate()*da).real
    return {'norm_squared':abs(a)**2,'norm_squared_rate':derivative,
        'identity_rate':2*f.imag*abs(a)**2/h,'factor_is_real':f.imag==0,
        'consequence':'This real scalar factor changes phase but cannot cause norm decay.' if f.imag==0 else 'Norm change follows the supplied imaginary scalar factor.',
        'scope':'Pointwise identity for i hbar dpsi/dt=F psi, including a state-dependent F. No nuclear decay mechanism is fitted.'}
