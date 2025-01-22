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
    ${browser_exists}    ${browser} =    Run Keyword And Ignore Error    Set Variable    ${BROWSER}
    Run Keyword If    '${browser_exists}' == 'PASS'
    ...    Log To Console    \nBrowser: ${browser}
    ...    ELSE
    ...    Log To Console    \nBrowser variable not set
    
    ${options_exists}    ${options} =    Run Keyword And Ignore Error    Set Variable    ${BROWSER_OPTIONS}
    Run Keyword If    '${options_exists}' == 'PASS'
    ...    Log To Console    \nBrowser Options: ${options}
    ...    ELSE
    ...    Log To Console    \nBrowser options not set
    
    ${timeout_exists}    ${timeout} =    Run Keyword And Ignore Error    Set Variable    ${TIMEOUT}
    Run Keyword If    '${timeout_exists}' == 'PASS'
    ...    Log To Console    \nTimeout: ${timeout}
    ...    ELSE
    ...    Log To Console    \nTimeout not set
