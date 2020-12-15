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
py.test tests/race_condition/test_race.py -k "test_should_simulate_race_condition"
```
It should succeed.

If we remove the lock like this:
```python
def lock_object(e: Dict[str, str]) -> bool:
    log.info(f"lock object {e['id']}")
    # with my_store_lock:
    #     if e["status"] == "pending":
    #         e["status"] = "in_progress"
    #         return True
    # 
    # return False
    return True
```
and run the test again, 
it should fail because `handle_object` has been called 4 times instead of twice. 

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
