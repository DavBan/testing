from testutils import Test


testGlobal=0
ExpectedGlobal = 1
def testGlobalIncr():
    global testGlobal
    testGlobal = testGlobal+1
testedFuncs={
    "Ret_1": lambda :1,
    "Ret_2": lambda :2,
    "Incr_1": lambda x:x+1,
    "Incr_from_GL": lambda : testGlobal+1,
    "Incr_GL": testGlobalIncr

}

testGlobalBool=True
testedHooks=[
    lambda x:True,
    lambda x:False,
    lambda x: x if x is not None else False,
    lambda x: not x,
    lambda x: testGlobalBool,
    lambda x: not testGlobalBool,
    lambda x: testGlobal == ExpectedGlobal
]

testResultList=[
    "{:<55} | Result".format("Test Name"),
    "-"*56 + "+" + "-"*10
    ]

def testing_test(test:Test, expected:bool=True):
    if test.run_test() == expected:
        print("Success")
        testResultList.append("{:<55} | Success".format(test.name))
    else:
        print("Fail")
        testResultList.append("{:<55} | Failed ".format(test.name))

def print_results():
    for result in testResultList:
        print(result)

test = Test("test_expected",testedFuncs["Ret_1"],[],1)
testing_test(test)
testing_test(test)

print("")
print("")



test = Test("test_unexpected",testedFuncs["Ret_2"],[], 1)
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("test_expected_change_expected_no_rst",testedFuncs["Ret_1"],[], 1)
testing_test(test, True)
test._expected_res = 2
testing_test(test, True)

print("")
print("")

test = Test("test_expected_change_expected_rst",testedFuncs["Ret_1"],[], 1)
testing_test(test, True)
test._expected_res = 2
test.reset_test()
testing_test(test, False)

print("")
print("")


test = Test("test_expected_calculus",testedFuncs["Incr_1"],[1], 2)
testing_test(test)
testing_test(test)

print("")
print("")

test = Test("test_expected_calculus_change_param_no_rst",testedFuncs["Incr_1"],[1], 2)
testing_test(test)
test._params=[2]
testing_test(test)

print("")
print("")

test = Test("test_expected_calculus_change_param_rst",testedFuncs["Incr_1"],[1], 2)
testing_test(test)
test._params=[2]
test.reset_test()
testing_test(test, False)

print("")
print("")

test = Test("Test_PretestHook_True_Expected", testedFuncs["Ret_1"], [], 1, testedHooks[0])
testing_test(test)
testing_test(test)

print("")
print("")

test = Test("Test_PretestHook_True_Unexpected", testedFuncs["Ret_1"], [], 2, testedHooks[0])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("Test_PretestHook_False_Expected", testedFuncs["Ret_1"], [], 1, testedHooks[1])
testing_test(test, False)
testing_test(test, False)


print("")
print("")

test = Test("Test_PretestHook_False_Unexpected", testedFuncs["Ret_1"], [], 2, testedHooks[1])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("Test_PretestHook_True_Change_To_False", testedFuncs["Ret_1"], [], 1, testedHooks[0])
testing_test(test, True)
test.set_pretest_hook(testedHooks[1])
testing_test(test, False)

print("")
print("")

test = Test("Test_PretestHook_paththrough", testedFuncs["Ret_1"], [], 1, testedHooks[2])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("Test_PretestHook_paththrough_inverted", testedFuncs["Ret_1"], [], 1, testedHooks[3])
testing_test(test, True)
testing_test(test, True)

print("")
print("")

test = Test("Test_PretestHook_Global_True", testedFuncs["Ret_1"], [], 1, testedHooks[4])
testing_test(test, True)
testing_test(test, True)

print("")
print("")

test = Test("Test_PretestHook_Global_True_inverted", testedFuncs["Ret_1"], [], 1, testedHooks[5])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

testGlobalBool = False
test = Test("Test_PretestHook_Global_False", testedFuncs["Ret_1"], [], 1, testedHooks[4])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("Test_PretestHook_Global_False_inverted", testedFuncs["Ret_1"], [], 1, testedHooks[5])
testing_test(test, True)
testing_test(test, True)

print("")
print("")

testGlobalBool = True
test = Test("Test_PretestHook_Global_True_Change_False_no_rst", testedFuncs["Ret_1"], [], 1, testedHooks[4])
testing_test(test, True)
testGlobalBool = False
testing_test(test, True)

print("")
print("")

testGlobalBool = True
test = Test("Test_PretestHook_Global_True_Change_False_rst", testedFuncs["Ret_1"], [], 1, testedHooks[4])
testing_test(test, True)
testGlobalBool = False
test.reset_test()
testing_test(test, False)

print("")
print("")

test = Test("Test_PostHoook_True_Expected", testedFuncs["Ret_1"], [], 1, posttest_hook=testedHooks[0])
testing_test(test, True)
testing_test(test, True)

print("")
print("")

test = Test("Test_PostHoook_True_Unexpected", testedFuncs["Ret_1"], [], 2, posttest_hook=testedHooks[0])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("Test_PostHoook_False_Expected", testedFuncs["Ret_1"], [], 1, posttest_hook=testedHooks[1])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("Test_PostHoook_False_Unexpected", testedFuncs["Ret_1"], [], 2, posttest_hook=testedHooks[1])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

test = Test("Test_PostHoook_True_Change_to_false_no_rst", testedFuncs["Ret_1"], [], 1, posttest_hook=testedHooks[0])
testing_test(test, True)
test.set_posttest_hook(testedHooks[1])
testing_test(test, False)

print("")
print("")

testGlobal=1
test = Test("Test_Incr_Global_No_PostHook", testedFuncs["Incr_GL"], [])
testing_test(test, True)
testing_test(test, True)

print("")
print("")

testGlobal=1
ExpectedGlobal = 2
test = Test("Test_Incr_Global_PostHook_Expected", testedFuncs["Incr_GL"], [], posttest_hook=testedHooks[6])
testing_test(test, True)
testing_test(test, True)

print("")
print("")

testGlobal=1
ExpectedGlobal = 3
test = Test("Test_Incr_Global_PostHook_UnExpected", testedFuncs["Incr_GL"], [], posttest_hook=testedHooks[6])
testing_test(test, False)
testing_test(test, False)

print("")
print("")

testGlobal=1
ExpectedGlobal = 3
test = Test("Test_Incr_Global_PostHook_UnExp_change_to exp no_rst", testedFuncs["Incr_GL"], [], posttest_hook=testedHooks[6])
testing_test(test, False)
testGlobal = 2
testing_test(test, False)

print("")
print("")

testGlobal=1
ExpectedGlobal = 3
test = Test("Test_Incr_Global_PostHook_UnExp_change_to exp rst", testedFuncs["Incr_GL"], [], posttest_hook=testedHooks[6])
testing_test(test, False)
testGlobal = 2
test.reset_test()
testing_test(test, True)

print("")
print("")

testGlobal=1
test = Test("Test_Incr_from_Global_exp", testedFuncs["Incr_from_GL"], [], 2)
testing_test(test, True)
testing_test(test, True)

print("")
print("")

testGlobal=1
test = Test("Test_Incr_from_Global_unexp", testedFuncs["Incr_from_GL"], [], 3)
testing_test(test, False)
testing_test(test, False)

print("")
print("")

testGlobal=1
test = Test("Test_Incr_from_Global_unexp_to_exp_no_rst", testedFuncs["Incr_from_GL"], [], 3)
testing_test(test, False)
testGlobal=2
testing_test(test, False)

print("")
print("")

testGlobal=1
test = Test("Test_Incr_from_Global_unexp_to_exp_rst", testedFuncs["Incr_from_GL"], [], 3)
testing_test(test, False)
testGlobal=2
test.reset_test()
testing_test(test, True)


print("")
print("")




print_results()