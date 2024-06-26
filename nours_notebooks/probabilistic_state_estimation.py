# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_probablistic_state_estimation.ipynb.

# %% auto 0
__all__ = ['x', 'y', 'f1', 'f2', 'f', 'J', 'DDist', 'JDist', 'calculate_B_matrix']

# %% ../nbs/01_probablistic_state_estimation.ipynb 3
class DDist:
    def __init__(self, dictionary:dict) -> None:
        self.d = dictionary
    def prob(self, elt # an element of the domain of this distribution
             ) -> float:
        if elt in self.d:
            return self.d[elt]
        else:
            return 0
    def support(self):
        return [k for k in self.d.keys() if self.prob(k) > 0]
    @property
    def dist(self):
        return self.d
    def draw(self):
        r = random.random()
        sum = 0.0
        for val in self.support():
            sum += self.prob(val)
            if r < sum:
                return val

# %% ../nbs/01_probablistic_state_estimation.ipynb 9
# Calculate the join distribution probabilities.
class JDist(DDist):
    def __init__(self, PA:DDist # P(A)
                 ,PBgA:callable # condtional probability P(B|A)
                 ) -> DDist:
        PAB = dict()
        for a in PA.dist.keys():
            PBgA_a = PBgA(a)
            for b in PBgA_a.dist.keys():
                PAB[(a,b)] = PA.prob(a) * PBgA_a.prob(b)
        self.d = PAB
    def marginalizeOut(self, 
                       idx:int # which random variable ..?
                       ) -> DDist:
        # A = a
        symbolKeys = self.d.keys()
        for key in symbolKeys:
            s = key[idx]
            
        return
    

# %% ../nbs/01_probablistic_state_estimation.ipynb 13
import numpy as np

def calculate_B_matrix(yaw:float, dt:float=0.1) -> np.array:
     """
     Calculates and returns the `B` matrix.

     A 3x2 matrix (number of states x number of control inputs).
     The control inputs are the forward speed and the
     rotation rate around the z axis from the x-axis in the 
     counterclockwise direction.

     [v, yaw_rate]

     This matrix expresses how the state of the system [x,y,yaw] changes
     from t-1 to t due to the control commands (i.e. control input).

     Parameters
     ----------
     yaw
          The yaw (rotation angle around the z axis) in radians.
     dt
          The change in time from time step t-1 to t in seconds.

     Returns
     -------
     np.ndarray: The B matrix as a NumPy array.
     """
     B = np.array([
          [np.cos(yaw) * dt, 0],
          [np.sin(yaw) * dt, 0],
          [0, dt]
     ])
     return B

# %% ../nbs/01_probablistic_state_estimation.ipynb 19
import sympy as sp

# Define the symbols
x, y = sp.symbols('x y')

# Define the function
f1 = sp.sin(x) + y**2
f2 = sp.cos(y) + x**2
f = sp.Matrix([f1, f2])

# Compute the Jacobian matrix
J = f.jacobian([x, y])

# Print the Jacobian matrix
print("Symbolic Jacobian matrix:")
sp.pprint(J)
sp.pprint(f)

