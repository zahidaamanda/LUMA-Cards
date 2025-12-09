from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.clock import Clock
from plyer import filechooser
import os
from kivy.app import App

# KV String untuk HalPoto
KV_POTO = '''
<ImageButton@Button>:
    color: 1, 1, 1, 1
    font_size: 18
    bold: False
    background_normal: 'Media/back.png'
    background_color: 1, 1, 1, 1

<RoundedUploadButton@Button>:
    background_normal: ''
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    font_size: 28
    bold: True
    size_hint: None, None
    size: 260, 80
    canvas.before:
        Color:
            rgba: 0.0039, 0.1922, 0.4471, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [40]

<RoundedDeleteButton@Button>:
    background_normal: ''
    background_color: 0, 0, 0, 0
    color: 1, 1, 1, 1
    font_size: 28
    bold: True
    size_hint: None, None
    size: 260, 80
    canvas.before:
        Color:
            rgba: 1.0, 0.541, 0.541, 1.0
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [40]

<RoundedSaveButton@Button>:
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

<ImagePreview@AsyncImage>:
    size_hint: None, None
    size: 300, 300
    allow_stretch: True
    keep_ratio: True

<HalPoto>:
    FloatLayout:
        Image:
            source: 'Media/Background.png'
            allow_stretch: True
            keep_ratio: True
            size_hint: 1, 1
        
        Image:
            source: 'Media/poto.png'
            size_hint: None, None
            size: 1566, 968
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        # Tombol Back
        ImageButton:
            text: ""
            size_hint: None, None
            size: 200, 85
            pos_hint: {'x': 0.02, 'top': 0.98}
            on_press: root.go_back_to_biodata()
        
        # Container untuk preview gambar
        ImagePreview:
            id: image_preview
            source: ''
            opacity: 0
            pos_hint: {'center_x': 0.5007, 'center_y': 0.502}
        
        # Container untuk tombol Select dan Delete
        BoxLayout:
            orientation: 'horizontal'
            size_hint: None, None
            size: 600, 100
            pos_hint: {'center_x': 0.518, 'center_y': 0.255}
            spacing: 15
            
            RoundedUploadButton:
                id: upload_button
                text: "Select"
                on_press: root.open_file_chooser()
            
            RoundedDeleteButton:
                id: delete_button
                text: "Delete"
                on_press: root.delete_image()
                disabled: True
        
        # Tombol Save TERPISAH
        RoundedSaveButton:
            id: save_button
            text: "Save"
            pos_hint: {'center_x': 0.79, 'center_y': 0.14}
            on_press: root.save_all_data()
            disabled: True
        
        # Label status
        Label:
            id: status_label
            text: ""
            color: 1, 0, 0, 1
            size_hint: None, None
            size: 400, 30
            pos_hint: {'center_x': 0.5, 'y': 0.16}
            opacity: 0
            font_size: 16
            bold: True
'''

# Load KV string
Builder.load_string(KV_POTO)

class HalPoto(Screen):
    """Screen untuk upload dan preview foto"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'poto'
        self.image_path = None
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif"""
        self.reset_state()
    
    def reset_state(self):
        """Reset semua state ke awal"""
        self.image_path = None
        if hasattr(self, 'ids'):
            self.ids.image_preview.source = ''
            self.ids.image_preview.opacity = 0
            self.ids.delete_button.disabled = True
            self.ids.save_button.disabled = True
            self.ids.status_label.opacity = 0
            self.ids.status_label.text = ""
    
    def open_file_chooser(self):
        """Buka native file chooser menggunakan Plyer"""
        try:
            # Gunakan path default ke Pictures folder atau home directory
            initial_path = os.path.expanduser("~")
            if os.path.exists(os.path.expanduser("~/Pictures")):
                initial_path = os.path.expanduser("~/Pictures")
            
            filechooser.open_file(
                title="Pilih Foto Profil",
                path=initial_path,
                filters=[("Image Files", "*.png", "*.jpg", "*.jpeg")],
                multiple=False,
                on_selection=self.handle_file_selection
            )
        except Exception as e:
            print(f"Error opening file chooser: {e}")
            self.show_status("Failed to open file chooser", True)
    
    def handle_file_selection(self, selection):
        """Handle hasil pemilihan file dari Plyer"""
        if selection:
            filepath = selection[0]
            Clock.schedule_once(lambda dt: self.load_image(filepath))
    
    def load_image(self, filepath):
        """Load dan validasi gambar"""
        try:
            # Normalize path untuk menghindari masalah dengan backslash/forwardslash
            filepath = os.path.normpath(filepath)
            
            if not os.path.exists(filepath):
                self.show_status("File is not found!", True)
                return
            
            valid_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
            file_ext = os.path.splitext(filepath)[1]
            
            if file_ext not in valid_extensions:
                self.show_status("Only file PNG, JPG, JPEG are supported!", True)
                return
            
            file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if file_size_mb > 10:
                self.show_status("Maximum file size 10MB!", True)
                return
            
            self.image_path = filepath
            
            # Tampilkan preview gambar
            self.ids.image_preview.source = filepath
            self.ids.image_preview.opacity = 1
            
            self.ids.delete_button.disabled = False
            self.ids.save_button.disabled = False
            
            self.show_status("Photo was successfully selected!", False)
            
            print(f"✓ Gambar dipilih: {filepath}")
            
        except Exception as e:
            print(f"✗ Error loading image: {e}")
            import traceback
            traceback.print_exc()
            self.show_status("Failed to load image", True)
    
    def delete_image(self):
        """Hapus gambar yang sudah dipilih"""
        if self.image_path:
            self.reset_state()
            self.show_status("Photo was successfully deleted", False)
            print("✓ Gambar dihapus")
        else:
            self.show_status("There are no photo to delete", True)
    
    def show_status(self, message, is_error=True):
        """Tampilkan pesan status sementara"""
        if hasattr(self, 'ids'):
            self.ids.status_label.text = message
            self.ids.status_label.color = (1, 0, 0, 1) if is_error else (0, 0.5, 0, 1)
            self.ids.status_label.opacity = 1
            
            Clock.schedule_once(lambda dt: setattr(self.ids.status_label, 'opacity', 0), 3)
    
    def go_back_to_biodata(self):
        """Kembali ke screen biodata"""
        if self.manager:
            self.manager.current = 'biodata'
    
    def save_all_data(self):
        """Simpan semua data (foto) dan lengkapi registrasi"""
        if not self.image_path:
            self.show_status("Please choose a photo first!", True)
            return
        
        # Dapatkan username dari screen signup
        signup_screen = self.manager.get_screen('signup')
        username = signup_screen.current_username
        
        if not username:
            self.show_status("Please signup first!", True)
            return
        
        # Dapatkan instance database dari App
        app = App.get_running_app()
        
        # Simpan foto ke database (akan disalin ke folder aplikasi)
        saved_photo_path = app.db.update_photo(username, self.image_path)
        
        if saved_photo_path:
            # Lengkapi registrasi
            app.db.complete_registration(username)
            
            print(f"✓ Semua data disimpan untuk user: {username}")
            print(f"  Foto disimpan di: {saved_photo_path}")
            
            # Reset form login
            try:
                login_screen = self.manager.get_screen('login')
                login_screen.username = ""
                login_screen.password = ""
                login_screen.login_status = ""
            except:
                pass
            
            # Tampilkan pesan sukses
            self.show_status("Registration successful! Return to login page...", False)
            
            # Tunggu 2 detik kemudian pindah ke login
            Clock.schedule_once(lambda dt: self.go_to_login(), 2)
        else:
            self.show_status("Failed to save photo!", True)
    
    def go_to_login(self):
        """Pindah ke screen login"""
        if self.manager:
            self.manager.current = 'login'