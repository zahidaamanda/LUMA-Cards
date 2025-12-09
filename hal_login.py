from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.app import App

# KV String untuk HalLogin
KV_LOGIN = '''
# Custom Widget Definitions
<TransparentButton@Button>:
    background_normal: ''
    background_color: 0, 0, 0, 0
    color: 0.0039, 0.1922, 0.4471, 1
    font_size: 16
    bold: True
    size_hint: None, None
    height: 40

<RoundedTextInput@TextInput>:
    background_normal: ''
    background_active: ''
    background_color: 0, 0, 0, 0
    foreground_color: 0, 0, 0, 1
    font_size: 20
    multiline: False
    size_hint: None, None
    size: 560, 78
    padding: [30, (self.height - self.line_height) / 2]
    halign: 'left'
    write_tab: False
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.8
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [30]
        Color:
            rgba: 0.0039, 0.1922, 0.4471, 0.5
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, 30]
            width: 1.5

<RoundedLoginButton@Button>:
    background_normal: ''
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    font_size: 32
    bold: True
    size_hint: None, None
    size: 260, 90
    canvas.before:
        Color:
            rgba: 0.0039, 0.1922, 0.4471, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [50]

<HalLogin>:
    FloatLayout:
        Image:
            source: 'Media/Background.png'
            allow_stretch: True
            keep_ratio: True
            size_hint: 1, 1
        
        Image:
            source: 'Media/login.png'
            size_hint: None, None
            size: 1566, 968
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            size: 400, 50
            pos_hint: {'center_x': 0.66, 'y': 0.3}
            spacing: 10
            
            TransparentButton:
                text: "________________"
                size_hint: None, None
                size: 100, 40
                on_press: root.go_to_signup()
        
        RoundedTextInput:
            id: username_input
            hint_text: "Username"
            pos_hint: {'center_x': 0.7, 'center_y': 0.598}
            text: root.username
            on_text: root.username = self.text
        
        RoundedTextInput:
            id: password_input
            hint_text: "Password"
            pos_hint: {'center_x': 0.7, 'center_y': 0.435}
            password: True
            text: root.password
            on_text: root.password = self.text
        
        RoundedLoginButton:
            text: "Login"
            pos_hint: {'center_x': 0.71, 'center_y': 0.25}
            on_press: root.verify_login()
        
        Label:
            id: status_label
            text: root.login_status
            color: 1, 0, 0, 1
            size_hint: None, None
            size: 300, 30
            pos_hint: {'center_x': 0.71, 'y': 0.17}
            opacity: 1 if root.login_status else 0
            font_size: 17
'''

# Load KV string
Builder.load_string(KV_LOGIN)

class HalLogin(Screen):
    """Screen untuk login dengan input fields dan tombol"""
    username = StringProperty("")
    password = StringProperty("")
    login_status = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        self.logged_in_user = ""  # Simpan username yang berhasil login
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif"""
        # Reset form saat screen aktif
        self.username = ""
        self.password = ""
        self.login_status = ""
        self.logged_in_user = ""
    
    def go_to_signup(self):
        """Pindah ke screen signup"""
        if self.manager:
            self.manager.current = 'signup'
    
    def verify_login(self):
        """Verifikasi login dengan database"""
        # Validasi input
        if not self.username:
            self.login_status = "Username cannot be empty!"
            return
        elif not self.password:
            self.login_status = "Password cannot be empty!"
            return
        
        # Dapatkan instance database dari App
        app = App.get_running_app()
        
        # Verifikasi login
        user_data = app.db.verify_login(self.username, self.password)
        
        if user_data:
            user_id, username = user_data
            
            # Cek apakah user sudah lengkap registrasinya
            progress = app.db.get_user_progress(username)
            
            if progress:
                signup_complete, biodata_complete, photo_complete = progress
                
                if not all([signup_complete, biodata_complete, photo_complete]):
                    self.login_status = "Registration is not complete!"
                    return
            
            print(f"✓ Login berhasil - Username: {username}, ID: {user_id}")
            self.logged_in_user = username
            
            # Pindah ke screen card
            if self.manager:
                self.manager.current = 'card'
        else:
            self.login_status = "Username or password is wrong!"