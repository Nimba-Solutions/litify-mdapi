*** Settings ***
Library         SeleniumLibrary
Library         OperatingSystem

*** Test Cases ***
Test Chrome Setup
    Log To Console    \n=== Starting Chrome Test ===
    Log To Console    \n=== Browser Options ===\n${BROWSER_OPTIONS}
    Open Browser    https://example.org    ${BROWSER}
    Page Should Contain    Example Domain
    ${title}=    Get Title
    Log To Console    \n=== Page Title ===\n${title}
    [Teardown]    Close Browser 