import unittest
import paramunittest

@paramunittest.parametrized(
    (22,10),
    (22,20)
)

class UtestParamunittest(paramunittest.ParametrizedTestCase):
    def setParameters(self, numa, numb):
        self.numa=numa
        self.numb=numb
    def test_number(self):
        print('numa={},numb={}'.format(self.numa,self.numb))
        self.assertGreater( self.numa, self.numb)


if __name__=='__main__':
    unittest.main()