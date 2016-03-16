    // server.js

// BASE SETUP
// =============================================================================

// call the packages we need
var express    = require('express');        // call express
var app        = express();                 // define our app using express
var bodyParser = require('body-parser');
var mongoose   = require('mongoose');
mongoose.connect('mongodb://localhost/api'); 
var methodOverride = require('method-override');
var _ = require('lodash');


//var Bear     = require('./app/models/bear'); // to be used if there is a model with this name
var http 	 = require("http");
var https = require("https"); 
var requestify = require('requestify');
//var serialize = require('dom-serialize');
//var htmlparser = require("htmlparser");

var htmlparser = require("htmlparser2");
var html = require('htmlparser-to-html');


// configure app to use bodyParser()
// this will let us get the data from a POST
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(methodOverride('X-HTTP-Method-Override'));

// CORS Support
app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});



var port = process.env.PORT || 8080;
        // set our port

// ROUTES FOR OUR API
// =============================================================================
var router = express.Router();              // get an instance of the express Router

// middleware to use for all requests
router.use(function(req, res, next) {
    // do logging
    console.log('Something is happening.');
    next(); // make sure we go to the next routes and don't stop here
});

// test route to make sure everything is working (accessed at GET http://localhost:8080/api)
/*router.get('/', function(req, res) {
    res.json({ message: 'hooray! welcome to our api!' });   

});*/

router.route('/')
    .get(function(req,resp){
        console.log("receiving Input");
        resp.send("receiving");
    })
    .post(function(req, resp) {
        //var url = req.body.url;
        url = "https://en.wikipedia.org/wiki/Odyssey"
        console.log("url="+url);
        var output = '';
        
        // sets the options for http request
        var options = {
          host: "proxy",
          port: 8080,
          path: url,
          //method : GET,POST,PUT
          /*headers: {
            Host: "www.google.co.in"
          }*///proxy: 'proxy.iiit.ac.in:8080'
        };

        var req = http.request(options,function(res) {
            console.log("Request began");
            

            res.on('data', function (chunk) {
                output += chunk;
            });
            // after receiving contents of the requested page
            res.on('end', function () {
                console.log('Request complete:');
                //console.log(output);
                
                // handler for HTML parser -> makes the DOM
                var handler = new htmlparser.DomHandler(function (error, dom) {
                    if (error)
                        //[...do something for errors...]
                    {
                        console.log(error.message);
                    }
                    else
                        //[...parsing done, do something...]
                        console.log("about to start subparsing\n");
                        
                        // used to traversal through the html : needs to be on a different
                        // server
                        //console.log(dom[0].next.next.children[1].children[9].attribs.href);
                        var subparsing = function(dom){
                            
                            for (var i in dom){    
                                if (dom[i].name){
                                    /*if(dom[i].name=="script"){
                                        continue;
                                    }*/
                                    /*if(dom[i].attribs && dom[i].attribs.href){
                                        dom[i].attribs.href = url  + "/../.."+ dom[i].attribs.href; 
                                    }*/
                                }


                                if(dom[i].data ){
                                    //console.log(dom[i]);
                                    if(dom[i].parent){
                                        // replacemenst
                                        dom[i].data=dom[i].data.replace(" an ", " /ən/ ");
                                        dom[i].data=dom[i].data.replace("The ", " /ðiː/ ");
                                        dom[i].data=dom[i].data.replace(" a ", " /eɪ/ ");
                                        dom[i].data=dom[i].data.replace("It ", " /ɪt/ ");
                                        dom[i].data=dom[i].data.replace(" is ", " /ɪz/ ");
                                        dom[i].data=dom[i].data.replace(" in ", " /ɪn/ ");
                                        dom[i].data=dom[i].data.replace(" most ", " /məʊst/ ");
                                        dom[i].data=dom[i].data.replace(" to ", " /tuː/ ");
                                        dom[i].data=dom[i].data.replace(" be ", " /biː/ ");
                                        

                                        //dom[i].data=result;
                                        //var result = dom[i].data.replace(" the ", " ðiː ");

                                        //console.log(dom[i].parent.name + ": " + dom[i].parent.type + ": " +dom[i].data);
                                    }
                                }
                                if(dom[i].children){
                                    
                                    subparsing(dom[i].children);
                                }
                            }
                        }
                        subparsing(dom);
                        // sending the changed HTML
                        resp.send(html(dom));
                        //resp.send(dom);
                });
                var parser = new htmlparser.Parser(handler);
                parser.write(output);
                parser.done();
                
            });
        });

        req.on('error', function (err) {
            console.log(err);

        });
        
        req.end();
        console.log("Script complete");
        
    })

// more routes for our API will happen here




// REGISTER OUR ROUTES -------------------------------
// all of our routes will be prefixed with /api
app.use('/api', router);

// START THE SERVER
// =============================================================================
app.listen(port);
console.log('Magic happens on port ' + port);
