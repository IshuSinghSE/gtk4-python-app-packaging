#!/usr/bin/env python3
"""Simple GTK app for testing packaging."""
import sys
try:
    import gi
    gi.require_version('Gtk', '4.0')
    from gi.repository import Gtk
except Exception as e:
    print('Gtk import failed:', e)
    sys.exit(1)

class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.example.idgaf')

    def do_activate(self):
        w = Gtk.Window(application=self)
        w.set_title('idgaf')
        w.set_default_size(300, 100)
        # Create a vertical box to hold the button and the label
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Button that will be visible initially
        btn = Gtk.Button(label='IDGAF')
        btn.set_hexpand(True)
        btn.set_vexpand(True)
        btn.set_halign(Gtk.Align.CENTER)
        btn.set_valign(Gtk.Align.CENTER)
        # Label that is initially hidden and shown when the button is clicked
        label = Gtk.Label(label="I Don't Give A Fuck")
        label.set_hexpand(True)
        label.set_vexpand(True)
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)
        label.set_visible(False)

        def on_button_clicked(button):
            # hide the button and show the label when clicked
            button.hide()
            label.show()

        btn.connect('clicked', on_button_clicked)

        box.append(btn)
        box.append(label)

        w.set_child(box)
        w.show()

def main(argv=None):
    app = MyApp()
    return app.run([] if argv is None else argv)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
