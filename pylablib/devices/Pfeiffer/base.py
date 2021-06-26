from ...core.utils import py3
from ...core.devio import comm_backend, interface

import collections



class PfeifferError(comm_backend.DeviceError):
    """Generic Pfeiffer device error"""
class PfeifferBackendError(PfeifferError,comm_backend.DeviceBackendError):
    """Generic Pfeiffer backend communication error"""



TTPG260SwitchSettings=collections.namedtuple("TTPG260SwitchSettings",["channel","low_thresh","high_thresh"])
TTPG260GaugeControlSettings=collections.namedtuple("TTPG260GaugeControlSettings",["activation_control","deactivation_control","on_thresh","off_thresh"])
class TPG260(comm_backend.ICommBackendWrapper):
    """
    TPG260 series (TPG261/262) pressure gauge.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=PfeifferError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="\r\n",term_write="",defaults={"serial":("COM1",9600)},reraise_error=PfeifferBackendError)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        gmux=([1,2],)
        smux=([1,2],1)
        self._add_status_variable("pressure",lambda channel: self.get_pressure(channel,status_error=False),ignore_error=(PfeifferError,),mux=gmux,priority=5)
        self._add_status_variable("channel_status",self.get_channel_status,mux=gmux,priority=5)
        self._add_status_variable("units",self.get_units)
        self._add_status_variable("enabled",self.is_enabled,priority=2)
        self._add_status_variable("switch_status",self.get_switch_status)
        self._add_info_variable("gauge_kind",self.get_gauge_kind,mux=gmux)
        self._add_settings_variable("display_channel",self.get_display_channel,self.set_display_channel)
        self._add_settings_variable("measurement_filter",self.get_measurement_filter,self.set_measurement_filter,mux=smux)
        self._add_settings_variable("calibration_factor",self.get_calibration_factor,self.set_calibration_factor,mux=smux,priority=-2)
        self._add_status_variable("switch_settings",self.get_switch_settings,mux=([1,2,3,4],),priority=-2)
        self._add_status_variable("gauge_control_settings",self.get_gauge_control_settings,mux=gmux,priority=-2)
        try:
            self.query("BAU")
        except self.instr.Error:
            self.close()
            raise
    
    def comm(self, msg):
        """Send a command to the device"""
        self.instr.write(msg+"\r\n")
        rsp=self.instr.readline()
        if len(rsp)==1:
            if rsp[:1]==b"\x15":
                raise PfeifferError("command '{}' resulted in negative acknowledgement from the device".format(msg))
            elif rsp[:1]==b"\x06":
                return
        raise PfeifferError("command '{}' resulted in an unexpected acknowledgement from the device: {}".format(msg,rsp))
    def _parse_value(self, value, data_type):
        if data_type in ["str","raw"]:
            return value
        if data_type=="int":
            return int(value)
        if data_type=="float":
            return float(value)
        raise ValueError("unrecognized data type: {}".format(data_type))
    def query(self, msg, data_type="str"):
        """Send a query to the device and return the reply"""
        self.comm(msg)
        self.instr.write(b"\05")
        res=py3.as_str(self.instr.readline())
        if data_type=="raw":
            return res
        res=[v.strip() for v in res.strip().split(",")]
        if not isinstance(data_type,(tuple,list)):
            data_type=[data_type]*len(res)
        if len(data_type)!=len(res):
            raise ValueError("supplied datatypes {} have different length from the results {}".format(data_type,res))
        res=[self._parse_value(v,dt) for (v,dt) in zip(res,data_type)]
        return res[0] if len(res)==1 else res

    _p_channel=interface.EnumParameterClass("channel",[1,2])
    _p_unit=interface.EnumParameterClass("units",{"mbar":0,"torr":1,"pa":2})
    @interface.use_parameters(_returns="units")
    def get_units(self):
        """Get device units for indication/reading (``"mbar"``, ``"torr"``, or ``"pa"``)"""
        return self.query("UNI","int")
    @interface.use_parameters(_returns="units")
    def set_units(self, units):
        """Set device units for indication/reading (``"mbar"``, ``"torr"``, or ``"pa"``)"""
        return self.query("UNI, {}".format(units),"int")
    def to_Pa(self, value, units=None):
        """
        Convert value in the given units to Pa.

        If `units` is ``None``, use the current display units.
        """
        units=units or self.get_units()
        conv_factor={"mbar":1E2,"torr":133.322,"pa":1}
        return value*conv_factor[units]
    def from_Pa(self, value, units=None):
        """
        Convert value in the given units from Pa.

        If `units` is ``None``, use the current display units.
        """
        units=units or self.get_units()
        conv_factor={"mbar":1E2,"torr":133.322,"pa":1}
        return value/conv_factor[units]
    def get_display_channel(self):
        """Get controller display channel"""
        return self.query("SCT","int")+1
    @interface.use_parameters
    def set_display_channel(self, channel=1):
        """Set controller display channel"""
        return self.query("SCT,{}".format(channel-1),"int")+1
    def get_display_resolution(self):
        """Get controller display resolution (number of digits)"""
        return self.query("DCD","int")
    def set_display_resolution(self, resolution=2):
        """Set controller display resolution (number of digits)"""
        return self.query("DCD,{}".format(resolution),"int")

    _p_gauge_enabled=interface.EnumParameterClass("gauge_enabled",{None:0,False:1,True:2})
    @interface.use_parameters(_returns="gauge_enabled")
    def is_enabled(self, channel=1):
        """
        Check if the gauge at the given channel is enabled.
        
        If the gauge cannot be turned on/off (e.g., not connected), return ``None``.
        """
        return self.query("SEN",["int","int"])[channel-1]
    @interface.use_parameters(_returns="gauge_enabled")
    def enable(self, enable=True, channel=1):
        """Enable or disable the gauge at the given channel"""
        vals=[0,0]
        vals[channel]=2 if enable else 1
        return self.query("SEN,{},{}".format(*vals),["int","int"])
    _p_gstat=interface.EnumParameterClass("gauge_status",{"ok":0,"under":1,"over":2,"sensor_error":3,"sensor_off":4,"no_sensor":5,"id_error":6})
    @interface.use_parameters(_returns="gauge_status")
    def get_channel_status(self, channel=1):
        """
        Get channel status.

        Can be ``"ok"``, ``"under"`` (underrange), ``"over"`` (overrange), ``"sensor_error"``, ``"sensor_off"``, ``"no_sensor"``, or ``"id_error"``.
        """
        return self.query("PR{}".format(channel),["int","float"])[0]
    @interface.use_parameters
    def get_pressure(self, channel=1, display_units=False, status_error=True):
        """
        Get pressure at a given channel.
        
        If ``display_units==False``, return result in Pa; otherwise, use display units obtained using :meth:`get_units`.
        If ``status_error==True`` and the channel status is not ``"ok"``, raise and error; otherwise, return ``None``.
        """
        stat,press=self.query("PR{}".format(channel),["int","float"])
        if stat!=0:
            if status_error:
                raise PfeifferError("pressure reading error: status {} ({})".format(stat,self._p_gstat.i(stat)))
            else:
                return None
        if not display_units:
            press=self.to_Pa(press)
        return press
    @interface.use_parameters
    def get_gauge_kind(self, channel=1):
        return self.query("TID",["str","str"])[channel-1]
    _p_filter=interface.EnumParameterClass("meas_filter",{"fast":0,"medium":1,"slow":2})
    @interface.use_parameters(_returns="meas_filter")
    def get_measurement_filter(self, channel=1):
        """Get gauge measurement filter (``"fast"``, ``"medium"``, or ``"slow"``)"""
        return self.query("FIL","int")[channel-1]
    @interface.use_parameters(_returns="meas_filter")
    def set_measurement_filter(self, meas_filter, channel=1):
        """Set gauge measurement filter (``"fast"``, ``"medium"``, or ``"slow"``)"""
        curr_filter=self.query("FIL","int")
        curr_filter[channel-1]=meas_filter
        return self.query("FIL,{},{}".format(*curr_filter),"int")[channel-1]
    @interface.use_parameters
    def get_calibration_factor(self, channel=1):
        """Get gauge calibration factor"""
        return self.query("CAL","float")[channel-1]
    @interface.use_parameters
    def set_calibration_factor(self, coefficient, channel=1):
        """Set gauge calibration factor"""
        curr_coefficient=self.query("CAL","float")
        curr_coefficient[channel-1]=coefficient
        return self.query("CAL,{},{}".format(*curr_coefficient),"float")[channel-1]
    _p_switch_func=interface.RangeParameterClass("switch_function",1,4)
    @interface.use_parameters(_returns=["channel",None,None])
    def get_switch_settings(self, switch_function):
        """
        Get settings for the given switch function (between 1 and 4).

        Return tuple ``(channel, low_thresh, high_thresh)``. The thresholds are given in Pa.
        """
        ch,lt,ht=self.query("SP{}".format(switch_function),["int","float","float"])
        units=self.get_units()
        return TTPG260SwitchSettings(ch+1,self.to_Pa(lt,units),self.to_Pa(ht,units))
    @interface.use_parameters(_returns=["channel",None,None])
    def setup_switch(self, switch_function, channel, low_thresh, high_thresh):
        """
        Get settings for the given switch function (between 1 and 4).

        Return tuple ``(channel, low_thresh, high_thresh)``. The thresholds are given in Pa.
        """
        units=self.get_units()
        low_thresh=self.from_Pa(low_thresh,units)
        high_thresh=self.from_Pa(high_thresh,units)
        ch,lt,ht=self.query("SP{},{},{},{}".format(switch_function,channel-1,low_thresh,high_thresh),["int","float","float"])
        return TTPG260SwitchSettings(ch+1,self.to_Pa(lt,units),self.to_Pa(ht,units))
    def get_switch_status(self):
        """Return status of the 4 switch functions"""
        return [bool(v) for v in self.query("SPS","int")]

    _p_activation_control=interface.EnumParameterClass("activation_control",{"none":0,"auto":1,"manual":2,"external":3,"hot_start":4})
    _p_deactivation_control=interface.EnumParameterClass("deactivation_control",{"none":0,"auto":1,"manual":2,"external":3,"self_control":4})
    @interface.use_parameters(_returns=["activation_control","deactivation_control",None,None])
    def get_gauge_control_settings(self, channel):
        """
        Get settings for the gauge control on the given channel.

        Return tuple ``(activation_control, deactivation_control, on_thresh, off_thresh)``. The thresholds are given in Pa.
        """
        acc,dacc,ont,offt=self.query("SC{}".format(channel),["int","int","float","float"])
        units=self.get_units()
        return TTPG260GaugeControlSettings(acc,dacc,self.to_Pa(ont,units),self.to_Pa(offt,units))
    @interface.use_parameters(_returns=["activation_control","deactivation_control",None,None])
    def setup_gauge_control(self, channel, activation_control, deactivation_control, on_thresh, off_thresh):
        """
        Setup gauge control on the given channel.

        Return tuple ``(activation_control, deactivation_control, on_thresh, off_thresh)``. The thresholds are given in Pa.
        """
        units=self.get_units()
        on_thresh=self.from_Pa(on_thresh,units)
        off_thresh=self.from_Pa(off_thresh,units)
        acc,dacc,ont,offt=self.query("SC{},{},{},{},{}".format(channel,activation_control,deactivation_control,on_thresh,off_thresh),["int","int","float","float"])
        return TTPG260GaugeControlSettings(acc,dacc,self.to_Pa(ont,units),self.to_Pa(offt,units))

    def _parse_errors(self, errs):
        if not isinstance(errs,list):
            errs=[errs]
        err_codes={0:"no_error",1:"watchdog",2:"task_fail",3:"eprom",4:"ram",5:"eeprom",6:"display",7:"adconv",
            9:"gauge_1_err",10:"gauge_1_id_err",11:"gauge_2_err",12:"gauge-2_id_err"}
        return [err_codes.get(er,er) for er in sorted(errs)]
    def get_current_errors(self):
        """
        Get a list of all present error messages.

        If there are no errors, return a single-element list ``["no_error"]``.
        """
        return self._parse_errors(self.query("RES","int"))
    def reset_error(self):
        """
        Cancel currently active errors and return to measurement mode.

        Return the list of currently present errors.
        If there are no errors, return a single-element list ``["no_error"]``.
        """
        return self._parse_errors(self.query("RES,1","int"))







class DPG202(comm_backend.ICommBackendWrapper):
    """
    DPG202/TPG202 control unit.

    Args:
        conn: serial connection parameters (usually port or a tuple containing port and baudrate)
    """
    Error=PfeifferError
    def __init__(self, conn):
        instr=comm_backend.new_backend(conn,"serial",term_read="\r",term_write="\r",datatype="str",defaults={"serial":("COM1",9600)},reraise_error=PfeifferBackendError)
        comm_backend.ICommBackendWrapper.__init__(self,instr)
        self._add_info_variable("device_name",self.get_device_name)
        self._add_info_variable("software_version",self.get_software_version)
        self._add_status_variable("last_error_code",self.get_error_code)
        self._add_status_variable("pressure",self.get_pressure,ignore_error=(PfeifferError,),priority=5)
        try:
            self.get_device_name()
        except self.instr.Error:
            self.close()
            raise

    _data_types={"boolean_old":0,"u_integer":1,"u_real":2,"string":4,"boolean_new":6,"u_short_int":7,"u_expo_new":10,"long_string":11} # data type indices
    _data_lengths={0:6,1:6,2:6,4:6,6:1,7:3,10:6,11:16} # data lengths
    def _parse_telegram(self, telegram, data_type=None):
        """Parse a telegram string and return its content: parameters, value, action, and address"""
        address,action,parameter,l,svalue,recv_checksum=int(telegram[:3]),int(telegram[3]),int(telegram[5:8]),int(telegram[8:10]),telegram[10:-3],int(telegram[-3:])
        checksum=sum([ord(c) for c in telegram[:-3]])%0x100
        if checksum!=recv_checksum:
            raise PfeifferError("incorrect checksum of the telegram: expected {}, calculated {}".format(recv_checksum,checksum))
        if l!=len(svalue):
            raise PfeifferError("incorrect specified length of the value: declared {}, actual {}".format(l,len(svalue)))
        if svalue=="NO_DEF":
            raise PfeifferError("parameter does not exist")
        elif svalue=="_RANGE":
            raise PfeifferError("value is out of range")
        elif svalue=="_LOGIC":
            raise PfeifferError("logic access violation")
        if data_type is None:
            value=svalue
        else:
            data_type=self._data_types.get(data_type,data_type)
            if data_type not in self._data_lengths:
                raise PfeifferError("unknown data type: {}".format(data_type))
            if l!=self._data_lengths[data_type]:
                raise PfeifferError("received parameter length {} doesn't correspond to the expected length for this data type {}".format(l,self._data_lengths[data_type]))
            if data_type in [0,6]: # boolean_old, boolean_new
                value=bool(int(svalue))
            elif data_type in [1,7]: # u_integer, u_short_int
                value=int(svalue)
            elif data_type==2: # u_real
                value=int(svalue)/1E2
            elif data_type in [4,11]: # string, long_string
                value=svalue
            elif data_type==10: # u_expo_new
                value=int(svalue[:4])*10**(int(svalue[4:6])-23)
        return parameter,value,action,address
    def _build_value_string(self, value, data_type):
        """Convert the value into a string using the given data type"""
        data_type=self._data_types.get(data_type,data_type)
        if data_type not in self._data_lengths:
            raise ValueError("unknown data type: {}".format(data_type))
        l=self._data_lengths[data_type]
        if data_type in [0,6]: # boolean_old, boolean_new
            svalue=("1" if value else "0")*l
        elif data_type==1: # u_integer
            svalue="{:06d}".format(int(value))
        elif data_type==7: # u_short_int
            svalue="{:03d}".format(int(value))
        elif data_type==2: # u_real
            svalue="{:06d}".format(int(value*1E2))
        elif data_type in [4,11]: # string, long_string
            svalue=str(value).ljust(l)
        elif data_type==10: # u_expo_new
            sexp="{:.3e}".format(value)
            m=int(sexp[0]+sexp[2:5])
            e=int(sexp[sexp.find("e")+1:])
            svalue="{:04d}{:02d}".format(m,e+20)
        if len(svalue)!=l:
            raise ValueError("string value '{}' has length {} instead of the expected length {}".format(svalue,len(svalue),l))
        return svalue
    def _build_telegram(self, parameter, value="=?", action=0, address=1):
        """Build a telegram string with the given content"""
        telegram="{:03d}{:d}0{:03d}{:02d}{}".format(address,action,parameter,len(value),value)
        checksum=sum([ord(c) for c in telegram])%0x100
        return "{}{:03d}".format(telegram,checksum)

    def query(self, parameter, value="=?", action=0, address=1, send_type=None, recv_type=None):
        """
        Send a query to the device and parse the reply.

        Args:
            parameter: parameter number
            value: value to send (``"=?"`` for a value request)
            action: request action (0 for value request, 1 for a command)
            address: unit address
            send_type: data type for the sent value (ignored for value requests)
            recv_type: data type for the received value (``None`` means returning a raw string value)
        """
        if value!="=?":
            if send_type is None:
                raise ValueError("send value type should be specified")
            value=self._build_value_string(value,send_type)
        req=self._build_telegram(parameter,value=value,action=action,address=address)
        self.instr.write(req)
        reply=self.instr.readline()
        rparameter,rvalue,raction,raddress=self._parse_telegram(reply,data_type=recv_type)
        if rparameter!=parameter:
            raise PfeifferError("reply parameter {} is different from the request parameter {}".format(rparameter,parameter))
        if raddress!=address:
            raise PfeifferError("reply address {} is different from the request address {}".format(raddress,address))
        if raction!=1:
            raise PfeifferError("expected reply action 01, got {:02d}".format(raction))
        return rvalue
    def get_value(self, parameter, data_type, address=1):
        """
        Send a data request to the device.

        Args:
            parameter: parameter number
            data_type: data type for the received value
            address: unit address
        """
        return self.query(parameter,recv_type=data_type,address=address)
    def comm(self, parameter, value, data_type, address=1):
        """
        Send a control command to the device.

        Args:
            parameter: parameter number
            value: associated command value
            data_type: data type for the sent value
            address: unit address
        """
        return self.query(parameter,value=value,action=1,send_type=data_type,address=address)
        
    
    def get_pressure(self, address=1):
        """Get pressure at a given unit address"""
        return self.get_value(740,"u_expo_new",address=address)*1E2
    
    def get_error_code(self, address=1):
        """Get the current error code at a given unit address"""
        return self.get_value(303,"string",address=address)
    def get_software_version(self, address=1):
        """Get the software version at a given unit address"""
        return self.get_value(312,"string",address=address)
    def get_device_name(self, address=1):
        """Get the name of the gauge at a given unit address"""
        return self.get_value(349,"string",address=address)