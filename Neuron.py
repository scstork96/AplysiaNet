class Neuron:

    # This method initializes the neuron by setting the four IK parameters (a, b, c, and d) and the step size.
    def __init__(self, a, b, c, d, initial_voltage, input_array, step_size, name):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.input_array = input_array
        self.step_size = step_size
        self.name = name

        # Time always starts at 0
        self.time = 0

        # The potential (v)  and recovery (u) parameters are initialized as described in the IK model.
        self.v = initial_voltage
        self.u = self.v * b

        # An array is initialized to hold the frequency calculations, one for each 0.000008 second interval.
        self.frequency = []

        # Since the biokinetic model always runs for 8.5 seconds, duration has been set to 8.5.
        self.duration = 8.5

        # This will hold the outputs from synapses for use in finding the next current
        self.output = [0]*(int((1 / self.step_size) * self.duration))

        # The index into the input and output arrays is initialized to 0
        self.index = 0

    # Returns the output as an array of currents at each time step
    def get_name(self):
        return self.name

    # Returns the output as an array of currents at each time step
    def get_output(self):
        return self.output

    # Returns the input array
    def get_input(self):
        return self.input_array

    # Sets the input array to the given input array
    def set_input(self, input_array):
        self.input_array = input_array

    # Sets the time to the given value and the current at this time to the given current
    def update(self, time):
        self.time = time
        self.membrane_dt()
        self.output[self.index] = self.v
        self.index += 1

    # This method updates the u and v parameter values using euler's method.
    def run_eulers_method(self):
        self.membrane_dt()
        return

    # This method computes the new voltage at each step. The following code was adapted from Tate Keller:
    def eulers_method(self, prev_voltage, voltage_step):
        return prev_voltage + self.step_size * voltage_step

    # This method sets the membrane potential after euler's method. The following code was adapted from Tate Keller:
    def membrane_dt(self):
        # If v is above the threshold, v is assigned the reset parameter c and u is assigned u plus the recovery parameter d.
        if self.v >= 30:
            self.v = self.c
            self.u = self.u + self.d

        # If v is not above the threshold, euler's method is performed, and the step being passed in is multiplied by
        # 1000 to convert from ms to s.
        else:
            self.v = self.eulers_method(self.v, (((0.04 * self.v**2) + (5 * self.v) + 140 - self.u + self.input_array[self.index - 1]) * 1000))
            self.u = self.eulers_method(self.u, ((self.a * ((self.b * self.v) - self.u)) * 1000))
        return

