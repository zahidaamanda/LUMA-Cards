from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.app import App

# KV String untuk HalSignup - Disesuaikan sama dengan HalLogin
KV_SIGNUP = '''
<ImageButton@Button>:
    color: 1, 1, 1, 1
    font_size: 18
    bold: False
    background_normal: 'Media/back.png'
    background_color: 1, 1, 1, 1

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

<RoundedSignupButton@Button>:
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

<HalSignup>:
    FloatLayout:
        Image:
            source: 'Media/Background.png'
            allow_stretch: True
            keep_ratio: True
            size_hint: 1, 1
        
        Image:
            source: 'Media/signup.png'
            size_hint: None, None
            size: 1566, 968
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        ImageButton:
            text: ""
            size_hint: None, None
            size: 200, 85
            pos_hint: {'x': 0.02, 'top': 0.98}
            on_press: root.go_back_to_login()
        
        RoundedTextInput:
            id: signup_username_input
            hint_text: "Create a Username"
            pos_hint: {'center_x': 0.7, 'center_y': 0.598}
            text: root.signup_username
            on_text: root.signup_username = self.text
        
        RoundedTextInput:
            id: signup_password_input
            hint_text: "Create a Password"
            pos_hint: {'center_x': 0.7, 'center_y': 0.418}
            password: True
            text: root.signup_password
            on_text: root.signup_password = self.text
        
        RoundedSignupButton:
            text: "Sign Up"
            pos_hint: {'center_x': 0.71, 'center_y': 0.28}
            on_press: root.signup_user()

        Label:
            id: signup_status_label
            text: root.signup_status
            color: 1, 0, 0, 1
            size_hint: None, None
            size: 300, 30
            pos_hint: {'center_x': 0.71, 'y': 0.19}
            opacity: 1 if root.signup_status else 0
            font_size: 17
'''

# Load KV string
Builder.load_string(KV_SIGNUP)

class HalSignup(Screen):
    signup_username = StringProperty("")
    signup_password = StringProperty("")
    signup_status = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'signup'
        self.current_username = ""  # Simpan username untuk tahap berikutnya
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif"""
        # Reset form saat screen aktif
        self.signup_username = ""
        self.signup_password = ""
        self.signup_status = ""
        self.current_username = ""
    
    def go_back_to_login(self):
        """Kembali ke screen login"""
        if self.manager:
            self.manager.current = 'login'
    
    def signup_user(self):
        """Membuat user baru di database"""
        # Validasi input
        if not self.signup_username:
            self.signup_status = "Username cannot be empty!"
            return
        elif not self.signup_password:
            self.signup_status = "Password cannot be empty!"
            return
        
        # Dapatkan instance database dari App
        app = App.get_running_app()
        
        # Cek apakah username sudah ada
        if app.db.check_username_exists(self.signup_username):
            self.signup_status = "Username has been used!"
            return
        
        # Simpan user ke database
        user_id = app.db.create_user(self.signup_username, self.signup_password)
        
        if user_id:
            print(f"✓ Signup berhasil - Username: {self.signup_username}, ID: {user_id}")
            self.current_username = self.signup_username  # Simpan untuk screen berikutnya
            
            # Pindah ke screen biodata
            if self.manager:
                self.manager.current = 'biodata'
        else:
            self.signup_status = "Cannot create an account. Try another username."