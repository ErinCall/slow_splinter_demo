To See The Slowness
===================

```Shell
git clone https://github.com/AndrewLorente/slow_splinter_demo.git
cd slow_splinter_demo
pip install -r requirements.txt
nosetests
```

Notice how the browser window stays open, doing nothing, for several seconds.

Investigation I Have Done
=========================

* The code only hangs if you include a static file in the page.
* It only hangs after two calls to `visit()`. The first two calls are fast; the third and any subsequent calls are slow.
* The code hangs during [an httplib request to the server, in the guts of `splinter.Browser.visit()`](https://github.com/cobrateam/splinter/blob/master/splinter/driver/webdriver/__init__.py#L44-L45)
* More precisely, the httplib request hangs iff it comes after a `304 Not Modified` response from the server. So the first call to visit() gets the static file and caches it, the second call gets a `304 Not Modified` response, and the third call is slow.
* The problem seems to be on splinter's side, not Flask's. I haven't been able to prove this, but I've demonstrated the slowness against a django project.
* The requests made by the browser itself are reliably fast. You can monkey-patch Splinter so it doesn't make the httplib requests, and then it will be fast:

```Python
from splinter.driver.webdriver.firefox import WebDriver
from splinter.browser import _DRIVERS
class FastFirefoxDriver(WebDriver):
    def visit(self, url):
        self.driver.get(url)
_DRIVERS['firefox'] = FastFirefoxDriver
```
