python-stats
============

Python library for recording application-specific metrics.

Library has been decoupled from Cloudkick internal code base and it currently
only exposes a single class - `Counter`.

Installation
============

```` bash
pip install pystats
````

Usage
======

```` python
from pystats.counter import Counter

counter = Counter()

# Increase the counter
counter.add('key_name', 1)

# Change the metric type (by default each metric type is float)
counter.set_type('key_name', 'float|int|gauge')

# Count how many time function has been executed (it basically just increased
# the counter where the counter key is a function name)
@count_calls
my_function('foo', '3', 55)

# Add average - minimum, maximum and average values will automatically be
# calculated and tracked for this key
counter.add_avg('key_name', value, type='float')

# Increase operation count
# This will increase the total and pending operational count for the provided
# key
counter.inc_ops('key_name')

# Mark pending operation as finished
# This will decrease the pending operation count for the provided key
counter.dec_ops('key_name')

# Change the counter status / health to "error"
counter.bad()

# Retrieve counter health
health = counter.health

# Retrieve all the metrics
metrics = counter.get_metrics(include_uptime=True)

# Retrieve counter stats object which contains all the metrics and counter
# health

stats = counter.to_stats()
````
