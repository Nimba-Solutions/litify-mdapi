*** Settings ***
Resource        cumulusci/robotframework/Salesforce.robot
Library         cumulusci.robotframework.PageObjects
Library         Process
Library         cumulusci.robotframework.CumulusCI  ${ORG}
Library         OperatingSystem
Suite Setup     Run Keywords
...             Setup Heroku Browser
...             Setup Test Data
...             Open Test Browser
Suite Teardown  Delete Records And Close Browser


*** Tasks ***
Edit And Save Named Credential
    [Documentation]             Edit and save Named Credential so that it can
    ...                         update to status "Authenticated".
    Navigate To Named Credentials
    Edit Named Credentials    
    Click Save
    Login as User       
    Select Confirm
    Verify Authentication Status Is Authenticated

*** Variables ***
${named_credential} =           //setup_platform_namedcredential-credential-table//a[text()='LitifyMDAPI']//parent::*
${edit_button} =                //input[@value='Edit']
${save_button} =                //input[@value='Save']
${confirm_button} =             //input[@value='Confirm']
${username_field} =             //input[@id='username']
${password_field} =             //input[@id='password']
${login_button} =               //input[@id='Login']
${iframe}                       //*[@id="setupComponent"]/div/div/div/force-aloha-page/div/iframe


*** Keywords ***
Setup Heroku Browser
    [Documentation]    Setup Chrome options specifically for Heroku environment
    ${is_heroku}=    Run Keyword And Return Status    Environment Variable Should Exist    DYNO
    Return From Keyword If    not ${is_heroku}
    
    ${timestamp}=    Evaluate    int(round(time.time() * 1000))    modules=time
    ${options}=    Evaluate    selenium.webdriver.ChromeOptions()    modules=selenium.webdriver
    Call Method    ${options}    add_argument    --user-data-dir=/tmp/chrome-data-${SUITE NAME}-${timestamp}
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage
    Set Global Variable    ${BROWSER_OPTIONS}    ${options}

Setup Test Data
    [Documentation]             Sets up all data required for test. Get Org Info.
    
    # Get org info which includes credentials
    ${org_info} =               Get Org Info
    Set Suite Variable          ${ORG_INFO}                 ${org_info}
    
    # Log the dictionary to see available keys
    Log Dictionary              ${ORG_INFO}
    
    # Get instance URL
    ${instance_url} =           Get From Dictionary         ${ORG_INFO}    instance_url
    Set Suite Variable          ${INSTANCE_URL}            ${instance_url}

Navigate To Named Credentials
    [Documentation]             Navigates to the Named Credentials home page.
    Go To                       ${INSTANCE_URL}/lightning/setup/NamedCredential/home

Edit Named Credentials
    [Documentation]             Click on edit button for provided Named Credential.
    # iframe for Salesforce Classic setup pages
    Click Element               ${named_credential}
    Select Frame                ${iframe}
    Click Element               ${edit_button}
    Unselect Frame  
    Wait Until Page Contains Element
    ...                         ${iframe}                  
    Sleep                       15s        

Click Save
    [Documentation]             Click Save Button on edit page.
    Select Frame                ${iframe}
    Wait Until Page Contains Element
    ...                         ${save_button}
    Click Element               ${save_button}     
    Wait Until Page Contains Element
    ...                         ${username_field}          timeout=15s

Login as User
    [Documentation]             Enter User credentials and click Login Button on login page.
    # Getting Access Token and storing variable
    ${access_token} =           Get From Dictionary        ${ORG_INFO}    access_token
    Set Suite Variable          ${ACCESS_TOKEN}            ${access_token}
    # Setting Username and Password
    Input Text                  ${username_field}            ${SF_USERNAME}
    Input Text                  ${password_field}            ${SF_PASSWORD}
    Click Element               ${login_button}
    Wait Until Page Contains Element 
    ...                         //input[@value='Confirm']
    ...                         timeout=15s

Select Confirm
    [Documentation]             Click Confirm Button on Confirm External Access page.
    Click Element               ${confirm_button}
    Sleep                       15s     
    Select Frame                ${iframe}   
    Wait Until Page Contains Element
    ...                         ${edit_button}                  
    ...                         timeout=15s

Verify Authentication Status Is Authenticated
    [Documentation]             Waits for Authenticaiton Status to load and then validates it's value
    ...                         is "Authenticated".
    Element Should Contain    //*[contains(@id,"authStatusSection")]    
    ...                        Authenticated
    Log                        Named Credential is Authenticated