Id userId = UserInfo.getUserId();
String password = '%%%PARAM_1%%%';

// If param1 is "random", generate a random password
if (password == 'random') {
    // Generate a random password that meets Salesforce requirements
    // At least 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
    String chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    String lowerChars = chars.toLowerCase();
    String numbers = '0123456789';
    String special = '!@#$%^&*()';
    
    password = String.valueOf(chars.charAt(Math.mod(Math.abs(Crypto.getRandomInteger()), chars.length()))) +
               String.valueOf(lowerChars.charAt(Math.mod(Math.abs(Crypto.getRandomInteger()), lowerChars.length()))) +
               String.valueOf(numbers.charAt(Math.mod(Math.abs(Crypto.getRandomInteger()), numbers.length()))) +
               String.valueOf(special.charAt(Math.mod(Math.abs(Crypto.getRandomInteger()), special.length())));
    
    // Add 4 more random chars to meet minimum length
    for (Integer i = 0; i < 4; i++) {
        password += String.valueOf(chars.charAt(Math.mod(Math.abs(Crypto.getRandomInteger()), chars.length())));
    }
}
System.debug('Attempting to set password for user: ' + userId + ' to: ' + password); 
System.setPassword(userId, password);
System.debug('OK'); 