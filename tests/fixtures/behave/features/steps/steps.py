from behave import given


@given(u"there is a proper Behave project set up")
def step_impl(context):
    raise NotImplementedError(u"STEP: Given there is a proper Behave project set up")


@when(u"I behave is executed through AnyTest")
def step_impl(context):
    raise NotImplementedError(u"STEP: When I behave is executed through AnyTest")


@then(u"tests are run")
def step_impl(context):
    raise NotImplementedError(u"STEP: Then tests are run")
