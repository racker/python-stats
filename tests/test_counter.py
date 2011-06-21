import sys
import unittest

from pystats.counter import Counter, Health, count_calls
from pystats.counter import CounterEnum, OpsEnum

class CounterTestCase(unittest.TestCase):
  def setUp(self):
    self.counter = Counter()
    super(CounterTestCase, self).setUp()

  def test_add(self):
    self.assertTrue('key1' not in self.counter._dcount)
    self.counter.add('key1')
    self.assertEqual(self.counter._dcount['key1'], 1)
    self.counter.add('key1', 2)
    self.assertEqual(self.counter._dcount['key1'], 3)

  def test_set_type(self):
    self.assertTrue('key1' not in self.counter._dcount)
    self.counter.add('key1')
    self.assertTrue('key1' not in self.counter._dt)
    self.counter.set_type('key1', 'int')
    self.assertEqual(self.counter._dt['key1'], 'int')

  def test_count_calls_decorator(self):
    @count_calls(counter=self.counter)
    def my_func():
      pass

    self.assertTrue('func_my_func' not in self.counter._dcount)
    my_func()
    self.assertEqual(self.counter._dcount['func_my_func'], 1)
    my_func()
    self.assertEqual(self.counter._dcount['func_my_func'], 2)

  def test_inc_ops_and_dec_ops(self):
    self.counter.inc_ops('key1')
    self.assertEqual(self.counter._dops['key1'][OpsEnum.TOTAL], 1)
    self.assertEqual(self.counter._dops['key1'][OpsEnum.PENDING], 1)

    self.counter.dec_ops('key1')
    self.assertEqual(self.counter._dops['key1'][OpsEnum.TOTAL], 1)
    self.assertEqual(self.counter._dops['key1'][OpsEnum.PENDING], 0)

    self.counter.inc_ops('key1')
    self.counter.inc_ops('key1')
    self.assertEqual(self.counter._dops['key1'][OpsEnum.TOTAL], 3)
    self.assertEqual(self.counter._dops['key1'][OpsEnum.PENDING], 2)

  def test_add_avg(self):
    self.counter.add_avg('key1', 5)
    self.assertTrue('key1' not in self.counter._dcount)

    vals = self.counter._davg['key1']
    self.assertEqual(vals[CounterEnum.COUNTER], 1)
    self.assertEqual(vals[CounterEnum.SUM], 5)
    self.assertEqual(vals[CounterEnum.MIN], 5)
    self.assertEqual(vals[CounterEnum.MAX], 5)

    self.counter.add_avg('key1', 4)
    self.assertEqual(vals[CounterEnum.COUNTER], 2)
    self.assertEqual(vals[CounterEnum.SUM], 9)
    self.assertEqual(vals[CounterEnum.MIN], 4)
    self.assertEqual(vals[CounterEnum.MAX], 5)

    self.counter.add_avg('key1', 1)
    self.assertEqual(vals[CounterEnum.COUNTER], 3)
    self.assertEqual(vals[CounterEnum.SUM], 10)
    self.assertEqual(vals[CounterEnum.MIN], 1)
    self.assertEqual(vals[CounterEnum.MAX], 5)

    metric = self._get_metric(counter=self.counter, key='key1_avg')
    self.assertEqual(metric['value'], ((5 + 4 + 1) / 3))

  def test_health_state_change(self):
    self.assertEqual(self.counter.health, Health.OK)
    self.counter.set_health(health=Health.ERR)
    self.assertEqual(self.counter.health, Health.ERR)
    self.counter.set_health(health=Health.WARN)
    self.assertEqual(self.counter.health, Health.WARN)
    self.counter.set_health(health=Health.OK)
    self.assertEqual(self.counter.health, Health.OK)

  def test_bind(self):
    def func(value):
      return value

    self.assertTrue('key2' not in self.counter._dcount)
    self.counter.add('key2', 111)

    self.counter.bind('key1', 'float', func, 'key2')
    self.assertTrue('key1' not in self.counter._dcount)

    self.counter.add_avg('key1', 1)
    self.counter.add_avg('key1', 100)
    self.counter.add_avg('key1', 20)

    metric = self._get_metric(counter=self.counter, key='key1')
    self.assertEqual(metric['value'], 111)

  def _get_metric(self, counter, key):
    metrics = counter.get_metrics()
    for item in metrics:
      if item['name'] == key:
        return item

    return None

if __name__ == '__main__':
  sys.exit(unittest.main())
