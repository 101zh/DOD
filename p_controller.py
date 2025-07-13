class PController:
    def __init__(self, kp, tolerance=0.1):
        self.kp = kp
        self.tolerance = tolerance
    
    def update(self, setpoint, current_value):
        error = setpoint - current_value
        at_setpoint = abs(error) <= self.tolerance
        
        # Only apply control if outside tolerance
        output = 0.0 if at_setpoint else self.kp * error
        
        return output, at_setpoint
