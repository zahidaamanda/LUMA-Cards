from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App

KV_CARD = '''
# Custom Widget Definitions untuk Card
<ImageButtonLogout@Button>:
    color: 1, 1, 1, 1
    font_size: 18
    bold: False
    background_normal: 'Media/logout.png'
    background_color: 1, 1, 1, 1

<DataLabel@Label>:
    color: 0, 0, 0, 1
    font_size: 32
    bold: True
    size_hint: None, None
    halign: 'left'
    valign: 'middle'
    text_size: self.width, None

<PhotoContainer@AsyncImage>:
    size_hint: None, None
    size: 300, 350
    pos_hint: {'center_x': 0.259, 'center_y': 0.48}
    opacity: 0
    allow_stretch: True
    keep_ratio: True

<HalCard>:
    FloatLayout:
        Image:
            source: 'Media/Background.png'
            allow_stretch: True
            keep_ratio: True
            size_hint: 1, 1
        
        Image:
            source: 'Media/card.png'
            size_hint: None, None
            size: 1566, 968
            pos_hint: {'left_x': 0.5, 'center_y': 0.5}
        
        # Labels untuk menampilkan data user
        DataLabel:
            id: full_name_label
            text: ""
            size: 450, 40
            pos_hint: {'center_x': 0.617, 'center_y': 0.64}
        
        DataLabel:
            id: no_id_label
            text: ""
            size: 450, 40
            pos_hint: {'center_x': 0.617, 'center_y': 0.56}
        
        DataLabel:
            id: division_label
            text: ""
            size: 450, 40
            pos_hint: {'center_x': 0.617, 'center_y': 0.4}
        
        DataLabel:
            id: birth_date_label
            text: ""
            size: 450, 40
            pos_hint: {'center_x': 0.617, 'center_y': 0.481}
        
        DataLabel:
            id: email_label
            text: ""
            size: 450, 40
            pos_hint: {'center_x': 0.617, 'center_y': 0.322}
        
        # Container untuk foto
        PhotoContainer:
            id: user_photo
        
        # Tombol logout
        ImageButtonLogout:
            text: ""
            size_hint: None, None
            size: 200, 85
            pos_hint: {'x': 0.02, 'top': 0.98}
            on_press: root.go_back_to_login()
'''

# Load KV string
Builder.load_string(KV_CARD)

class HalCard(Screen):
    """Screen untuk menampilkan data user dari database"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'card'
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif - load data user"""
        # Dapatkan username yang login dari screen login
        login_screen = self.manager.get_screen('login')
        username = login_screen.logged_in_user
        
        if username:
            print(f"Loading data for user: {username}")
            self.load_user_data(username)
        else:
            print("No logged in user found")
            # Jika tidak ada user yang login, kembali ke login
            self.go_back_to_login()
    
    def load_user_data(self, username):
        """Memuat data user dari database dan menampilkannya"""
        # Dapatkan instance database dari App
        app = App.get_running_app()
        
        # Ambil data user dari database
        user_data = app.db.get_user_data(username)
        
        if user_data:
            full_name, no_id, division, birth_date, email, photo_path = user_data
            
            # Tampilkan data di labels
            self.ids.full_name_label.text = full_name or "N/A"
            self.ids.no_id_label.text = no_id or "N/A"
            self.ids.division_label.text = division or "N/A"
            self.ids.birth_date_label.text = birth_date or "N/A"
            self.ids.email_label.text = email or "N/A"
            
            # Tampilkan foto jika ada
            if photo_path:
                print(f"Loading photo from: {photo_path}")
                try:
                    self.ids.user_photo.source = photo_path
                    self.ids.user_photo.opacity = 1
                    print(f"✓ Foto berhasil dimuat")
                except Exception as e:
                    print(f"✗ Error loading photo: {e}")
                    self.ids.user_photo.opacity = 0
                    self.ids.user_photo.source = ''
            else:
                self.ids.user_photo.opacity = 0
                self.ids.user_photo.source = ''
                print("✗ Foto tidak ditemukan atau tidak ada")
            
            print(f"✓ Data user ditampilkan untuk: {username}")
        else:
            print(f"✗ Tidak ada data untuk user: {username}")
            self.ids.full_name_label.text = "Data not found!"
    
    def go_back_to_login(self):
        """Kembali ke screen login"""
        if self.manager:
            # Reset login screen
            login_screen = self.manager.get_screen('login')
            login_screen.username = ""
            login_screen.password = ""
            login_screen.login_status = ""
            login_screen.logged_in_user = ""
            
            self.manager.current = 'login'