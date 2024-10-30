from ... import device_thread



class DP1116A(device_thread.DeviceThread):
    """
    Rigol DP1116A DC power supply device thread.

    Device args:
        - ``conn``: device connection (usually, a VISA connection address)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``enabled``: whether the output is enabled
        - ``voltage``: measured output voltage
        - ``current``: measured output current
        - ``voltage_setpoint``: specified output voltage setpoint
        - ``current_setpoint``: specified output current setpoint

    Commands:
        - ``enable_output``: enable or disable the output
        - ``set_voltage``: set output voltage
        - ``set_current``: set output current
    """
    def connect_device(self):
        with self.using_devclass("Rigol.DP1116A",host=self.remote) as cls:
            self.device=cls(addr=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote_mode="force", remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote_mode=remote_mode
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,0.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("set_voltage")
        self.add_device_command("set_current")
        self.add_device_command("enable_output")
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            self.v["enabled"]=self.device.is_output_enabled()
            self.v["voltage"]=self.device.get_voltage()
            self.v["current"]=self.device.get_current()
            self.v["voltage_setpoint"]=self.device.get_voltage_setpoint()
            self.v["current_setpoint"]=self.device.get_current_setpoint()
        else:
            self.v["enabled"]=False
            self.v["voltage"]=0
            self.v["current"]=0
            self.v["voltage_setpoint"]=0
            self.v["current_setpoint"]=0