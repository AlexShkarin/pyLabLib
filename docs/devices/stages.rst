.. _stages:

.. note::
    General device communication concepts are described on the corresponding :ref:`page <devices>`.

Stages
======================================

Basic example
--------------------------------------

Almost all stages implement the same basic functionality for homing, motion, stopping, and querying the status::

    stage = Thorlabs.KinesisMotor("27000001")  # connect to the stage
    stage.home()  # home the stage
    stage.wait_for_home()  # wait until homing is done
    stage.move_by(1000)  # move by 1000 steps
    stage.wait_move()  # wait until moving is done
    stage.jog("+")  # initiate jog (continuous move) in the given direction
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

When stepper motors are used, the size of each step (or microstep) is a (reasonably) well-defined fraction of a turn, so counting them gives fairly reproducible results. However, piezo slip-stick sliders (such as Attocube or SmarAct) have inherently unreliable steps size which depends on, e.g., load, direction, position, temperature, or other environmental factors. In this case steps counting, while possible, usually leads to long-term drifts.

If the reliable counting is impossible, like in the case of sliders or regular (as opposed to stepper) motors, the manufacturer might add a hardware position readout. It can be digital (encoder) or analog (e.g., resistive, capacitive, or interferometric readout). The first kind is generally simpler, cheaper and more reliable, but the second one can provide much higher resolution, and can work in more extreme environments (high vacuum, cryogenics). In both cases, the controllers would typically have some kind of feedback loop to smoothly control the motion speed to approach a given position.


Steps and real coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Almost all stages allow control or readout of position in motor steps, encoder steps, or some other internal units. It is usually not straightforward, or sometimes even impossible, to convert those to real units. In cases where it is possible, it is defined by the motor gearbox and the screw pitch (for linear stages); in most cases, this ratio is provided in the motor or translation stage manual (which can be different from the motor controller manual, and the two might even be completely independent). Sometimes, one even has to do explicit calculations, e.g., getting the number of microsteps per revolution from the controller and motor manufacturer, and the displacement per step from the stage manufacturer.


Speed control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In many cases, the motor speed is ramped up and down linearly rather than abruptly; hence, both the "cruising" speed and the ramping acceleration can, in principle, be configured. Usually they are defined in, respectively, steps/s and steps/s^2, although sometimes internal units have to be used.




Application notes and examples
-------------------------------------------

Here we talk more practically about performing tasks common to most stages.



Currently supported stages
-------------------------------------------