# from ...core.devio import SCPI, interface
# from .base import ThorlabsError, ThorlabsBackendError

# import collections

# TPM100DeviceInfo=collections.namedtuple("TPM100DeviceInfo",["name","serial","firmware"])
# TPM100SensorInfo=collections.namedtuple("TPM100SensorInfo",["name","serial","calibration","type","subtype","flags"])
# class PM100(SCPI.SCPIDevice):
#     """
#     Thorlabs PM100 optical Power Meter.

#     Args:
#         addr: connection address (usually, a VISA connection string)
#     """
#     Error=ThorlabsError
#     ReraiseError=ThorlabsBackendError
#     def __init__(self, addr):
#         SCPI.SCPIDevice.__init__(self,addr)
#         self._sensor_modes=self._check_sensor_modes()
#         self._add_info_variable("device_info",self.get_device_info)
#         self._add_info_variable("sensor_info",self.get_sensor_info)
#         self._add_info_variable("supported_modes",self.get_supported_sensor_modes)
#         self._add_status_variable("mode",self.get_sensor_mode,self.set_sensor_mode)
#         def mode_func(mode):
#             return lambda: self.get_reading(sensor_mode=mode)
#         for mode in self._sensor_modes:
#             self._add_status_variable("reading/{}".format(mode),mode_func(mode))
    
#     def get_device_info(self):
#         """
#         Get device info.

#         Return tuple ``(name, serial, firmware)``.
#         """
#         info=self.ask("*IDN?",["string"]*4)
#         return TPM100DeviceInfo(*info[1:])
#     _sensor_flags=[("power",1),("energy",2),("response_set",16),("wavelength_set",32),("tau_set",64),("temp_sens",256)]
#     def get_sensor_info(self):
#         """
#         Get sensor info.

#         Return tuple ``(name, serial, calibration, type, subtype, flags)``.
#         For devices with integrated sensors (e.g., PM160) the sensor name is the same as the device name.
#         """
#         info=self.ask(":SYSTEM:SENSOR:IDN?",["string","string","string","int","int","int"])
#         flags=tuple([n for (n,v) in self._sensor_flags if info[-1]&v])
#         return TPM100SensorInfo(info[0],info[1],info[2],info[3],info[4],flags)
    
#     def _check_sensor_modes(self):
#         return [m for m in self._all_sensor_modes if self._is_command_valid(":SENSE:{}:RANGE?".format(m.upper()),cached=False)]
#     # def update_sensor_modes(self):
#     #     self._sensor_modes=self._check_sensor_modes()
#     _all_sensor_modes=["power","energy","voltage","current","frequency"]
#     _p_sensor_mode=interface.EnumParameterClass("sensor_mode",{"power":"POW","energy":"ENER","voltage":"VOLT","current":"CURR","frequency":"FREQ"},value_case="upper")
#     def get_supported_sensor_modes(self):
#         """
#         Get a list of supported sensor modes.

#         Can contain ``"power"``, ``"energy"``, ``"voltage"``, ``"current"``, or ``"frequency"``.
#         """
#         return self._sensor_modes
#     def _check_sensor_mode(self, sensor_mode):
#         if sensor_mode.lower() not in self._sensor_modes:
#             raise ValueError("mode '{}' is not available with this device; available modes are {}".format(sensor_mode,self._sensor_modes))

#     @interface.use_parameters(_returns="sensor_mode")
#     def get_sensor_mode(self):
#         """
#         Get current sensor mode.

#         Can be ``"power"``, ``"energy"``, ``"voltage"``, ``"current"``, or ``"frequency"``.
#         """
#         return self.ask(":CONFIGURE?")
#     @interface.use_parameters
#     def set_sensor_mode(self, sensor_mode="power"):
#         """
#         Set current sensor mode.

#         Can be one of the modes returned by :meth:`get_supported_sensor_modes`.
#         """
#         self._check_sensor_mode(sensor_mode)
#         self.write(":CONFIGURE:{}".format(sensor_mode.upper()))
#         return self.get_sensor_mode()
    
#     def get_reading(self, sensor_mode=None, measure=True):
#         """
#         Get the reading in a given mode.

#         If ``sensor_mode is None``, return reading in the currently set up mode (:meth:`get_sensor_mode`), which is a bit faster then setting a definite mode.
#         If ``measure==True``, initiate a new measurement; otherwise, return the last measured value.
#         """
#         if sensor_mode is not None:
#             self.set_sensor_mode(sensor_mode)
#         comm=":READ?" if measure else ":FETCH?"
#         return self.ask(comm,"float")

#     def get_power(self):
#         """Measure and return the optical power"""
#         return self.get_reading(sensor_mode="power")
