.. _dataproc:

=========================
Data processing utilities
=========================


-------
Fitting
-------

Class :class:`.fitting.Fitter` is a user-friendly wrapper around :func:`scipy.optimize.least_squares` routine. Dealing with fitting is made more convenient in a couple of ways:

- it is easy to specify the x-parameter name (in the case it is not the first parameter), or specify multiple x-parameters;
- all of the fit and fixed parameters are specified by name; it is easy to switch between any parameter being fit or fixed;
- the wrapper automatically handles complex parameters (split into real and imaginary parts), numpy arrays, lists, ot tuples (including nested structures);
- the final parameters (fit and fixed) are returned in a single dictionary indexed by their names;
- the wrapper also returns the fit function with all of the parameters bound to the final fit and fixed values;
- the fit function result is flattened during fitting, so it, for example, works for functions returning 2D arrays.

**Examples**

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