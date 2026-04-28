import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def __del__(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        number = max(0, min(int(number), 255))
        bin_val = [int(bit) for bit in bin(number)[2:].zfill(8)]
        GPIO.output(self.bits_gpio, bin_val)

    def sequential_counting_adc(self):
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            
            if GPIO.input(self.comp_gpio) == 1:
                return value
        
        return 255

    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()
        voltage = (digital_value / 255.0) * self.dynamic_range
        return voltage

if __name__ == "__main__":
    MY_DYNAMIC_RANGE = 3.3 
    
    adc = R2R_ADC(dynamic_range=MY_DYNAMIC_RANGE)
    
    try:
        while True:
            voltage = adc.get_sc_voltage()
            print(f"{voltage:.3f}")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        pass
    finally:
        del adc