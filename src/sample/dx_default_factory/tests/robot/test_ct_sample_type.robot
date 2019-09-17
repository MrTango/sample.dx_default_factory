# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s sample.dx_default_factory -t test_sample_type.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src sample.dx_default_factory.testing.SAMPLE_DX_DEFAULT_FACTORY_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/sample/dx_default_factory/tests/robot/test_sample_type.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a SampleType
  Given a logged-in site administrator
    and an add SampleType form
   When I type 'My SampleType' into the title field
    and I submit the form
   Then a SampleType with the title 'My SampleType' has been created

Scenario: As a site administrator I can view a SampleType
  Given a logged-in site administrator
    and a SampleType 'My SampleType'
   When I go to the SampleType view
   Then I can see the SampleType title 'My SampleType'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add SampleType form
  Go To  ${PLONE_URL}/++add++SampleType

a SampleType 'My SampleType'
  Create content  type=SampleType  id=my-sample_type  title=My SampleType

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the SampleType view
  Go To  ${PLONE_URL}/my-sample_type
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a SampleType with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the SampleType title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
