*** Settings ***
Library         SeleniumLibrary
Library         Process
Library         OperatingSystem

*** Keywords ***
Set Chrome Options
    ${options_dict}=    Evaluate    json.loads('''${BROWSER_OPTIONS}''')    json
    Log To Console    \n=== Chrome Options Dictionary ===
    Log To Console    ${options_dict}
    
    ${chrome_options}=    Evaluate    selenium.webdriver.ChromeOptions()    modules=selenium.webdriver
    
    # Set binary location from environment
    ${chrome_binary}=    Get Environment Variable    CHROME_BINARY_PATH
    Call Method    ${chrome_options}    binary_location    ${chrome_binary}
    Log To Console    \n=== Using Chrome Binary ===
    Log To Console    ${chrome_binary}
    
    # Then add arguments
    FOR    ${arg}    IN    @{options_dict}[args]
        Call Method    ${chrome_options}    add_argument    ${arg}
    END
    
    # Enable logging with proper dictionary
    ${log_prefs}=    Create Dictionary    browser=ALL    driver=ALL
    Call Method    ${chrome_options}    set_capability    goog:loggingPrefs    ${log_prefs}
    
    # Log final options
    ${options_str}=    Evaluate    str($chrome_options.to_capabilities())    modules=selenium.webdriver
    Log To Console    \n=== Final Chrome Options ===
    Log To Console    ${options_str}
    
    RETURN    ${chrome_options}

Log Chrome Options
    ${chrome_options}=    Set Chrome Options
    Log To Console    \n=== REQUESTED Chrome Options (from BROWSER_OPTIONS) ===
    Log To Console    ${BROWSER_OPTIONS}
    ${driver_path}=    Get Environment Variable    CHROMEDRIVER_PATH
    Log To Console    \n=== Using ChromeDriver ===
    Log To Console    ${driver_path}
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