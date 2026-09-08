"""Elemental observations. SI optics; eV junction energies; explicit interventions.
Model families are not identified with one another. No element inference from a spectrum.
"""
import math
import numpy as np
EPS0=8.8541878188e-12
C=299792458.
HBAR_EV=6.582119569e-16
G0=7.748091729e-5

def stop(message):return {'_status':'blocked','reason':message}
def spacing(i,*_):
 p=i['case'];x=np.array(p['energies_eV'],float);u=np.array(p['uncertainties_eV'],float)
 if len(x)<2 or x.shape!=u.shape or not np.all(np.isfinite(x)) or np.any(x<=0) or np.any(u<0):return stop('Positive energies and matching nonnegative uncertainties required.')
 return {'energies_eV':x.tolist(),'increments_eV':np.diff(x).tolist(),'ratios':(x[1:]/x[:-1]).tolist(),'cumulative_work_eV':np.cumsum(x).tolist(),'source_flags':p['source_flags'],'increment_uncertainty_bound_eV':(u[1:]+u[:-1]).tolist(),'scope':'Sequential isolated-ion thresholds at fixed nuclear Z. Sum is minimum reversible ionization work, not a conducting-solid energy band or measured kinetic path.'}

def film_core(w,n,d,ns):
 n=np.asarray(n,complex);w=np.asarray(w,float)
 r01=(1-n)/(1+n);r12=(n-ns)/(n+ns);p=np.exp(2j*np.pi*n*d/w)
 den=1+r01*r12*p*p;r=(r01+r12*p*p)/den;t=(2/(1+n))*(2*n/(n+ns))*p/den
 R=abs(r)**2;T=ns*abs(t)**2;A=1-R-T
 return {'R':R.tolist(),'T':T.tolist(),'A':A.tolist(),'reflection_phase_rad':np.angle(r).tolist(),'bulk_R':abs((1-n)/(1+n))**2,'r':r,'t':t}

def film(i,*_):
 p=i['case'];w=np.array(p['wavelength_nm'],float);n=np.array(p['n'],float)+1j*np.array(p['k'],float);d=float(p['thickness_nm']);ns=float(p['substrate_index'])
 if not(10<=d<=200) or ns<=0 or w.shape!=n.shape or np.any(w<=0) or np.any(n.real<=0) or np.any(n.imag<0):return stop('This material-film study requires 10–200 nm thickness, positive dielectric substrate, wavelengths and passive n+ik. Atomic-layer bulk extrapolation is outside scope.')
 out=film_core(w,n,d,ns);out.pop('r');out.pop('t');out['bulk_R']=out['bulk_R'].tolist()
 eps=n*n;out.update({'wavelength_nm':w.tolist(),'sigma1_S_per_m':(EPS0*(2*np.pi*C/(w*1e-9))*eps.imag).tolist(),'intensity_skin_depth_nm':(w/(4*np.pi*n.imag)).tolist(),'thickness_nm':d,'substrate_index':ns,'scope':'Normal-incidence coherent Maxwell film response using declared bulk optical constants held fixed during geometric thinning. No roughness/percolation/atomic reconstruction or DC inference.'})
 return out

def color(i,ctx,deps,*_):
 p=i['case'];o=next(iter(deps.values()))['value'];w=np.array(o['wavelength_nm']);cmf=np.array(p['cmf']);light=np.array(p['illuminant']);R=np.array(o['R'])
 if cmf.shape!=(len(w),3) or light.shape!=w.shape or np.any(cmf<0) or np.any(light<0):return stop('Matching nonnegative CIE observer and illuminant arrays required.')
 norm=np.trapezoid(light*cmf[:,1],w);xyz=np.trapezoid(R[:,None]*light[:,None]*cmf,w,axis=0)/norm
 white=np.trapezoid(light[:,None]*cmf,w,axis=0)/norm
 linear=np.array([[3.2406,-1.5372,-.4986],[-.9689,1.8758,.0415],[.0557,-.204,1.057]])@xyz
 clipped=np.clip(linear,0,1);srgb=np.where(clipped<=.0031308,12.92*clipped,1.055*clipped**(1/2.4)-.055)
 return {'XYZ_D65':xyz.tolist(),'white_XYZ':white.tolist(),'xy':(xyz[:2]/sum(xyz)).tolist(),'srgb':srgb.tolist(),'gamut_clipped':bool(np.any(linear<0) or np.any(linear>1)),'hex':'#'+''.join(f'{round(c*255):02x}' for c in srgb),'scope':'CIE 1931 2-degree / D65, 380–780 nm truncated observer. Specular reflected daylight; sRGB swatch is not a photograph or geometry-independent material color.'}

def components(i,*_):
 p=i['case'];E=np.asarray(p['energy_eV'],float);q=p['parameters'];scale=float(p.get('interband_scale',1));gam=float(p.get('drude_gamma_scale',1))
 if np.any(E<=0) or not 0<=scale<=1 or gam<=0:return stop('Positive photon energy/damping and interband scale in [0,1] required.')
 wp=q['plasma_eV'];D=-q['drude_strength']*wp*wp/(E*(E+1j*q['drude_gamma_eV']*gam));B=np.zeros_like(D)
 for r in q['oscillators']:B+=r['strength']*wp*wp/(r['energy_eV']**2-E**2-1j*E*r['gamma_eV'])
 eps=1+D+scale*B;n=np.sqrt(eps);fac=EPS0*E/HBAR_EV
 return {'energy_eV':E.tolist(),'epsilon_real':eps.real.tolist(),'epsilon_imag':eps.imag.tolist(),'n':n.real.tolist(),'k':n.imag.tolist(),'drude_sigma1':(fac*D.imag).tolist(),'interband_sigma1':(fac*scale*B.imag).tolist(),'dc_model_S_per_m':EPS0*q['drude_strength']*wp**2/(HBAR_EV*q['drude_gamma_eV']*gam),'removed_oscillator_strength_eV2':float((1-scale)*wp*wp*sum(r['strength'] for r in q['oscillators'])),'scope':'Published Rakić Lorentz–Drude fit; oscillator/damping interventions are causal model controls, not measured atom removal. Optical-fit DC limit is an extrapolation.'}

def channels(i,*_):
 p=i['case'];t=np.asarray(p['transmissions'],float)
 if t.ndim!=1 or not len(t) or np.any(~np.isfinite(t)) or np.any(t<0) or np.any(t>1):return stop('Transmission eigenvalues in [0,1] required.')
 g=float(t.sum());s2=float(t@t);F=float(np.sum(t*(1-t))/g) if g else None
 return {'G_over_G0':g,'G_S':g*G0,'Fano':F,'participation':g*g/s2 if s2 else 0.,'active_above_threshold':int(sum(t>p.get('threshold',.01))),'minimum_channels_from_G_F':int(math.ceil(g/(1-F)-1e-10)) if g else 0,'scope':'Spin-degenerate, elastic, energy-independent low-bias transmission channels. Channel moments do not uniquely identify three or more transmissions.'}

def junction(i,*_):
 p=i['case'];theta=float(p['theta_rad']);gap=float(p['gap_eV']);gamma=float(p['gamma_eV']);E=float(p.get('probe_energy_eV',0))
 if gap<=0 or gamma<=0:return stop('Positive level gap and lead broadening required.')
 sz=np.diag([1.,-1.]);sx=np.array([[0.,1.],[1.,0.]])
 H=gap/2*(np.cos(theta)*sz+np.sin(theta)*sx);vals,U=np.linalg.eigh(H)
 L=np.diag([gamma,0]);R=np.diag([0,gamma]);GR=np.linalg.inv(E*np.eye(2)-H+.5j*(L+R))
 t=float(np.trace(L@GR@R@GR.conj().T).real);D=sz;dip=float(abs(np.vdot(U[:,1],D@U[:,0]))**2)
 S=np.eye(2)-1j*gamma*GR
 return {'levels_eV':vals.tolist(),'gap_eV':gap,'G_over_G0':t,'Fano':1-t,'dipole_strength':dip,'parameter_projector_metric':.25,'scattering_unitarity_residual':float(np.linalg.norm(S.conj().T@S-np.eye(2))),'scope':'Electronic-sheet two-level Hamiltonian with explicitly attached wide-band leads and fixed dipole. Same object, different readouts; model not fitted to Au/Ag/Cu/Pt.'}

def side_peel(i,*_):
 p=i['case'];g=float(p['coupling_eV']);ed=float(p['side_energy_eV']);E=float(p['probe_energy_eV']);gamma=float(p['gamma_eV'])
 if gamma<=0 or g<0:return stop('Nonnegative side coupling and positive lead width required.')
 if g==0:
  gr=1/(E+1j*gamma);se=0j
 elif abs(E-ed)<1e-14:
  return {'G_over_G0':0.,'bare_deletion_G_over_G0':float(gamma**2/(E*E+gamma**2)),'self_energy_pole':True,'feedback_equal_time':g*g,'scope':'Exact Fano antiresonance in a coherent side-coupled orbital model; no inelastic broadening on side orbital.'}
 else:
  se=g*g/(E-ed);gr=1/(E+1j*gamma-se)
 H=np.array([[0,g],[g,ed]]);full=None
 if g>0:
  full=np.linalg.inv(E*np.eye(2)-H+1j*np.diag([gamma,0]))[0,0]
 return {'G_over_G0':float(gamma**2*abs(gr)**2),'bare_deletion_G_over_G0':float(gamma**2/(E*E+gamma**2)),'self_energy_real_eV':float(np.real(se)),'feedback_equal_time':g*g,'schur_full_residual':float(abs(gr-full)) if full is not None else 0.,'scope':'Coherent side-orbital coupling removal. Removing a coupled path may raise conductance by releasing destructive interference; fixed-positive-channel theorem does not apply.'}
