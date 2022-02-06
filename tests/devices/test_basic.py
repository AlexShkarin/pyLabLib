import pytest

class DeviceTester:
    """
    Generic device tester.

    Takes device class and creation arguments and implements some basic tests.
    """
    test_open_rep=2
    include=-10
    get_set_all_exclude=()

    @classmethod
    def post_open(cls, device):
        pass
    def test_open_close(self, devopener):
        device=devopener()
        assert device.is_opened()
        for _ in range(self.test_open_rep):
            device.close()
            assert not device.is_opened()
            device.close()
            assert not device.is_opened()
            device.open()
            self.post_open(device)
            assert device.is_opened()
            device.open()
            assert device.is_opened()
    def test_opened(self, devopener):
        """Test opening and closing errors"""
        device=devopener()
        assert device.is_opened()

    def test_get_full_info(self, devopener, stress_factor):
        """Test info getting errors"""
        device=devopener()
        for _ in range(stress_factor):
            info=device.get_full_info(self.include)
            print(device,info)
    def _assert_settings(self, old_settings, new_settings):
        assert old_settings==new_settings
    @pytest.mark.devchange(2)
    def test_get_set_all(self, devopener, stress_factor):
        """Test getting and re-applying settings error"""
        device=devopener()
        for _ in range(stress_factor):
            settings=device.get_settings(self.include)
            print(device,settings)
            for k in self.get_set_all_exclude:
                del settings[k]
            device.apply_settings(settings)
            new_settings=device.get_settings(self.include)
            for k in self.get_set_all_exclude:
                del new_settings[k]
            self._assert_settings(settings,new_settings)

    def check_get_par(self, device, name, par_name=None):
        """
        Test parameter getting.
        
        `name` is either a parameter name (``"get_"`` is appended to its name automatically),
        or a single-element tuple with the exact getter function name.
        If `par_name` is not ``None``, also check that this parameter result is equal to the getter value.
        """
        if not isinstance(name,tuple):
            name=("get_"+name,)
        par_name=par_name or name
        assert hasattr(device,name[0])
        if par_name:
            assert getattr(device,name[0])()==device.dv[par_name]
    def check_get_set(self, device, name, value, par_name=None):
        """
        Test parameter setting and getting.
        
        `name` is either a parameter name (``"get_"`` and ``"set"`` are appended to its name automatically),
        or a 2-element tuple with the exact getter and setter function name.
        If `par_name` is not ``None``, also check that this parameter result is equal to the getter value.
        """
        if not isinstance(name,tuple):
            name=("get_"+name,"set_"+name)
        if par_name is None:
            par_name=name if name in device._device_vars else ""
        assert hasattr(device,name[0])
        assert hasattr(device,name[1])
        if par_name:
            assert getattr(device,name[0])()==device.dv[par_name]
        getattr(device,name[1])(value)
        assert getattr(device,name[0])()==value
        if par_name:
            assert getattr(device,name[0])()==device.dv[par_name]