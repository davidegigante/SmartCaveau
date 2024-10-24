from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivy.clock import Clock
import paho.mqtt.client as mqtt
import ujson
import json
import time
from kivy.core.window import Window
import re
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDFlatButton

KV = """
MDScreen:
    MDBottomNavigation:
        selected_color_background: "orange"
        text_color_active: "lightgrey"
        
        MDBottomNavigationItem:
            id: bottom_navigation
            name: 'screen_1'
            text: 'Unlock'
            icon: 'lock'
            
            MDScreen:
                
                MDGridLayout:
                    cols: 3
                    rows: 1
                    spacing: "50dp"
                    size_hint: (0.99, 0.12)

                    MDSwitch:
                        id: toggle_infrared
                        active: False
                        on_active: app.toggle()

                    MDLabel:
                        text: "Alarm"
                        color: "orange"

                    MDIconButton:
                        on_release: app.blocca()
                        padding: "10dp"
                        icon: "lock"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "orange"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "56dp", "56dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

            BoxLayout:
                orientation: 'vertical'
                spacing: "30dp"
                padding: "20dp"

                BoxLayout:
                    size_hint_y: None
                    height: "58dp"
                    pos_hint: {"center_x": 0.5}
                    canvas:
                        Color:
                            rgba: 1, 1, 1, 0.2
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                            radius: [20,]

                    MDTextField:
                        id: text_field
                        hint_text: "  PIN"
                        height: "48dp"
                        multiline: False
                        readonly: True
                        pos_hint: {"center_x": 0.5}
                        cursor_color: 0, 0, 0, 1
                        color_active: 1, 1, 1, 1
                        line_color_focus: 1, 1, 1, 1
                        line_color_normal: 1, 1, 1, 0.5
                        line_anim: True
                        halign: "center"  # Centra il testo orizzontalmente
                        text_size: self.size  # Imposta la dimensione del testo uguale alla dimensione del campo di testo

                MDGridLayout:
                    id: grid_layout
                    cols: 3
                    spacing: "60dp"
                    size_hint: (0.83, 0.8)
                    pos_hint: {"center_x": 0.5}

                    MDIconButton:
                        on_release: app.update_text_number("1")
                        icon: "numeric-1"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("2")
                        icon: "numeric-2"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("3")
                        icon: "numeric-3"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("4")
                        icon: "numeric-4"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("5")
                        icon: "numeric-5"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("6")
                        icon: "numeric-6"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("7")
                        icon: "numeric-7"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("8")
                        icon: "numeric-8"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("9")
                        icon: "numeric-9"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_delete()
                        icon: "keyboard-backspace"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "red"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_number("0")
                        icon: "numeric-0"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "grey"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale

                    MDIconButton:
                        on_release: app.update_text_confirm()
                        icon: "check-bold"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1  # Colore del testo (bianco)
                        md_bg_color: "green"  # Sfondo arancione (RGBA)
                        user_font_size: "48sp"  # Dimensione del testo
                        size_hint: None, None  # Disabilita la ridimensionabilità in base al contenuto
                        size: "70dp", "70dp"  # Dimensione fissa per rendere il bottone circolare
                        elevation_normal: 12  # Aggiungi un'ombra leggera per un effetto tridimensionale


        MDBottomNavigationItem:
            name: 'screen_2'
            text: 'Change Password'
            icon: 'key-change'

            BoxLayout:
                orientation: 'vertical'
                spacing: "25dp"
                padding: "20dp"
                pos_hint: {"center_x": 0.5, "center_y": 0.5}  # Centra il layout nella schermata
                size_hint: (0.8, 0.5)

                Label:
                    text: 'Insert new numeric password'
                    color: "white"

                MDTextField:
                    id: old_password_field
                    hint_text: 'Old Password'
                    password: True
                    size_hint_x: None
                    width: "200dp"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}


                MDTextField:
                    id: new_password_field
                    hint_text: 'New Password'
                    password: True
                    size_hint_x: None
                    width: "200dp"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}

                Label:
                    id: label_password 
                    text: " "
                    color: "orange"
                    align: "center"
                
                MDRaisedButton:
                    text: 'Confirm'
                    on_release: app.change_password()
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    md_bg_color: "orange"

        MDBottomNavigationItem:
            name: 'screen_3'
            text: 'Notification'
            icon: 'message'
            id: screen_3
            badge_icon: ""
            on_tab_press: app.switch_screen(self.name)

            ScrollView:
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    id: notification_list

"""

class App(MDApp):
    psw = "0000"
    error_counter = 0
    flagerror = False
    errorStr = ""
    notification_counter = 0
    wait = 10
    last_click = 0
    MAX_ATTEMPTS = 5
    notifications = []

    def check_password(self, file_path: str) -> tuple:
        try:
            with open(file_path, 'x') as file:
                file.write(f'password: 0000\n')
                print(f"Il file '{file_path}' è stato creato con successo.")
                return (False, '0000')
        except FileExistsError:
            with open(file_path, 'r') as file:
                stored_password = file.readline().strip().split(': ')[1]
                print(f"La password presente nel file '{file_path}' è: {stored_password}")
                return (True, stored_password)
    
    def build(self):
        Window.size = (360, 650)
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.psw = self.check_password("password.txt")[1]
        return Builder.load_string(KV)

    def update_text_number(self, text):
        text_field = self.root.ids.text_field
        if not self.contains_only_numbers(text_field.text):
            text_field.text = ""
        if self.flagerror and self.error_counter < self.MAX_ATTEMPTS:
            text_field.text = text
            self.flagerror = False
        elif self.error_counter < self.MAX_ATTEMPTS :
            text_field.text += text
            self.flagerror = False

        current_click = time.time() 
        offset = current_click - self.last_click 
        if self.error_counter >= self.MAX_ATTEMPTS and offset >= self.wait: 
            self.flagerror = False 
            text_field.text = text 
            self.error_counter = 0

    def update_text_delete(self):
        text_field = self.root.ids.text_field
        current_text = text_field.text
        if (current_text == "CAVEAU OPENED"):
            current_text = ""
        if self.contains_only_numbers(current_text):
            text_field.text = current_text[:-1]

    def update_text_confirm(self):
        text_field = self.root.ids.text_field
        current_text = text_field.text
        msg = 0
        global client
        global topic
        global client_id
        global infrared_alarm

        if self.error_counter < self.MAX_ATTEMPTS:
            if not self.contains_only_numbers(current_text):
                print("Codice non inserito")
                text_field.text = "PLEASE INSERT CODE!"
            else:
                if current_text == self.psw:
                    print("corretto")
                    if infrared_alarm:
                        text_field.text = "ALARM STOPPED"
                        infrared_alarm = False
                    else:
                        text_field.text = "CAVEAU OPENED"
                        self.root.ids.toggle_infrared.active = False
                        msg = ujson.dumps({
                            'client_id': client_id,
                            'op_code' : 2, 
                            'alarm_set': False
                        })
                        client.publish(topic, msg)
                    Clock.schedule_once(lambda dt: self.clear_text_field(), 10)
                    self.error_counter = 0  # Reimposta il contatore degli errori a 0 dopo un inserimento corretto
                    msg = ujson.dumps({
                        'client_id': client_id,
                        'op_code' : 1,
                        'open_caveau': True, 
                        'attempt_number': self.error_counter
                    })
                    self.flagerror = False
                else:
                    print("sbagliato")
                    self.errorStr = str(self.MAX_ATTEMPTS -1 - self.error_counter) + " ATTEMPTS LEFT"
                    self.flagerror = True
                    self.error_counter += 1  # Incrementa il contatore degli errori
                    msg = ujson.dumps({
                        'client_id': client_id,
                        'op_code' : 1,
                        'open_caveau': False, 
                        'attempt_number': self.error_counter
                    })
                    if self.error_counter >= self.MAX_ATTEMPTS:
                        self.errorStr = f"CAVEAU BLOCKED! WAIT FOR {self.wait} SEC"
                        text_field.text = self.errorStr
                        self.last_click = time.time()
                        Clock.schedule_once(lambda dt: self.clear_text_field(), self.wait)
                        # Aggiungi qui le azioni da intraprendere quando si raggiunge il limite di errori
                        msg = ujson.dumps({
                            'client_id': client_id,
                            'op_code' : 1,
                            'open_caveau': False, 
                            'attempt_number': self.MAX_ATTEMPTS
                        })
                    else:
                        text_field.text = self.errorStr
                        
                client.publish(topic, msg)

    def contains_only_numbers(self, string):
        string = string.strip()  # Rimuove gli spazi iniziali e finali
        return re.match(r'^\d+$', string) is not None

    def save_password(self, file_path, new_pass: str):
        with open(file_path, 'w') as file:
            file.write(f'password: {new_pass}')
    
    def clear_label(self):
        lbl = self.root.ids.label_password
        lbl.text = ""
    
    def change_password(self):
        old_password = self.root.ids.old_password_field.text
        new_password = self.root.ids.new_password_field.text
        lbl_password = self.root.ids.label_password

        if old_password.strip() == "" or new_password.strip() == "":
            lbl_password.text = "Compile both fields!"
        elif not self.contains_only_numbers(new_password):
            lbl_password.text = "Please use numbers only!"
        elif new_password == self.psw:
            lbl_password.text = "Cannot use the same password as new one!"
        elif old_password == self.psw:
            lbl_password.text = "Password changed successfully!"
            self.psw = new_password
            self.save_password("password.txt", new_password)
        else:
            lbl_password.text = "Old password wrong! Try again."
            
        self.root.ids.old_password_field.text = ""
        self.root.ids.new_password_field.text = ""
        Clock.schedule_once(lambda dt: self.clear_label(), 10)
    
    def blocca (self):
        global client
        global topic
        global client_id
        msg = ujson.dumps({
            'client_id': client_id,
            'op_code' : 1,
            'open_caveau': False,
            'attempt_number': 0
        })
        client.publish(topic, msg)
        print("Bloccato")

    def clear_text_field(self):
        text_field = self.root.ids.text_field
        text_field.text = ""
    
    def switch_screen(self, screen_name):
        if screen_name == 'screen_3':
            # Aggiungi gli item di notifica
            for notification in self.notifications[::-1]:
                notification_text = 'Attempted Burglary'
                notification_time = notification[4:]  # Orario della notifica
                item = OneLineListItem(text=f'{notification_time} - {notification_text}')
                self.root.ids.notification_list.add_widget(item)
            
            self.notifications = []

            # Rimuovi il badge
            self.notification_counter = 0
            self.root.ids.screen_3.badge_icon = ""

        else:
            # Aggiungi il badge solo se ci sono notifiche non lette
            if self.notification_counter > 0:
                strBadge= "numeric-" + str(self.notification_counter)
                self.root.ids.screen_3.badge_icon = strBadge
    
    def increment_notification_counter(self):
        self.notification_counter += 1
        strBadge= "numeric-" + str(self.notification_counter)
        self.root.ids.screen_3.badge_icon = strBadge

        
    def toggle(self):
        global client
        global topic
        global client_id
        
        if self.root.ids.toggle_infrared.active :
            msg = ujson.dumps({
            'client_id': client_id,
            'op_code' : 2,
            'alarm_set': True
            })
            print("Alarm Active")
        else:
            msg = ujson.dumps({
            'client_id': client_id,
            'op_code' : 2, 
            'alarm_set': False
        })
            print("Alarm Disabled")
        
        client.publish(topic, msg)

def on_connect(client, userdata, flags, rc):
    global loop_flag
    global topic
    client.subscribe(topic, 1)
    print("Connected with result code "+str(rc))
    print("\n connected with client "+ str(client))
    print("\n connected with userdata "+str(userdata))
    print("\n connected with flags "+str(flags))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    
def on_log(client, userdata, level, buf):
    print("\n log:client = "+ str(client))
    print("\n log:level ="+str(level))
    print("\n log:buffer "+str(buf))

def on_subscribe(client, userdata, msg, qos_l):
    print("\non_sub: client ="+str(client))
    print("\non_sub: msg ="+str(msg))
    print("\non_sub: qos level ="+str(qos_l))

def on_unsubscribe(client, userdata, mid):
    print("\sub: client ="+str(client))

def on_message(client, userdata, msg):
    global client_id
    global infrared_alarm
    
    msg_payload = msg.payload.decode('utf-8')
    msg = ujson.loads(msg_payload)
    
    if msg['client_id'] != client_id:
        print("\n on message: "+ str(msg))
        infrared_alarm = True
        app = App.get_running_app()
        app.increment_notification_counter()
        app.notifications.append(time.ctime(time.time()))
        Clock.schedule_once(lambda dt: setattr(app.root.ids.text_field, 'text', "INSERT CODE TO STOP ALARM"))

def on_publish(client,userdata,result): #create function for callback
    print("\non_publish data published \n")
    print("\non_pub: result = ", result)

topic = "SHIELDGuardian/test"
client_id = 'dashboard1'
infrared_alarm = False
try:
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect("test.mosquitto.org", 1883, 60)
    client.on_publish = on_publish
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.on_disconnect = on_disconnect
    client.on_log = on_log
    client.loop_start()
    App().run()
except Exception as e:
    print('exception: ', e)
finally:
    client.disconnect()
    client.loop_stop()



