import time
import os
import subprocess
import wx
import wx.html2 as webview

quality = "source"
stream = "misterslin"

class MainWindow(wx.Frame):
    def __init__(self, parent, title, frame=None):
        
        
        wx.Frame.__init__(self, parent, title=title, size=(500,400))
        
        self.current = "http://www.twitch.tv/directory"
        self.frame = frame
        self.CreateStatusBar() # A StatusBar in the bottom of the window
        if frame:
            self.titleBase = frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)

        btn = wx.Button(self, -1, "Home", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnHomeButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Load", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnLoadButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Manual", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnManualButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        # Setting up the menu.
        filemenu = wx.Menu()
        qualitymenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        sourceQual = qualitymenu.Append(101,"&Source", kind=wx.ITEM_RADIO)
        highQual = qualitymenu.Append(102,"&High", kind=wx.ITEM_RADIO)
        medQual = qualitymenu.Append(103,"&Medium", kind=wx.ITEM_RADIO)
        lowQual = qualitymenu.Append(104,"&Low", kind=wx.ITEM_RADIO)
        mobileQual = qualitymenu.Append(105,"&Mobile", kind=wx.ITEM_RADIO)

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(qualitymenu,"&Quality")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnSource, sourceQual)
        self.Bind(wx.EVT_MENU, self.OnHigh, highQual)
        self.Bind(wx.EVT_MENU, self.OnMedium, medQual)
        self.Bind(wx.EVT_MENU, self.OnLow, lowQual)
        self.Bind(wx.EVT_MENU, self.OnMobile, mobileQual)

        self.Show(True)
        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.wv.LoadURL(self.current)

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "GUI for livestreamer", "About Livestreamer Pro", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnSource(self,e):
        global quality
        quality = "source"
        print quality

    def OnHigh(self,e):
        global quality
        quality = "high"
        print quality

    def OnMedium(self,e):
        global quality
        quality = "medium"
        print quality

    def OnLow(self,e):
        global quality
        quality = "low"
        print quality

    def OnMobile(self,e):
        global quality
        quality = "mobile"
        print quality

    def OnWebViewLoaded(self, evt):
        # The full document has loaded
        s = evt.GetURL()
        if "javascript" in s:
            print "not a stream page"
        elif "api" in s:
            print "not a stream page"
        elif "chatdepot" in s:
            print "not a stream page"
        elif "twitter" in s:
            print "not a stream page"
        elif "facebook" in s:
            print "not a stream page"
        elif "cdn" in s:
            print "not a stream page"
        elif "directory/game/" in s:
            print "not a stream page"
        elif "directory#/directory" in s:
            print "not a stream page"
        elif "about:blank" in s:
            print "not a stream page"
        else:
            self.current = evt.GetURL()
            print self.current
            global stream
            stream = self.current[32:]
            print stream
        
        #self.current = evt.GetURL()
        #print self.current
        #self.location.SetValue(self.current)

    def OnHomeButton(self,e):
        self.wv.LoadURL("http://www.twitch.tv/directory")

    def OnLoadButton(self,e):
        #stream = self.current
        global stream
        print stream
        self.wv.LoadURL("http://www.twitch.tv/directory")
        subprocess.call(["livestreamer", "twitch.tv/" + stream, quality])

    def OnManualButton(self,e):
        global stream
        dlg = wx.TextEntryDialog(self, "Stream name",
                                "Enter Twitch Name Only",
                                stream, wx.OK|wx.CANCEL)
        dlg.CentreOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            stream = dlg.GetValue()
            check = subprocess.check_output(["livestreamer", "twitch.tv/" + stream + " " + quality + " -l error"])
            print check
            if "Available streams:" in check:
                dlg2 = wx.MessageDialog( self, "Unavailable quality", "Error", wx.OK)
                dlg2.ShowModal() # Show it
                dlg2.Destroy() # finally destroy it when finished.
                

            dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Livestreamer Pro")
app.MainLoop()

#os.system('livestreamer http://twitch.tv/misterslin best')
#subprocess.call(['livestreamer', 'twitch.tv/' + stream, quality])
