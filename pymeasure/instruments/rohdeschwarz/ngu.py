#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2026 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging

from pymeasure.instruments import Instrument, SCPIMixin
from pymeasure.instruments.common_base import identity, CommonBase
from pymeasure.instruments.validators import strict_discrete_set, strict_range

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class NGUBaseClass(SCPIMixin, Instrument):
    """Base class for Rohde&Schwarz NGU source measure units."""

    DEFAULT_NAME = "NGUBaseClass"

    def __init__(self, adapter, name=None, voltage_range=6, current_range=2, **kwargs):
        super().__init__(
            adapter,
            name if name is not None else self.DEFAULT_NAME,
            **kwargs
        )
        self.voltage_range_values = self.SOURCE_VOLTAGE_RANGES
        self.current_range_values = self.SOURCE_CURRENT_RANGES

        self.voltage_range_set_process = self._update_voltage_validator_range
        self.current_range_set_process = self._update_current_validator_range

        self.voltage_range = voltage_range
        self.current_range = current_range

    # -- System commands --
    uptime = Instrument.measurement(
        "SYST:UPTIME?",
        "Measure system uptime",
    )

    # Beeper settings
    def beep(self):
        """Emit a single beep from the instrument."""
        self.write("SYST:BEEP:WARN")
    """
    beeper_enabled = Instrument.control(
        None
    )

    beep_on_error = Instrument.setting(
        None
    )

    beep_on_complete = Instrument.setting(
        None
    )

    beep_on_cc = Instrument.setting(
        None
    )

    beep_on_protection = Instrument.setting(
        None
    )

    # Trigger settings
    trigger_enabled = Instrument.control(
        None
    )

    trigger_source = Instrument.control(
        None
    )

    trigger_DIO_pin = Instrument.control(
        None
    )

    trigger_mode = Instrument.control(
        None
    )
    """
    priority_mode = Instrument.control(
        "SOUR:PRI?",
        "SOUR:PRI %s",
        "Control whether device should keep voltage or current constant (setpoint)",
        validator=strict_discrete_set,
        values={"voltage": "VOLTage", "current": "CURRent"},
        map_values=True,
        cast=str,
    )

    # Voltage setpoint settings
    voltage_range = Instrument.control(
        "SOUR:VOLT:RANG?",
        "SOUR:VOLT:RANG %d",
        "Control the output voltage range",
        validator=strict_discrete_set,
        dynamic=True
    )

    voltage_setpoint = Instrument.control(
        "SOUR:VOLT?",
        "SOUR:VOLT %g",
        "Control the output voltage setpoint",
        validator=strict_range,
        dynamic=True
    )

    current_range = Instrument.control(
        "SOUR:CURR:RANG?",
        "SOUR:CURR:RANG %d",
        "Control the output current range",
        validator=strict_discrete_set,
        dynamic=True
    )
    current_setpoint = Instrument.control(
        "SOUR:CURR?",
        "SOUR:CURR %g",
        "Control the output current setpoint",
        validator=strict_range,
        dynamic=True
    )

    # Measurement commands
    voltage = Instrument.measurement(
        "MEAS:VOLT?",
        "Measure voltage at output or sense input if connected",
    )

    voltage_statistics = Instrument.measurement(
        "MEAS:VOLT:STAT?",
        "Measure voltage statistics: [MIN, MAX, AVG]",
        get_process_list=identity,
        separator=",",
        cast=float,
    )

    current = Instrument.measurement(
        "MEAS:CURR?",
        "Measure current at the output in A",
    )

    current_statistics = Instrument.measurement(
        "MEAS:CURR:STAT?",
        "Measure current statistics: [MIN, MAX, AVG]",
        get_process_list=identity,
        separator=",",
        cast=float,
    )

    power = Instrument.measurement(
        "MEAS:POW?",
        "Measure output power in W",
    )

    power_statistics = Instrument.measurement(
        "MEAS:POW:STAT?",
        "Measure power statistics: [MIN, MAX, AVG]",
        get_process_list=identity,
        separator=",",
        cast=float,
    )

    energy = Instrument.measurement(
        "MEAS:ENER?",
        "Measure consumed energy. Unit defined in MEAS:ENER:UNIT",
    )

    energy_unit = Instrument.control(
        "MEAS:ENER:UNIT?",
        "MEAS:ENER:UNIT %s",
        "Control energy unit: either Wh or Ws",
        validator=strict_discrete_set,
        values={"Ws": "WS", "Wh": "WH"},
        map_values=True,
    )

    statistics_count = Instrument.measurement(
        "MEAS:STAT:COUNT?",
        "Measure number of samples for statistics",
    )

    def reset_statistics(self):
        """Clear statistics sample buffer"""
        self.write("MEAS:STAT:RESET")


    # --- Output commands ---
    output_enabled = Instrument.control(
        "OUTP?",
        "OUTP %d",
        "Control the output on or off or check the output status.",
        validator=strict_discrete_set,
        values={True: 1, False: 0},
        map_values=True,
    )

    output_mode = Instrument.control(
        "OUTP:MODE?",
        "OUTP:MODE %s",
        "Control the device output mode to SINK, SOURCE or AUTO (default)",
        validator=strict_discrete_set,
        values=["AUTO", "SINK", "SOURCE"]
    )

    output_delay = Instrument.control(
        "OUTP:DEL:DUR?",
        "OUTP:DEL:DUR %f",
        "Control the output delay duration in seconds",
        validator=strict_range,
        values=[0.001, 10.0],
    )

    output_delay_enabled = Instrument.control(
        "OUTP:DEL?",
        "OUTP:DEL %d",
        "Control the output delay unit",
        validator=strict_discrete_set,
        values={True: 1, False: 0},
        map_values=True,
    )

    output_ftr_enabled = Instrument.control(
        "OUTP:FTR?",
        "OUTP:FTR %d",
        "Control the output fast transient response",
        validator=strict_discrete_set,
        values={True: 1, False: 0},
        map_values=True,
    )

    output_capacitance = Instrument.control(
        "OUTP:MODE:CAP?",
        "OUTP:MODE:CAP %s",
        "Control the device output capacitance mode",
        validator=strict_discrete_set,
        values=["OFF", "LOW", "HIGH"]
    )

    output_trigger = Instrument.control(
        "OUTP:TRIG:BEH?",
        "OUTP:TRIG:BEH %s",
        "Control the output trigger mode",
        validator=strict_discrete_set,
        values=["ON", "OFF", "GATED"]
    )

    output_trigger_enabled = Instrument.control(
        "OUTP:TRIG?",
        "OUTP:TRIG %d",
        "Control external trigger for output",
        validator=strict_discrete_set,
        values={True: 1, False: 0},
        map_values=True,
    )

    # Arbitrary Sequence Commands ---------------------------------------------
    '''
    def clear_sequence(self, channel):
        """Clear the sequence of the selected channel."""
        channel = strict_discrete_set(channel, [1, 2, 3, 4])
        self.write(f"ARB:CLEAR {channel}")

    sequence = Instrument.setting(
        "ARB:DATA %s",
        "Set sequence of triplets of voltage (V), current (A) and dwell "
        "time (s).",
        set_process=process_sequence,
    )

    repetitions = Instrument.control(
        "ARB:REP?",
        "ARB:REP %s",
        "Control umber of repetitions (0...255). If 0 is entered, the sequence is"
        "repeated indefinitely.",
        validator=strict_discrete_set,
        values=range(256),
        cast=int,
    )

    def load_sequence(self, slot):
        """Load a saved waveform from internal memory (slot 1, 2 or 3)."""
        slot = strict_discrete_set(slot, [1, 2, 3])
        self.write(f"ARB:REST {slot}")

    def save_sequence(self, slot):
        """
        Save the sequence defined in the sequence property to internal memory
        (slot 1, 2 or 3).
        """
        slot = strict_discrete_set(slot, [1, 2, 3])
        self.write(f"ARB:SAVE {slot}")

    def start_sequence(self, channel):
        """Start the sequence of the selected channel."""
        channel = strict_discrete_set(channel, [1, 2, 3, 4])
        self.write(f"ARB:START {channel}")

    def stop_sequence(self, channel):
        """Stop the sequence defined in the sequence property of the selected
        channel."""
        channel = strict_discrete_set(channel, [1, 2, 3, 4])
        self.write(f"ARB:STOP {channel}")

    def transfer_sequence(self, channel):
        """
        Transfer the sequence defined in the sequence property to the selected
        channel.
        """
        channel = strict_discrete_set(channel, [1, 2, 3, 4])
        self.write(f"ARB:TRAN {channel}")
    '''


class NGUUnipolarMixin(CommonBase):
    def _update_voltage_validator_range(self, value):
        self.voltage_setpoint_values = [0.0, float(value)]
        return value

    def _update_current_validator_range(self, value):
        self.current_setpoint_values = [0.0, float(value)]
        return value


class NGUBipolarMixin(CommonBase):
    def _update_voltage_validator_range(self, value):
        mode = self.priority_mode
        if mode == "voltage":
            self.voltage_setpoint_values = [-float(value), float(value)]
        elif mode == "current":
            self.voltage_setpoint_values = [0.0, float(value)]
        else:
            raise ValueError("No output priority mode configured")
        self.negative_voltage_setpoint_values = [-float(value), 0.0]
        return value

    def _update_current_validator_range(self, value):
        mode = self.priority_mode
        if mode == "current":
            self.current_setpoint_values = [-float(value), float(value)]
        elif mode == "voltage":
            self.current_setpoint_values = [0.0, float(value)]
        else:
            raise ValueError("No output priority mode configured")
        self.negative_current_setpoint_values = [-float(value), 0.0]
        return value

    negative_voltage_setpoint = Instrument.control(
        "SOUR:VOLT:NEG?",
        "SOUR:VOLT:NEG %g",
        "Control the negative output voltage setpoint",
        validator=strict_range,
        check_set_errors=True,
        dynamic=True,
    )

    negative_current_setpoint = Instrument.control(
        "SOUR:CURR:NEG?",
        "SOUR:CURR:NEG %g",
        "Control the negative output current setpoint",
        validator=strict_range,
        check_set_errors=True,
        dynamic=True,
    )

class NGUConstantResistanceMixin(CommonBase):
    resistance_setpoint = Instrument.control(
        "SOUR:RES?",
        "SOUR:RES %g",
        "Control load resistance in constant resistance mode",
        validator=strict_range,
        values=[0.0, 1.0E4],
    )

    resistance_enabled = Instrument.control(
        "SOUR:RES:STAT?",
        "SOUR:RES:STAT %d",
        "Control constant load resistance mode",
        validator=strict_discrete_set,
        values={True: 1, False:0},
        map_values=True,
    )

class NGUModulationInputMixin(CommonBase):
    modulation_enabled = Instrument.control(
        "SOUR:MOD?",
        "SOUR:MOD %d",
        "Enable output modulation by modulation input voltage",
        validator=strict_discrete_set,
        values={True: 1, False:0},
        map_values=True,
    )

    modulation_gain = Instrument.control(
        "SOUR:MOD:GAIN?",
        "SOUR:RES:GAIN %f",
        "Control gain of modulation input signal",
        validator=strict_discrete_set,
        values=[0.5, 1.0, 2.0],
    )

class NGU201(NGUBaseClass, NGUUnipolarMixin, NGUConstantResistanceMixin):
    DEFAULT_NAME = "NGU201"
    SOURCE_VOLTAGE_RANGES = [20.0, 6.0]
    SOURCE_CURRENT_RANGES = [8.0, 3.0, 0.1, 0.01]


class NGU401(NGUBaseClass, NGUBipolarMixin, NGUModulationInputMixin):
    DEFAULT_NAME = "NGU401"
    SOURCE_VOLTAGE_RANGES = [20.0, 6.0]
    SOURCE_CURRENT_RANGES = [8.0, 3.0, 0.1, 0.01]


class NGU411(NGUBaseClass, NGUBipolarMixin, NGUModulationInputMixin):
    DEFAULT_NAME = "NGU411"
    SOURCE_VOLTAGE_RANGES = [20.0, 6.0]
    SOURCE_CURRENT_RANGES = [2.0, 0.1, 0.01]
