import unittest
import stdconst
from ConstructionTime import ConstructionTimeCalculator

import os


PATH = os.getcwd() + '/sheets/ConstructionSpreadSheet1.csh';
PATH2 = os.getcwd() + '/sheets/ConstructionSpreadSheet2.csh';


TEST1PATH = os.getcwd() + '/test_sheets/test_overhead.csh';
TEST2PATH = os.getcwd() + '/test_sheets/test_overhead2.csh';
TEST3PATH = os.getcwd() + '/test_sheets/test_overhead3.csh';


 
constr = ConstructionTimeCalculator();
constr.add_functions({'apply_overhead': stdconst.apply_overhead, 'ignore': stdconst.ignore, 'mutate': stdconst.mutate,
                                'quadratic_mutate': stdconst.quadratic_mutate, 'sqrt': stdconst.sqrt});


class TestStringMethods(unittest.TestCase):



    def test_worksheet_one(self):
        constr.clear();
        constr.import_spreadsheet(PATH);

        self.assertAlmostEqual(constr.calculate(), 165.0, places=1);

    def test_worksheet_two(self):
        constr.clear();
        constr.import_spreadsheet(PATH2);

        self.assertAlmostEqual(constr.calculate(), 2344.54, places=1);


    def test_overhead(self):
        constr.clear();
        constr.import_spreadsheet(TEST1PATH);

        self.assertAlmostEqual(constr.calculate(), 110.0, places=1);

    def test_overhead2(self):
        constr.clear();
        constr.import_spreadsheet(TEST2PATH);

        self.assertAlmostEqual(constr.calculate(), 10.0, places=1);

    def test_overhead3(self):
        constr.clear();
        constr.import_spreadsheet(TEST3PATH);

        self.assertAlmostEqual(constr.calculate(), 10000.0, places=1);

if __name__ == '__main__':
    unittest.main();