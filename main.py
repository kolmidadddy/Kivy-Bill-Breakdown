import json
from plyer import email
from helpers import username_helper

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.core.window import Window

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.theming import ThemableBehavior
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem
from kivymd.uix.navigationdrawer import MDNavigationDrawer, MDNavigationLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton


Window.size = (500,800)

def create_box_layout():
    return BoxLayout(orientation='vertical')

def create_main_box():
    return BoxLayout(orientation='vertical', padding=10, spacing=5)

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
        self.dialog = MDDialog(title='Information', text='This is a popup message!',
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

        # # navigator button
        # nav_button= MDIconButton(icon="dots-vertical",
        #                           pos_hint={'center_x': 0.5, 'center_y': 0.5},
        #                           on_release=self.show_navigator)
        # toolbar.right_action_items = [["dots-vertical", lambda x: self.drop_down_menu()]]
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
        
        list_view.add_widget(item2)
        list_view.add_widget(item3)

        # binding 
        item1.bind(on_release=self.goto_bill_breakdown) 
        list_view.add_widget(item1)

        # add the scroll view to the box layout
        box.add_widget(scroll)

        # add the box layout to the screen
        self.add_widget(box)
    
    def goto_bill_breakdown(self,instance):
        self.manager.current = 'BillBreakdown'
    
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
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5},
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
                                       'Custom break-down by percentage/ratio', 
                                       'Custom break-down by amount'),
                                size_hint_y=0.6)
        main_box.add_widget(self.spinner)

        # Custom grid layout for inputs
        self.custom_grid = GridLayout(cols=2, spacing=5)
        main_box.add_widget(self.custom_grid)

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

        elif self.spinner.text == 'Custom break-down by percentage/ratio':
            percentages = [float(text_input.text) for text_input in self.custom_grid.children[::-2]] # Extract inputs
            if sum(percentages) != 100:
                self.result_label.text = 'Percentages do not add up to 100%'
                return
            amounts = [total_bill * p / 100 for p in percentages]
            result_text = ', '.join([f'RM{amount:.2f}' for amount in amounts])
            self.result_label.text = 'Amounts: ' + result_text

        elif self.spinner.text == 'Custom break-down by amount':
            amounts = [float(text_input.text) for text_input in self.custom_grid.children[::-2]] # Extract inputs
            if sum(amounts) != total_bill:
                self.result_label.text = f'Discrepancy detected: Sum of individual amounts (RM{sum(amounts):.2f}) does not match total bill (RM{total_bill:.2f})'
                return
            result_text = ', '.join([f'RM{amount:.2f}' for amount in amounts])
            self.result_label.text = 'Amounts: ' + result_text

        else:
            custom_value = float(self.custom_input.text)
            # Able to customize the following logic as per your requirements
            amount = total_bill * custom_value / 100
            self.result_label.text = f'First person pays: RM{amount:.2f}, Second person pays: RM{total_bill - amount:.2f}'

    def save_results(self, instance):
        if not self.result_label.text:
            return

        data = {
            'total_bill': self.total_bill_input.text,
            'number_of_people': self.people_input.text,
            'breakdown_type': self.spinner.text,
            'result': self.result_label.text
        }

        with open('results.json', 'a') as file:
            json.dump(data, file)
            file.write('\n')

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
            label = MDLabel(text=f"Total Bill: {result['total_bill']}, People: {result['number_of_people']}, Type: {result['breakdown_type']}, Result: {result['result']}")
            box.add_widget(label)

        self.scroll_view.add_widget(box)
        self.box.add_widget(self.scroll_view)

    
    def on_spinner_select(self, instance, value):
        if value == 'Custom break-down':
            self.custom_input.disabled = False
        else:
            self.custom_input.disabled = True

    # def share_results(self, instance):
    #     main_box = BoxLayout(orientation='vertical', padding=10, spacing=5)
    #     if not self.result_label.text:
    #         # Don't attempt to share if there's no result
    #         return

    #     subject = "Bill Breakdown"
    #     body = f"Here's the breakdown of the bill:\n\n{self.result_label.text}"
        
    #     # Open the email client with pre-filled subject and body
    #     email.send(subject=subject, text=body)

    def back_to_dashboard(self):
        self.manager.current ='Dashboard'

class BreakdownApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Dark"

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='Login'))
        sm.add_widget(DashboardScreen(name='Dashboard'))
        sm.add_widget(BillBreakdownScreen(name='BillBreakdown'))
        return sm    

if __name__ == '__main__':
    BreakdownApp().run()




# import json
# from plyer import email


# from kivy.app import App
# from kivy.core.window import Window
# from kivy.graphics import Rectangle, Color
# from kivy.uix.label import Label
# from kivy.uix.widget import Widget
# from kivy.uix.button import Button
# from kivy.uix.spinner import Spinner
# from kivy.uix.dropdown import DropDown
# from kivy.uix.textinput import TextInput
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.scrollview import ScrollView

# class BreakdownApp(App):
#     def build(self):
#         # Main vertical layout
#         main_box = BoxLayout(orientation='vertical', padding=10, spacing=5)

#         # self.box = BoxLayout(orientation='vertical', padding=10, spacing=5)

#         # # Horizontal layout for side-by-side boxes
#         # side_by_side_box = BoxLayout(orientation='horizontal', spacing=10)

#         # Header with custom color
#         header = BoxLayout(size_hint=(1, 0.1), orientation='horizontal')
#         with header.canvas.before:
#             Color(0.2, 0.5, 0.8, 1)  # Set the color (Red, Green, Blue, Alpha)
#             self.rect = Rectangle(pos=header.pos, size=header.size)
#         header.bind(pos=self.update_rect, size=self.update_rect)

#         # Dropdown menu
#         self.dropdown = DropDown()
#         self.save_button = Button(text='Save Results', size_hint_y=None, height=44)
#         self.save_button.bind(on_press=self.save_results)
#         self.dropdown.add_widget(self.save_button)

#         self.query_button = Button(text='View Previous Results', size_hint_y=None, height=44)
#         self.query_button.bind(on_press=self.query_results)
#         self.dropdown.add_widget(self.query_button)

#         self.share_button = Button(text='Share Results', size_hint_y=None, height=44)
#         self.share_button.bind(on_press=self.share_results)  # You can define this function to share the results
#         self.dropdown.add_widget(self.share_button)

#         # Trigger button to open dropdown
#         self.main_button = Button(text='Options', size_hint=(0.2, 1))
#         self.main_button.bind(on_release=self.dropdown.open)
#         self.dropdown.bind(on_select=lambda instance, x: setattr(self.main_button, 'text', x))

#         header.add_widget(self.main_button) # Add dropdown button to header

#         title_label = Label(text='Bill Break-down', font_size='20sp', halign='center', bold=True)
#         header.add_widget(title_label)

#         main_box.add_widget(header) # Add header to main layout

#         # Left-side box for 'Enter Total Bill (RM):'
#         left_box = BoxLayout(orientation='vertical', spacing=5)
#         total_bill_label = Label(text='Enter Total Bill (RM):')
#         self.total_bill_input = TextInput(input_filter='float')
#         left_box.add_widget(total_bill_label)
#         left_box.add_widget(self.total_bill_input)

#         # Right-side box for 'Enter Number of People:'
#         right_box = BoxLayout(orientation='vertical', spacing=5)
#         people_label = Label(text='Enter Number of People:')
#         self.people_input = TextInput(input_filter='int')
#         right_box.add_widget(people_label)
#         right_box.add_widget(self.people_input)

#         # Add left and right boxes to horizontal layout
#         side_by_side_box = BoxLayout(orientation='horizontal', spacing=5)
#         side_by_side_box.add_widget(left_box)
#         side_by_side_box.add_widget(right_box)

#         # Add horizontal layout to main vertical layout
#         # main_box = BoxLayout(orientation='vertical', spacing=5)
#         main_box.add_widget(side_by_side_box)

#         # Add calculate button
#         self.calculate_button = Button(text='Calculate', size_hint=(1, 0.15))
#         self.calculate_button.bind(on_press=self.break_down)
#         main_box.add_widget(self.calculate_button)

#         # Choose break-down type
#         self.spinner = Spinner(text='Equal break-down', values=('Equal break-down', 'Custom break-down by percentage/ratio', 'Custom break-down by amount'))
#         right_box.add_widget(self.spinner)

#         # Custom grid layout for inputs
#         self.custom_grid = GridLayout(cols=2, spacing=5)
#         right_box.add_widget(self.custom_grid)

#         self.breakdown_button = Button(text='Calculate', size_hint=(1, 0.15))
#         self.breakdown_button.bind(on_press=self.break_down)
#         right_box.add_widget(self.breakdown_button)

#         self.result_label = Label(text='', size_hint=(1, 0.2))
#         right_box.add_widget(self.result_label)

#         return main_box
    
#     def update_rect(self, instance, value):
#         self.rect.pos = instance.pos
#         self.rect.size = instance.size
    
#     def break_down(self, instance):
#         total_bill = float(self.total_bill_input.text)
#         num_people = int(self.people_input.text)
#         if self.spinner.text == 'Equal break-down':
#         # Custom breakdown logic by equality
#             self.result_label.text = f'Each person pays: RM{total_bill / num_people:.2f}'

#         elif self.spinner.text == 'Custom break-down by percentage/ratio':
#             percentages = [float(text_input.text) for text_input in self.custom_grid.children[::-2]] # Extract inputs
#             if sum(percentages) != 100:
#                 self.result_label.text = 'Percentages do not add up to 100%'
#                 return
#             amounts = [total_bill * p / 100 for p in percentages]
#             result_text = ', '.join([f'RM{amount:.2f}' for amount in amounts])
#             self.result_label.text = 'Amounts: ' + result_text

#         elif self.spinner.text == 'Custom break-down by amount':
#             amounts = [float(text_input.text) for text_input in self.custom_grid.children[::-2]] # Extract inputs
#             if sum(amounts) != total_bill:
#                 self.result_label.text = f'Discrepancy detected: Sum of individual amounts (RM{sum(amounts):.2f}) does not match total bill (RM{total_bill:.2f})'
#                 return
#             result_text = ', '.join([f'RM{amount:.2f}' for amount in amounts])
#             self.result_label.text = 'Amounts: ' + result_text

#         else:
#             custom_value = float(self.custom_input.text)
#             # Able to customize the following logic as per your requirements
#             amount = total_bill * custom_value / 100
#             self.result_label.text = f'First person pays: RM{amount:.2f}, Second person pays: RM{total_bill - amount:.2f}'

#     def save_results(self, instance):
#         if not self.result_label.text:
#             return

#         data = {
#             'total_bill': self.total_bill_input.text,
#             'number_of_people': self.people_input.text,
#             'breakdown_type': self.spinner.text,
#             'result': self.result_label.text
#         }

#         with open('results.json', 'a') as file:
#             json.dump(data, file)
#             file.write('\n')

#     def query_results(self, instance):
#         results = []
#         try:
#             with open('results.json', 'r') as file:
#                 for line in file:
#                     results.append(json.loads(line.strip()))
#         except FileNotFoundError:
#             pass

#         self.box.clear_widgets()
#         self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
#         box = BoxLayout(orientation='vertical', size_hint_y=None)
#         box.bind(minimum_height=box.setter('height'))

#         for result in results:
#             label = Label(text=f"Total Bill: {result['total_bill']}, People: {result['number_of_people']}, Type: {result['breakdown_type']}, Result: {result['result']}")
#             box.add_widget(label)

#         self.scroll_view.add_widget(box)
#         self.box.add_widget(self.scroll_view)

    
#     def on_spinner_select(self, instance, value):
#         if value == 'Custom break-down':
#             self.custom_input.disabled = False
#         else:
#             self.custom_input.disabled = True

#     def share_results(self, instance):
#         if not self.result_label.text:
#             # Don't attempt to share if there's no result
#             return

#         subject = "Bill Breakdown"
#         body = f"Here's the breakdown of the bill:\n\n{self.result_label.text}"
        
#         # Open the email client with pre-filled subject and body
#         email.send(subject=subject, text=body)

# if __name__ == '__main__':
#     BreakdownApp().run()
