#####################
# LOAD DEPENDENCIES #
#####################

import unittest, os
import linref as lr
import pandas as pd


##################
# LOAD TEST DATA #
##################
data = {}
fd = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
labels = [os.path.splitext(fn)[0] for fn in os.listdir(fd)]
print(labels)
for fp in os.listdir(fd):
    label = os.path.splitext(os.path.basename(fp))
    data[label] = pd.read_csv(os.path.join(fd, fp))


#####################
# DEFINE TEST CASES #
#####################

class TestInitCollection(unittest.TestCase):

    def test_init_basic(self):
        ec = lr.EventsCollection(
            data['linear_events'], keys=['RID','YEAR'], beg='BMP', end='EMP')
        self.assertIsInstance(ec, lr.EventsCollection)

    def test_init_standard(self):
        ec = lr.from_standard(data['linear_events'])
        self.assertIsInstance(ec, lr.EventsCollection)

    def test_init_bad_targets(self):
        self.assertRaises(ValueError,
            lr.EventsCollection(
                data['linear_events'],
                keys=['ASDF','YEAR'],
                beg='BMP', end='EMP'))
        self.assertRaises(ValueError,
            lr.EventsCollection(
                data['linear_events'],
                keys=['RID','YEAR'],
                beg='ASDF', end='EMP'))
        self.assertRaises(ValueError,
            lr.EventsCollection(
                data['linear_events'],
                keys=['RID','YEAR'],
                beg='BMP', end='ASDF'))

    def test_init_unsorted(self):
        ec_sorted = lr.from_standard(
            data['linear_events'].sort_values(['RID','YEAR','BMP','EMP']))
        ec_unsorted = lr.from_standard(
            data['linear_events'])
        self.assertFalse(ec_sorted.df.equals(ec_unsorted.df))


class TestIntersecting(unittest.TestCase):

    def test_intersecting(self):
        """
        Test basic use of intersecting on EventsGroup.
        """
        ec = lr.from_standard(data['linear_events'])
        df = ec['A', 2020].intersecting(0.55, 1.05)
        self.assertTrue(df.equals(data['linear-events_dissolve']))


class TestDissolve(unittest.TestCase):

    def test_dissolve(self):
        """
        Test basic use of dissolve on lr.EventsCollection.
        """
        ec = lr.from_standard(data['linear_events'])
        df = ec.dissolve(attr=['A'], aggs=['B'], agg_func=list, fillna='z').df
        self.assertTrue(df.equals(data['linear_events_dissolve']))


#############
# RUN TESTS #
#############

if __name__ == '__main__':
    unittest.main()