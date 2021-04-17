import contextlib



class DeviceTester:
    """
    Generic device tester.

    Takes device class and creation arguments and implements some basic tests.
    """
    def __init__(self, devclass, *args, **kwargs):
        self.devclass=devclass
        self.args=args
        self.kwargs=kwargs
        self.open_rep=0
        self.dev=None
    
    @contextlib.contextmanager
    def opened(self):
        """Conext manager for opening the device"""
        if self.dev is not None:
            yield self.dev
            return
        opened=False
        try:
            self.dev=self.devclass(*self.args,**self.kwargs)
            opened=True
            for _ in range(self.open_rep):
                self.dev.close()
                opened=False
                self.dev.open()
                opened=True
            yield self.dev
        finally:
            if opened:
                self.dev.close()
            self.dev=None
    def test_open_close(self):
        """Test opening and closing errors"""
        with self.opened() as dev:
            assert dev.is_opened()
        if self.dev is None:
            assert not dev.is_opened()
    def test_get_info(self, include=-10):
        """Test info getting errors"""
        with self.opened() as dev:
            dev.get_settings(include)
            info=dev.get_full_info(include)
            print(dev,info)
    def test_get_set_all(self, include=-10):
        """Test getting and re-applying settings error"""
        with self.opened() as dev:
            settings=dev.get_settings(include)
            dev.apply_settings(settings)
            assert dev.get_settings(include)==settings

    def test_get_par(self, name, par_name=None):
        """
        Test parameter getting.
        
        `name` is either a parameter name (``"get_"`` is appended to its name automatically),
        or a single-element tuple with the exact getter function name.
        If `par_name` is not ``None``, also check that this parameter result is equal to the getter value.
        """
        if not isinstance(name,tuple):
            name=("get_"+name,)
        par_name=par_name or name
        with self.opened() as dev:
            assert hasattr(dev,name[0])
            if par_name:
                assert getattr(dev,name[0])()==dev.dev[par_name]
    def test_get_set(self, name, value, par_name=None):
        """
        Test parameter setting and getting.
        
        `name` is either a parameter name (``"get_"`` and ``"set"`` are appended to its name automatically),
        or a 2-element tuple with the exact getter and setter function name.
        If `par_name` is not ``None``, also check that this parameter result is equal to the getter value.
        """
        with self.opened() as dev:
            if not isinstance(name,tuple):
                name=("get_"+name,"set_"+name)
            if par_name is None:
                par_name=name if name in dev._device_vars else ""
            assert hasattr(dev,name[0])
            assert hasattr(dev,name[1])
            if par_name:
                assert getattr(dev,name[0])()==dev.dev[par_name]
            getattr(dev,name[1])(value)
            assert getattr(dev,name[0])()==value
            if par_name:
                assert getattr(dev,name[0])()==dev.dev[par_name]

    def test_all(self, noset=True):
        """Apply all tests"""
        self.test_open_close()
        self.test_get_info()
        if not noset:
            self.test_get_set_all()