
import logging.handlers
from typing import Callable, Any, Iterable
import logging
import sys
import re

class Test():
    def __init__(self, name:str, testedMethod: Callable, parameters:list|dict, expectedResults:Any|None=None):
        self._name = "TC_" + name.replace("\n", "_").replace(" ", "_").upper()
        self._id = -1
        self._tested_method = testedMethod
        self._params = parameters
        self._expected_res = expectedResults
        self._last_run_result = None
        self._logger:logging.Logger = logging.getLogger(self._name)
        self._logger.setLevel(level=logging.INFO)
    
    def set_id(self, n_id:int):
        self._id = n_id

    @property
    def name(self):
        name = self._name
        if self._id != -1:
            name = "{}_{:05d}".format(name, self._id)
        return name
    
    def __str__(self):
        return self.name
    

    def set_logger(self, parentName:str="", logfile:str|None= None):
        log_name = self.name
        if parentName != "":
            log_name = parentName + "." + log_name
        self._logger:logging.Logger = logging.getLogger(log_name)
        self._logger.setLevel(level=logging.INFO)
        if logfile != None:
            self._logger.addHandler(logging.FileHandler(logfile))
        if parentName == "":
            self._logger.addHandler(logging.StreamHandler(stream=sys.stdout))

    def pre_test(self):
        self._logger.info("Start of Test Case " + self.name)

    def post_test(self):
        self._logger.info("End of Test Case " + str(self))
    
    def run_test(self):
        self.pre_test()
        if self._last_run_result != None:
            self._logger.info("Test Case " + str(self) + " has already been run")
            self._logger.info("Last result will be used : " + str(self._last_run_result))
            return self._last_run_result
        self._logger.info("Test of function : " + str(self._tested_method))
        self._logger.info("With parameters : " + str(self._params))
        self._logger.info("Expected Results is : " + str(self._expected_res))
        if(isinstance(self._params, list)):
            ret = self._tested_method(*self._params)
        else:
            ret = self._tested_method(**self._params)
            
        self._last_run_result = (ret == self._expected_res)
        if not self._last_run_result:
            self._logger.warning("TEST CASE FAILED : Results is " + str(ret))
            return self._last_run_result
        self._logger.warning("TEST CASE SUCCESS : Results is " + str(ret))
        self.post_test()
        return self._last_run_result

class Tester():
    def __init__(self, name: str, desc:str="", logfile:str|None=None, listoftest:Iterable[Test]=[]):

        self._name = name
        self._desc = desc
        self._test_list:Iterable[Test] = listoftest
        
        self._logger:logging.Logger = logging.getLogger(self._name)
        self._logger.setLevel(level=logging.INFO)
        if logfile != None:
            self._logger.addHandler(logging.FileHandler(logfile))
        self._logger.addHandler(logging.StreamHandler(stream=sys.stdout))
        index=0
        for test in self._test_list:
            test.set_logger(self._name)
            test.set_id(index)
            index += 1
    
    @property
    def name(self):
        return self._name

    def get_test_case_by_name(self, tc_pattern:str) -> Iterable[Test]:
        tc_re = re.compile(tc_pattern)
        return filter(function= lambda x : tc_re.search(x.name) != None , iterable=self._test_list)
    
    def run_test_by_name(self, tc_pattern:str):
        for test in self.get_test_case_by_name(tc_pattern=tc_pattern):
            test.run_test()


    def run_test_by_id(self, id:int):
        list(self._test_list)[id].run_test()
    
    def __str__(self):
        return self.name

    def run_all_tests(self)-> bool:
        self._logger.info("Start of test " + str(self) + ":")
        self._logger.info(self._desc)
        testres:bool = True
        for test in self._test_list:
            res = test.run_test()
            self._logger.info(str(res))
            
            testres = False if not res else testres
        if testres: 
            self._logger.info("Test "+ str(self) + " : SUCCESS")
        else:
            self._logger.warning("Test " + str(self) + " : FAIL")
        self._logger.info("End of test " + str(self))

