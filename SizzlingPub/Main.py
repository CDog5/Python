from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
class MyLayout(Widget):
    name = ObjectProperty(None)
    email = ObjectProperty(None)
    def btn(self):
        name = self.name.text
        email = self.email.text
        print(f'Name: {name} Email: {email} Table No: {tableno}')
##class MyLayout(GridLayout):
##    def __init__(self,**kwargs):
##        super(MyLayout,self).__init__(**kwargs)
##        self.inside = GridLayout()
##        self.inside.cols = 2
##        self.cols = 1
##        self.inside.add_widget(Label(text="Name: "))
##        self.name = TextInput(multiline=False)
##        self.inside.add_widget(self.name)
##        self.inside.add_widget(Label(text="Email: "))
##        self.email = TextInput(multiline=False)
##        self.inside.add_widget(self.email)
##        self.inside.add_widget(Label(text="Table no: "))
##        self.tblno = TextInput(multiline=False)
##        self.inside.add_widget(self.tblno)
##        self.submit = Button(text="Submit")
##        self.submit.bind(on_press=self.pressed)
##        self.add_widget(self.inside)
##        self.add_widget(self.submit)
##    def pressed(self,instance):
##        name = self.name.text
##        email = self.email.text
##        tableno = self.tblno.text
##        print(f'Name: {name} Email: {email} Table No: {tableno}')
        
class SizzlingPubsApp(App):
    def build(self):
        return MyLayout()
SizzlingPubsApp().run()

