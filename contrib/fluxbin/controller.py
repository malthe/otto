from fluxbin import app
import webob
from webob import exc
import os.path
from chameleon.zpt.template import PageTemplateFile

# setup the templates returns the master template 
here = os.path.abspath(os.path.dirname(__file__))
get_template = lambda t_name: PageTemplateFile(os.path.join(here, t_name))
master_template = get_template('templates/mastertemplate.pt')
root_template = get_template('templates/mytemplate.pt')

@app.route("/")
def root_controller(request):
    response = webob.Response(root_template.render(master=master_template, 
                                                   request=request))
    return response

@app.route("/auth/:signature")
def urlauth_controller(request, signature):
    auth_cookie, site_id = app.get_site_info(signature)
    resp = exc.HTTPTemporaryRedirect(location=u"/site/%s"%site_id)
    resp.set_cookie('authinfo', auth_cookie, path="/")
    return resp

@app.route("/site/:siteid")
def siteroot_controller(request, siteid):
    found_cookie = request.cookies.get('authinfo', "NO COOKIE")
    echo_str = unicode('Found siteid %s and cookie %s' % (siteid, found_cookie))
    return webob.Response(echo_str)
            
@app.route("/logout")
def logout_controller(request):
    resp = webob.Response(u"You are now logged out !")
    resp.delete_cookie('authinfo')
    return resp
   