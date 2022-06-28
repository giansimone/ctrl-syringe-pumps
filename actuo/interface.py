DEFAULT_ADR_ACTO1 = 0

DEFAULT_ADR_ACTO2 = 1

RATE_UNITS = ['UM', 'MM', 'UH', 'MH']

DIAMETER_RANGE = [0.1, 50.0]


def send_cmd(func):
    """Send a command over the serial bus."""
    def wrapper(self, *args, **kwargs):
        msg, dev_adr = func(self, *args, **kwargs)
        adress = str(dev_adr).zfill(2)
        rx_msg = self.tx_cmd(adr=adress, cmd=msg)
        print('Command sent over the serial bus. Received command: ' + rx_msg)
        return rx_msg
    return wrapper


class Interface:
    """Interface to control the syringe pumps in the network."""

    def __init__(self, adr1=DEFAULT_ADR_ACTO1, adr2=DEFAULT_ADR_ACTO2) -> None:
        """Constructor."""
        self.ADR1, self.ADR2 = adr1, adr2
    
    @send_cmd
    def test_pump(self, adr : int):
        """Test the selected pump."""
        return 'VER', adr

    @send_cmd
    def set_diameter(self, adr : int, val : int):
        """Set the inside syringe diamenter for the selected pump."""
        lower_val, upper_val = DIAMETER_RANGE
        if lower_val<val<upper_val:
            wrap_cmd = 'DIA ' + str(val)
            return wrap_cmd, adr
        else:
            raise ValueError('The inside diameter must be within the range [0.1, 50] mm.')
    
    @send_cmd
    def set_direction_infuse(self, adr : int):
        """Set the infuse mode for the selected pump."""
        return 'DIR INF', adr
    
    @send_cmd
    def set_direction_withdraw(self, adr : int):
        """Set the withdraw mode for selected pump."""
        return 'DIR WDR', adr
    
    @send_cmd
    def set_direction_reverse(self, adr : int):
        """Reverse the flow for the selected pump."""
        return 'DIR REV', adr
    
    @send_cmd
    def set_pumping_rate(self, adr : int, val : float, rate_unit : str):
        """Set the pumping rate for the selected pump."""
        if any(rate_unit in s for s in RATE_UNITS):
            wrap_cmd = 'RAT ' + str(val) + ' ' + rate_unit
            return wrap_cmd, adr
        else:
            raise ValueError('Value error for the rate units.')
    
    @send_cmd
    def run_pump(self, adr : int):
        """"Run the selected pump."""
        return 'RUN', adr

    @send_cmd
    def stop_pump(self, adr : int):
        """Pause the selected pump."""
        return 'STP', adr