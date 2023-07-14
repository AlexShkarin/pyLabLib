from ... import device_thread



class Keithley2110Thread(device_thread.DeviceThread):
    """
    Keithley 2110 bench-top multimeter device thread.

    Device args:
        - ``conn``: device connection (usually a VISA name)

    Variables:
        - ``readings/<n>``: last measured readings on one of the two measurement channels (``<n>`` is 1 or 2)
        - ``functions/<n>``: selected measurement functions one of the two measurement channels (``<n>`` is 1 or 2)
        - ``parameters``: measurement function parameters

    Commands:
        - ``set_function``: set measurement function for one or both measurement channels
        - ``set_function_parameters``: set measurement parameters (range, resolution, etc.) for a given function
        - ``set_configuration``: quickly set measurement configuration (function and parameters) for the primary measurement channels
        - ``setup_averaging``: setup readings averaging
    """
    full_info_variables="all"
    def connect_device(self):
        with self.using_devclass("Keithley.Keithley2110",host=self.remote) as cls:
            self.device=cls(addr=self.conn)  # pylint: disable=not-callable
    def setup_task(self, conn, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,.2)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("set_function")
        self.add_device_command("set_function_parameters")
        self.add_device_command("set_configuration")
        self.add_device_command("setup_averaging")
    def update_measurements(self):
        if self.open():
            self.v["readings"]=dict(zip(["1","2"],self.device.get_reading("all")))
        else:
            self.v["readings"]={"1":None,"2":None}
    def update_parameters(self):
        if self.open():
            sett=self.device.get_settings("all")
            self.v["functions"]=dict(zip(["1","2"],sett["functions"]))
            for k,v in sett.items():
                if k.startswith("parameters/"):
                    self.v[k]=v
        else:
            self.v["functions"]={"1":"none","2":"none"}
            self.v["parameters"]={}
            self.sleep(1.)