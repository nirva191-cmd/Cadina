from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform

CONFIG = {
    "line_phone_number": "+573001234567"
}

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        top_bar = BoxLayout(size_hint_y=None, height='50dp')
        top_bar.add_widget(Label(text='Mensajes', font_size=20))
        btn_settings = Button(text='Ajustes', size_hint_x=None, width='80dp')
        btn_settings.bind(on_press=self.go_to_settings)
        top_bar.add_widget(btn_settings)
        root.add_widget(top_bar)
        
        chat_layout = BoxLayout(orientation='vertical', spacing=10)
        chat_layout.add_widget(Label(text='Bandeja de mensajes interna', size_hint_y=None, height='30dp'))
        
        self.message_log = TextInput(
            text="[Sistema]: Usando línea propia configurada: " + CONFIG["line_phone_number"] + "\n",
            readonly=True,
            multiline=True
        )
        chat_layout.add_widget(self.message_log)
        
        send_box = BoxLayout(size_hint_y=None, height='50dp', spacing=5)
        self.recipient_input = TextInput(hint_text='Número destino', multiline=False, size_hint_x=0.4)
        self.msg_input = TextInput(hint_text='Mensaje...', multiline=False, size_hint_x=0.5)
        btn_send = Button(text='Enviar', size_hint_x=0.3)
        btn_send.bind(on_press=self.send_internal_sms)
        
        send_box.add_widget(self.recipient_input)
        send_box.add_widget(self.msg_input)
        send_box.add_widget(btn_send)
        chat_layout.add_widget(send_box)
        
        root.add_widget(chat_layout)
        
        bottom_bar = BoxLayout(size_hint_y=None, height='60dp')
        btn_call = Button(text='Abrir Dialer Interno')
        btn_call.bind(on_press=self.go_to_dialer)
        bottom_bar.add_widget(btn_call)
        root.add_widget(bottom_bar)
        
        self.add_widget(root)

    def on_enter(self):
        current_num = CONFIG["line_phone_number"]
        self.message_log.text += f"[Info]: Línea activa en ajustes -> {current_num}\n"

    def go_to_settings(self, instance):
        self.manager.current = 'settings'

    def go_to_dialer(self, instance):
        self.manager.current = 'dialer'

    def send_internal_sms(self, instance):
        recipient = self.recipient_input.text.strip()
        message = self.msg_input.text.strip()
        line_num = CONFIG["line_phone_number"]
        
        if not recipient or not message:
            return

        if platform == 'android':
            try:
                from jnius import autoclass
                # Corrección del acceso a Manifest y permisos para evitar excepciones en pyjnius
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                
                # Se utiliza el string directo del permiso en lugar de android.Manifest
                permission_sms = "android.permission.SEND_SMS"
                PackageManager = autoclass('android.content.pm.PackageManager')
                
                if activity.checkSelfPermission(permission_sms) != PackageManager.PERMISSION_GRANTED:
                    activity.requestPermissions([permission_sms], 1)
                    self.message_log.text += "[Permiso]: Solicitando SEND_SMS. Concede el permiso e intenta de nuevo.\n"
                    return

                SmsManager = autoclass('android.telephony.SmsManager')
                sms_manager = SmsManager.getDefault()
                sms_manager.sendTextMessage(recipient, None, f"[{line_num}]: {message}", None, None)
                self.message_log.text += f"[Enviado desde {line_num} a {recipient}]: {message}\n"
            except Exception as e:
                self.message_log.text += f"[Error SMS]: {e}\n"
        else:
            self.message_log.text += f"[Simulación Enviado] De {line_num} para {recipient}: {message}\n"
        
        self.msg_input.text = ""

class DialerScreen(Screen):
    def __init__(self, **kwargs):
        super(DialerScreen, self).__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.display = TextInput(text="", font_size=32, halign='center', multiline=False, size_hint_y=None, height='60dp')
        root.add_widget(self.display)
        
        buttons = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]
        
        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for char in row:
                btn = Button(text=char, font_size=24)
                btn.bind(on_press=self.on_button_press)
                h_layout.add_widget(btn)
            root.add_widget(h_layout)
            
        action_layout = BoxLayout(size_hint_y=None, height='60dp', spacing=10)
        btn_call_action = Button(text='Llamar Interno', background_color=(0, 1, 0, 1))
        btn_call_action.bind(on_press=self.execute_internal_call)
        
        btn_back = Button(text='Volver')
        btn_back.bind(on_press=self.go_back)
        
        action_layout.add_widget(btn_call_action)
        action_layout.add_widget(btn_back)
        root.add_widget(action_layout)
        
        self.add_widget(root)

    def on_button_press(self, instance):
        self.display.text += instance.text

    def execute_internal_call(self, instance):
        target_number = self.display.text.strip()
        line_num = CONFIG["line_phone_number"]
        if not target_number:
            return

        if platform == 'android':
            try:
                from jnius import autoclass
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                activity = PythonActivity.mActivity
                
                permission_call = "android.permission.CALL_PHONE"
                PackageManager = autoclass('android.content.pm.PackageManager')
                
                if activity.checkSelfPermission(permission_call) != PackageManager.PERMISSION_GRANTED:
                    activity.requestPermissions([permission_call], 2)
                    return

                intent = Intent(Intent.ACTION_CALL)
                intent.setData(Uri.parse(f"tel:{target_number}"))
                activity.startActivity(intent)
            except Exception as e:
                print(f"Error al ejecutar llamada directa: {e}")
        else:
            print(f"[Simulación Llamada]: Iniciando llamada desde la línea {line_num} hacia {target_number}")

    def go_back(self, instance):
        self.manager.current = 'main'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        root.add_widget(Label(text='Ajustes de Línea', font_size=22, size_hint_y=None, height='40dp'))
        root.add_widget(Label(text='Número de teléfono configurado para la línea:', size_hint_y=None, height='30dp'))
        
        self.phone_input = TextInput(text=CONFIG["line_phone_number"], multiline=False, size_hint_y=None, height='50dp')
        root.add_widget(self.phone_input)
        
        btn_save = Button(text='Guardar', size_hint_y=None, height='50dp', background_color=(0, 0.7, 1, 1))
        btn_save.bind(on_press=self.save_config)
        root.add_widget(btn_save)
        
        btn_back = Button(text='Volver', size_hint_y=None, height='50dp')
        btn_back.bind(on_press=self.go_back)
        root.add_widget(btn_back)
        
        root.add_widget(Label())
        self.add_widget(root)

    def on_enter(self, *args):
        self.phone_input.text = CONFIG["line_phone_number"]

    def save_config(self, instance):
        CONFIG["line_phone_number"] = self.phone_input.text.strip()
        self.manager.current = 'main'

    def go_back(self, instance):
        self.manager.current = 'main'

class MainMessageApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DialerScreen(name='dialer'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    MainMessageApp().run()
