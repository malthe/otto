from otto import WebObApplication

class FluxBinApplication(WebObApplication):
    def get_site_info(self, signature):
        return (u'siteid', u"abcdef")

app = FluxBinApplication()
