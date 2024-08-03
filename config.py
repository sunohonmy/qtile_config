# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os
import subprocess
from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.backend.wayland import InputConfig
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
#from qtile_extras.layout.decorations.borders import RoundedCorners

mod = "mod4"
altMod = "mod1"
terminal = "kitty"
browser = "firefox"
bemenu = "bemenu-run -b"
screenshot = 'grim -t jpeg -g "$(slurp)" ~/Pictures/Screenshots/$(date +%Y-%m-%d_%H-%m-%s).jpg'

@hook.subscribe.startup
def autostart_once():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([altMod], "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow/shrink windows left/right.
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the right"
    ),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    #Spawn terminal
    Key([altMod, "control"], "t", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different groups as defined below
    Key([mod], "Tab", lazy.screen.next_group(), desc="Toggle between groups"),
    #Toggle between layouts
    Key([mod, "shift"], "Tab", lazy.next_layout(), desc = "Toggle between layouts"),
    #Kill window
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Custom Keys
    Key([altMod], "Return", lazy.spawn(bemenu), desc = "Launch bemenu"),
    Key([mod], "Print", lazy.spawn("sh -c 'grim -t jpeg ~/Pictures/Screenshots/$(date +%Y-%m-%d_%H-%m-%s).jpg'"), desc = "Save fullscreen screenshot as a jpg"),
    Key([], "Print", lazy.spawn("sh -c 'grim - | wl-copy"), desc = "Copy  fullscreen screenshot to the clipboard"),
    Key([mod, "shift"], "s", lazy.spawn(f"sh -c '{screenshot}'"), desc = "Take screenshot of selected area and save as a jpg"),
    Key([altMod], "space", 
        lazy.window.move_to_top(),
        desc = "Swith to next window and move that window above all other windows with similar priority" ),
]

# Add key bindings to switch VTs (Virtual Terminals) in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [
    Group('1', label='', layout = 'monadtall'),
    Group('2', label='', layout = 'floating'),
    Group('3', label='', layout = 'monadtall'),
    Group('4', label='', layout = 'floating'),
    Group('5', label='', layout = 'monadtall'),
    Group('6', label='', layout = 'floating'),
    Group('7', label='', layout = 'monadtall'),
    Group('8', label='', layout = 'floating'),
    Group('9', label='', layout = 'monadtall'),
]

# group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
# group_labels = ["", "", "", "", "", "", "", "", ""]
# group_layouts = ["monadtall", "floating", "monadtall", "floating", "monadtall", "floating", "monadtall", "floating", "monadtall"]

# for i in range(len(group_names)):
#     groups.append(
#         Group(
#             name=group_names[i],
#             layout=group_layouts[i].lower(),
#             label=group_labels[i],
#         )
#     )


for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )

def init_colours():
    return [
        ["de97b1"], # colour 0
        ["AE77AB"], # colour 1
        ["3A3073"], # colour 2
        ["3798CD"], # colour 3
        ["1C1F50"] # colour 4
    ]

colours = init_colours()

def init_layout_default():
    return {
        "margin": 5,
        "border_focus": colours[3], #RoundedCorners(colour = colours[3]),
        "border_normal": colours[2], #RoundedCorners(colour = colours[2]),
        "border_width": 3
    }

layout_default = init_layout_default()

layouts = [
    layout.MonadTall(
        **layout_default,
        single_border_width = 4,
    ),
    layout.Max(
        **layout_default,
    ),
    layout.Floating(
        **layout_default,
    ),
]

extraDecorations = {
    "decorations": [
        PowerLineDecoration(
            path ="forward_slash",
            #extrawidth = 2,
        )
    ]
}

widget_defaults = dict(
    font="NotoSans Nerd Font",
    fontsize=13,
    padding=3,
    **extraDecorations,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length= 1),
                widget.Chord(
                    font = "NotoSans Nerd Font",
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),

                #widget.Spacer(length = 100,),
                widget.GroupBox(
                    font = "NotoSans Nerd Font",
                    highlight_method='text',
                    disable_drag=True,
                    this_screen_border = colours[3],
                    this_current_screen_border = colours[3],
                    urgent_alert_method = "line",
                    #background = colours[2],
                ),

                widget.CurrentLayout(
                    font = "NotoSans Nerd Font",
                    background = colours[1],
                ),

                widget.WindowName(
                    font = "NotoSans Nerd Font",
                    max_chars = 50,
                    #background = colours[2],

                ),

                widget.Spacer(
                    #background = colours[1],
                ),

                widget.Memory(
                    font = "NotoSans Nerd Font",
                    format = "{MemUsed: .0f}{mm} ({MemPercent:.0f}%)",
                    background = colours[2],
                ),

                widget.UPowerWidget(
                    font = "NotoSans Nerd Font",
                    background = colours[1],
                ),

                widget.Clock(
                    font = "NotoSans Nerd Font",
                    format="%a, %d %b %y | %H:%M %Z",
                    background = colours[2],
                ),
                
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                widget.StatusNotifier(
                    background = colours[1],
                    padding = 5,
                ),

                widget.QuickExit(
                    font = "NotoSans Nerd Font",
                    default_text='   ', 
                    countdown_format='{}',
                ),
            ],
            36,
            #border_width = 4,
            #border_color = "#fff",
            margin = [6, 75, 3, 75],
            background = colours[4],
        ),
        #wallpaper = "/home/sunohonmy/Pictures/solo_leveling_ep_12_1.jpg",
        #wallpaper_mode = "fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus = colours[3],
    border_normal = colours[2],
    border_width = 4,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(wm_class="pavucontrol"),
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
follow_mouse_focus = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = {
    "type:pointer": InputConfig(accel_profile="flat"),
    "type:keyboard": InputConfig(kb_layout="gb"),
}

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = "breeze_cursors"
wl_xcursor_size = 24




# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
