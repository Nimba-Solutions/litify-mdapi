Id userId = UserInfo.getUserId();
System.setPassword(userId, '%%%PARAM_1%%%');
System.debug('Password set for user: ' + userId); 