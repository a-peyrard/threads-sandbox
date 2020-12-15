## Small project to play with threads in python

### Race conditions

This is a playground to see how to unit test race condition.

The main file can be launched using:
```bash
export PYTHONPATH=`pwd`
python threads/race_condition/main.py
```
It will run 2 threads running a function that was having race condition. 

_the race condition have been solved by a lock to reserve an object, 
i.e. changing the status in an atomic way before handling the object._

The unit test can be run like this:
```bash
fixme...
```

### Steps

Here we are just introducing some step context that allow us to control the execution. 
Before executing any command, the runnable function is waiting to be allowed to execute the step, 
and then notifying for completion.

Like that we can have the main thread allowing specific steps to be executed in child steps, 
and control the child threads executions. 
The main file can be launched using:
```bash
export PYTHONPATH=`pwd`
python threads/step/main.py
```

### How to install
- create a virtual environment (virtualenvwrapper is a nice solution)
- `make requirements` will install the requirements
- `make test` will run all the tests
