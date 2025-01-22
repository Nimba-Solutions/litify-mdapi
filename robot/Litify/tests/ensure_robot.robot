*** Settings ***
Resource        cumulusci/robotframework/Salesforce.robot
Library         cumulusci.robotframework.PageObjects
Library         cumulusci.robotframework.CumulusCI  ${ORG}
Library         OperatingSystem

*** Tasks ***
Verify Robot Framework
    [Documentation]    Verifies that Robot Framework is running correctly and prints session details
    Log Environment Details
    Log Browser Options
    Log CumulusCI Details

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
    Log    Browser: ${BROWSER}
    Log    Browser Options: ${BROWSER_OPTIONS}
    Log    Timeout: ${TIMEOUT}

Log CumulusCI Details
    [Documentation]    Logs CumulusCI configuration details
    ${org_info}=      Get Org Info
    Log Dictionary    ${org_info}
    ${instance_url}=  Get From Dictionary    ${org_info}    instance_url
    Log    Instance URL: ${instance_url}
    Log    Username: ${SF_USERNAME}
    Log    CumulusCI Version: ${CUMULUSCI_VERSION} 