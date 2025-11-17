*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  test
    Set Password  1234
    Set Password Confirmation  1234
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  a
    Set Password  1234
    Set Password Confirmation  1234
    Click Button  Register
    Username Should Be Too Short

Register With Valid Username And Too Short Password
    Set Username  abcde
    Set Password  1
    Set Password Confirmation  1
    Click Button  Register
    Password Should Be Too Short

Register With Valid Username And Invalid Password
    Set Username  abcde
    Set Password  aa^¨¤
    Set Password Confirmation  aa^¨¤
    Click Button  Register
    Password Should Be Invalid

Register With Nonmatching Password And Password Confirmation
    Set Username  abcde
    Set Password  1234
    Set Password Confirmation  qwerty
    Click Button  Register
    Passwords Should Not Match

Register With Username That Is Already In Use
    Set Username  abcde
    Set Password  1234
    Set Password Confirmation  1234
    Click Button  Register
    Go To Register Page
    Set Username  abcde
    Set Password  qwerty
    Set Password Confirmation  qwerty
    Click Button  Register
    Username Should Be Already In Use

*** Keywords ***
Register Should Succeed
    Welcome Message Should Be Visible

Username Should Be Too Short
    Error message about too short username should be visible

Password Should Be Too Short
    Error message about too short password should be visible

Password Should Be Invalid
    Error message about invalid password should be visible

Passwords Should Not Match
    Error message about non-matching passwords should be visible

Username Should Be Already In Use
    Error message about username already in use should be visible

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  id=password_confirmation  ${password}


*** Keywords ***
Reset Application And Go To Register Page
    Reset Application
    Go To Register Page