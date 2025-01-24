*** Settings ***
Resource        cumulusci/robotframework/Salesforce.robot
Library         SeleniumLibrary
Suite Teardown  Close All Browsers

*** Test Cases ***
Log Chrome Options
    ${options_dict}=    Evaluate    json.loads('''${BROWSER_OPTIONS}''')    json
    ${chrome_options}=    Evaluate    selenium.webdriver.ChromeOptions()    modules=selenium.webdriver
    FOR    ${arg}    IN    @{options_dict}[args]
        Call Method    ${chrome_options}    add_argument    ${arg}
    END