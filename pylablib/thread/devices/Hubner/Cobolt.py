from ... import device_thread


class CoboltThread(device_thread.DeviceThread):
    """
    Hubner Cobolt MLD/DPL laser controller.

    Device args:
        - ``conn``: device connection (usually, COM-port address)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``power``: current actual output laser power
        - ``current``: current laser drive current
        - ``enabled``: indicates whether the laser is on
        - ``mode``: device operating mode/status (``"off"``, ``"continuous"``, ``"on_off_mod"``, ``"wait_key"``, etc.)
        - ``error_state``: device error state (``"none"`` if no error)
        - ``output_mode``: output mode (``"cpower"``, ``"ccurrent"``, ``"mod"``)
        - ``interlock``: indicates whether the interlock is closed (enabled)
        - ``key_switch``: indicates whether the key switch is on (enabled)
        - ``analog_modulation``: indicates whether the analog modulation is on
        - ``digital_modulation``: indicates whether the digital modulation is on
        - ``temperature_baseplate``: laser base plate temperature
        - ``temperature_head``: laser head temperature

    Commands:
        - ``enable``: enable or disable the laser output
    """
    def connect_device(self):
        with self.using_devclass("Hubner.Cobolt",host=self.remote) as cls:
            self.device=cls(conn=self.conn)  # pylint: disable=not-callable
            self.device.is_enabled()
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.5)
        self.add_device_command("enable",post_update="update_measurements")
        self.add_device_command("clear_error",post_update="update_measurements")
        self.add_device_command("set_output_power",post_update="update_measurements")
        self.add_device_command("set_output_current",post_update="update_measurements")
        self.add_device_command("set_output_mode",post_update="update_measurements")
        self.add_device_command("enable_analog_modulation",post_update="update_measurements")
        self.add_device_command("enable_digital_modulation",post_update="update_measurements")

    def update_measurements(self):
        if self.open():
            self.v["power"]=self.device.get_output_power()
            self.v["current"]=self.device.get_output_current()
            self.v["enabled"]=self.device.is_enabled()
            self.v["mode"]=self.device.get_operating_mode()
            self.v["error_state"]=self.device.get_error_state()
            self.v["output_mode"]=self.device.get_output_mode()
            self.v["interlock"]=self.device.get_interlock()
            self.v["key_switch"]=self.device.get_key_switch()
            self.v["analog_modulation"]=self.device.is_analog_modulation_enabled()
            self.v["digital_modulation"]=self.device.is_digital_modulation_enabled()
            self.v["temperature_baseplate"]=self.device.get_baseplate_temperature()
            self.v["temperature_head"]=self.device.get_head_temperature()
        else:
            self.v["power"]=-1
            self.v["current"]=0
            self.v["enabled"]=False
            self.v["mode"]="off"
            self.v["error_state"]="none"
            self.v["output_mode"]="cpower"
            self.v["interlock"]=False
            self.v["key_switch"]=False
            self.v["analog_modulation"]=False
            self.v["digital_modulation"]=False
            self.v["temperature_baseplate"]=0
            self.v["temperature_head"]=0