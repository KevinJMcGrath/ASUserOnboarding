import wx

class MainApp:
    def __init__(self):
        self.app = wx.App()
        self.primary_window = PrimaryFrame()

    def start_gui(self):
        self.primary_window.Show()
        self.app.MainLoop()

class PrimaryFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='AS User Onboarding')

        self.pnl_primary = wx.Panel(self)
        self.nbk_primary = wx.Notebook(self.pnl_primary)
