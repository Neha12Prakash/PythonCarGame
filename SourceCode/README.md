# Author: Neha Prakash

## Overview

This is an alternative implementation of the [pyhop](https://bitbucket.org/dananau/pyhop/src/master/)
planner created by [Dana Nau](http://www.cs.umd.edu/~nau/). Here are the main modifications:
* Each planner, defined by a set of operators and methods, is instantiated as 
  an object of the `Planner` class. This allows multiple distinct planners to 
  coexist in a single program.
* Operators and Methods return `None` when they are not applicable.
* Methods return a `TaskList` object to specify what should happen next. 
  `TaskList` objects represent the following scenarios:
  * Successful plan completion
  * Exactly one task list option.
  * Multiple task list options, one of which is to be selected nondeterministically
    by the planner.
* Methods are declared in the same way as operators, by simply listing the Python functions corresponding to the  
  methods. Alternative task lists for a given method are then specified by using nondeterministic task options.
* States and goals are consolidated into a single data type. Printing states
  is simplified by the implementation of a `__repr__()` method.

## HTN Planning

Pyhop is a hierarchical task network (HTN) planner. To use an HTN planner, one must specify the following:

* **State**: Complete description of the current world state. In Pyhop, you can use an arbitrary Python data structure to describe the state.
* **Operators**: Each operator describes a state transformation. Operators can optionally include preconditions. If a precondition is not met, the operator will fail. In Pyhop, you will write one Python function for each operator.
* **Methods**: Methods encode a planning algorithm that decomposes a task into operators and other methods. In Pyhop, you will write one Python function for each method.


## Installation

```
pip3 install git+https://github.com/gjf2a/pyhop_anytime
```

## License

Following the original 
[pyhop](https://bitbucket.org/dananau/pyhop/src/master/) implementation, 
this project is licensed under the 
[Apache License, Version 2.0 (the "License")](http://www.apache.org/licenses/LICENSE-2.0).

