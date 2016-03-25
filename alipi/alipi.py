from flask import (Flask, request, render_template, make_response,
                   session, jsonify, g, url_for, send_from_directory, redirect)
from bson import Code
from urllib import unquote_plus, quote_plus
from flask_cors import cross_origin
from urlnorm import urlnorm
import lxml.html
import pymongo
import urllib2
import StringIO
import conf
import sweetmaker
import oursql
import json


app = Flask(__name__)
import requests
app.config['SECRET_KEY'] = conf.SECRET_KEY[0]


@app.before_request
def first():
    g.connection = pymongo.MongoClient('localhost', 27017)  # Create the
    # object once and use it.
    g.db = g.connection[conf.MONGODB[0]]


@app.teardown_request
def close(exception):
    g.connection.disconnect()


@app.route('/')
def start_page():
    if 'verified' in request.cookies and request.cookies['verified'] == 'True':
        d = {}
        d['foruri'] = request.args['foruri']
        myhandler1 = urllib2.Request(d['foruri'],
                                     headers={'User-Agent':
                                              "Mozilla/5.0 (X11; " +
                                              "Linux x86_64; rv:25.0)" +
                                              "Gecko/20100101 Firefox/25.0)"})
    # A fix to send user-agents, so that sites render properly.
        try:
            a = urllib2.urlopen(myhandler1)
            if a.geturl() != d['foruri']:
                return ("There was a server redirect, please click on the" +
                        " <a href='http://y.a11y.in/web?foruri={0}'>link</a> to" +
                        " continue.".format(quote_plus(a.geturl())))
            else:
                page = a.read()
                a.close()
        except ValueError:
            return ("The link is malformed, click " +
                    "<a href='http://y.a11y.in/web?foruri={0}&lang={1}" +
                    "&interactive=1'>" +
                    "here</a> to be redirected.".format(
                        quote_plus(unquote_plus(d['foruri'].encode('utf-8'))),
                        request.args['lang']))
        except urllib2.URLError:
            return render_template('error.html')
        try:
            page = unicode(page, 'utf-8')  # Hack to fix improperly displayed chars on wikipedia.
        except UnicodeDecodeError:
            pass  # Some pages may not need be utf-8'ed
        try:
            g.root = lxml.html.parse(StringIO.StringIO(page)).getroot()
        except ValueError:
            g.root = lxml.html.parse(d['foruri']).getroot()  # Sometimes creators of the page lie about the encoding, thus leading to this execption. http://lxml.de/parsing.html#python-unicode-strings
        if request.args.has_key('lang') == False and request.args.has_key('blog') == False:
            g.root.make_links_absolute(d['foruri'],
                                       resolve_base_href=True)
            for i in g.root.iterlinks():
                if i[1] == 'href' and i[0].tag != 'link':
                    try:
                        i[0].attrib['href'] = 'http://{0}?foruri={1}'.format(
                            conf.DEPLOYURL[0], quote_plus(i[0].attrib['href']))
                    except KeyError:
                        i[0].attrib['href'] = '{0}?foruri={1}'.format(
                            conf.DEPLOYURL[0], quote_plus(
                                i[0].attrib['href'].encode('utf-8')))
            setScripts()
            g.root.body.set("onload", "a11ypi.loadOverlay();")


        elif request.args.has_key('lang') == True and request.args.has_key('interactive') == True and request.args.has_key('blog') == False:
            setScripts()
            setSocialScript()
            g.root.body.set("onload", "a11ypi.ren();a11ypi.tweet(); " +
                            "a11ypi.facebook(); a11ypi.loadOverlay();")
            g.root.make_links_absolute(d['foruri'], resolve_base_href=True)
            response = make_response()
            response.data = lxml.html.tostring(g.root)
            return response

        elif request.args.has_key('lang') == True and request.args.has_key('blog') == False:
            script_jq_mini = g.root.makeelement('script')
            g.root.body.append(script_jq_mini)
            script_jq_mini.set("src", conf.JQUERYURL[0] + "/jquery.min.js")
            script_jq_mini.set("type", "text/javascript")
            d['lang'] = request.args['lang']
            script_test = g.root.makeelement('script')
            g.root.body.append(script_test)
            script_test.set("src", conf.APPURL[0] + "/alipi/ui.js")
            script_test.set("type", "text/javascript")
            g.root.body.set("onload", "a11ypi.ren()")

        elif request.args.has_key('interactive') == True and request.args.has_key('blog') == True and request.args.has_key('lang') == True:
            setScripts()
            setSocialScript()
            g.root.body.set("onload", "a11ypi.filter(); a11ypi.tweet();" +
                            "a11ypi.facebook(); a11ypi.loadOverlay();")
            g.root.make_links_absolute(d['foruri'], resolve_base_href=True)

        elif request.args.has_key('interactive') == False and request.args.has_key('blog') == True:
            setScripts()
            g.root.make_links_absolute(d['foruri'], resolve_base_href=True)
            g.root.body.set('onload', 'a11ypi.loadOverlay();')

        response = make_response()
        response.data = lxml.html.tostring(g.root)
        return response
    else:
        session['params'] = request.args.to_dict()
        return redirect(url_for('verify'))

@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "GET":
        return render_template('verify.html')
    else:
        captcha_string = request.form.get('g-recaptcha-response')
        gVerify = requests.get(conf.RECAPTCHA_URL + "?secret=" + conf.RECAPTCHA_SECRET + "&response=" + captcha_string)
        if gVerify.json()['success'] is True:
            print session.get('params')
            response = make_response(redirect(url_for('start_page', **session.get('params'))))

            response.set_cookie('verified', 'True', 1800)
            return response
        else:
            return redirect(url_for('verify'))


@app.route("/get/username", methods=["GET"])
def getUsername():
    if 'username' in session:
        return jsonify({"username": session['username']})
    else:
        return jsonify({"status": "Not logged in"})


def setScripts():
    script_test = g.root.makeelement('script')
    script_auth = g.root.makeelement('script')
    # script_oauth = g.root.makeelement('script')

    g.root.body.append(script_auth)
    # g.root.body.append(script_oauth)
    g.root.body.append(script_test)

    script_test.set("src", conf.APPURL[0] + "/alipi/pack.min.js")
    script_test.set("type", "text/javascript")

    script_auth.set("src", conf.APPURL[0] + "/alipi/oauth.js")
    script_auth.set("type", "text/javascript")

    style = g.root.makeelement('link')
    g.root.body.append(style)
    style.set("rel", "stylesheet")
    style.set("type", "text/css")
    style.set("href", conf.APPURL[0] + "/alipi/pack.min.css")


def setSocialScript():
    info_button = g.root.makeelement('button')
    g.root.body.append(info_button)
    info_button.set("id", "info")
    info_button.set("class", "alipi")
    info_button.set("onClick", "a11ypi.showInfo(a11ypi.responseJSON);")
    info_button.text = "Info"
    info_button.set("title", "Have a look at the information of each" +
                    " renarrated element")

    share_button = g.root.makeelement('button')
    g.root.body.append(share_button)
    share_button.set("id", "share")
    share_button.set("class", "alipi")
    share_button.set("onClick", "a11ypi.share();")
    share_button.text = "Share"
    share_button.set("title", "Share your contribution in your social network")

    see_orig = g.root.makeelement('button')
    g.root.body.append(see_orig)
    see_orig.set("id", "orig-button")
    see_orig.set("class", "alipi")
    see_orig.set("onClick", "a11ypi.showOriginal();")
    see_orig.text = "Original Page"
    see_orig.set("title", "Go to Original link, the original page of this" +
                 " renarrated page")

    tweetroot = g.root.makeelement("div")
    tweetroot.set("id", "tweet-root")
    tweetroot.set("class", "alipi")
    tweetroot.set("style", "display:none;padding:10px;")
    g.root.body.append(tweetroot)

    tweet = g.root.makeelement("a")
    tweet.set("id", "tweet")
    tweet.set("href", "https://twitter.com/share")
    tweet.set("class", "alipi twitter-share-button")
    tweet.set("data-via", "a11ypi")
    tweet.set("data-lang", "en")
    tweet.set("data-url", "http://y.a11y.in/web?foruri={0}&lang={1}&" +
              "interactive=1".format(quote_plus(request.args['foruri']),
                                     (request.args['lang']).encode(
                                         'unicode-escape')))
    tweet.textContent = "Tweet"
    tweetroot.append(tweet)

    fblike = g.root.makeelement("div")
    fblike.set("id", "fb-like")
    fblike.set("class", "alipi fb-like")
    fblike.set("style", "display:none;padding:10px;")
    fblike.set("data-href", "http://y.a11y.in/web?foruri={0}&lang={1}&" +
               "interactive=1".format(quote_plus(request.args['foruri']),
                                      (request.args['lang']).encode(
                                          'unicode-escape')))
    fblike.set("data-send", "true")
    fblike.set("data-layout", "button_count")
    fblike.set("data-width", "50")
    fblike.set("data-show-faces", "true")
    fblike.set("data-font", "arial")
    g.root.body.append(fblike)

    style = g.root.makeelement('link')
    g.root.body.append(style)
    style.set("rel", "stylesheet")
    style.set("type", "text/css")
    style.set("href", "http://y.a11y.in/alipi/stylesheet.css")


@app.route('/redirect')
def redirect_uri():
    auth_tok = None
    if request.args.get('code'):
        payload = {
            'scopes': 'email sweet',
            'client_secret': conf.APP_SECRET,
            'code': request.args.get('code'),
            'redirect_uri': conf.REDIRECT_URI,
            'grant_type': 'authorization_code',
            'client_id': conf.APP_ID
        }
        # token exchange endpoint
        oauth_token_x_endpoint = conf.SWEETURL[0] + '/oauth/token'
        resp = requests.post(oauth_token_x_endpoint, data=payload)
        auth_tok = json.loads(resp.text)

        if 'error' in auth_tok:
            print auth_tok['error']
            return make_response(auth_tok['error'], 200)

        session['auth_tok'] = auth_tok

        username_request = requests.get(conf.SWEETURL[0] +
                                        '/api/users/me?access_token=' +
                                        session['auth_tok']['access_token'])
        session['username'] = username_request.json()['username']
    if 'auth_tok' in session:
        auth_tok = session['auth_tok']
    else:
        auth_tok = {'access_token': '', 'refresh_token': ''}

    print auth_tok
    return render_template('index.html', username=session['username'])


@app.route('/directory')
def show_directory():
    collection = g.db['post']
    query = collection.group(
        key=Code('function(doc){' +
                 'return {"about" : doc.about,"lang":doc.lang}}'),
        condition={"about": {'$regex': '^[/\S/]'}},
        initial={'na': []},
        reduce=Code('function(doc,out){out.na.push(doc.blog)}')
        )
    query.reverse()
    return render_template('directory.html', name=query, mymodule=quote_plus,
                           myset=set, mylist=list)


@app.route('/getLoc', methods=['GET'])
def get_loc():

    term = request.args['term']
    connection = oursql.Connection(conf.DBHOST[0], conf.DBUSRNAME[0],
                                   conf.DBPASSWD[0], db=conf.DBNAME[0])
    cursor = connection.cursor(oursql.DictCursor)
    cursor.execute('select l.name, c.country_name from `location` as l, ' +
                   ' `codes` as c where l.name like ? and l.code=c.code' +
                   ' limit ?', (term+'%', 5))
    r = cursor.fetchall()
    connection.close()
    d = {}
    d['return'] = r
    response = jsonify(d)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/getLang', methods=['GET'])
def get_lang():
    term = request.args['term']
    connection = oursql.Connection(conf.DBHOST[0], conf.DBUSRNAME[0],
                                   conf.DBPASSWD[0], db=conf.DBNAME[0])
    cursor = connection.cursor(oursql.DictCursor)
    cursor.execute('select * from `languages` as l  where l.name like' +
                   ' ? limit ?', (term+'%', 5))
    r = cursor.fetchall()
    connection.close()
    d = {}
    d['return'] = r
    response = jsonify(d)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/blank', methods=['GET'])
def serve_blank():
    return render_template('blank.html')


@app.route('/info', methods=['GET'])
def serve_info():
    coll = g.db['post']
    d = {}
    cntr = 0
    for i in coll.find({"about": unquote_plus(request.args['about']),
                        "lang": request.args['lang']}):
        i['_id'] = str(i['_id'])
        d[cntr] = i
        cntr += 1
    response = jsonify(d)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/find')
def find_renarrartion():
    """Experimental API to query for re-narrations.
    The API accepts following params:
    url - url of the page for which re-narrations are needed
    language - language of re-narration
    author (optional) - author(s) of the re-narration"""

    lang = request.args['lang']
    url = urlnorm(request.args['url'])
    collection = g.db['post']
    if 'author' in request.args:
        authors = request.args.getlist('author')
        query = collection.find({'about': url,
                                 'lang': lang,
                                 'author': {'$in': authors}})
    else:
        query = collection.find({'about': url,
                                 'lang': lang})
    d = {}
    cntr = 0
    for i in query:
        i['_id'] = str(i['_id'])
        d[cntr] = i
        cntr += 1
    response = jsonify(d)
    return response


@app.route("/replace", methods=['GET'])
@cross_origin(headers=['Content-Type'])
def replace():
    lang = request.args['lang']
    url = urlnorm(request.args['url'])
    if 'author' in request.args:
        query = query_by_params(url, lang, request.args.get('author'))
    else:
        query = query_by_params(url, lang)

    for i in query:
        for y in i['narration']:
            del(y['_id'])
    d = {}
    d['r'] = query
    response = jsonify(d)
    return response


def query_by_params(url, language, author=None):
    collection = g.db['post']
    if author is None:
        query = collection.group(
            key=Code('function(doc){' +
                     'return {"xpath": doc.xpath, "about": doc.url}}'),
            condition={"about": url, "lang": language},
            initial={'narration': []},
            reduce=Code('function(doc,out){out.narration.push(doc);}')
        )
    else:
        query = collection.group(
            key=Code('function(doc){' +
                     'return {"xpath": doc.xpath, "about": doc.url}}'),
            condition={"about": url, "lang": language, "author": author},
            initial={'narration': []},
            reduce=Code('function(doc,out){out.narration.push(doc);}')
        )
    return query


@app.route('/feeds', methods=['GET'])
def serve_feed_temp():
    return render_template("feeds.html")


@app.route('/feed', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def serve_feed():
    coll = g.db['post']
    d = {}
    cntr = 0
    for i in coll.find().sort('_id', direction=-1):
        if i['data'] != '<br/>':
            i['_id'] = str(i['_id'])
            d[cntr] = i
            cntr += 1
    response = jsonify(d)
    return response


@app.route('/about', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def serve_authors():
    coll = g.db['post']
    d = {}
    cntr = 0
    for i in coll.find({"about": unquote_plus(request.args['about'])}):
        i['_id'] = str(i['_id'])
        d[cntr] = i
        cntr += 1
    response = jsonify(d)
    return response


#Retrieve all information about a specific $about and a given $author.
@app.route('/author', methods=['GET'])
@cross_origin(headers=['Content-Type'])
def serve_author():
    coll = g.db['post']
    d = {}
    cntr = 0
    for i in coll.find({"about": unquote_plus(request.args['about']),
                        "author": unquote_plus(request.args['author'])}):
        i['_id'] = str(i['_id'])
        d[cntr] = i
        cntr += 1
    response = jsonify(d)
    return response


@app.route('/getAllLang', methods=['GET'])
def get_all_lang():
    term = request.args['term']
    connection = oursql.Connection(conf.DBHOST[0], conf.DBUSRNAME[0],
                                   conf.DBPASSWD[0], db=conf.DBNAME[0])
    cursor = connection.cursor(oursql.DictCursor)
    cursor.execute('select * from `languages` as l  where l.name like ?',
                   (term+'%',))
    r = cursor.fetchall()
    connection.close()
    d = {}
    d['return'] = r
    response = jsonify(d)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/publish', methods=['POST'])
def publish():
    data = json.loads(request.form['data'])
    collection = g.db['post']
    page = {}
    if type(data) is unicode:  # A hack to fix malformed data. FIXME.
        data = json.loads(data)
    content = []
    for i in data:
        print i

        # Create content objects here for posting to blog.  DELETEME.
        if 'comments' in i:
            page['comments'] = i['comments']
        else:
            # normalize URLs before inserting to DB
            i['about'] = urlnorm(i['about'])
            contentobj = {}
            contentobj['type'] = i['elementtype']
            contentobj['attr'] = {"language": i['lang'],
                                  "location": i['location'],
                                  "about": i['about'],
                                  "xpath": i['xpath']}
            contentobj['data'] = i['data']
            content.append(contentobj)
            i['bxpath'] = ''
            collection.insert(i)

    page['title'] = "Re-narration of " + content[0]['attr']['about']
    page['name'] = "About " + content[0]['attr']['about']
    page['content'] = content

    g.response_from_blogger = requests.api.post(conf.CUSTOM_BLOG_POST_URL[0],
                                                json.dumps(page),
                                                headers={"content-type":
                                                         "application/json"})
    print "response from blogger " + repr(g.response_from_blogger)
    sweet(data)
    reply = make_response()
    return reply


def sweet(data):
    """ A function to sweet the data that is inserted.
    Accepts a <list of dicts>. """
    for i in data:
        print i
        if 'type' in i:
            del(i['_id'])
            sweetmaker.sweet(conf.SWEET_STORE_ADD[0] +
                             "?access_token=" + session['auth_tok']
                             ['access_token'],
                             [{"what": i['type'],
                               "who": session['username'],
                               "where":i['about'],
                               "how":{'blogUrl': '{0}/#{1}'.format(
                                   conf.CUSTOM_BLOG_URL[0],
                                   g.response_from_blogger.json()['name']),
                                    'language': i['lang'],
                                    'location': i['location'],
                                    'xpath': i['xpath']}}])
    return True
        # data = json.dumps(data)
    # req = requests.api.post(conf.SWEETURL[0]+"/add",{'data':data})
    # if req.status_code == 200:
    #     reply = make_response()
    #     return reply


@app.route("/askSWeeT", methods=['POST'])
def askSweet():
    data = json.loads(request.form['data'])
    for i in data:
        response = requests.api.get(conf.SWEETURL[0]+"/query/"+i['id'])
        collection = g.db['post']
        rep = response.json()
        rep['bxpath'] = ''
        if response.status_code == 200:
            collection.insert(rep)
    reply = make_response()
    return reply


@app.route("/menu", methods=['GET'])
@cross_origin(headers=['Content-Type'])
def menuForDialog():
    if 'option' not in request.args:
        collection = g.db['post']
        c = {}
        cntr = 0
        url = urlnorm(request.args.get('url'))
        for i in collection.find({"about":
                                  url}).distinct('lang'):
            for j in collection.find({"about": url,
                                      'lang': i}).distinct('type'):
                d = {}
                d['lang'] = i
                d['type'] = j
                c[cntr] = d
                cntr += 1
        print c
        return jsonify(c)

    else:
        collection = g.db['post']
        #get the ren languages for the received url
        langForUrl = collection.group(
            key=Code('function(doc){return {"about" : doc.about}}'),
            condition={"about": d['url'], "blog": {'$regex':
                                                   '/'+d['option']+'.*/'}},
            initial={'lang': []},
            reduce=Code('function(doc, out){' +
                        'if (out.lang.indexOf(doc.lang) == -1)' +
                        'out.lang.push(doc.lang)}')  # here xpath for test
            )

        #send the response
        if (langForUrl):
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.data = json.dumps(langForUrl[0]['lang'])
            return response
        else:
            return "empty"


@app.route("/domain")
def serve_domain_info():
    collection = g.db['post']
    url = urlnorm(request.args.get('url'))
    #all re-narrations of the same xpath are grouped
    query = collection.group(
        key=None,
        condition={"about": {'$regex': url+'*'}},
        initial={'narration': []},
        reduce=Code('function(doc,out){out.narration.push(doc["about"]);}')
    )

    string = ''
    if len(query) == 0:
        return jsonify({'0': 'empty'})
    else:
        otherlist = {}
        cntr = -1
        mylist = query[0]['narration']
        for i in mylist:
            if i in otherlist:
                pass
            else:
                cntr += 1
                otherlist[cntr] = str(i)
                return jsonify(otherlist)


@app.route('/saveSession', methods=['POST'])
def saveSession():
    g.url = request.form['url']
    response = make_response()
    return response

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, request.path[1:])

import logging
import os
from logging import FileHandler

fil = FileHandler(os.path.join(os.path.dirname(__file__), 'logme'), mode='a')
fil.setLevel(logging.ERROR)
app.logger.addHandler(fil)

if __name__ == '__main__':
    app.run(debug=True, host=conf.MONGOHOST[0])
