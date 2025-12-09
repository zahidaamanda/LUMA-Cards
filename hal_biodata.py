from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.app import App

KV_BIODATA = '''
<BiodataTextInput@TextInput>:
    background_normal: ''
    background_active: ''
    background_color: 0, 0, 0, 0
    foreground_color: 0, 0, 0, 1
    font_size: 22
    multiline: False
    size_hint: None, None
    size: 590, 78
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

<LargeBiodataTextInput@TextInput>:
    background_normal: ''
    background_active: ''
    background_color: 0, 0, 0, 0
    foreground_color: 0, 0, 0, 1
    font_size: 22
    multiline: False
    size_hint: None, None
    size: 1275, 78
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

<RoundedNextButton@Button>:
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

<HalBiodata>:
    FloatLayout:
        # Background image
        Image:
            source: 'Media/Background.png'
            allow_stretch: True
            keep_ratio: True
            size_hint: 1, 1
        
        # Form background image
        Image:
            id: biodata_bg
            source: 'Media/biodata.png'
            size_hint: None, None
            size: 1566, 968
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        # INPUT 1: No.ID
        BiodataTextInput:
            id: no_id_input
            hint_text: "No.ID"
            pos_hint: {'center_x': 0.3, 'center_y': 0.448}
            text: root.no_id
            on_text: root.no_id = self.text
        
        # INPUT 2: Division
        BiodataTextInput:
            id: division_input
            hint_text: "Division"
            pos_hint: {'center_x': 0.3, 'center_y': 0.27}
            text: root.division
            on_text: root.division = self.text
        
        # INPUT 3: Birth Date
        BiodataTextInput:
            id: birth_date_input
            hint_text: "Birth Date (Ex. 01 January 2008)"
            pos_hint: {'center_x': 0.697, 'center_y': 0.448}
            text: root.birth_date
            on_text: root.birth_date = self.text
        
        # INPUT 4: E-mail
        BiodataTextInput:
            id: email_input
            hint_text: "E-mail"
            pos_hint: {'center_x': 0.697, 'center_y': 0.27}
            text: root.email
            on_text: root.email = self.text
        
        # INPUT 5: Full Name
        LargeBiodataTextInput:
            id: full_name_input
            hint_text: "Full Name"
            pos_hint: {'center_x': 0.5, 'center_y': 0.608}
            text: root.full_name
            on_text: root.full_name = self.text
        
        RoundedNextButton:
            text: "Next"
            pos_hint: {'center_x': 0.79, 'center_y': 0.14}
            on_press: root.save_biodata() 
        
        # Status Label
        Label:
            id: biodata_status_label
            text: root.biodata_status
            color: 1, 0, 0, 1
            size_hint: None, None
            size: 300, 30
            pos_hint: {'center_x': 0.2, 'y': 0.18}
            opacity: 1 if root.biodata_status else 0
            font_size: 17
'''

# Load KV string
Builder.load_string(KV_BIODATA)

class HalBiodata(Screen):
    """Screen untuk biodata dengan 5 input text"""
    full_name = StringProperty("")
    no_id = StringProperty("")
    division = StringProperty("")
    birth_date = StringProperty("")
    email = StringProperty("")
    biodata_status = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'biodata'
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif"""
        # Reset form saat screen aktif
        self.full_name = ""
        self.no_id = ""
        self.division = ""
        self.birth_date = ""
        self.email = ""
        self.biodata_status = ""
    
    def save_biodata(self):
        """Simpan biodata ke database"""
        # Validasi input
        if not self.full_name:
            self.biodata_status = "Full Name cannot be empty!"
            return
        elif not self.no_id:
            self.biodata_status = "No.ID cannot be empty!"
            return
        elif not self.division:
            self.biodata_status = "Division cannot be empty!"
            return
        elif not self.birth_date:
            self.biodata_status = "Birth Date cannot be empty!"
            return
        elif not self.email:
            self.biodata_status = "E-mail cannot be empty!"
            return
        
        # Dapatkan username dari screen signup
        signup_screen = self.manager.get_screen('signup')
        username = signup_screen.current_username
        
        if not username:
            self.biodata_status = "Please signup first!"
            return
        
        # Dapatkan instance database dari App
        app = App.get_running_app()
        
        # Update biodata di database
        success = app.db.update_biodata(
            username, 
            self.full_name, 
            self.no_id, 
            self.division, 
            self.birth_date, 
            self.email
        )
        
        if success:
            print(f"✓ Biodata disimpan untuk user: {username}")
            print(f"  Full Name: {self.full_name}")
            print(f"  No.ID: {self.no_id}")
            print(f"  Division: {self.division}")
            print(f"  Birth Date: {self.birth_date}")
            print(f"  E-mail: {self.email}")
            
            # Pindah ke screen poto
            if self.manager:
                self.manager.current = 'poto'
        else:
            self.biodata_status = "Failed to save biodata!"

