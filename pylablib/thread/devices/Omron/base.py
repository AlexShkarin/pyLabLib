from ... import device_thread



class OmronE5xCControllerThread(device_thread.DeviceThread):
    """
    Omron E5_C temperature controller device thread.

    Device args:
        - ``conn``: serial connection parameters for RS485 adapter (usually port, a tuple containing port and baudrate,
            or a tuple with full specification such as ``("COM1", 9600, 8, 'E', 1)``)
        - ``daddr``: default device Modbus address

    Variables:
        - ``measurement/i``: last measured value in the integer format
        - ``setpoint/i``: temperature setpoint value in the integer format
    """
    def connect_device(self):
        with self.using_devclass("Omron.OmronE5xCController",host=self.remote) as cls:
            self.device=cls(conn=self.conn,daddr=self.daddr)  # pylint: disable=not-callable
            self.device.get_measurementi()
    def setup_task(self, conn, daddr=1, remote=None):  # pylint: disable=arguments-differ
        self.device_reconnect_tries=5
        self.conn=conn
        self.daddr=daddr
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,0.5)
        self.add_job("update_parameters",self.update_parameters,2)
        self.add_device_command("set_setpointi",post_update=["update_measurements","update_parameters"],limit_queue=1,on_full_queue="skip_oldest")
    def update_measurements(self):
        """Update current measurements"""
        if self.open():
            self.v["measurement/i"]=self.device.get_measurementi()
            self.v["setpoint/i"]=self.device.get_setpointi()
        else:
            self.v["measurement/i"]=0
            self.v["setpoint/i"]=0
            self.sleep(1.)