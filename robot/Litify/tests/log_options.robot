*** Settings ***
Library         OperatingSystem
Library         SeleniumLibrary

*** Keywords ***
Verify Robot Framework
    [Documentation]    Verifies that Robot Framework is running correctly and prints session details
    Log Environment Details
    Log Browser Options

Log Environment Details
    [Documentation]    Logs details about the execution environment
    ${os_info}=       Get Environment Variable    OS    default=Unknown
    ${path}=          Get Environment Variable    PATH    default=Unknown
    Log    Operating System: ${os_info}    level=INFO
    Log    PATH: ${path}    level=INFO
    Log    Working Directory: ${CURDIR}    level=INFO
    ${chrome_path}=    Run Process    which chrome    shell=True
    Log    Chrome Path: ${chrome_path.stdout}    level=INFO
    ${chrome_version}=    Run Process    chrome --version    shell=True
    Log    Chrome Version: ${chrome_version.stdout}    level=INFO

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

    # Log Chrome-specific details if browser is Chrome
    Run Keyword If    '${browser_exists}' == 'PASS' and '${browser}' == 'chrome'    Log Chrome Details

Log Chrome Details
    [Documentation]    Logs detailed information about Chrome configuration
    ${tmp_dirs}=    Run Process    ls -la /tmp/chrome*    shell=True
    Log    Chrome temp directories: ${tmp_dirs.stdout}    level=INFO
    
    ${chrome_procs}=    Run Process    ps aux | grep -i chrome    shell=True
    Log    Running Chrome processes: ${chrome_procs.stdout}    level=INFO
    
    ${chrome_binary}=    Run Process    ls -la /app/.chrome-for-testing/chrome-linux64/chrome    shell=True
    Log    Chrome binary details: ${chrome_binary.stdout}    level=INFO
    
    # Try to get Chrome capabilities if webdriver is active
    ${status}    ${capabilities}=    Run Keyword And Ignore Error
    ...    Get WebDriver Capabilities
    Run Keyword If    '${status}' == 'PASS'
    ...    Log    Chrome capabilities: ${capabilities}    level=INFO
    ...    ELSE
    ...    Log    Could not get Chrome capabilities: ${capabilities}    level=INFO
