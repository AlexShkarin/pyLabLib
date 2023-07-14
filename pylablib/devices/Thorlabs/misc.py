from ...core.devio import SCPI, interface
from ...core.utils import funcargparse
from .base import ThorlabsError, ThorlabsBackendError

import collections

TPMDeviceInfo=collections.namedtuple("TPMDeviceInfo",["manufacturer","name","serial","firmware"])
TPMSensorInfo=collections.namedtuple("TPMSensorInfo",["name","serial","calibration","type","subtype","flags"])
class GenericPM(SCPI.SCPIDevice):
    """
    Generic Thorlabs optical Power Meter.

    Args:
        addr: connection address (usually, a VISA connection string or a COM port for bluetooth devices)
    """
    Error=ThorlabsError
    ReraiseError=ThorlabsBackendError
    def __init__(self, addr):
        super().__init__(addr,backend_defaults={"serial":("COM1",115200)})
        with self._close_on_error():
            self.flush()
            self.write("INIT")
            self.update_sensor_modes()
        self._add_info_variable("device_info",self.get_device_info)
        self._add_info_variable("sensor_info",self.get_sensor_info)
        self._add_info_variable("supported_modes",self.get_supported_sensor_modes)
        self._add_settings_variable("mode",self.get_sensor_mode,self.set_sensor_mode)
        self._add_settings_variable("autorange",self.is_autorange_enabled,self.enable_autorange)
        self._add_status_variable("range",self.get_range)
        self._add_info_variable("wavelength_range",self.get_wavelength_range)
        self._add_settings_variable("wavelength",self.get_wavelength,self.set_wavelength)
        self._add_status_variable("reading",self.get_reading)
    
    def open(self):
        super().open()
        self.flush()
    def get_device_info(self):
        """
        Get device info.

        Return tuple ``(manufacturer, name, serial, firmware)``.
        """
        info=self.ask("*IDN?",["string"]*4)
        return TPMDeviceInfo(*info)
    _sensor_flags=[("power",1),("energy",2),("response_set",16),("wavelength_set",32),("tau_set",64),("temp_sens",256)]
    def get_sensor_info(self):
        """
        Get sensor info.

        Return tuple ``(name, serial, calibration, type, subtype, flags)``.
        For devices with integrated sensors (e.g., PM160) the sensor name is the same as the device name.
        """
        info=self.ask(":SYST:SENS:IDN?",["string","string","string","int","int","int"])
        flags=tuple([n for (n,v) in self._sensor_flags if info[-1]&v])
        return TPMSensorInfo(info[0],info[1],info[2],info[3],info[4],flags)
    
    def _enumerate_sensor_modes(self):
        return [(m,c) for (m,c) in self._all_sensor_modes.items() if self._is_command_valid(":SENSE:{}:RANGE?".format(c),cached=False)]
    def update_sensor_modes(self):
        """Update the list of supported sensor modes (only makes sense if the sensor has been changed since the connection was opened)"""
        self._sensor_modes=self._enumerate_sensor_modes()
    _all_sensor_modes={"power":"POW","energy":"ENER","voltage":"VOLT","current":"CURR","frequency":"FREQ"}
    _p_sensor_mode=interface.EnumParameterClass("sensor_mode",_all_sensor_modes,value_case="upper")
    def get_supported_sensor_modes(self):
        """
        Get a list of supported sensor modes.

        Can contain ``"power"``, ``"energy"``, ``"voltage"``, ``"current"``, or ``"frequency"``.
        """
        return [m for m,_ in self._sensor_modes]
    def _check_sensor_mode(self, sensor_mode):
        if sensor_mode.upper() not in [c for _,c in self._sensor_modes]:
            raise ThorlabsError("mode '{}' is not available with this device; available modes are {}".format(sensor_mode,self._sensor_modes))

    @interface.use_parameters(_returns="sensor_mode")
    def get_sensor_mode(self):
        """
        Get current sensor mode.

        Can be ``"power"``, ``"energy"``, ``"voltage"``, ``"current"``, or ``"frequency"``.
        """
        return self.ask(":CONF?")
    @interface.use_parameters
    def set_sensor_mode(self, sensor_mode="power"):
        """
        Set current sensor mode.

        Can be one of the modes returned by :meth:`get_supported_sensor_modes`.
        """
        self._check_sensor_mode(sensor_mode)
        self.write(":CONF:{}".format(sensor_mode.upper()))
        return self.get_sensor_mode()
    
    @interface.use_parameters
    def is_autorange_enabled(self, sensor_mode=None):
        """
        Check if autorange is enabled for the given sensor mode.

        If `sensor_mode` is ``None``, return value for the current sensor mode.
        """
        if sensor_mode is None:
            sensor_mode=self._wop.get_sensor_mode()
        return self.ask(":SENS:{}:RANG:AUTO?".format(sensor_mode),"bool")
    def enable_autorange(self, enable=True, sensor_mode=None):
        """
        Enable or disable autorange for the given sensor mode.

        If `sensor_mode` is ``None``, set value for the current sensor mode.
        """
        if sensor_mode is None:
            sensor_mode=self._wop.get_sensor_mode()
        self.write(":SENS:{}:RANG:AUTO".format(sensor_mode),enable,"bool")
        return self._wip.is_autorange_enabled(sensor_mode)
    
    @interface.use_parameters
    def get_range(self, sensor_mode=None):
        """
        Get measurement range for the given sensor mode.

        If `sensor_mode` is ``None``, return value for the current sensor mode.
        """
        if sensor_mode is None:
            sensor_mode=self._wop.get_sensor_mode()
        return self.ask(":SENS:{}:RANG?".format(sensor_mode),"float")
    @interface.use_parameters
    def set_range(self, rng=None, sensor_mode=None):
        """
        Set measurement range for the given sensor mode.

        If `rng` is ``None`` or ``"full"``, set the maximal range.
        If `sensor_mode` is ``None``, return value for the current sensor mode.
        """
        if sensor_mode is None:
            sensor_mode=self._wop.get_sensor_mode()
        if rng is None or rng=="full":
            rng=self.ask(":SENS:{}:RANG? MAX".format(sensor_mode),"float")*.99
        self.write(":SENS:{}:RANG".format(sensor_mode),rng,"float")
        return self._wip.get_range(sensor_mode)
    
    def get_wavelength(self):
        """Get current wavelength (in nm)"""
        return self.ask(":SENS:CORR:WAV?","float")*1E-9
    def get_wavelength_range(self):
        """Get available wavelength range (in nm)"""
        return (self.ask(":SENS:CORR:WAV? MIN","float")*1E-9,self.ask(":SENS:CORR:WAV? MAX","float")*1E-9)
    def set_wavelength(self, wavelength):
        """Set current wavelength (in nm)"""
        self.write(":SENS:CORR:WAV",wavelength*1E9,"float")
        return self.get_wavelength()
    
    _overrng_threshold=1E12
    def get_reading(self, sensor_mode=None, measure=True, overrng="keep"):
        """
        Get the reading in a given mode.

        If `sensor_mode` is ``None``, return reading in the currently set up mode (:meth:`get_sensor_mode`); otherwise, set the sensor mode to the requested one.
        If ``measure==True``, initiate a new measurement; otherwise, return the last measured value.
        `overrng` describes behavior if the power readings are outside of the current range;
        can be ``"keep"`` (keep the default device behavior, which returns a very large number, about 9.9E37),
        ``"error"`` (raise an error), or ``"max"`` (trim to the maximal value for the current range).
        """
        funcargparse.check_parameter_range(overrng,"overrng",["keep","max","error"])
        if sensor_mode is not None:
            self.set_sensor_mode(sensor_mode)
        comm=":READ?" if measure else ":FETCH?"
        value=self.ask(comm,"float")
        if overrng!="keep" and value>=self._overrng_threshold:
            if overrng=="error":
                raise ThorlabsError("the value is higher than the measurement range")
            value=self._wip.get_range(sensor_mode=sensor_mode)
        return value

    def get_power(self):
        """Measure and return the optical power"""
        return self.get_reading(sensor_mode="power")




class PM160(GenericPM):
    """
    Thorlabs PM160 optical Power Meter.

    Args:
        addr: connection address (usually, a VISA connection string or a COM port for bluetooth devices)
    """