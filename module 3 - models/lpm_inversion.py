import numpy as np

# the details of this model aren't super important 
# ...unless you're feeling adventurous, then have at it
def lpm_wk(t,a,b,c,q_future = None):
    ''' Lumped parameter model for calibration.
    
    Inputs:
    -------
    t : array-like
        time (independent variable)
    a : float
        parameter coefficient of first term of ODE
    b : float
        parameter coefficient of second term of ODE
    c : float 
        parameter coefficient of third term of ODE
    q_future: float
        constant flow rate for post calibration period (for model prediction)
        
    Notes:
    ------
    To be used as an input to curve_fit (automatic Python calibration) this function MUST be defined
    with the independent variable as the first input, and parameters as subsequent inputs.
    '''
    # rescale the parameters
    a = a*1.e-8               # [s-1]
    b = b*1.e-5               # [m-1.s-2]
    c = c*1.e3                # [m-1.s-1]
    
    dt = 365*24*3600.         # time step [s]
    p0 = 56.26e5              # initial reservoir pressure [Pa]

    # load production history
    tq,q = np.genfromtxt('production_history.csv', delimiter = ',', unpack=True)
    # append future flow rate if appropriate
    if q_future is not None:
        tq = np.concatenate([tq, np.arange(tq[-1]+1, tq[-1]+51, 1)])
        q = np.concatenate([q, q_future*np.ones(50)])
    
    # solve the ODE (we're not using scipy ODE method now)
    p = [p0]                  # initial value [Pa]
    for i in range(len(q)-2): # iteration using improved Euler method
        y0 = p0-p[-1]
        f0 = -a*(y0)+b*q[i]+c*(q[i+1]-q[i])/dt
        y1 = y0 + dt*f0
        f1 = -a*(y1)+b*q[i+1]+c*(q[i+2]-q[i+1])/dt
        y2 = y0 + (dt/2)*(f0+f1)
        p.append(p0-y2)

    # last step, we'll interpolate (piecewise linear) the solution onto the array of input times
    pi = np.interp(t, tq[:-1], p) 
    return pi*1.e-5    # reservoir pressure [bars]

from scipy.optimize import curve_fit                     # the function we'll be using for automatic calibration

# the inputs to curve_fit are, in order
# - a function, representing the model (see above definition of lpm_wk)
# - an array of independent variables, corresponding to the data/measurements
# - an array of dependent variables, the data/measurements
# - an initial guess of the parameters (in our case, initial a, b and c)
# there are two outputs: the best-fitting parameter values and their covariances (we'll ignore the second part)

# let's see how it works!
    # load in the data again
tp, p = np.genfromtxt('pressure_history.csv', delimiter=',', unpack=True)
    # define an initial guess for the parameters
par_i = [5, 8, -3]
par, pcov = curve_fit(lpm_wk, tp, p, par_i)
print(par)

# convert fitted parameters to SI values (see lpm_wk definition for more details)
a_fit, b_fit, c_fit = par                 # 'unpack' the list of best-fit parameters to individual variables
a_SI = a_fit*1.e-8      # [/s]
b_SI = b_fit*1.e-5      # [/m /s^2]
c_SI = c_fit*1.e3       # [/m /s]

# other reservoir parameters (SI values)
g = 9.81                # [m/s^2]
A = 15.e6               # [m^2]
S0 = 0.3                # []

# calculate porosity
phi = (g/(A*(1-S0)))/(b_SI**2/(b_SI-a_SI*c_SI))
print(phi)