__author__ = 'naetech'

import sys

import wx
import wx.html
import wx.html2
import wx.lib.wxpTag

from operator import or_

class GUI:

    def show_error(self, title, message):
        app = wx.PySimpleApp()
        dlg = ErrorDialog(None, title, message)
        dlg.ShowModal()
        dlg.Destroy()
        app.MainLoop()

    def show_browser(self, maximized, fullscreen, width, height, port):
        app = wx.App()
        browser_window = WebBrowser(width, height, None, -1)
        browser_window.browser.LoadURL("http://localhost:%s" % (port))

        if maximized:
            browser_window.Maximize()

        browser_window.Show()

        if fullscreen:
            browser_window.ShowFullScreen(True)

        app.MainLoop()

class WebBrowser(wx.Frame):

    def __init__(self, width, height, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = wx.html2.WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((width, height))

        self.Bind(wx.EVT_CLOSE, self.event_browser_closed)
        self.Bind(wx.EVT_CHAR_HOOK, self.handle_keystrokes)
        self.Bind(wx.html2.EVT_WEBVIEW_TITLE_CHANGED, self.title_changed, self.browser)

    def title_changed(self, event):
        self.SetTitle(event.GetString())

    def handle_keystrokes(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.ShowFullScreen(False)
        elif key_code == wx.WXK_F11:
            if self.IsFullScreen():
                self.ShowFullScreen(False)
            else:
                self.ShowFullScreen(True)
        else:
            event.Skip()

    def event_browser_closed(self, event):
        self.Destroy()

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