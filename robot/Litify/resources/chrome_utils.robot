*** Settings ***
Library         SeleniumLibrary
Library         Process
Library         OperatingSystem

*** Keywords ***
Set Chrome Options
    ${options_dict}=    Evaluate    json.loads('''${BROWSER_OPTIONS}''')    json
    ${chrome_options}=    Evaluate    selenium.webdriver.ChromeOptions()    modules=selenium.webdriver
    FOR    ${arg}    IN    @{options_dict}[args]
        Call Method    ${chrome_options}    add_argument    ${arg}
    END
    # Enable logging with proper dictionary
    ${log_prefs}=    Create Dictionary    browser=ALL    driver=ALL
    Call Method    ${chrome_options}    set_capability    goog:loggingPrefs    ${log_prefs}
    RETURN    ${chrome_options}

Log Chrome Options
    ${chrome_options}=    Set Chrome Options
    Log To Console    \n=== REQUESTED Chrome Options (from BROWSER_OPTIONS) ===
    Log To Console    ${BROWSER_OPTIONS}
    ${CURDIR}=    Get Environment Variable    WORKSPACE    ${CURDIR}
    ${driver_path}=    Join Path    ${CURDIR}    drivers    chromedriver.exe
    Create Webdriver    Chrome    executable_path=${driver_path}    chrome_options=${chrome_options}
    ${selenium}=    Get Library Instance    SeleniumLibrary
    ${driver}=    Set Variable    ${selenium.driver}
    ${logs}=    Evaluate    $driver.get_log('driver')
    Log To Console    \n=== Chrome Driver Logs ===
    Log To Console    ${logs}
    Close Browser

Log Environment Details
    Log To Console    \n=== Environment Details ===
    Log To Console    Starting test execution... 