*** Settings ***
Resource    cumulusci/robotframework/Salesforce.robot

*** Test Cases ***
Log Chrome Options
    Open Test Browser
    ${options}=    Get Environment Variable    BROWSER_OPTIONS    default=None
    Log To Console    \n=== CHROME OPTIONS FROM ENVIRONMENT ===
    Log To Console    ${options}
    
    ${selenium}=    Get Library Instance    SeleniumLibrary
    ${driver}=    Get WebDriver
    Log To Console    \n=== CHROME CAPABILITIES ===
    Log To Console    ${driver.capabilities}
    [Teardown]    Close Browser

*** Keywords ***
Get WebDriver
    [Documentation]    Get the current WebDriver instance
    ${selenium}=    Get Library Instance    SeleniumLibrary
    [Return]    ${selenium.driver}
