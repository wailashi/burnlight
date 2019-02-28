# Burnlight
Burnlight is a server and client for automating the control 
of the GPIO pins on a Raspberry Pi.

## Features
- Run custom schedules controlling one or more GPIO pins.
- Web API for remote management and monitoring.
- Paired input and output for feedback on controlled systems.

## Requirements
* [Flask](http://flask.pocoo.org/) - Serves the API.
* [gevent](http://www.gevent.org/) - Runs the scheduling threads.
* [Lark parser](https://github.com/lark-parser/lark) - Parses BSL programs.
* [gpiozero](https://gpiozero.readthedocs.io) - Controls GPIO outputs on Raspberry Pi computers.

## Getting started on Raspbian
Install Burnlight using pip:
```
$ pip install burnlight
```
Start the server:
```
$ burnlightd
```
Create a file `schedule.bsl` with the following contents:
```
{
    loop 10: {
        (On,1),
        (Off,1)
    }
}
```
Add and start the schedule using the client
```
$ burnlight schedules add schedule.bsl --start_time now
```


## Burnlight Scheduling Language (BSL)
Schedules are described with a simple language.

The following program will turn the on output for one second each minute for one hour.

```
{
    loop 60: {
        (On,1),
        (Off,59)
    }
}
```

BSL currently supports programs consisting of sequences of output statements
and loops.

The simplest program possible is `{}`, which will do absolutely nothing.
We can make it slightly more interesting by using _output statements_.
An output statement takes the for `(<state>,<duration>)` where `<state>` is
the desired output state, `On` or `Off`, and `<duration>` is the duration
the output should be in that state in seconds.

The following program turns the output on for ten seconds:
```
{
    (On, 10),
    (Off, 1)
}
```

