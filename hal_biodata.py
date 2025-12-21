from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import sp
from datetime import datetime, date
import calendar

KV_BIODATA = '''
# Custom widget untuk tombol tanggal di kalender
<DatePickerDayButton@Button>:
    background_normal: ''
    background_color: 0.9, 0.9, 0.9, 1
    color: 0.0039, 0.1922, 0.4471, 0.5
    font_size: 18
    size_hint: None, None
    size: 40, 40

<DatePickerDayButtonSelected@DatePickerDayButton>:
    background_color: 0.0039, 0.1922, 0.4471, 1
    color: 1, 1, 1, 1

<DatePickerDayButtonDisabled@DatePickerDayButton>:
    background_color: 0.95, 0.95, 0.95, 1
    color: 0.7, 0.7, 0.7, 1
    disabled: True

# Popup DatePicker
<DatePickerPopup>:
    size_hint: (0.8, 0.8)
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    background_color: 0, 0, 0, 0
    background: ''
    auto_dismiss: False  # Jangan auto dismiss
    
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [20]
            Color:
                rgba: 0.0039, 0.1922, 0.4471, 1
            Line:
                rounded_rectangle: [self.x, self.y, self.width, self.height, 20]
                width: 2
        
        # Header dengan navigasi bulan/tahun
        BoxLayout:
            size_hint_y: None
            height: 60
            spacing: 10
            
            Button:
                text: '<<'
                size_hint: None, None
                size: 50, 50
                font_size: 18
                background_color: 0.0039, 0.1922, 0.4471, 1
                color: 1, 1, 1, 1
                on_press: root.prev_year()
            
            Button:
                text: '<'
                size_hint: None, None
                size: 50, 50
                font_size: 24
                background_color: 0.0039, 0.1922, 0.4471, 1
                color: 1, 1, 1, 1
                on_press: root.prev_month()
            
            BoxLayout:
                orientation: 'horizontal'
                spacing: 5
                
                Spinner:
                    id: month_spinner
                    text: ''
                    values: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                    size_hint: None, None
                    size: 150, 50
                    font_size: 20
                    on_text: root.on_month_selected(self.text)
                
                Spinner:
                    id: year_spinner
                    text: ''
                    values: []
                    size_hint: None, None
                    size: 100, 50
                    font_size: 20
                    on_text: root.on_year_selected(self.text)
            
            Button:
                text: '>'
                size_hint: None, None
                size: 50, 50
                font_size: 24
                background_color: 0.0039, 0.1922, 0.4471, 1
                color: 1, 1, 1, 1
                on_press: root.next_month()
            
            Button:
                text: '>>'
                size_hint: None, None
                size: 50, 50
                font_size: 18
                background_color: 0.0039, 0.1922, 0.4471, 1
                color: 1, 1, 1, 1
                on_press: root.next_year()
        
        # Grid hari dalam minggu
        GridLayout:
            cols: 7
            size_hint_y: None
            height: 40
            spacing: 2
            
            Label:
                text: 'Mon'
                bold: True
                color: 0.0039, 0.1922, 0.4471, 1
            Label:
                text: 'Tue'
                bold: True
                color: 0.0039, 0.1922, 0.4471, 1
            Label:
                text: 'Wed'
                bold: True
                color: 0.0039, 0.1922, 0.4471, 1
            Label:
                text: 'Thu'
                bold: True
                color: 0.0039, 0.1922, 0.4471, 1
            Label:
                text: 'Fri'
                bold: True
                color: 0.0039, 0.1922, 0.4471, 1
            Label:
                text: 'Sat'
                bold: True
                color: 0.0039, 0.1922, 0.4471, 1
            Label:
                text: 'Sun'
                bold: True
                color: 1, 0, 0, 1
        
        # Grid tanggal
        GridLayout:
            id: calendar_grid
            cols: 7
            spacing: 2
        
        # Tombol Clear dan Close
        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10
            
            Button:
                text: 'Clear'
                background_color: 0.8, 0, 0, 0.8
                color: 1, 1, 1, 1
                on_press: root.do_clear_date()
            
            Button:
                text: 'Select'
                background_color: 0.0039, 0.1922, 0.4471, 1
                color: 1, 1, 1, 1
                on_press: root.do_select_date()
            
            Button:
                text: 'Close'
                background_color: 0.5, 0.5, 0.5, 0.8
                color: 1, 1, 1, 1
                on_press: root.dismiss()

# Widget khusus untuk DatePicker menggunakan TextInput readonly
<DatePickerInput@TextInput>:
    background_normal: ''
    background_active: ''
    background_color: 0, 0, 0, 0
    foreground_color: 0, 0, 0, 1  # WARNA HITAM untuk teks
    font_size: 22
    multiline: False
    readonly: True  # Readonly seperti button
    size_hint: None, None
    size: 590, 78
    padding: [30, (self.height - self.line_height) / 2]
    halign: 'left'
    write_tab: False
    hint_text: "Birth Date (DD-MM-YYYY)"
    hint_text_color: 0.5, 0.5, 0.5, 1
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

# Widget input lainnya
<BiodataTextInput@TextInput>:
    background_normal: ''
    background_active: ''
    background_color: 0, 0, 0, 0
    foreground_color: 0, 0, 0, 1  # WARNA HITAM
    font_size: 22
    multiline: False
    size_hint: None, None
    size: 590, 78
    padding: [30, (self.height - self.line_height) / 2]
    halign: 'left'  # Rata kiri
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
    foreground_color: 0, 0, 0, 1  # WARNA HITAM
    font_size: 22
    multiline: False
    size_hint: None, None
    size: 1275, 78
    padding: [30, (self.height - self.line_height) / 2]
    halign: 'left'  # Rata kiri
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

# Layout utama screen biodata
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
        
        # INPUT 3: Birth Date - MENGGUNAKAN TextInput READONLY
        DatePickerInput:
            id: birth_date_input
            hint_text: "Birth Date (DD-MM-YYYY)"
            pos_hint: {'center_x': 0.697, 'center_y': 0.448}
            text: root.birth_date
            on_focus: if self.focus: root.open_date_picker()
        
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


class DatePickerPopup(ModalView):
    """Popup untuk memilih tanggal"""
    current_year = NumericProperty(datetime.now().year)
    current_month = NumericProperty(datetime.now().month)
    selected_date = ObjectProperty(None)
    
    def __init__(self, callback, initial_date=None, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback  # Simpan callback untuk digunakan nanti
        self.temp_selected_date = initial_date  # Gunakan temporary storage untuk tanggal yang dipilih
    
        current_year = datetime.now().year
        start_year = 1980
        year_values = [str(y) for y in range(start_year, current_year + 11)]
        self.ids.year_spinner.values = year_values
        
        if initial_date:
            self.current_year = initial_date.year
            self.current_month = initial_date.month
            if self.current_year < start_year:
                self.current_year = start_year
            elif self.current_year > current_year + 10:
                self.current_year = current_year + 10
        
        self.update_spinners()
        self.update_calendar()
    
    def update_spinners(self):
        """Update spinner bulan dan tahun"""
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        self.ids.month_spinner.text = month_names[self.current_month - 1]
        self.ids.year_spinner.text = str(self.current_year)
    
    def update_calendar(self):
        """Update tampilan kalender"""
        # Hapus widget tanggal lama
        grid = self.ids.calendar_grid
        grid.clear_widgets()
        
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        first_day = calendar.monthrange(self.current_year, self.current_month)[0]
        first_day = first_day if first_day != 6 else -1
        
        # Tambahkan hari kosong di awal jika perlu
        for i in range(first_day):
            btn = Button(
                text='',
                background_color=(0.95, 0.95, 0.95, 1),
                color=(0.7, 0.7, 0.7, 1),
                disabled=True,
                size_hint=(None, None),
                size=(40, 40)
            )
            grid.add_widget(btn)
        
        # Tambahkan tanggal
        for week in cal:
            for day in week:
                if day == 0:
                    btn = Button(
                        text='',
                        background_color=(0.95, 0.95, 0.95, 1),
                        color=(0.7, 0.7, 0.7, 1),
                        disabled=True,
                        size_hint=(None, None),
                        size=(40, 40)
                    )
                    grid.add_widget(btn)
                else:
                    current_date = date(self.current_year, self.current_month, day)
                    
                    # Periksa apakah tanggal ini yang dipilih
                    is_selected = (self.temp_selected_date and 
                                 current_date == self.temp_selected_date)
                    
                    if is_selected:
                        btn = Button(
                            text=str(day),
                            background_color=(0.0039, 0.1922, 0.4471, 1),
                            color=(1, 1, 1, 1),
                            size_hint=(None, None),
                            size=(40, 40)
                        )
                    else:
                        btn = Button(
                            text=str(day),
                            background_color=(0.9, 0.9, 0.9, 1),
                            color=(0, 0, 0, 1),
                            size_hint=(None, None),
                            size=(40, 40)
                        )
                    
                    # Bind event click
                    btn.bind(on_press=lambda instance, d=current_date: self.select_date_temp(d))
                    grid.add_widget(btn)
    
    def select_date_temp(self, selected_date):
        """Pilih tanggal sementara (belum diterapkan)"""
        self.temp_selected_date = selected_date
        self.update_calendar()  # Refresh untuk menunjukkan pilihan baru
    
    def on_month_selected(self, month_name):
        """Tangani pemilihan bulan dari spinner"""
        month_names = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        if month_name in month_names:
            self.current_month = month_names.index(month_name) + 1
            self.update_calendar()
    
    def on_year_selected(self, year_str):
        """Tangani pemilihan tahun dari spinner"""
        try:
            self.current_year = int(year_str)
            self.update_calendar()
        except ValueError:
            pass
    
    def prev_month(self):
        """Pergi ke bulan sebelumnya"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        
        # Batasi tahun minimal 1980
        if self.current_year < 1980:
            self.current_year = 1980
        
        self.update_spinners()
        self.update_calendar()
    
    def next_month(self):
        """Pergi ke bulan berikutnya"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        
        self.update_spinners()
        self.update_calendar()
    
    def prev_year(self):
        """Pergi ke tahun sebelumnya"""
        self.current_year -= 1
        # Batasi tahun minimal 1980
        if self.current_year < 1980:
            self.current_year = 1980
        
        self.update_spinners()
        self.update_calendar()
    
    def next_year(self):
        """Pergi ke tahun berikutnya"""
        self.current_year += 1
        self.update_spinners()
        self.update_calendar()
    
    def do_clear_date(self):
        """Hapus tanggal yang dipilih"""
        self.temp_selected_date = None
        if self.callback:
            self.callback(None)  # Panggil callback dengan None
        self.dismiss()
    
    def do_select_date(self):
        """Pilih tanggal dari kalender"""
        if self.temp_selected_date and self.callback:
            self.callback(self.temp_selected_date)  # Panggil callback dengan tanggal
        self.dismiss()


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
        self.date_picker_popup = None
    
    def on_enter(self):
        """Dipanggil ketika screen ini aktif"""
        # Reset form saat screen aktif
        self.full_name = ""
        self.no_id = ""
        self.division = ""
        self.birth_date = ""
        self.email = ""
        self.biodata_status = ""
        
        # Set focus ke full name input
        self.ids.full_name_input.focus = True
    
    def open_date_picker(self):
        """Buka popup date picker"""
        self.ids.birth_date_input.focus = False
        
        # Parse tanggal awal jika ada
        initial_date = None
        if self.birth_date:
            try:
                # Parse format DD-MM-YYYY
                day, month, year = map(int, self.birth_date.split('-'))
                initial_date = date(year, month, day)
            except:
                pass
        
        # Buat callback function yang aman
        def on_date_selected(selected_date):
            if selected_date:
                formatted_date = selected_date.strftime("%d-%m-%Y")
                self.birth_date = formatted_date
            else:
                self.birth_date = ""

            self.date_picker_popup = None
        self.date_picker_popup = DatePickerPopup(
            callback=on_date_selected,
            initial_date=initial_date
        )
        self.date_picker_popup.open()
    
    def validate_date_format(self, date_str):
        """Validasi format tanggal DD-MM-YYYY"""
        if not date_str:
            return False
        
        try:
            parts = date_str.split('-')
            if len(parts) != 3:
                return False
            
            day, month, year = map(int, parts)

            if not (1 <= month <= 12):
                return False
                
            if month in [1, 3, 5, 7, 8, 10, 12]:
                max_day = 31
            elif month in [4, 6, 9, 11]:
                max_day = 30
            else:  
                # Periksa tahun kabisat
                if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                    max_day = 29
                else:
                    max_day = 28
            
            if not (1 <= day <= max_day):
                return False
            
            # Validasi tahun (1980 - tahun sekarang + 1)
            current_year = datetime.now().year
            if not (1980 <= year <= current_year + 1):
                return False
            
            # Buat objek date untuk validasi final
            date(year, month, day)
            return True
            
        except (ValueError, AttributeError):
            return False
    
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
        
        # Validasi format tanggal
        if not self.validate_date_format(self.birth_date):
            self.biodata_status = "Invalid date format! Use DD-MM-YYYY (1980-now)"
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
            # Pindah ke screen poto
            if self.manager:
                self.manager.current = 'poto'
        else:
            self.biodata_status = "Failed to save biodata!"

    def on_touch_down(self, touch):
        """Handle touch events untuk membuka date picker"""
        # Cek jika touch di dalam area birth_date_input
        birth_date_input = self.ids.birth_date_input
        if birth_date_input.collide_point(*touch.pos):
            self.open_date_picker()
            return True
        return super().on_touch_down(touch)
