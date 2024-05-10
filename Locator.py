"""
    omer moshayov
    Window
"""

import wx
import subprocess
from client import*
from constants import*
import hashlib

##############################################################################
#                        log in / register window                            #
##############################################################################

class Options(wx.Frame):
    """
    a window with two options: log in/ sign in
    """
    try:

        def __init__(self, parent):
            """
            constructor.
            """
            try:
                super(Options, self).__init__(parent, title="Locator",
                                              size=(FRAME_WIDTH, FRAME_LENGTH))
                self.params = []
                self.combo_box = None
                self.client = Client(CLIENT_IP, PORT, "sjd cnj")
                self.InitUI()
            except socket.error as msg:
                print("socket error:", msg)
            except Exception as msg:
                print("general error: ", msg)

        def InitUI(self):
            """
            initiates window controls and displays it.
            """
            try:
                menu_bar = wx.MenuBar()
                menu = wx.Menu()
                menu_item = menu.Append(wx.ID_CLOSE, 'Quit', 'Quit application')
                menu_bar.Append(menu, '&Menu')
                self.SetMenuBar(menu_bar)
                self.Bind(wx.EVT_MENU, self.onQuit, menu_item)
                pnl = wx.Panel(self)
                cbtn1 = wx.Button(pnl, label='sign up', pos=(COMMAND_LABEL_X, COMMAND_LABEL_Y))
                cbtn1.Bind(wx.EVT_BUTTON, self.on_send)
                cbtn2 = wx.Button(pnl, label='log in', pos=(BUTTON_X, BUTTON_Y))
                cbtn2.Bind(wx.EVT_BUTTON, self.on_click_log_in)
                cbtn1.Bind(wx.EVT_BUTTON, self.on_click_sign_up)
                self.Centre()
                self.Show(True)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def onQuit(self, e):
            """
            called on quit selection.
            quits window.
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_click_log_in(self, e):
            """
            called on button click and opens the
            next window: log in
            """
            try:
                LogIn(None, self.client)
                self.Close()
                wx.App().MainLoop()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_click_sign_up(self, e):
            """
            called on button click and opens the
            next window: sign up.
            """
            try:
                SignUp(None, self.client)
                wx.App().MainLoop()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_send(self, e):
            """
            closes the window
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg
    except socket.error as msg:
        print("socket error:", msg)
    except Exception as msg:
        print("general error: ", msg)


##############################################################################
#                             log in window                                  #
##############################################################################


class LogIn(wx.Frame):
    """
    Log in window
    """
    try:

        def __init__(self, parent, client):
            """
            constructor.
            """
            try:
                super(LogIn, self).__init__(parent, title="Log In",
                                            size=(FRAME_WIDTH, FRAME_LENGTH))
                self.params = []
                self.combo_box = None
                self.client = client
                self.InitUI()
            except socket.error as msg:
                print("socket error:", msg)
            except Exception as msg:
                print("general error: ", msg)

        def InitUI(self):
            """
            initiates window controls and displays it.
            """
            try:
                menu_bar = wx.MenuBar()
                menu = wx.Menu()
                menu_item = menu.Append(wx.ID_CLOSE, 'Quit', 'Quit application')
                menu_bar.Append(menu, '&Menu')
                self.SetMenuBar(menu_bar)
                self.Bind(wx.EVT_MENU, self.onQuit, menu_item)
                pnl = wx.Panel(self)
                sb = wx.StaticBox(pnl, label='')
                sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
                text_one = wx.StaticText(pnl, label='User Name')
                param_one = wx.TextCtrl(pnl)
                self.params.append(param_one)
                sbs.Add(text_one)
                sbs.Add(self.params[FIRST_TEXTBOX], flag=wx.LEFT, border=BORDER)
                text_two = wx.StaticText(pnl, label='Password')
                param_two = wx.TextCtrl(pnl, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)
                self.params.append(param_two)
                sbs.Add(text_two)
                sbs.Add(self.params[SECOND_TEXTBOX], flag=wx.LEFT, border=BORDER)
                pnl.SetSizer(sbs)
                cbtn = wx.Button(pnl, label='log in', pos=(SEND_BUTTON_X, SEND_BUTTON_Y))
                cbtn.Bind(wx.EVT_BUTTON, self.on_send)
                back_btn = wx.Button(pnl, label='Back to options', pos=(BACK_BUTTON_X, BACK_BUTTON_Y))
                back_btn.Bind(wx.EVT_BUTTON, self.on_back)
                self.Bind(wx.EVT_TEXT_ENTER, self.on_send, self.params[SECOND_TEXTBOX])
                self.Centre()
                self.Show(True)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_back(self, event):
            self.Close()
            Options(None)
            wx.App().MainLoop()

        def onQuit(self, e):
            """
            called on quit selection.
            quits window.
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_click(self, e):
            """
            called on button click and displays a message box.
            """
            try:
                wx.MessageBox("button clicked", "title", wx.OK)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_send(self, e):
            """
            when the user presses the send button,
            this function is called.
            sending the server the name of the client so the
            server could check if the client exists.
            if the client exists it continues to the command
            window and if not it print an appropriate response
            in a message box.
            """
            try:
                prm = self.params[FIRST].GetLineText(FIRST)
                pswd = self.params[SECOND].GetLineText(FIRST)
                hasher = hashlib.sha256()
                bpswd = pswd.encode('utf-8')
                hasher.update(bpswd)
                pswd = hasher.hexdigest()
                # self.client = Client(CLIENT_IP, PORT, prm)
                command = "SEARCH"
                request = command + " " + prm + " " + pswd
                response = self.client.send_and_receive(request)
                if response == "False":
                    response = "user name or password incorrect"
                    wx.MessageBox(response, "Response", wx.OK |
                                  wx.ICON_INFORMATION)
                if response == "True":
                    self.client.set_name(prm)
                    Commands(None, prm, self.client)
                    self.Close()
                    wx.App().MainLoop()
                if response == "Exiting Program...":
                    self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg
    except socket.error as msg:
        print("socket error:", msg)
    except Exception as msg:
        print("general error: ", msg)


##############################################################################
#                             sign up window                                 #
##############################################################################

class SignUp(wx.Frame):
    """
    Sign up window
    """
    try:

        def __init__(self, parent, client):
            """
            constructor.
            """
            try:
                super(SignUp, self).__init__(parent, title="Sign Up",
                                             size=(FRAME_WIDTH, FRAME_LENGTH))
                self.combo_box = None
                self.name = None
                self.password = None
                self.client = client
                self.InitUI()
            except socket.error as msg:
                print("socket error:", msg)
            except Exception as msg:
                print("general error: ", msg)

        def InitUI(self):
            """
            initiates window controls and displays it.
            """
            try:
                menu_bar = wx.MenuBar()
                menu = wx.Menu()
                menu_item = menu.Append(wx.ID_CLOSE, 'Quit', 'Quit application')
                menu_bar.Append(menu, '&Menu')
                self.SetMenuBar(menu_bar)
                self.Bind(wx.EVT_MENU, self.onQuit, menu_item)
                pnl = wx.Panel(self)
                sb = wx.StaticBox(pnl, label='Parameters')
                sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
                text_one = wx.StaticText(pnl, label='User Name')
                self.name = wx.TextCtrl(pnl)
                sbs.Add(text_one)
                sbs.Add(self.name, flag=wx.LEFT, border=BORDER)
                text_two = wx.StaticText(pnl, label='Password (6 characters, including letters and numbers)')
                self.password = wx.TextCtrl(pnl, style=wx.TE_PROCESS_ENTER | wx.TE_PASSWORD)
                sbs.Add(text_two)
                sbs.Add(self.password, flag=wx.LEFT, border=BORDER)
                pnl.SetSizer(sbs)
                cbtn = wx.Button(pnl, label='sign up', pos=(SEND_BUTTON_X, SEND_BUTTON_Y))
                cbtn.Bind(wx.EVT_BUTTON, self.on_sign_up)
                self.password.Bind(wx.EVT_TEXT_ENTER, self.on_sign_up)
                self.Centre()
                self.Show(True)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_sign_up(self, e):
            """
            creates a file and writes the given
            username and password in this file.
            """
            f = open("client_sign_up.txt", "w")
            nm = self.name.GetLineText(FIRST)
            pswd = self.password.GetLineText(FIRST)
            if " " not in nm:
                wx.MessageBox("you have to enter last name as well")
            else:
                if not self.check_password(pswd):
                    wx.MessageBox("Weak password, password must contain letters, numbers and at least six characters")
                else:
                    hasher = hashlib.sha256()
                    bpswd = pswd.encode('utf-8')
                    hasher.update(bpswd)
                    pswd = hasher.hexdigest()
                    f.write(nm + "\n" + pswd)
                    f.close()
                    DETACHED_PROCESS = 0x00000008
                    results = \
                        subprocess.Popen(["C:\\Networks\\Python3.8\\python.exe"],
                                         close_fds=True,
                                         creationflags=DETACHED_PROCESS)
                    command = "ADD"
                    prm = nm + " " + pswd
                    request = command + " " + prm
                    # self.client = Client(CLIENT_IP, PORT, nm)
                    response = self.client.send_and_receive(request)
                    wx.MessageBox(response, "Response", wx.OK |
                                  wx.ICON_INFORMATION)
                    #  self.client = Client(CLIENT_IP, PORT, nm)
                    self.Close()

        def check_password(self, pswd):
            """
            This function checks if the password contain at lest one digit
            and at least one english letter. I added this function to
            require strong passwords from clients.
            """
            if len(pswd) >= 6:
                flag1 = False
                flag2 = False
                for x in range(len(pswd)):
                    if pswd[x].isdigit():
                        flag1 = True
                    if pswd[x].isalpha():
                        flag2 = True
                return flag1 and flag2
            return False

        def onQuit(self, e):
            """
            called on quit selection.
            quits window.
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_click(self, e):
            """
            called on button click and displays a message box.
            """
            try:
                wx.MessageBox("button clicked", "title", wx.OK)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_send(self, e):
            """
            closes the window
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg
    except socket.error as msg:
        print("socket error:", msg)
    except Exception as msg:
        print("general error: ", msg)


##############################################################################
#                            commands window                                 #
##############################################################################

class Commands(wx.Frame):
    """
    a window with two options: log in/ sign in
    """
    try:

        def __init__(self, parent, clients_name, client):
            """
            constructor.
            """
            try:
                super(Commands, self).__init__(parent,
                                               title="Commands",
                                               size=(FRAME_WIDTH,
                                                     FRAME_LENGTH))
                self.params = []
                self.combo_box = None
                self.name = clients_name
                self.client = client
                self.bitmap = None
                self.InitUI()
            except socket.error as msg:
                print("socket error:", msg)
            except Exception as msg:
                print("general error: ", msg)

        def InitUI(self):
            """
            initiates window controls and displays it.
            """
            try:
                menu_bar = wx.MenuBar()
                menu = wx.Menu()
                menu_item = menu.Append(wx.ID_CLOSE, 'Quit', 'Quit application')
                menu_bar.Append(menu, '&Menu')
                self.SetMenuBar(menu_bar)
                self.Bind(wx.EVT_MENU, self.onQuit, menu_item)
                pnl = wx.Panel(self)
                cbtn1 = wx.Button(pnl, label='get location', pos=(COMMAND_LABEL_X, COMMAND_LABEL_Y))
                cbtn1.Bind(wx.EVT_BUTTON, self.on_send)
                cbtn2 = wx.Button(pnl, label='make a sound', pos=(BUTTON_X, BUTTON_Y))
                cbtn2.Bind(wx.EVT_BUTTON, self.on_click_sound)
                cbtn1.Bind(wx.EVT_BUTTON, self.on_click_get_location)
                back_btn = wx.Button(pnl, label='Back to options', pos=(BACK_BUTTON_X, BACK_BUTTON_Y))
                back_btn.Bind(wx.EVT_BUTTON, self.on_back)
                self.Centre()
                self.Show(True)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_back(self, event):
            self.Close()
            Options(None)
            wx.App().MainLoop()

        def onQuit(self, e):
            """
            called on quit selection.
            quits window.
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_click_sound(self, e):
            """
            called on button click and makes the PC
            make a sound.
            """
            try:
                command = "BEEP"
                prm = self.name
                request = command + " " + prm
                response = self.client.send_and_receive(request)
                wx.MessageBox(response, "Sound", wx.OK |
                              wx.ICON_INFORMATION)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_click_get_location(self, e):
            """
            called on button click and displays a message box
            including the location of the PC.
            """
            try:
                photo_place = "location_map.jpg"
                command = "GET_LOCATION"
                prm = self.name
                request = command + " " + prm
                response = self.client.send_and_receive(request)
                Map(None, photo_place, response)
                wx.App().MainLoop()

            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_send(self, e):
            """
            closes the window
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg
    except socket.error as msg:
        print("socket error:", msg)
    except Exception as msg:
        print("general error: ", msg)


##############################################################################
#                            maps window                                     #
##############################################################################

class Map(wx.Frame):
    """
    a window with two options: log in/ sign in
    """
    try:

        def __init__(self, parent, photo_place, location):
            """
            constructor.
            """
            try:
                super(Map, self).__init__(parent,
                                          title="Map",
                                          size=(406,
                                                470))
                self.params = []
                self.combo_box = None
                self.bitmap = None
                self.photo_place = photo_place
                self.location = location
                self.InitUI()
            except socket.error as msg:
                print("socket error:", msg)
            except Exception as msg:
                print("general error: ", msg)

        def InitUI(self):
            """
            initiates window controls and displays it.
            """
            try:
                # generate menu
                menu_bar = wx.MenuBar()
                menu = wx.Menu()
                menu_item = menu.Append(wx.ID_CLOSE, 'Quit',
                                        'Quit application')
                menu_bar.Append(menu, '&Map')
                self.SetMenuBar(menu_bar)

                # bind quit menu item to on_quit method
                self.Bind(wx.EVT_MENU, self.onQuit, menu_item)

                # generate panel
                pnl = wx.Panel(self)

                # A static box is a vertical / horizontal sequence of items
                sb = wx.StaticBox(pnl, label='Map')

                # A static box sizer provides a border around a static box
                sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

                self.on_click_show_map()

                self.Centre()
                self.Show(True)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def onQuit(self, e):
            """
            called on quit selection.
            quits window.
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_click_show_map(self):
            """
            called on button click and displays a message box
            including the location of the PC.
            """
            try:
                response = Location_handler.create_map(self.location)
                if response is True:
                    image_final = wx.Image(self.photo_place,
                                           wx.BITMAP_TYPE_ANY)
                    image_final = image_final.Scale(400, 400,
                                                    wx.IMAGE_QUALITY_HIGH)
                    self.bitmap = wx.StaticBitmap(self, -1,
                                                  wx.Bitmap(image_final))
                    self.bitmap.SetPosition(200, 100)
                else:
                    wx.MessageBox(response, "cant show map", wx.OK |
                                  wx.ICON_INFORMATION)
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg

        def on_send(self, e):
            """
            closes the window
            """
            try:
                self.Close()
            except socket.error as msg:
                print("socket error:", msg)
                return "socket error: %s" % msg
            except Exception as msg:
                print("general error: ", msg)
                return "general error: %s" % msg
    except socket.error as msg:
        print("socket error:", msg)
    except Exception as msg:
        print("general error: ", msg)


def main():
    """
    initiates wx, runs the window and runs event loop.
    :return:
    """
    try:
        app = wx.App()
        # start window
        Options(None)
        app.MainLoop()
        # start window
        LogIn(None)
        app.MainLoop()
        # start window
    except socket.error as msg:
        print("socket error:", msg)
    except Exception as msg:
        print("general error: ", msg)


if __name__ == '__main__':
    main()
