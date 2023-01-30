.. _stages_basics:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices_basics>`.

Stages control basics
======================================

Basic example
--------------------------------------

Almost all stages implement the same basic functionality for moving, stopping, homing, and querying the status::

    stage = Thorlabs.KinesisMotor("27000001")  # connect to the stage
    stage.home()  # home the stage
    stage.wait_for_home()  # wait until homing is done
    stage.move_by(1000)  # move by 1000 steps
    stage.wait_move()  # wait until moving is done
    stage.jog("+")  # initiate jog (continuous move) in the positive direction
    time.sleep(1.)  # wait for 1 second
    stage.stop()  # stop the motion
    stage.close()

Some stages will miss some of this functions (e.g., no homing), but if it's present, it works roughly in the same manner.

Some concepts are explained below in more detail.

Basic concepts
--------------------------------------

Counters, encoders, homing, and limit switches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stages have two basic strategies for keeping track of the position. The first one is counting the steps. The problem with it is that once the device is powered up, its position in unknown. Hence, it requires some kind of homing procedure, which usually involves moving to a predefined position and zeroing out the step counter there. This position is defined by the hardware, usually in the form of a limit switch: a physical switch located at the end of the stage travel range, which changes the state when the stage reaches its position. It also usually automatically turns off the motion when tripped, to prevent the motor from overheating or the stage from breaking.

When stepper motors are used, the size of each step (or microstep, if used) is a reasonably well-defined fraction of a turn, so counting them gives fairly reproducible results. On the other hand, piezo slip-stick sliders (such as Attocube, SmarAct, or Picomotor) have inherently unreliable steps size which depends on, e.g., load, direction, position, temperature, or other environmental factors. In this case steps counting, while possible, usually leads to long-term drifts.

If the reliable counting is impossible, like in the case of sliders or regular DC (as opposed to stepper) motors, the manufacturer might add a hardware position readout. It can be digital (encoder) or analog (e.g., resistive, capacitive, or optical readout). The first kind is generally simpler, cheaper and more reliable, but the second one can provide much higher resolution, and can work in more extreme environments (high vacuum, cryogenics). In both cases, the controllers would typically have some kind of feedback loop to smoothly control the motion speed and direction to approach a given position.


Steps and real coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Almost all stages allow control or readout of position in motor steps, encoder steps, or some other internal units. It is usually not straightforward, or sometimes even impossible, to convert those to real units. In cases where it is possible, it is defined by the motor gearbox and the screw pitch (for linear stages); in most cases, this ratio is provided in the motor or translation stage manual (which can be different from the motor controller manual, and the two might even be completely independent). Sometimes, one even has to do explicit calculations, e.g., getting the number of microsteps per revolution from the controller and motor manufacturer, and the displacement per step from the stage manufacturer.


Speed control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In many cases, the motor speed is ramped up and down linearly rather than abruptly; hence, both the "cruising" speed and the ramping acceleration can, in principle, be configured. Usually they are defined in, respectively, steps/s and steps/s^2, although sometimes internal units have to be used.




Application notes and examples
-------------------------------------------

Here we talk more practically about using pylablib to perform common tasks.


Motion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most standard motion methods are ``move_to``, which moves to a specified position, ``move_by``, which moves by a specified distance or number of steps, and ``jog``, which moves continuously in a given direction until stopped or run into a limit switch. If both ``move_to`` and ``move_by`` are present, they usually perform the same operation under the hood: ``stage.move_by(s)`` and ``stage.move_to(stage.get_position()+s)`` yield the same result.

In almost all cases these commands are asynchronous, in the sense that they simply initialize the motion and continue immediately::

    >> stage.move_by(1000)
    >> stage.is_moving()  # the stage is moving, but the execution continues
    True
    >> time.sleep(1.)
    >> stage.is_moving()  # after 1s the motion is done
    False

To stop immediately (which is usually only used with ``jog`` commands) you can use the ``stop`` method. In some cases, there are two different stop kinds: "soft" with a ramp-down, or "hard" which immediately ceases motion.


Status and synchronization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the motion commands are asynchronous, the devices provide two methods to synchronize it with the script execution. The first one, ``is_moving``, checks if the stage is currently in motion. The second one, ``wait_move``, pauses the execution until the stage motion is finished.

In addition, many stages provide methods to obtain additional information, e.g., ``get_status`` (which, usually, returns state of motion, limit switches, possible errors, etc.), or ``get_current_speed``.


Position readout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a stage has position readout (either hardware sensor, or step counting), it is implemented with the ``get_position`` method. In most cases, it will be accompanied with the ``set_position_reference`` method, which lets one change the currently stored position, effectively adding an offset to all further position readings::

    >> stage.get_position()
    10000
    >> stage.set_position_reference(20000)  # change current reference to 
    >> stage.get_position()  # note that it reacts immediately, unlike move_to; no physical motion happened
    20000
    >> stage.move_to(21000)  # move by 1000 steps; equivalent to .move_by(1000), or .move_to(11000) before the reference change

Note that it only changes the internal counter state, and does not cause any stage motion (which is performed by ``move_to``).


Axis selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many controllers support simultaneous control of several different motors. In this case, all of their methods take an additional ``axis`` (in most cases) or ``channel`` argument, which specify the exact motor. In cases where usually only one motor is controlled (e.g., TMCM1110 or Thorlabs KDC101), this parameters is set to the default value, and is closer to the end of the parameter list. If having multiple controlled stages is the default (e.g., Attocube ANC350 or Arcus Performax), this parameter is usually the first one, and it has to be specified. In this cases, the methods frequently allow to set this parameter to ``"all"``, which means that the action is performed for all axes, or the results is returned for all axes (usually in a form of a list or a dictionary).

The channels are usually specified by their index starting from 0 or 1, although some stages adopt a different labeling (e.g., Arcus Performax labels them as X, Y, Z, and U). The exact specification is given in the specific class description.


Homing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As mentioned above, often stages require homing to get absolute position readings. It needs to be done every time the stage is power-cycled, but the homing parameters usually persist between different re-connections.

If homing is implemented, it is done using the ``home`` method. In addition, there can also be an ``is_homed`` method, which checks if the homing has already been performed. If the method is present, then by default ``home`` will not execute if ``is_homed`` returns ``True``, unless forced.

Some stages do not have an explicit homing method, but can be manually homed by, e.g., running the stage to the limit switch and setting the position reference to 0.