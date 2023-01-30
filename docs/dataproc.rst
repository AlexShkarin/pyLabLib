.. _dataproc:

Data processing
=========================


.. _dataproc_fitting:

Fitting
-------------------------

Class :class:`.fitting.Fitter` is a user-friendly wrapper around :func:`scipy.optimize.least_squares` routine. Dealing with fitting is made more convenient in a couple of ways:

    - It is easy to specify the x-parameter name (in the case it is not the first parameter), or specify multiple x-parameters;
    - All of the fit and fixed parameters are specified by name; it is easy to switch between any parameter being fit or fixed;
    - The wrapper automatically handles complex parameters (split into real and imaginary parts), numpy arrays, lists, or tuples (including nested structures);
    - The final parameters (fit and fixed) are returned in a single dictionary indexed by their names;
    - The wrapper also returns the fit function with all of the parameters bound to the final fit and fixed values;
    - The fit function result is flattened during fitting, so it works for functions returning multi-dimensional (for example, 2D) arrays.

Examples
~~~~~~~~~~~~~~~~~~~~~~~~~

Fitting a Lorentzian::

    def lorentzian(frequency, position=0., width=1., height=1.):
        return height/(1.+4.*(frequency-position)**2/width**2)

    ## creating the fitter
    # fit_parameters dictionary specifies the initial guess
    fit_par = {"position":0.5, "height":1.}
    fitter = pll.Fitter(lorentzian, xarg_name="frequency", fit_parameters=fit_par)
    # additional fit parameter is supplied during the call
    fit_par, fit_func = fitter.fit(xdata, ydata, fit_parameters={"width":1.0})
    plot(xdata, ydata)  # plot the experimental data
    plot(xdata, fit_func(xdata))  # plot fit result

Fitting a sum of complex Lorentzians with the same width::

    def lorentzian_sum(frequency, positions, width, amplitudes):
        # list of complex lorentzians
        #   positions and amplitudes are lists, one per peak
        lorentzians = [a/(1.+2j*(frequency-p)/width) for (a,p) in zip (amplitudes,positions)]
        return np.sum(lorentzians, axis=0)

    ## creating the fitter
    # fit_parameters dictionary specifies the initial guess
    #     (complex initial guess for the "amplitude" parameter hints that this parameter is complex)
    fit_par = {"positions":[0.,0.5,1.], "amplitudes":[1.+0.j]*3}
    fitter = pll.Fitter(lorentzian_sum, xarg_name="frequency", fit_parameters=fit_par)
    # fixed parameter is supplied during the call (could have also been supplied on Fitter initialization)
    fit_par, fit_func = fitter.fit(xdata, ydata, fixed_parameters = {"width":0.3})
    plot(xdata, ydata.real)  # plot the experimental data
    plot(xdata, fit_func(xdata).real)  # plot fit result

Fitting 2D Gaussian and getting the parameter estimation errors::

    def gaussian(x, y, pos, width, height):
        return np.exp( -((x-pos[0])**2+(y-pos[1])**2)/(2*width**2) )*height

    ## creating the fitter
    # fit_parameters dictionary specifies the initial guess
    fit_par = {"pos":(100,100), "width":10., "height":5.}
    fitter = pll.Fitter(gaussian, xarg_name=["x","y"], fit_parameters=fit_par)
    xs, ys = np.meshgrid(np.arange(img.shape[0]), np.arange(img.shape[1]), indexing="ij") # building x and y coordinates for the image
    # fit_stderr is a dictionary containing the fit error for the corresponding parameters
    fit_par, fit_func, fit_stderr = fitter.fit([xs,ys], img, return_stderr=True)
    imshow(fit_func(xs, ys))  # plot fit result

The full module documentation is given at :mod:`pylablib.core.dataproc.fitting`.


.. _dataproc_filtering:

Filtering and decimation
-------------------------

There are several functions present for filtering the data to smooth it or reduce its size. Most of them are thin wrapper around standard numpy or scipy method, but they provide more universal interface which work both with numpy arrays and pandas DataFrames:

    - First are the decimation functions: :func:`.filters.decimate` (and its special case :func:`.filters.binning_average`), :func:`.filters.decimate_full` and :func:`.filters.decimate_datasets`. The first one splits the supplied trace into consecutive segments of `n` points and compresses them into a single value using the supplied method (e.g., ``"mean"`` will average them together, which is used for :func:`.filters.binning_average`). The second one completely decimates the dataset along the given axis (which is essentially identical to using the standard numpy methods such as ``np.mean`` or ``np.max``). The last one decimates several datasets together, which is similar to combining them into a large ``(n+1)D`` array and fully decimating along the given axis::

        >> trace = np.arange(10)
        >> pll.binning_average(trace, 3)  # average every block of 3 points to a single value
        array([1., 4., 7.])
        >> pll.decimate(trace, 3, dec="max")
        array([2, 5, 8])
        >> pll.decimate_full(trace, "mean")  # same as np.mean(trace)
        4.5
        >> trace2 = np.arange(10)**2
        >> pll.decimate_datasets([trace, trace2], "sum")  # same as np.sum([trace, trace2],axis=0)
        array([ 0,  2,  6, 12, 20, 30, 42, 56, 72, 90])

    - Sliding decimation methods :func:`.filters.sliding_average`, :func:`.filters.median_filter` and :func:`.filters.sliding_filter` are related, but use a sliding window of `n` points instead of complete decimation of `n` points together. They only work for 1D traces or 2D multi-column datasets. Note that :func:`.filters.sliding_filter` is implemented through a simple Python loop, so it is fairly inefficient::

        >> trace = np.arange(10)
        >> pll.sliding_average(trace, 4)  # average points in 4-point window (by default use "reflect" boundary conditions)
        array([0.75, 1.5 , 2.5 , 3.5 , 4.5 , 5.5 , 6.5 , 7.5 , 8.25, 8.5 ])
        >> pll.sliding_filter(trace, 4, "max")  # find maximum of points in 4-point window
        array([2, 3, 4, 5, 6, 7, 8, 9, 9, 9])

    - Next are convolution filters which operate by convolving the trace with a given kernel function. These involve :func:`.filters.gaussian_filter` (and :func:`.filters.gaussian_filter_nd`, which is simply a wrapper around :func:`scipy.ndimage.gaussian_filter`), and a more generic :func:`.filters.convolution_filter`. Related are infinite impulse response (IIR) filter :func:`.filters.low_pass_filter` and :func:`.filters.high_pass_filter`, which mimic standard single-pole low-pass and high-pass filters. In principle, they can be modeled as a convolution with an exponential decay, but the implementation using the recursive filters is more efficient for large widths.
    - Finally, there are Fourier filters, which Fourier-transform the trace, scale the transform values, and transform it back to the real domain. These involve the main function :func:`.filters.fourier_filter`, which takes a generic frequency response function, as well as two specific response function generators :func:`.filters.fourier_filter_bandpass` and :func:`.filters.fourier_filter_bandstop`, both generating hard frequency cutoff filters.
    - In addition to "post-processing" filters described above, there are also "real-time" filters which serve to filter data as it is acquired, e.g., to filter out temporary noise or spikes. There are two filters of this kind: :class:`.filters.RunningDecimationFilter` and :class:`.filters.RunningDebounceFilter`. They are implemented as classes, and both have methods to add a new datapoint, to get the current filter value, and to reset the filter.


.. _dataproc_fourier:

Fourier transform
-------------------------

There is a couple of methods to work with Fourier transform. They are built around :func:`numpy.fft.fft`, but allow more convenient normalization (e.g., in units of power spectral density), and work better with pandas DataFrames. They also have an option to automatically trim the trace length to the nearest "good" size, which is a product of small primes. This can have fairly strong (up to a factor of several) effect on the transform runtime, while typically trimming off less than 1% of the data.

The main methods are :func:`.fourier.fourier_transform` for the direct transform, :func:`.fourier.inverse_fourier_transform` for the inverse transform, and :func:`.fourier.power_spectral_density` for the power spectral density::

    >> x = np.random.normal(size=10**5)  # normal distribution centered at 0 with a width of 1
    >> PSD = pll.power_spectral_density(x, dt=1E-3)  # by default, use density normalization; assume time step of 1ms
    >> df = PSD[1,0] - PSD[0,0]
    >> df  # total span is 1kHz with 10**5 points, resulting in 0.01Hz step
    0.01
    >> np.sum(PSD[:,1]) * df  # integrated PSD is equal to the original trace RMS squared, which is about 1 for the normal distribution
    1.005262206692361
    >> np.mean(x**2)
    1.005262206692361


.. _dataproc_feature:

Feature detection
-------------------------

There are several methods for simple feature detection:

  - The peak detection, which is usually achieved by the combination of :func:`.feature.multi_scale_peakdet` and :func:`.feature.find_peaks_cutoff`. The first applies difference-of-Lorentzians or difference-of-Gaussians filter, which detects peaks of a particular width. The second finds peaks using a cutoff.
  - Another way to find peaks is using :func:`.feature.find_local_extrema`, which finds local minima or maxima in a sliding window of a given width.
  - Switching between two states with a noisy trace can be detected using :func:`.feature.latching_trigger`. It implements a more robust approach to find when the trace is above/below threshold by considering two thresholds: a higher "on" thresholds and a lower "off" threshold. It makes the on/off state "latch" to its current value and is robust to small trace fluctuations around the threshold, which would lead to rapid on/off switches in a single-threshold scheme.


.. _dataproc_misc:

Miscellaneous utilities
-------------------------

Additionally, there is a variety of small functions to simplify some data analyses and transforms:

    - Checking trace properties: :func:`.dataproc.utils.is_ascending`, :func:`.dataproc.utils.is_descending`, :func:`.dataproc.utils.is_ordered`, :func:`.dataproc.utils.is_linear`.
    - Sorting by a given column: :func:`.dataproc.utils.sort_by`; work both on pandas and numpy arrays
    - Filtering: :func:`.dataproc.utils.filter_by` and :func:`.dataproc.utils.unique_slices` (a simple analog of pandas :meth:`pandas.DataFrame.groupby`, which works on numpy arrays)
    - Binary search (both in ordered and unordered 1D arrays): :func:`.dataproc.utils.find_closest_arg`, :func:`.dataproc.utils.find_closest_value`, and :func:`.dataproc.utils.get_range_indices`.
    - Traces step analysis and unwrapping: :func:`.dataproc.utils.find_discrete_step` tries to find a single number which divides all values within a reasonable precision, and :func:`.dataproc.utils.unwrap_mod_data` "unwraps" modulo data (e.g., phase, which is defined mod 2pi) provided that the steps between two consecutive points are less than 1/2 of the module.
    - Cutting the trace to the given range, or cutting out a given range: :func:`.dataproc.utils.cut_to_range` and :func:`.dataproc.utils.cut_out_regions`.
    - Converting between 2-column "XY" and complex representations: :func:`.dataproc.utils.xy2c` and :func:`.dataproc.utils.c2xy`
    - Scalar numerical utilities: :func:`.utils.numerical.limit_to_range` (limit a value to lie in a given range, including option for no limits in one or both directions), :func:`.utils.numerical.gcd` and :func:`.utils.numerical.gcd_approx` (greatest common divisor or its approximate version for non-integer values)