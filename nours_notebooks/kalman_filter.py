# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_Kalman_filter.ipynb.

# %% auto 0
__all__ = ['x_estimated', 'P_estimated', 'velocity', 'process_noise', 'measurement_noise', 'KalmanFilter']

# %% ../nbs/02_Kalman_filter.ipynb 9
# Linear Kalman Filter
class KalmanFilter:
    def __init__(self, transition_matrix:np.array, # system model
                 measurment_matrix:np.array, # measurement model
                 init_state:np.array, # initial state
                 state_cov:np.array, # initial state covariance]
                 process_noise_cov:np.array, # process noise covariance
                 measurement_noise_cov:np.array # measurement noise covariance
                 ) -> None:
        self.A = transition_matrix
        self.H = measurment_matrix
        self.x = init_state
        self.P = state_cov
        self.Q = process_noise_cov
        self.R = measurement_noise_cov

    def predict(self) -> None:
        self.x = self.A.dot(self.x)
        self.P = self.A.dot(self.P).dot(self.A.T) + self.Q
    
    def correct(self) -> np.array:
        z = self.H.dot(self.x) + np.random.normal(0, np.sqrt(self.R))
        return z - self.H.dot(self.x)
    
    def compute_kalman_gain(self) -> np.array: # Kalman Gain
        '''
        The Kalman gain is calculated by multiplying the predicted state covariance by
        the transpose of the measurement model and dividing it by the innovation covariance.
        '''
        # innovation covariance
        S = self.H.dot(self.P).dot(self.H.T) + self.R
        return self.P.dot(self.H.T).dot(inv(S))

    def update(self) -> None:
        y = self.correct()
        self.K = self.compute_kalman_gain()
        self.x = self.x + self.K.dot(y)
        self.P = self.P - self.K.dot(self.H).dot(self.P)


# %% ../nbs/02_Kalman_filter.ipynb 13
# Initialize the filter with an initial estimate of the position and the associated uncertainty (covariance)
x_estimated = 0
P_estimated = 1

# Define the velocity and the process noise
velocity = 1
process_noise = 0.1

# Define the measurement noise
measurement_noise = 0.1

for i in range(10):
    # Generate a measurement with some random noise
    measurement = i + np.random.normal(0, measurement_noise)

    # Prediction step
    x_predicted = x_estimated + velocity
    P_predicted = P_estimated + process_noise

    # Correction step
    K = P_predicted / (P_predicted + measurement_noise)
    x_estimated = x_predicted + K * (measurement - x_predicted)
    P_estimated = (1 - K) * P_predicted

    # Print the estimated position
    print("Estimated position: {}".format(x_estimated))
