//A sample configuration file for JS variables.  Copy this file to "config.js"
/*config['hostname'] = "hostname of the domain from the application is served"
 * config['deploy'] = "URL of where the application is deployed, same as DEPLOYURL in conf.py"
 * config['root'] = "Same as APPURL from conf.py"
 * config['sweet'] = "URL for the sweet store, same as SWEETURL from conf.py"
 */
var config = {
  'hostname': "127.0.0.1",
  'deploy': "http://localhost:5000",
  'root': "http://localhost",
	'sweet': "http://localhost:5001",
  'app_id': 'your app id from sweet store',
  'app_secret': 'your app secret from sweet store',
  "endpoints": { "get": "/api/sweets/q",
                "post": "/api/sweets",
                "auth": "/oauth/authorize",
                "login": "/auth/login",
                "logout": "/auth/logout"
              },
  'oauth_redirect_uri': 'http://localhost:5000/redirect'
