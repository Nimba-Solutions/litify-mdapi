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
    Log    Operating System: ${os_info}    level=INFO
    Log    PATH: ${path}    level=INFO
    Log    Working Directory: ${CURDIR}    level=INFO

Log Browser Options
    [Documentation]    Logs the browser configuration being used
    ${browser_exists}    ${browser} =    Run Keyword And Ignore Error    Set Variable    ${BROWSER}
    Run Keyword If    '${browser_exists}' == 'PASS'
    ...    Log    Browser: ${browser}    level=INFO
    ...    ELSE
    ...    Log    Browser variable not set    level=INFO
    
    ${options_exists}    ${options} =    Run Keyword And Ignore Error    Set Variable    ${BROWSER_OPTIONS}
    Run Keyword If    '${options_exists}' == 'PASS'
    ...    Log    Browser Options: ${options}    level=INFO
    ...    ELSE
    ...    Log    Browser options not set    level=INFO
    
    ${timeout_exists}    ${timeout} =    Run Keyword And Ignore Error    Set Variable    ${TIMEOUT}
    Run Keyword If    '${timeout_exists}' == 'PASS'
    ...    Log    Timeout: ${timeout}    level=INFO
    ...    ELSE
    ...    Log    Timeout not set    level=INFO
