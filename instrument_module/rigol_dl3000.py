"""This module is for implementing remote control of Rigol DL3000 series
programmable DC electronic loads.

This module works for the following models:
DL3021
DL3021A
DL3031
DL3031A

M. Capotosto
10/8/2026
"""

from time import sleep
from .visa_utils import connect_usb_instrument, \
    connect_ethernet_instrument  # Importing utility module


DELAY = 0.01  # 10ms delay


class DL3000:
    """Create Electronic Load Class"""

    # *************************************************************************
    # ******Initialize Connection******
    def __init__(self, connection_method, address):
        if connection_method == "USB":
            self.device, self.address, self.status = \
                connect_usb_instrument(address)
            self.connected_with = 'USB' \
                if self.status == "Connected" else None
        elif connection_method == "IP":
            self.device, self.address, self.status = \
                connect_ethernet_instrument(address)
            self.connected_with = 'Ethernet' \
                if self.status == "Connected" else None
        else:
            self.device = None
            self.address = None
            self.status = "Not Connected"
            self.connected_with = None

    # *************************************************************************
    # ******IEEE 488.2 Common Commands******
    def get_idn(self):
        """Query instrument identification string."""
        command = "*IDN?"
        idn = self.device.query(command)
        sleep(DELAY)
        return idn.strip()

    def clear_status(self):
        """Clear status registers and error queue."""
        command = "*CLS"
        self.device.write(command)
        sleep(DELAY)

    def factory_reset(self):
        """Restore instrument factory default settings."""
        command = "*RST"
        self.device.write(command)
        sleep(5)  # Wait for reset to finish

    def opc(self):
        """Query operation complete. Returns True when complete."""
        command = "*OPC?"
        response = self.device.query(command)
        sleep(DELAY)
        return bool(int(response))

    def self_test(self):
        """Query instrument self-test results."""
        command = "*TST?"
        response = self.device.query(command)
        sleep(DELAY)
        return response.strip()

    # *************************************************************************
    # ******System Commands******
    def system_error(self):
        """Read one entry from the instrument error queue."""
        command = ":SYST:ERR?"
        response = self.device.query(command)
        sleep(DELAY)
        return response.strip()

    def system_version(self):
        """Query the SCPI version supported by the instrument."""
        command = ":SYST:VERS?"
        response = self.device.query(command)
        sleep(DELAY)
        return response.strip()

    # *************************************************************************
    # ******Input Configuration******
    def toggle_input(self, state):
        """Turn the electronic load input ON or OFF.

        Values:
            ON | OFF
            1  | 0
        """
        command = f":SOUR:INP {state}"
        self.device.write(command)
        sleep(DELAY)

    def get_input_state(self):
        """Query electronic load input state.

        Returns:
            True when input is ON, False when input is OFF.
        """
        command = ":SOUR:INP?"
        state = int(float(self.device.query(command)))
        sleep(DELAY)
        return bool(state)

    # *************************************************************************
    # ******Static Function Configuration******
    def set_function(self, mode):
        """Set static operating mode.

        Values:
            CC | CURR | CURRENT
            CV | VOLT | VOLTAGE
            CR | RES | RESISTANCE
            CP | POW | POWER
        """
        mode_map = {
            "CC": "CURR",
            "CURR": "CURR",
            "CURRENT": "CURR",
            "CV": "VOLT",
            "VOLT": "VOLT",
            "VOLTAGE": "VOLT",
            "CR": "RES",
            "RES": "RES",
            "RESISTANCE": "RES",
            "CP": "POW",
            "POW": "POW",
            "POWER": "POW",
        }
        mode_key = str(mode).upper()
        if mode_key not in mode_map:
            raise ValueError("Mode must be CC, CV, CR, or CP.")

        command = f":SOUR:FUNC {mode_map[mode_key]}"
        self.device.write(command)
        sleep(DELAY)

    def get_function(self):
        """Query static operating mode.

        Returns:
            CC | CV | CR | CP
        """
        command = ":SOUR:FUNC?"
        mode = self.device.query(command)
        sleep(DELAY)
        return mode.strip()

    def set_function_mode(self, mode):
        """Set the command group controlling input regulation.

        Values:
            FIX | FIXED
            LIST
            WAV | WAVE
            BATT | BATTERY
            OCP
            OPP
        """
        mode_map = {
            "FIX": "FIX",
            "FIXED": "FIX",
            "LIST": "LIST",
            "WAV": "WAV",
            "WAVE": "WAV",
            "BATT": "BATT",
            "BATTERY": "BATT",
            "OCP": "OCP",
            "OPP": "OPP",
        }
        mode_key = str(mode).upper()
        if mode_key not in mode_map:
            raise ValueError(
                "Mode must be FIX, LIST, WAV, BATT, OCP, or OPP."
            )

        command = f":SOUR:FUNC:MODE {mode_map[mode_key]}"
        self.device.write(command)
        sleep(DELAY)

    def get_function_mode(self):
        """Query the command group controlling input regulation."""
        command = ":SOUR:FUNC:MODE?"
        mode = self.device.query(command)
        sleep(DELAY)
        return mode.strip()

    # *************************************************************************
    # ******Constant Current (CC) Configuration******
    def set_current(self, val):
        """Set regulated current in CC mode. Unit: A."""
        command = f":SOUR:CURR {val}"
        self.device.write(command)
        sleep(DELAY)

    def get_current(self):
        """Query regulated current setting in CC mode. Unit: A."""
        command = ":SOUR:CURR?"
        val = float(self.device.query(command))
        sleep(DELAY)
        return val

    def set_current_range(self, val):
        """Set current range in CC/transient mode.

        DL3021 examples:
            4 A low range
            40 A high range

        MIN, MAX, and DEF are also accepted by the instrument.
        """
        command = f":SOUR:CURR:RANG {val}"
        self.device.write(command)
        sleep(DELAY)

    def get_current_range(self):
        """Query current range in CC mode. Unit: A."""
        command = ":SOUR:CURR:RANG?"
        val = float(self.device.query(command))
        sleep(DELAY)
        return val

    def set_current_slew(self, val):
        """Set both rising and falling CC slew rate. Unit: A/us."""
        command = f":SOUR:CURR:SLEW {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_current_slew_positive(self, val):
        """Set transient rising slew rate. Unit: A/us."""
        command = f":SOUR:CURR:SLEW:POS {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_current_slew_negative(self, val):
        """Set transient falling slew rate. Unit: A/us."""
        command = f":SOUR:CURR:SLEW:NEG {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_von(self, val):
        """Set starting voltage (Von) in CC mode. Unit: V."""
        command = f":SOUR:CURR:VON {val}"
        self.device.write(command)
        sleep(DELAY)

    def get_von(self):
        """Query starting voltage (Von) in CC mode. Unit: V."""
        command = ":SOUR:CURR:VON?"
        val = float(self.device.query(command))
        sleep(DELAY)
        return val

    def set_cc_voltage_limit(self, val):
        """Set voltage limit in CC mode. Unit: V."""
        command = f":SOUR:CURR:VLIM {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_cc_current_limit(self, val):
        """Set current limit in CC mode. Unit: A."""
        command = f":SOUR:CURR:ILIM {val}"
        self.device.write(command)
        sleep(DELAY)

    # *************************************************************************
    # ******Constant Voltage (CV) Configuration******
    def set_voltage(self, val):
        """Set regulated voltage in CV mode. Unit: V."""
        command = f":SOUR:VOLT {val}"
        self.device.write(command)
        sleep(DELAY)

    def get_voltage(self):
        """Query regulated voltage setting in CV mode. Unit: V."""
        command = ":SOUR:VOLT?"
        val = float(self.device.query(command))
        sleep(DELAY)
        return val

    def set_voltage_range(self, val):
        """Set voltage range in CV mode."""
        command = f":SOUR:VOLT:RANG {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_cv_voltage_limit(self, val):
        """Set voltage limit in CV mode. Unit: V."""
        command = f":SOUR:VOLT:VLIM {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_cv_current_limit(self, val):
        """Set current limit in CV mode. Unit: A."""
        command = f":SOUR:VOLT:ILIM {val}"
        self.device.write(command)
        sleep(DELAY)

    # *************************************************************************
    # ******Constant Resistance (CR) Configuration******
    def set_resistance(self, val):
        """Set regulated resistance in CR mode. Unit: ohm."""
        command = f":SOUR:RES {val}"
        self.device.write(command)
        sleep(DELAY)

    def get_resistance(self):
        """Query regulated resistance setting in CR mode. Unit: ohm."""
        command = ":SOUR:RES?"
        val = float(self.device.query(command))
        sleep(DELAY)
        return val

    def set_resistance_range(self, val):
        """Set resistance range in CR mode."""
        command = f":SOUR:RES:RANG {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_cr_voltage_limit(self, val):
        """Set voltage limit in CR mode. Unit: V."""
        command = f":SOUR:RES:VLIM {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_cr_current_limit(self, val):
        """Set current limit in CR mode. Unit: A."""
        command = f":SOUR:RES:ILIM {val}"
        self.device.write(command)
        sleep(DELAY)

    # *************************************************************************
    # ******Constant Power (CP) Configuration******
    def set_power(self, val):
        """Set regulated power in CP mode. Unit: W."""
        command = f":SOUR:POW {val}"
        self.device.write(command)
        sleep(DELAY)

    def get_power(self):
        """Query regulated power setting in CP mode. Unit: W."""
        command = ":SOUR:POW?"
        val = float(self.device.query(command))
        sleep(DELAY)
        return val

    def set_cp_voltage_limit(self, val):
        """Set voltage limit in CP mode. Unit: V."""
        command = f":SOUR:POW:VLIM {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_cp_current_limit(self, val):
        """Set current limit in CP mode. Unit: A."""
        command = f":SOUR:POW:ILIM {val}"
        self.device.write(command)
        sleep(DELAY)

    # *************************************************************************
    # ******Measurement Commands******
    def measure_voltage(self):
        """Measure input voltage. Unit: V."""
        command = ":MEAS:VOLT?"
        volt = float(self.device.query(command))
        sleep(DELAY)
        return volt

    def measure_voltage_max(self):
        """Measure maximum input voltage. Unit: V."""
        command = ":MEAS:VOLT:MAX?"
        volt = float(self.device.query(command))
        sleep(DELAY)
        return volt

    def measure_voltage_min(self):
        """Measure minimum input voltage. Unit: V."""
        command = ":MEAS:VOLT:MIN?"
        volt = float(self.device.query(command))
        sleep(DELAY)
        return volt

    def measure_current(self):
        """Measure input current. Unit: A."""
        command = ":MEAS:CURR?"
        curr = float(self.device.query(command))
        sleep(DELAY)
        return curr

    def measure_current_max(self):
        """Measure maximum input current. Unit: A."""
        command = ":MEAS:CURR:MAX?"
        curr = float(self.device.query(command))
        sleep(DELAY)
        return curr

    def measure_current_min(self):
        """Measure minimum input current. Unit: A."""
        command = ":MEAS:CURR:MIN?"
        curr = float(self.device.query(command))
        sleep(DELAY)
        return curr

    def measure_power(self):
        """Measure input power. Unit: W."""
        command = ":MEAS:POW?"
        power = float(self.device.query(command))
        sleep(DELAY)
        return power

    def measure_resistance(self):
        """Measure input resistance. Unit: ohm."""
        command = ":MEAS:RES?"
        resistance = float(self.device.query(command))
        sleep(DELAY)
        return resistance

    # *************************************************************************
    # ******Trigger / Transient Commands******
    def set_trigger_source(self, source):
        """Set trigger source.

        Values:
            BUS | EXT | EXTERNAL | MAN | MANUAL
        """
        source_map = {
            "BUS": "BUS",
            "EXT": "EXT",
            "EXTERNAL": "EXT",
            "MAN": "MAN",
            "MANUAL": "MAN",
        }
        source_key = str(source).upper()
        if source_key not in source_map:
            raise ValueError("Trigger source must be BUS, EXT, or MAN.")

        command = f":TRIG:SOUR {source_map[source_key]}"
        self.device.write(command)
        sleep(DELAY)

    def get_trigger_source(self):
        """Query trigger source."""
        command = ":TRIG:SOUR?"
        source = self.device.query(command)
        sleep(DELAY)
        return source.strip()

    def trigger(self):
        """Generate an immediate trigger when BUS trigger is selected."""
        command = ":TRIG"
        self.device.write(command)
        sleep(DELAY)

    def toggle_transient(self, state):
        """Turn transient generator ON or OFF."""
        command = f":SOUR:TRAN {state}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_mode(self, mode):
        """Set CC transient mode.

        Values:
            CONT | CONTINUOUS
            PULS | PULSE
            TOGG | TOGGLE
        """
        mode_map = {
            "CONT": "CONT",
            "CONTINUOUS": "CONT",
            "PULS": "PULS",
            "PULSE": "PULS",
            "TOGG": "TOGG",
            "TOGGLE": "TOGG",
        }
        mode_key = str(mode).upper()
        if mode_key not in mode_map:
            raise ValueError("Transient mode must be CONT, PULS, or TOGG.")

        command = f":SOUR:CURR:TRAN:MODE {mode_map[mode_key]}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_level_a(self, val):
        """Set CC transient Level A. Unit: A."""
        command = f":SOUR:CURR:TRAN:ALEV {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_level_b(self, val):
        """Set CC transient Level B. Unit: A."""
        command = f":SOUR:CURR:TRAN:BLEV {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_width_a(self, val):
        """Set CC transient Level A width. Unit: ms."""
        command = f":SOUR:CURR:TRAN:AWID {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_width_b(self, val):
        """Set CC transient Level B width. Unit: ms."""
        command = f":SOUR:CURR:TRAN:BWID {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_frequency(self, val):
        """Set CC continuous transient frequency. Unit: kHz."""
        command = f":SOUR:CURR:TRAN:FREQ {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_period(self, val):
        """Set CC continuous transient period. Unit: ms."""
        command = f":SOUR:CURR:TRAN:PER {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_transient_duty_cycle(self, val):
        """Set CC continuous transient duty cycle. Unit: percent."""
        command = f":SOUR:CURR:TRAN:ADUT {val}"
        self.device.write(command)
        sleep(DELAY)

    # *************************************************************************
    # ******List Mode Commands******
    def set_list_mode(self, mode):
        """Set list operating mode.

        Values:
            CC | CV | CR | CP
        """
        mode = str(mode).upper()
        if mode not in ("CC", "CV", "CR", "CP"):
            raise ValueError("List mode must be CC, CV, CR, or CP.")

        command = f":SOUR:LIST:MODE {mode}"
        self.device.write(command)
        sleep(DELAY)

    def set_list_range(self, val):
        """Set list range for the active list operating mode."""
        command = f":SOUR:LIST:RANG {val}"
        self.device.write(command)
        sleep(DELAY)

    def set_list_count(self, count):
        """Set number of list cycles. 0 means infinite."""
        command = f":SOUR:LIST:COUN {count}"
        self.device.write(command)
        sleep(DELAY)

    def set_list_steps(self, steps):
        """Set number of list steps. Valid instrument range: 2 to 512."""
        command = f":SOUR:LIST:STEP {steps}"
        self.device.write(command)
        sleep(DELAY)

    def set_list_level(self, step, val):
        """Set list level for one step."""
        command = f":SOUR:LIST:LEV {step},{val}"
        self.device.write(command)
        sleep(DELAY)

    def set_list_width(self, step, val):
        """Set list dwell time for one step. Unit: s."""
        command = f":SOUR:LIST:WID {step},{val}"
        self.device.write(command)
        sleep(DELAY)

    # *************************************************************************
    # ******Convenience Functions******
    def apply_cc(self, current, input_state=None):
        """Configure FIXed CC operation and optionally turn input ON/OFF."""
        self.set_function_mode("FIX")
        self.set_function("CC")
        self.set_current(current)
        if input_state is not None:
            self.toggle_input(input_state)

    def apply_cv(self, voltage, input_state=None):
        """Configure FIXed CV operation and optionally turn input ON/OFF."""
        self.set_function_mode("FIX")
        self.set_function("CV")
        self.set_voltage(voltage)
        if input_state is not None:
            self.toggle_input(input_state)

    def apply_cr(self, resistance, input_state=None):
        """Configure FIXed CR operation and optionally turn input ON/OFF."""
        self.set_function_mode("FIX")
        self.set_function("CR")
        self.set_resistance(resistance)
        if input_state is not None:
            self.toggle_input(input_state)

    def apply_cp(self, power, input_state=None):
        """Configure FIXed CP operation and optionally turn input ON/OFF."""
        self.set_function_mode("FIX")
        self.set_function("CP")
        self.set_power(power)
        if input_state is not None:
            self.toggle_input(input_state)

    def load_test(self):
        """Basic electronic load test."""
        print(self.get_idn())
        self.apply_cc(current=0.1, input_state="ON")
        sleep(1)
        print(f"Voltage: {self.measure_voltage()} V")
        print(f"Current: {self.measure_current()} A")
        print(f"Power: {self.measure_power()} W")
        self.toggle_input("OFF")


if __name__ == "__main__":
    load = DL3000(connection_method="IP", address="10.0.142.3")

    if load.status == "Connected":
        print(load.get_idn())
        load.apply_cc(current=0.1, input_state="ON")
        sleep(1)
        print(f"Voltage: {load.measure_voltage()} V")
        print(f"Current: {load.measure_current()} A")
        print(f"Power: {load.measure_power()} W")
        load.toggle_input("OFF")
    else:
        print("Could not connect to instrument.")
