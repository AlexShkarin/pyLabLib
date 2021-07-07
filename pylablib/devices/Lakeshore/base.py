from ...core.devio import SCPI, interface, comm_backend

import numpy as np
import collections


class LakeshoreError(comm_backend.DeviceError):
    """Generic Lakeshore devices error"""
class LakeshoreBackendError(LakeshoreError,comm_backend.DeviceBackendError):
    """Generic Lakeshore backend communication error"""

TLakeshore218AnalogSettings=collections.namedtuple("TLakeshore218AnalogSettings",["bipolar","mode","channel","source","high_value","low_value","man_value"])
TLakeshore218FilterSettings=collections.namedtuple("TLakeshore218FilterSettings",["enabled","points","window"])
TLakeshore218CurveHeader=collections.namedtuple("TLakeshore218CurveHeader",["name","serial","fmt","limit","coeff"])
class Lakeshore218(SCPI.SCPIDevice):
    """
    Lakeshore 218 temperature controller.

    The channels are enumerated from 1 to 8 and are split into 2 groups: ``"A"`` for 1-4 and ``"B"`` for 5-8.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    _default_write_sync=True
    Error=LakeshoreError
    ReraiseError=LakeshoreBackendError
    _nchannels=8
    def __init__(self, conn):
        SCPI.SCPIDevice.__init__(self,conn,backend="serial",term_write="\r\n",term_read="\r\n",backend_defaults={"serial":("COM1",9600,7,'E',1)})
        channels=range(1,self._nchannels+1)
        self._add_settings_variable("enabled",self.is_enabled,self.set_enabled,mux=(channels,0))
        self._add_settings_variable("sensor_type",self.get_sensor_type,self.set_sensor_type,mux=("AB",0))
        self._add_settings_variable("sensor_curve_index",self.get_sensor_curve_index,self.set_sensor_curve_index,mux=(channels,0))
        self._add_status_variable("temperature",self.get_all_temperatures)
        self._add_status_variable("sensor_reading",self.get_all_sensor_readings,priority=-1)
        self._add_status_variable("analog_output",self.get_analog_output,mux=((1,2),))
        self._add_settings_variable("analog_output_settings",self.get_analog_output_settings,self.setup_analog_output,priority=-3,mux=((1,2),0))
        self._add_settings_variable("filter_settings",self.get_filter_settings,self.setup_filter,priority=-3,mux=(channels,0))
        try:
            self.get_id(timeout=2.)
        except self.instr.Error:
            self.close()
            raise
    _float_fmt="{:.3f}"

    _p_channel=interface.RangeParameterClass("channel",1,_nchannels)
    @interface.use_parameters
    def is_enabled(self, channel):
        """Check if a given channel is enabled"""
        return self.ask("INPUT? {}".format(channel),"bool")
    @interface.use_parameters
    def set_enabled(self, channel, enabled=True):
        """Enable or disable a given channel"""
        self.write("INPUT {} {}".format(channel, 1 if enabled else 0))
        return self.is_enabled(channel)
    
    _p_group=interface.EnumParameterClass("group",["A","B"])
    _p_sensor_type=interface.EnumParameterClass("sensor_type",{"diode_2.5":0,"diode_7.5":1,"plat_250":2,"plat_500":3,"plat_5k":4,"cernox":5})
    @interface.use_parameters
    def get_sensor_type(self, group):
        """
        Get sensor type for a given group (``"A"`` for sensors 1-4 or ``"B"`` for sensors 5-8).

        For types, see ``INTYPE`` command description in the Lakeshore 218 programming manual.
        """
        return self.ask("INTYPE? {}".format(group),"int")
    @interface.use_parameters
    def set_sensor_type(self, group, sensor_type):
        """
        Set sensor type for a given group (``"A"`` for sensors 1-4 or ``"B"`` for sensors 5-8).

        For types, see ``INTYPE`` command description in the Lakeshore 218 programming manual.
        """
        self.write("INTYPE",[group,sensor_type])
        self.wait_dev()
        return self._wip.get_sensor_type(group)
    
    @interface.use_parameters
    def get_sensor_curve_index(self, channel):
        """
        Get sensor curve index for a given channel (1 to 8).
        
        For curve descriptions, see ``INCRV`` command description in the Lakeshore 218 programming manual.
        """
        return self.ask("INCRV? {}".format(channel),"int")
    @interface.use_parameters
    def set_sensor_curve_index(self, channel, index):
        """
        Get sensor curve index for a given channel (1 to 8).
        
        For curve descriptions, see ``INCRV`` command description in the Lakeshore 218 programming manual.
        """
        self.write("INCRV",[channel,index])
        self.wait_dev()
        return self._wip.get_sensor_curve_index(channel)
    
    _p_curve_format=interface.EnumParameterClass("curve_format",{"volt_k":2,"ohm_k":3,"logohm_k":4})
    _p_curve_coeff=interface.EnumParameterClass("curve_coeff",{"neg":1,"pos":2})
    @interface.use_parameters(_returns=(None,None,"curve_format",None,"curve_coeff"))
    def get_curve_header(self, index):
        """
        Get header of a given curve (1-9 or 21-28).

        Return tuple ``(name, serial, fmt, limit, coeff)``.
        For values descriptions, see ``CRVHDR`` command description in the Lakeshore 218 programming manual.
        """
        return TLakeshore218CurveHeader(*self.ask("CRVHDR? {}".format(index),["string","string","int","float","int"]))
    @interface.use_parameters(fmt="curve_format",coeff="curve_coeff")
    def set_curve_header(self, index, name=None, serial=None, fmt=None, limit=None, coeff=None):
        """
        Set header of a given user curve (21-28).

        For values descriptions, see ``CRVHDR`` command description in the Lakeshore 218 programming manual.
        """
        cheader=tuple(self._wap.get_curve_header(index))
        header=[(cv if nv is None else nv) for cv,nv in zip(cheader,[name,serial,fmt,limit,coeff])]
        self.write("CRVHDR",[index]+header,["int","string","string","int","float","int"])
        return self._wip.get_curve_header(index)
    def get_curve(self, index, trim_zeros=True):
        """
        Get values of a given curve (1-9 or 21-28).

        Return 2-column numpy array with up to 200 points, where the first column is sensor reading, and the second is temperature;
        for associated sensor units, see :meth:`get_curve_header`.
        If ``trim_zeros==True``, trim the trailing zero-valued points.
        Note, that it takes about 10 seconds to complete.
        """
        curve_pts=200
        curve=[self.ask("CRVPT? {} {}".format(index,i),["float","float"]) for i in range(1,curve_pts+1)]
        curve=np.array(curve)
        if trim_zeros:
            for tl in range(curve_pts-1,-1,-1):
                if np.any(curve[tl]!=0):
                    break
            curve=curve[:tl]
        return curve
    def set_curve(self, index, curve):
        """
        Set values of a given user curve (21-28).

        `curve` is a 2-column numpy array with up to 200 points, where the first column is sensor reading, and the second is temperature;
        for associated sensor units, see :meth:`get_curve_header`.
        Note, that it takes about 20 seconds to complete.
        """
        curve=list(curve)[:200]
        curve+=[(0,0)]*(200-len(curve))
        for i,(s,t) in enumerate(curve):
            self.write("CRVPT",[index,i+1,s,t],["int","int","float","float"])
        return self.get_curve(index)
    
    @interface.use_parameters
    def get_temperature(self, channel):
        """Get readings (in Kelvin) on a given channel (1 to 8)"""
        return self.ask("KRDG? {}".format(channel),"float")
    def get_all_temperatures(self):
        """Get readings (in Kelvin) on all channels"""
        data=self.ask("KRDG? 0")
        return [float(x.strip()) for x in data.split(",")]
    
    @interface.use_parameters
    def get_sensor_reading(self, channel):
        """Get readings (in sensor units) on a given channel (1 to 8)"""
        return self.ask("SRDG? {}".format(channel),"float")
    def get_all_sensor_readings(self):
        """Get readings (in sensor units) on all channels"""
        data=self.ask("SRDG? 0")
        return [float(x.strip()) for x in data.split(",")]

    _p_output=interface.RangeParameterClass("output",1,2)
    _p_output_mode=interface.EnumParameterClass("output_mode",{"off":0,"input":1,"manual":2})
    _p_source=interface.EnumParameterClass("source",{"kelvin":1,"celsius":2,"sensor":3,"linear":4})
    @interface.use_parameters(_returns=(None,"output_mode",None,"source",None,None,None))
    def get_analog_output_settings(self, output):
        """
        Get analog output settings for a given output (1 or 2).

        For parameters, see :meth:`setup_analog_output` and ``ANALOG`` command description in the Lakeshore 218 programming manual.
        """
        values=self.ask("ANALOG? {}".format(output),["bool","int","int","int","float","float","float"])
        return TLakeshore218AnalogSettings(*values)
    @interface.use_parameters(mode="output_mode")
    def setup_analog_output(self, output, bipolar=None, mode=None, channel=None, source=None, high_value=None, low_value=None, man_value=None):
        """
        Setup analog output settings for a given output (1 or 2).

        For parameters, see ``ANALOG`` command description in the Lakeshore 218 programming manual.
        Value of ``None`` means keeping the current parameter value.
        """
        current=self._wap.get_analog_output_settings(output)
        value=[c if v is None else v for c,v in zip(current,[bipolar,mode,channel,source,high_value,low_value,man_value])]
        self.write("ANALOG",[output]+value)
        return self._wip.get_analog_output_settings(output)
    def set_analog_output_value(self, output, value, bipolar=False, enabled=True):
        """
        Set manual analog output value.

        A simplified version of :meth:`setup_analog_output`.
        """
        if not enabled:
            self.setup_analog_output(output,mode="off")
        else:
            self.setup_analog_output(output,bipolar=bipolar,mode="manual",man_value=value)
        return self.get_analog_output(output)
    @interface.use_parameters
    def get_analog_output(self, output):
        """Get value (in percents of the total range) at a given output (1 or 2)"""
        return self.ask("AOUT? {}".format(output),"float")

    @interface.use_parameters
    def get_filter_settings(self, channel):
        """
        Get input filter settings for a given channel (1 to 8).

        For parameters, see :meth:`setup_filter` and ``FILTER`` command description in the Lakeshore 218 programming manual.
        """
        values=self.ask("FILTER? {}".format(channel),["bool","int","int"])
        return TLakeshore218FilterSettings(*values)
    @interface.use_parameters
    def setup_filter(self, channel, enabled=None, points=None, window=None):
        """
        Setup input filter settings for a given channel (1 to 8).

        For parameters, see ``FILTER`` command description in the Lakeshore 218 programming manual.
        Value of ``None`` means keeping the current parameter value.
        """
        current=self._wip.get_filter_settings(channel)
        value=[c if v is None else v for c,v in zip(current,[enabled,points,window])]
        self.write("FILTER",[channel]+value)
        return self._wip.get_filter_settings(channel)




TLakeshore370RangeSettings=collections.namedtuple("TLakeshore370RangeSettings",["exc_mode","exc_range","res_range","autorange","enable"])
TLakeshore370AnalogSettings=collections.namedtuple("TLakeshore370AnalogSettings",["bipolar","mode","channel","source","high_value","low_value","man_value"])
TLakeshore370FilterSettings=collections.namedtuple("TLakeshore370FilterSettings",["enabled","settle_time","window"])
class Lakeshore370(SCPI.SCPIDevice):  # TODO: finish / check
    """
    Lakeshore 370 resistance bridge / temperature controller.

    All channels are enumerated from 0.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=LakeshoreError
    ReraiseError=LakeshoreBackendError
    _nchannels=16
    def __init__(self, conn):
        SCPI.SCPIDevice.__init__(self,conn,backend="serial",term_write="\r\n",term_read="\r\n",backend_defaults={"serial":("COM1",9600,7,'E',1)})
        channels=range(1,self._nchannels+1)
        self._add_status_variable("analog_output",self.get_analog_output,mux=((1,2),))
        self._add_settings_variable("analog_output_settings",self.get_analog_output_settings,self.setup_analog_output,priority=-3,mux=((1,2),0))
        self._add_settings_variable("filter_settings",self.get_filter_settings,self.setup_filter,priority=-3,mux=(channels,0))
        try:
            self.get_id(timeout=2.)
        except self.instr.Error:
            self.close()
            raise
    
    _p_channel=interface.RangeParameterClass("channel",1,_nchannels)
    @interface.use_parameters
    def get_temperature(self, channel):
        """Get temperature readings (in K) on a given channel"""
        return self.ask("RDGR? {:2d}".format(channel),"float")
    @interface.use_parameters
    def get_resistance(self, channel):
        """Get resistance readings (in Ohm) on a given channel"""
        return self.ask("RDGR? {:2d}".format(channel),"float")
    @interface.use_parameters
    def get_sensor_power(self, channel):
        """Get dissipated power (in W) on a given channel"""
        return self.ask("RDGPWR? {:2d}".format(channel),"float")
    
    def select_channel(self, channel):
        """Select measurement channel"""
        self.write("SCAN {:2d},0".format(channel))
    def get_channel(self):
        """Get current measurement channel"""
        return int(self.ask("SCAN?").split(",")[0].strip())

    _p_excitation_mode=interface.RangeParameterClass("excitation_mode",{"v":0,"i":1})
    @interface.use_parameters(_returns=("exc_mode",None,None,None,None))
    def get_channel_range_settings(self, channel):
        """
        Setup the current measurement channel range parameters.

        For parameters, see :meth:`setup_channel_range` and ``RDGRNG`` command description in the Lakeshore 370 programming manual.
        """
        values=self.ask("RDGRNG? {:2d}".format(channel),["int","int","int","bool","bool"])
        return TLakeshore370RangeSettings(*values)
    @interface.use_parameters(exc_mode="excitation_mode")
    def setup_channel_range(self, channel=None, exc_mode="v", exc_range=1, res_range=22, autorange=True, enable=True):
        """
        Setup the measurement channel range (all channels by default).

        `exc_mode` is the excitation mode (``"i"`` or ``"v"``), `exc_range` is the excitation range (1 is smallest), `res_range` is the resistance range (1 is smallest).
        For range descriptions, see Lakeshore 370 programming manual.
        """
        channel=0 if channel is None else channel
        autorange=1 if autorange else 0
        cs_off=0 if enable else 1
        self.write("RDGRNG",[channel,exc_mode,exc_range,res_range,autorange,cs_off])
        return self._wip.get_channel_range_settings(channel or 1)
    
    # def setup_heater_openloop(self, heater_range, heater_percent, heater_res=100.):
    #     """
    #     Setup a heater in the open loop mode.

    #     `heater_range` is the heating range, `heater_percent` is the excitation percentage within the range, `heater_res` is the heater resistance (in Ohm).
    #     For range descriptions, see Lakeshore 370 programming manual.
    #     """
    #     self.write("CMODE 3")
    #     self.write("CSET 1,0,1,25,1,{},{:f}".format(heater_range,heater_res))
    #     self.write("HTRRNG {}".format(heater_range))
    #     self.write("MOUT {:f}".format(heater_percent))
    # def get_heater_settings_openloop(self):
    #     """
    #     Get heater settings in the open loop mode.

    #     Return tuple ``(heater_range, heater_percent, heater_res)``, where `heater_range` is the heating range,
    #     `heater_percent` is the excitation percentage within the range, `heater_res` is the heater resistance (in Ohm).
    #     For range descriptions, see Lakeshore 370 programming manual.
    #     """
    #     cset_reply=[s.strip() for s in self.ask("CSET?").split(",")]
    #     heater_percent=self.ask("MOUT?","float")
    #     heater_range=self.ask("HTRRNG?","int")
    #     #return int(cset_reply[5]),heater_percent,float(cset_reply[6])
    #     return heater_range,heater_percent,float(cset_reply[6])
    
    _p_output=interface.RangeParameterClass("output",1,2)
    _p_output_mode=interface.EnumParameterClass("output_mode",{"off":0,"input":1,"manual":2,"zone":3,"still":4})
    _p_source=interface.EnumParameterClass("source",{"kelvin":1,"ohm":2,"linear":3})
    @interface.use_parameters(_returns=(None,"output_mode",None,"source",None,None,None))
    def get_analog_output_settings(self, output):
        """
        Get analog output settings for a given output (1 or 2).

        For parameters, see :meth:`setup_analog_output` and ``ANALOG`` command description in the Lakeshore 370 programming manual.
        """
        values=self.ask("ANALOG? {}".format(output),["bool","int","int","int","float","float","float"])
        return TLakeshore370AnalogSettings(*values)
    @interface.use_parameters(mode="output_mode")
    def setup_analog_output(self, output, bipolar=None, mode=None, channel=None, source=None, high_value=None, low_value=None, man_value=None):
        """
        Setup analog output settings for a given output (1 or 2).

        For parameters, see ``ANALOG`` command description in the Lakeshore 370 programming manual.
        Value of ``None`` means keeping the current parameter value.
        """
        current=self._wap.get_analog_output_settings(output)
        value=[c if v is None else v for c,v in zip(current,[bipolar,mode,channel,source,high_value,low_value,man_value])]
        self.write("ANALOG",[output]+value)
        return self._wip.get_analog_output_settings(output)
    def set_analog_output_value(self, output, value, bipolar=False, enabled=True):
        """
        Set manual analog output value.

        A simplified version of :meth:`setup_analog_output`.
        """
        if not enabled:
            self.setup_analog_output(output,mode="off")
        else:
            self.setup_analog_output(output,bipolar=bipolar,mode="manual",man_value=value)
        return self.get_analog_output(output)
    @interface.use_parameters
    def get_analog_output(self, output):
        """Get value (in percents of the total range) at a given output (1 or 2)"""
        return self.ask("AOUT? {}".format(output),"float")

    @interface.use_parameters
    def get_filter_settings(self, channel):
        """
        Get input filter settings for a given channel (1 to 16).

        For parameters, see :meth:`setup_filter` and ``FILTER`` command description in the Lakeshore 370 programming manual.
        """
        values=self.ask("FILTER? {}".format(channel),["bool","int","int"])
        return TLakeshore370FilterSettings(*values)
    @interface.use_parameters
    def setup_filter(self, channel, enabled=None, settle_time=None, window=None):
        """
        Setup input filter settings for a given channel (1 to 16).

        For parameters, see ``FILTER`` command description in the Lakeshore 370 programming manual.
        Value of ``None`` means keeping the current parameter value.
        """
        current=self._wip.get_filter_settings(channel)
        value=[c if v is None else v for c,v in zip(current,[enabled,settle_time,window])]
        self.write("FILTER",[channel]+value)
        return self._wip.get_filter_settings(channel)