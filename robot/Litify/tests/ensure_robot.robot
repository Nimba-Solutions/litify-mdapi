*** Settings ***
Library         OperatingSystem

*** Tasks ***
Verify Robot Framework
    [Documentation]    Verifies that Robot Framework is running correctly and prints session details
    Log Environment Details
    Log Browser Options

*** Keywords ***
Log Environment Details
    [Documentation]    Logs details about the execution environment
    ${os_info}=       Get Environment Variable    OS    default=Unknown
    ${path}=          Get Environment Variable    PATH    default=Unknown
    Log    Operating System: ${os_info}
    Log    PATH: ${path}
    Log    Working Directory: ${CURDIR}

Log Browser Options
    [Documentation]    Logs the browser configuration being used
    ${status}    ${value} =    Run Keyword And Ignore Error    Variable Should Exist    ${BROWSER}
    Run Keyword If    '${status}' == 'PASS'    Log    Browser: ${BROWSER}
    ...    ELSE    Log    Browser variable not set
    
    ${status}    ${value} =    Run Keyword And Ignore Error    Variable Should Exist    ${BROWSER_OPTIONS}
    Run Keyword If    '${status}' == 'PASS'    Log    Browser Options: ${BROWSER_OPTIONS}
    ...    ELSE    Log    Browser options not set
    
    ${status}    ${value} =    Run Keyword And Ignore Error    Variable Should Exist    ${TIMEOUT}
    Run Keyword If    '${status}' == 'PASS'    Log    Timeout: ${TIMEOUT}
    ...    ELSE    Log    Timeout not set
