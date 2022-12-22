from ... import device_thread



class VC7055Thread(device_thread.DeviceThread):
    """
    Voltcraft VC-7055BT bench-top multimeter device thread.

    Device args:
        - ``conn``: device connection (usually a COM-port name such as ``"COM1"``).

    Variables:
        - ``readings/<n>``: last measured readings on one of the two measurement channels (``<n>`` is 1 or 2)
        - ``functions/<n>``: selected measurement functions one of the two measurement channels (``<n>`` is 1 or 2)
        - ``range``: measurement range
        - ``rate``: measurement rate

    Commands:
        - ``set_function``: set measurement function for one or both measurement channels
        - ``set_range``: set measurement range
        - ``enable_autorange``: enable or disable measurement autorange
        - ``set_measurement_rate``: set measurement rate (``"fast""``, ``"med"``, or ``"slow"``)
    """
    full_info_variables="all"
    def connect_device(self):
        with self.using_devclass("Voltcraft.VC7055",host=self.remote) as cls:
            self.device=cls(addr=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("set_function")
        self.add_device_command("set_range")
        self.add_device_command("enable_autorange")
        self.add_device_command("set_measurement_rate")
    def update_measurements(self):
        if self.open():
            self.v["readings"]=dict(zip(["1","2"],self.device.get_readings("all")))
        else:
            self.v["readings"]={"1":None,"2":None}
    def update_parameters(self):
        if self.open():
            sett=self.device.get_settings("all")
            self.v["functions"]=dict(zip(["1","2"],sett["function"]))
            self.v["range"]=self.device.get_range()
            self.v["rate"]=self.device.get_measurement_rate()
        else:
            self.v["functions"]={"1":"none","2":"none"}
            self.v["range"]=None
            self.v["rate"]="slow"
            self.sleep(1.)