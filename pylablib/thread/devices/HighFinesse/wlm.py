from ... import device_thread
from ....devices import M2



class WLMThread(device_thread.DeviceThread):
    """
    HighFinesse WS6/7 wavemeter device thread.

    Device args:
        - ``version``: wavemeter version; if ``None``, use any available version
        - ``dll_path``: path to ``wlmData.dll``; if ``None``, use standard locations or search based on the version
        - ``channel``: wavemeter channel index or a list of indices
        - ``**kwargs``: additional arguments supplied on the device creation (e.g., ``app_path``)
        - ``remote``: address of the remote host where the device is connected; ``None`` (default) for local device, or ``"disconnect"`` to not connect

    Variables:
        - ``frequency``, ``wavelength``: last measured frequency and wavelength (in vacuum);
            frequency and wavelength of 0 indicates invalid values: over- or underflow, disconnected channel or wavemeter
        - ``measurement_status``: status of the last measurement; can be ``"ok"`` for a valid measurement,
            ``"under"``, ``"over"``, ``"nosig"``, ``"badsig"`` or ``"noval"`` to indicate measurement problems,
            or ``"disconn"`` if the device is disconnected
        - ``parameters``: main wavemeter parameters: exposure and exposure mode, switcher mode, pulse mode, etc.
    """
    def connect_device(self):
        with self.using_devclass("HighFinesse.WLM",host=self.remote) as cls:
            self.device=cls(version=self.version,dll_path=self.dll_path,**self.dev_kwargs)  # pylint: disable=not-callable
            self.device.get_frequency(error_on_invalid=False)
    def setup_task(self, version=None, dll_path=None, channel=1, remote=None, **kwargs):  # pylint: disable=arguments-differ
        self.version=version
        self.dll_path=dll_path
        self.channel=channel
        self.dev_kwargs=kwargs
        self.remote=remote
        self.add_job("update_measurements",self.update_measurements,0.02 if remote else 0.005) # frequency update period is >15ms anyway; lower period for remote due to network latency
        self.add_job("update_parameters",self.update_parameters,1.)
    def _set_frequency_variable(self, channel, branch=None):
        if self.open():
            freq=self.device.get_frequency(channel=channel,error_on_invalid=False)
            if freq in ["under","over","nosig","badsig","noval"]:
                data=freq,0,0
            else:
                data="ok",freq,M2.c/freq
        else:
            data="disconn",0,0
        for k,d in zip(["measurement_status","frequency","wavelength"],data):
            if branch is None:
                self.v[k]=d
            else:
                self.v[k,branch]=d
    def update_measurements(self):
        """Update current measurements"""
        if isinstance(self.channel,list):
            for ch in self.channel:
                self._set_frequency_variable(ch,ch)
        else:
            self._set_frequency_variable(self.channel)
        if not self.open():
            self.sleep(.2)