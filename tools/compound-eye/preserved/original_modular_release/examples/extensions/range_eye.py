"""Complete example plugin: a scalar range, added without modifying the engine."""
import math
def run(inputs,context,dependencies,spec,runtime):
    values=inputs['values']
    if not isinstance(values,list) or not values or any(type(x) not in (int,float) or not math.isfinite(x) for x in values):
        raise ValueError('A nonempty list of finite numbers is required.')
    return {'minimum':min(values),'maximum':max(values),'range':max(values)-min(values),'count':len(values)}
