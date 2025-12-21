from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.graphics import Fbo, Color, Rectangle, ClearColor, ClearBuffers
from kivy.core.image import Image as CoreImage
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
import os
from datetime import datetime
import platform
from kivy.clock import Clock

KV_CARD = '''
# Custom Widget Definitions untuk Card
<ImageButtonLogout@Button>:
    color: 1, 1, 1, 1
    font_size: 18
    bold: False
    background_normal: 'Media/logout.png'
    background_color: 1, 1, 1, 1

<DownloadButton@Button>:
    background_color: 0.2, 0.6, 0.9, 1
    color: 1, 1, 1, 1
    font_size: 18
    bold: True
    size_hint: None, None
    size: 200, 60
    background_normal: ''

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
    pos_hint: {'center_x': 0.3, 'center_y': 0.48}
    opacity: 0
    allow_stretch: True
    keep_ratio: True

<CardContent@FloatLayout>:
    # Container untuk elemen-elemen yang akan didownload
    Image:
        source: 'Media/card.png'
        size_hint: None, None
        size: 1566, 968
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    
    # Labels untuk menampilkan data user
    DataLabel:
        id: full_name_label
        text: ""
        size: 450, 40
        pos_hint: {'center_x': 0.655, 'center_y': 0.64}
    
    DataLabel:
        id: no_id_label
        text: ""
        size: 450, 40
        pos_hint: {'center_x': 0.655, 'center_y': 0.56}
    
    DataLabel:
        id: division_label
        text: ""
        size: 450, 40
        pos_hint: {'center_x': 0.655, 'center_y': 0.4}
    
    DataLabel:
        id: birth_date_label
        text: ""
        size: 450, 40
        pos_hint: {'center_x': 0.655, 'center_y': 0.481}
    
    DataLabel:
        id: email_label
        text: ""
        size: 450, 40
        pos_hint: {'center_x': 0.655      , 'center_y': 0.322}
    
    # Container untuk foto
    PhotoContainer:
        id: user_photo

<HalCard>:
    FloatLayout:
        # Background (tidak akan ikut didownload)
        Image:
            source: 'Media/Background.png'
            allow_stretch: True
            keep_ratio: True
            size_hint: 1, 1
        
        # Container untuk card content
        CardContent:
            id: card_content
        
        # Tombol logout (tidak akan ikut didownload)
        ImageButtonLogout:
            id: logout_button
            text: ""
            size_hint: None, None
            size: 200, 85
            pos_hint: {'x': 0.02, 'top': 0.98}
            on_press: root.go_back_to_login()
        
        # Tombol download
        DownloadButton:
            id: download_button
            text: "Download Card"
            pos_hint: {'center_x': 0.5, 'y': 0.02}
            on_press: root.download_card_as_png()
'''

# Load KV string
Builder.load_string(KV_CARD)

class HalCard(Screen):
    """Screen untuk menampilkan data user dari database"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'card'
        self.is_capturing = False
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif - load data user"""
        # Dapatkan username yang login dari screen login
        login_screen = self.manager.get_screen('login')
        username = login_screen.logged_in_user
        
        if username:
            self.load_user_data(username)
        else:
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
            self.ids.card_content.ids.full_name_label.text = full_name or "N/A"
            self.ids.card_content.ids.no_id_label.text = no_id or "N/A"
            self.ids.card_content.ids.division_label.text = division or "N/A"
            self.ids.card_content.ids.birth_date_label.text = birth_date or "N/A"
            self.ids.card_content.ids.email_label.text = email or "N/A"
            
            # Tampilkan foto jika ada
            if photo_path:
                print(f"Loading photo from: {photo_path}")
                try:
                    self.ids.card_content.ids.user_photo.source = photo_path
                    self.ids.card_content.ids.user_photo.opacity = 1
                    print(f"✓ Foto berhasil dimuat")
                except Exception as e:
                    print(f"✗ Error loading photo: {e}")
                    self.ids.card_content.ids.user_photo.opacity = 0
                    self.ids.card_content.ids.user_photo.source = ''
            else:
                self.ids.card_content.ids.user_photo.opacity = 0
                self.ids.card_content.ids.user_photo.source = ''

        else:
            self.ids.card_content.ids.full_name_label.text = "Data not found!"
    
    def download_card_as_png(self):
        """Mendownload card content sebagai PNG file"""
        if self.is_capturing:
            return
            
        try:
            self.is_capturing = True
            print("Starting download process...")
            
            # Tampilkan status
            self.show_status_popup("Mempersiapkan card...", auto_dismiss=False)
            
            # Tunggu sedikit untuk memastikan UI siap
            Clock.schedule_once(lambda dt: self._prepare_capture(), 0.2)
            
        except Exception as e:
            print(f"✗ Error in download_card_as_png: {e}")
            import traceback
            traceback.print_exc()
            self.show_status_popup(f"Error: {str(e)}", is_error=True, auto_dismiss=True)
            self.is_capturing = False
    
    def _prepare_capture(self):
        """Persiapkan capture"""
        try:
            # Sembunyikan tombol yang tidak ingin di-capture
            self.ids.logout_button.opacity = 0
            self.ids.download_button.opacity = 0
            
            # Force layout update
            self.ids.card_content._trigger_layout()
            
            # Tunggu layout selesai
            Clock.schedule_once(lambda dt: self._capture_card(), 0.1)
            
        except Exception as e:
            print(f"Error in prepare_capture: {e}")
            self.restore_ui()
            self.is_capturing = False
    
    def _capture_card(self):
        """Capture card setelah UI siap"""
        try:
            # Buat nama file
            full_name = self.ids.card_content.ids.full_name_label.text
            if full_name and full_name != "N/A" and full_name != "Data not found!":
                safe_name = "".join(c for c in full_name if c.isalnum() or c in (' ', '-', '_')).strip()
                if not safe_name:
                    safe_name = "user_card"
                filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            else:
                filename = f"user_card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            print(f"Filename: {filename}")
            self.show_status_popup("Menyimpan card...", auto_dismiss=False)
        
            card_content = self.ids.card_content
            
            # Cek apakah export_to_png tersedia
            if hasattr(card_content, 'export_to_png'):
                print("Using export_to_png method")
                save_path = self.get_save_path(filename)
                
                # Simpan ukuran asli
                original_size = card_content.size
                original_size_hint = card_content.size_hint
                original_pos_hint = card_content.pos_hint
                
                try:
                    # Set ukuran yang tepat untuk export
                    card_content.size_hint = (None, None)
                    card_content.pos_hint = {}
                    card_content.size = (1566, 968)
                    card_content.pos = (0, 0)
                    
                    # Force layout
                    card_content._trigger_layout()
                    
                    # Export ke PNG
                    card_content.export_to_png(save_path)
                    
                    print(f"✓ Card exported to: {save_path}")
                    
                finally:
                    # Kembalikan ke ukuran asli
                    card_content.size = original_size
                    card_content.size_hint = original_size_hint
                    card_content.pos_hint = original_pos_hint
                    
            else:
                print("Using manual FBO method")
                save_path = self.get_save_path(filename)
                
                # Buat FBO dengan ukuran card
                fbo = Fbo(size=(1566, 968))
                
                with fbo:
                    ClearColor(0, 0, 0, 0)
                    ClearBuffers()
                    Color(1, 1, 1, 1)
                    Rectangle(pos=(0, 0), size=(1566, 968))
                
                self._render_widget_to_fbo(card_content, fbo)
                
                fbo.draw()
                
                texture = fbo.texture
                img = CoreImage(texture, ext='png')
                img.save(save_path, flipped=False)
                
                print(f"✓ Card saved via FBO to: {save_path}")
            
            self.restore_ui()
            
            Clock.schedule_once(lambda dt: self.show_success_popup(save_path), 0.5)
            
        except Exception as e:
            print(f"✗ Error during capture: {e}")
            import traceback
            traceback.print_exc()
            
            self.restore_ui()
        
            self.show_status_popup(f"Gagal menyimpan: {str(e)}", is_error=True, auto_dismiss=True)
            
        finally:
            self.is_capturing = False
    
    def _render_widget_to_fbo(self, widget, fbo):
        """Render widget ke FBO dengan pendekatan manual"""
        try:
            # Simpan state asli
            original_canvas = widget.canvas
            original_pos = widget.pos
            original_size = widget.size
            original_size_hint = widget.size_hint
            original_pos_hint = widget.pos_hint
            
            try:
                # Set widget ke posisi dan ukuran yang sesuai untuk FBO
                widget.size_hint = (None, None)
                widget.pos_hint = {}
                widget.size = (1566, 968)
                widget.pos = (0, 0)
                
                # Force layout
                widget._trigger_layout()
                
                # Render ke FBO
                fbo.add(widget.canvas)
                
                # Update FBO
                fbo.ask_update()
                
            finally:
                # Hapus dari FBO
                fbo.remove(widget.canvas)
                
                # Kembalikan ke state asli
                widget.canvas = original_canvas
                widget.pos = original_pos
                widget.size = original_size
                widget.size_hint = original_size_hint
                widget.pos_hint = original_pos_hint
                
        except Exception as e:
            print(f"Error in render_widget_to_fbo: {e}")
            raise
    
    def get_save_path(self, filename):
        """Mendapatkan path untuk menyimpan file"""
        # Coba beberapa lokasi yang umum
        system = platform.system()
        
        # Lokasi yang akan dicoba (prioritas)
        if system == 'Windows':
            possible_dirs = [
                os.path.join(os.path.expanduser("~"), "Downloads", "ID_Cards"),
                os.path.join(os.path.expanduser("~"), "Documents", "ID_Cards"),
                os.path.join(os.path.expanduser("~"), "Desktop", "ID_Cards"),
                os.path.join(os.getcwd(), "saved_cards")
            ]
        elif system == 'Darwin':  # macOS
            possible_dirs = [
                os.path.join(os.path.expanduser("~"), "Downloads", "ID_Cards"),
                os.path.join(os.path.expanduser("~"), "Documents", "ID_Cards"),
                os.path.join(os.path.expanduser("~"), "Desktop", "ID_Cards"),
                os.path.join(os.getcwd(), "saved_cards")
            ]
        else:  # Linux atau lainnya
            possible_dirs = [
                os.path.join(os.path.expanduser("~"), "Downloads", "ID_Cards"),
                os.path.join(os.path.expanduser("~"), "Documents", "ID_Cards"),
                os.path.join(os.path.expanduser("~"), "Desktop", "ID_Cards"),
                os.path.join(os.getcwd(), "saved_cards")
            ]
        
        # Pilih direktori pertama yang bisa diakses
        save_dir = None
        for dir_path in possible_dirs:
            try:
                os.makedirs(dir_path, exist_ok=True)
                # Test write permission
                test_file = os.path.join(dir_path, "test.tmp")
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                save_dir = dir_path
                print(f"✓ Using directory: {save_dir}")
                break
            except Exception as e:
                print(f"✗ Cannot use {dir_path}: {e}")
                continue
        
        # Jika semua gagal, gunakan direktori saat ini
        if save_dir is None:
            save_dir = os.getcwd()
            print(f"⚠ Falling back to current directory: {save_dir}")
            os.makedirs(save_dir, exist_ok=True)
        
        full_path = os.path.join(save_dir, filename)
        print(f"Full save path: {full_path}")
        
        return full_path
    
    def show_status_popup(self, message, is_error=False, auto_dismiss=True):
        """Menampilkan popup status"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        
        try:
            title = "Error" if is_error else "Status"
            color = (1, 0, 0, 1) if is_error else (0, 0, 0, 1)
            
            label = Label(text=message, color=color, padding=10)
            popup = Popup(
                title=title,
                content=label,
                size_hint=(0.6, 0.3),
                auto_dismiss=auto_dismiss
            )
            
            if auto_dismiss and not is_error:
                Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
            
            popup.open()
            return popup
            
        except Exception as e:
            print(f"Error showing popup: {e}")
            return None
    
    def show_success_popup(self, save_path):
        """Menampilkan popup sukses dengan opsi open folder"""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        
        def open_folder(instance):
            import subprocess
            folder_path = os.path.dirname(save_path)
            try:
                if platform.system() == 'Windows':
                    os.startfile(folder_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.Popen(['open', folder_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', folder_path])
            except Exception as e:
                print(f"Error opening folder: {e}")
                self.show_status_popup(f"Cannot open folder: {str(e)}", is_error=True, auto_dismiss=True)
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Tampilkan nama file saja
        file_name = os.path.basename(save_path)
        folder_name = os.path.basename(os.path.dirname(save_path))
        
        label = Label(
            text=f'Card berhasil disimpan!\n\nNama file: {file_name}\nFolder: {folder_name}',
            size_hint_y=0.7,
            halign='center',
            valign='middle'
        )
        label.bind(size=lambda s, w: s.setter('text_size')(s, (w, None)))
        
        btn_box = BoxLayout(size_hint_y=0.3, spacing=10)
        open_btn = Button(text='Buka Folder', background_color=(0.2, 0.6, 0.9, 1))
        ok_btn = Button(text='OK', background_color=(0.4, 0.4, 0.4, 1))
        
        open_btn.bind(on_press=open_folder)
        ok_btn.bind(on_press=lambda x: popup.dismiss())
        
        btn_box.add_widget(open_btn)
        btn_box.add_widget(ok_btn)
        
        content.add_widget(label)
        content.add_widget(btn_box)
        
        popup = Popup(
            title='Sukses',
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def restore_ui(self):
        """Restore UI ke keadaan semula"""
        try:
            self.ids.logout_button.opacity = 1
            self.ids.download_button.opacity = 1
        except Exception as e:
            print(f"Error restoring UI: {e}")
    
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
