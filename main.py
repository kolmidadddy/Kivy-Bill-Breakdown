import json
import os
import shutil
import smtplib
from helpers import username_helper
from email.message import EmailMessage

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image


from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton

Window.size = (335,595)

def create_box_layout():
    return BoxLayout(orientation='vertical')

def create_main_box():
    return BoxLayout(orientation='vertical', padding=10, spacing=5)

class SplashScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        float_layout = FloatLayout()
        gif_image = Image(source='assets\spin.gif', allow_stretch=True)
        float_layout.add_widget(gif_image)
        self.add_widget(float_layout)
        Clock.schedule_once(self.goto_main_screen, 20) # 10 seconds delay
        
    def goto_main_screen(self,*args):
        self.manager.current ='Login'
        
class LoginScreen(Screen):
    def __init__(self,**kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # using a BoxLayout to arrange the toolbar vertically
        box = create_box_layout()

        # Adding a title label
        toolbar = MDTopAppBar(title='Welcome to Bill Breakdown Application',elevation=6)
        # title_label = MDLabel(text="Bill Breakdown App :')"+"\n"+
        #                       "_______________________________", 
        #                     theme_text_color="Secondary",
        #                     pos_hint={'center_x': 0.5, 'center_y': 0.65}, halign="center",
        #                     font_style="H4")
        button = MDRectangleFlatButton(text ="Enter", pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                       on_release=self.show_data)
        
        # Add an icon to the right side of the toolbar
        toolbar.right_action_items = [["information", lambda x: self.popup_message()]]

        # scroll view abd list view before
        scroll = ScrollView()

        # add toolbar as widget 
        box.add_widget(toolbar)
        box.add_widget(scroll)

        # add the box layout to the screen
        self.add_widget(box)
        self.username = Builder.load_string(username_helper)

        # self.add_widget(title_label)  # Adding the title label to the screen
        self.add_widget(self.username)
        self.add_widget(button)

    def show_data(self,obj):
        if self.username.text is "":
            check_string = "Please enter a username!"
        else:
            check_string = self.username.text 
        

        close_btn = MDFlatButton(text='Close',on_release=self.close_dialog)
        self.done_btn = MDFlatButton(text='Done', on_release= self.donebutton)
        self.dialog = MDDialog(title= 'Hello Dear', text = check_string,
                      size_hint=(0.5,1),
                      buttons =[close_btn,self.done_btn])
        self.dialog.open()

    def popup_message(self):
        # create the close button for the dialog
        close_button = MDFlatButton(text='Close', on_release=self.close_dialog)

        # create the dialog
        self.dialog = MDDialog(title='Information', text='Navigate social dining with ease using our Bill Break-down App! Designed for students, this app offers flexible options for splitting bills equally or by custom ratios and percentages. Store results for future reference or share instantly with friends. Simplify shared expenses, one meal at a time.',
                                                        
                               size_hint=(0.8, 0.3),
                               buttons=[close_button])

        # open the dialog
        self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def donebutton(self,obj):
        self.dialog.dismiss()
        self.manager.current = 'Dashboard'

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)

        # using a BoxLayout to arrange the toolbar and the scroll view vertically
        box = create_box_layout()

        # create the toolbar and the back button
        toolbar = MDTopAppBar(title='Dashboard',elevation=10)
        back_button = MDIconButton(icon="arrow-left",
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                   on_release=self.back_to_login)
        toolbar.left_action_items = [["arrow-left", lambda x: self.back_to_login()]]

        box.add_widget(toolbar)

        # scroll view abd list view before
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)

        icon1 = IconLeftWidget(icon= "calculator")
        icon2 = IconLeftWidget(icon= "eye")
        icon3 = IconLeftWidget(icon= "share")

        item1 = OneLineIconListItem(text='Bill Breakdown Calculator')
        item2 = OneLineIconListItem(text='View Previous Results')
        item3 = OneLineIconListItem(text='Share Results')

        item1.add_widget(icon1)
        item2.add_widget(icon2)
        item3.add_widget(icon3)
        
        # binding 
        item1.bind(on_release=self.goto_bill_breakdown)
        item2.bind(on_release=self.goto_view_results)
        item3.bind(on_release=self.goto_share_results)  
        list_view.add_widget(item1)
        list_view.add_widget(item2)
        list_view.add_widget(item3)

        # add the scroll view to the box layout
        box.add_widget(scroll)

        # add the box layout to the screen
        self.add_widget(box)
    
    def goto_bill_breakdown(self, instance):
        self.manager.current = 'BillBreakdown'
        
    def goto_share_results(self, instance):
        self.manager.current = 'ShareResults'
        
    def goto_view_results(self, instance):
        self.manager.current = 'ViewPreviousResults'
    
    def back_to_login(self):
        self.manager.current ='Login'

class BillBreakdownScreen(Screen):
    def __init__(self, **kwargs):
        super(BillBreakdownScreen, self).__init__(**kwargs)
        # Main vertical layout
        main_box = create_main_box()

        # create the toolbar and the back button to dashboard
        toolbar = MDTopAppBar(title='Bill Breakdown Calculator', elevation=10)
        back_button = MDIconButton(icon="arrow-left",
                                   pos_hint={'center_x': 0.2, 'center_y': 0.5},
                                   on_release=self.back_to_dashboard)
        toolbar.left_action_items = [["arrow-left", lambda x: self.back_to_dashboard()]]
        main_box.add_widget(toolbar)
        
        # scroll view and list view before
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)

        # add the scroll view to the box layout
        main_box.add_widget(scroll)

        self.add_widget(main_box)

        # Total bill widgets
        total_bill_label = MDLabel(text='Enter Total Bill (RM):')
        self.total_bill_input = TextInput(input_filter='float')
        main_box.add_widget(total_bill_label)
        main_box.add_widget(self.total_bill_input)

        # Number of people widgets
        people_label = MDLabel(text='Enter Number of People:')
        self.people_input = TextInput(input_filter='int')
        main_box.add_widget(people_label)
        main_box.add_widget(self.people_input)

        # Add calculate button
        self.calculate_button = MDRectangleFlatButton(text='Calculate', size_hint=(1, 0.15))
        self.calculate_button.bind(on_press=self.break_down)
        main_box.add_widget(self.calculate_button)

        # Choose break-down type
        self.spinner = Spinner(text='Equal break-down', 
                               values=('Equal break-down', 
                                       'Custom break-down by ratio'),
                                size_hint_y=0.6)
        self.spinner.bind(text=self.on_spinner_select)  # Bind the event handler
        main_box.add_widget(self.spinner)

        # Custom grid layout for inputs
        self.custom_grid = GridLayout(cols=2, spacing=5)
        main_box.add_widget(self.custom_grid)
        
        bottom_app_bar = FloatLayout(size_hint_y=0.15)
        
        # create the FAB and bind the action to save results()
        fab_button = MDFloatingActionButton(
            icon="content-save",
            pos_hint={"center_x": 0.8, "center_y": 0.5},
            on_release=self.save_results
        )
        # Attach the FAB to the bottom bar
        bottom_app_bar.add_widget(fab_button)

        # Add the bottom app bar to the main layout
        main_box.add_widget(bottom_app_bar)

        # Result field
        resultlabel = MDLabel(text='Results: ',text_color =(0.40, 0.01, 0.24, 1), size_hint=(1,0.2))
        self.result_label = MDTextField(text='', size_hint=(1, 0.2), readonly=True)
        main_box.add_widget(resultlabel)
        main_box.add_widget(self.result_label)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def break_down(self, instance):
        total_bill = float(self.total_bill_input.text)
        num_people = int(self.people_input.text)
        if self.spinner.text == 'Equal break-down':
        # Custom breakdown logic by equality
            self.result_label.text = f'Each person pays: RM{total_bill / num_people:.2f}'
            
        elif self.spinner.text == 'Custom break-down by ratio':
            # Extract the ratio values from the TextInput widgets in the custom grid
            ratio_values = [int(text_input.text) for text_input in self.custom_grid.children if isinstance(text_input, TextInput)][::-1]

            # Calculate the total ratio value
            total_ratio = sum(ratio_values)

            # Calculate the amounts for each person based on the ratios
            amounts = [total_bill * r / total_ratio for r in ratio_values]

            # Create the result text
            result_text = ', '.join([f'Ratio {i+1}: RM{amount:.2f}' for i, amount in enumerate(amounts)])
            self.result_label.text = result_text
    
    def save_results(self, instance):
        self.username = Builder.load_string(username_helper)
        if not self.result_label.text:
            return

        data = {
            'total_bill': self.total_bill_input.text,
            'number_of_people': self.people_input.text,
            'breakdown_type': self.spinner.text,
            'result': self.result_label.text
        }

        try:
            with open('results.json', 'r') as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        results.append(data)

        with open('results.json', 'w') as file:
            json.dump(results, file)
            
        # Optional: Provide feedback to the user that the save was successful
        toast("Results saved successfully!")

    def query_results(self, instance):
        results = []
        try:
            with open('results.json', 'r') as file:
                for line in file:
                    results.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass

        self.box.clear_widgets()
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        box = BoxLayout(orientation='vertical', size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        for result in results:
            label = MDLabel(text=f"Total: {result['total_bill']}, People: {result['number_of_people']}, Type: {result['breakdown_type']}, Result: {result['result']}")
            box.add_widget(label)

        self.scroll_view.add_widget(box)
        self.box.add_widget(self.scroll_view)

    def on_spinner_select(self, instance, value):
        self.custom_grid.clear_widgets()  # Clear existing widgets
        if value == 'Custom break-down by ratio':
            # Number of ratios you want to allow
            num_ratios = 3
            for i in range(num_ratios):
                ratio_label = MDLabel(text=f'Enter Ratio {i+1}:')
                ratio_input = TextInput(input_filter='int')
                self.custom_grid.add_widget(ratio_label)
                self.custom_grid.add_widget(ratio_input)

            # Update the grid layout to have two columns
            self.custom_grid.cols = 2

    def back_to_dashboard(self):
        self.manager.current ='Dashboard'

class ViewPreviousResults(Screen):
    def __init__(self, **kwargs):
        super(ViewPreviousResults, self).__init__(**kwargs)
        # using a BoxLayout to arrange the toolbar and the scroll view vertically
        box = create_box_layout()
        
        # create the toolbar and the back button to dashboard
        toolbar = MDTopAppBar(title='View Previous Results', elevation=10)
        back_button = MDIconButton(icon="arrow-left",
                                   pos_hint={'center_x': 0.2, 'center_y': 0.5},
                                   on_release=self.back_to_dashboard)
        toolbar.left_action_items = [["arrow-left", lambda x: self.back_to_dashboard()]]
        box.add_widget(toolbar)
        
        # Read results from JSON file
        try:
            with open('results.json', 'r') as file:
                results = json.load(file)
        except FileNotFoundError:
            return
        
        # Extract data in the format needed by MDDataTable
        rows = [(
            result['total_bill'],
            result['number_of_people'],
            result['breakdown_type'],
            result['result']
        ) for result in results]
        
        # Create the data table
        table = MDDataTable(
            size_hint=(0.9, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            rows_num=len(rows),
            column_data=[
                ("Total", dp(30)),
                ("No. of People", dp(30)),
                ("Type", dp(30)),
                ("Result", dp(40))
            ],
            row_data=rows
        )
        box.add_widget(table)
        self.add_widget(box)
         
    def back_to_dashboard(self):
        self.manager.current = 'Dashboard'

class ShareResults(Screen):
    def __init__(self, **kwargs):
        super(ShareResults, self).__init__(**kwargs)
        box = create_box_layout()
        
        toolbar = MDTopAppBar(title='Share Your Results To...', elevation=20)
        back_button = MDIconButton(icon="arrow-left",
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                   on_release=self.back_to_dashboard)
        toolbar.left_action_items = [["arrow-left", lambda x: self.back_to_dashboard()]]
        
        box.add_widget(toolbar)
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)
        
        # Generate report and add to the scroll view
        report_path = self.generate_report()
        if report_path:
            with open(report_path, 'r') as file:
                for line in file:
                    list_view.add_widget(OneLineListItem(text=line.strip()))
                # Create a button to trigger report generation and sharing
                
        share_button = OneLineListItem(text="Share Report")
        share_button.bind(on_release=lambda x: self.share_report())
        list_view.add_widget(share_button)
        
        # add the scroll view to the box layout
        box.add_widget(scroll)
        # add the box layout to the screen
        self.add_widget(box)
        
    def generate_report(self):
        # Read results from JSON file
        try:
            with open('results.json', 'r') as file:
                results = json.load(file)
        except FileNotFoundError:
            print("File not found!")
            return

        # Create a report in text format
        report_text = "Total, No. of People, Type, Result\n"  # Header
        for result in results:
            line = f"{result['total_bill']}, {result['number_of_people']}, {result['breakdown_type']}, {result['result']}\n"
            report_text += line

        # Save the report as a file
        report_path = 'report.txt'
        with open(report_path, 'w') as file:
            file.write(report_text)

        return report_path
    
    def share_report(self):
        report_path = self.generate_report()
        if not report_path:
            print("Failed to generate report!")
            return
        
        self.report_path = report_path
        share_options = ShareOptions(self)
        dialog = MDDialog(content_cls=share_options, title="Choose an option to share the report:")
        share_options.dialog = dialog
        dialog.open()
        
    def send_via_email(self, report_path):
        msg = EmailMessage()
        msg['Subject'] = 'Your Report'
        msg['From'] = 'your_email@example.com'
        msg['To'] = 'recipient@example.com'
        msg.set_content('Here is the report you requested.')

        with open(report_path, 'rb') as file:
            file_data = file.read()
            file_name = report_path.split('/')[-1]

        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        with smtplib.SMTP_SSL('smtp.example.com', 465) as smtp:
            smtp.login('your_email@example.com', 'your_password')
            smtp.send_message(msg)

        print('Email sent successfully!')
        
    def save_to_directory(self, report_path):
        filechooser = FileChooserIconView(path='/', filters=['*.txt'])
        target_path = filechooser.selection[0]  # Get the selected path

        try:
            shutil.copy(report_path, target_path)
            print(f'Report saved to {target_path} successfully!')
        except Exception as e:
            print(f'Failed to save report: {str(e)}')
            
    def back_to_dashboard(self):
        self.manager.current ='Dashboard'

class ShareOptions(BoxLayout):
    def __init__(self, parent_screen, **kwargs):
        super(ShareOptions, self).__init__(**kwargs)
        self.parent_screen = parent_screen
        self.orientation = 'vertical'
        self.add_widget(MDRaisedButton(text="Open in Default Application", on_release=self.open_default))
        self.add_widget(MDRaisedButton(text="Send via Email", on_release=self.send_email))
        self.add_widget(MDRaisedButton(text="Save to Specific Directory", on_release=self.save_directory))

    def open_default(self, instance):
        self.parent_screen.open_default()
        self.dialog.dismiss()

    def send_email(self, instance):
        self.parent_screen.send_via_email(self.parent_screen.report_path)
        self.dialog.dismiss()

    def save_directory(self, instance):
        self.parent_screen.save_to_directory(self.parent_screen.report_path)
        self.dialog.dismiss()

class BreakdownApp(MDApp):
    def build(self):
        Builder.load_file('splashScreen.kv')
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"
        
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='SplashScreen'))
        sm.add_widget(LoginScreen(name='Login'))
        sm.add_widget(DashboardScreen(name='Dashboard'))
        sm.add_widget(BillBreakdownScreen(name='BillBreakdown'))
        sm.add_widget(ShareResults(name='ShareResults'))
        sm.add_widget(ViewPreviousResults(name='ViewPreviousResults'))
        
        # start with the splash screen
        sm.current = 'SplashScreen'
        return sm    


if __name__ == '__main__':
    BreakdownApp().run()