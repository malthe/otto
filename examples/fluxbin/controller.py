from fluxbin import app
import webob

@app.route("/auth/:siteid")
def url_auth(request, signature):
    site_cookie, sited_id = app.get_site_info(signature)
    return webob.Response(u"something - %s" % siteid)
