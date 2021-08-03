from ..generic import lasers


class FinesseThread(lasers.IPumpLaserThread):
    _device_class="LaserQuantum.Finesse"
    def setup_task(self, conn, remote=None):
        super().setup_task(conn,remote=remote)
        self.add_device_command("set_shutter",post_update=None)
    def update_measurements(self):
        super().update_measurements()
        if self.is_opened():
            self.v["shutter"]=self.device.is_shutter_opened()
        else:
            self.v["shutter"]=False