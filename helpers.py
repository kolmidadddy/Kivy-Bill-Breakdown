username_helper = """
MDTextField:
    hint_text:"Enter Username"
    helper_text: "or click on forgot username"
    helper_text_mode:"on_focus"
    icon_right:'calculator'
    icon_right_color: app.theme_cls.primary_color
    pos_hint:{'center_x': 0.5, 'center_y': 0.5}
    size_hint_x:None
    width:300
"""

screen_helper = """
ScrollView:
    BoxLayout:
        orientation: 'Dashboard'
        MDTopAppBar:
            title: 'User Profile'
            right_action_items:[["dots-vertical", lambda x: app.navigation_draw()]]
            elevation: 10

        MDBottomBAppBar:
            MDTopAppBar:
                title:''
                right_action_items:[["clock", lambda x: app.navigation_draw()]]
                mode: 'end'
                type: 'bottom'
                on_action_button: app.navigation_draw()
"""

dropdownmenu_helper = """
BoxLayout:
    orientation= 'vertical'

    MDTopAppBar:
    title: "Menu"
    use_overflow: True
    overflow_cls: CustomOverFlowMenu()
    right_action_items:
        [
        ["dots-vertical", lambda x: app.callback(x),"Exit"]
        ]
    
    MDLabel:
        text: "Content"
        halign: "center
"""

# navigation_helper = """
# ScreenManager:
#     id: screen_m
#     Screen:
#         BoxLayout:
#             orientation: "vertical"

#             MDToolbar:
#                 id: toolbar
#                 title: "User Profile"
#                 md_bg_color: app.theme_cls.primary_color
#                 elevation: 10
#                 left_action_items: [["dots-vertical", lambda x: nav_drawer.set_state("open")]]

#             Widget:

#             MDNavigationDrawer:
#                 id: nav_drawer
#                 orientation: 'vertical'
#                 spacing: '8dp'
#                 padding: '8dp'
                
#                 AnchorLayout:
#                     anchor_x: "left"
#                     size_hint_y: None
#                     height: avatar.height
                

#                 Image:
#                     source: 'shark.jpeg'

#                 MDLabel:
#                     text: ' username'
#                     font_style: 'Subtitle1'
#                     size_hint_y: None
#                     height: self.texture_size[1]

#                 MDLabel:
#                     text: ' manthalok@gmail.com'
#                     font_style: 'Caption'
#                     size_hint_y: None
#                     height: self.texture_size[1]

#                 ScrollView:
#                     MDList:
#                         OneLineListItem:
#                             text: "Screen 1"
#                             on_press:
#                                 nav_drawer.set_state("close")
#                                 screen_manager.current = "screen1"
#                         OneLineListItem:
#                             text: "Screen 2"
#                             on_press:
#                                 nav_drawer.set_state("close")
#                                 screen_manager.current = "screen2"
# """


