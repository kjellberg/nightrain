__author__ = 'naetech'

import sys

import wx
import wx.html
import wx.html2
import wx.lib.wxpTag

from Classes.PHP import PHPServerThread

class GUI:

    def show_error(self, title, message):
        app = wx.PySimpleApp()
        dlg = ErrorDialog(None, title, message)
        dlg.ShowModal()
        dlg.Destroy()
        app.MainLoop()

    def show_browser(self, php_path, port, webroot, wait_time):
        app = wx.App()
        dialog = WebBrowser(php_path, port, webroot, wait_time, None, -1)
        dialog.browser.LoadURL("http://localhost:%s" % (port))
        dialog.Show()
        app.MainLoop()

class WebBrowser(wx.Dialog):

    program_php_server_thread = None

    def __init__(self, php_path, port, webroot, wait_time, *args, **kwds):
        self.program_php_server_thread = PHPServerThread(php_path, port, webroot)
        self.program_php_server_thread.daemon = True
        self.program_php_server_thread.start()
        if wait_time:
            print "Going to delay the execution by %s seconds" % (wait_time)
            self.program_php_server_thread.pause_execution(wait_time)

        wx.Dialog.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((700, 700))
        self.Bind(wx.EVT_CLOSE, self.event_browser_closed)

    def event_browser_closed(self, event):
        self.Close(True)
        self.program_php_server_thread.stop()

class ErrorDialog(wx.Dialog):
    text = '''
<html>
<body bgcolor="#FFF">
<center><table bgcolor="#F2DEDE" width="100%%" cellspacing="0"
cellpadding="0" border="1" bordercolor="red">
<tr>
    <td align="center" color="red">
        <font color="red">
            <h1>%s</h1>
        </font>
    </td>
</tr>
</table>

<p cellspacing="0" cellpadding="5">
    %s
</p>

<p>
    <wxp module="wx" class="Button">
        <param name="label" value="OK">
        <param name="id"    value="ID_OK">
    </wxp>
</p>
</center>
</body>
</html>
'''
    def __init__(self, parent, title, error_msg):
        wx.Dialog.__init__(self, parent, -1, 'System Error',)
        html = wx.html.HtmlWindow(self, -1, size=(420, -1))
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        py_version = sys.version.split()[0]
        txt = self.text % (title, error_msg)
        html.SetPage(txt)
        btn = html.FindWindowById(wx.ID_OK)
        ir = html.GetInternalRepresentation()
        html.SetSize( (ir.GetWidth()+25, ir.GetHeight()+25) )
        self.SetClientSize(html.GetSize())
        self.CentreOnParent(wx.BOTH)