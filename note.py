#!/bin/python
from threading import Thread
import socket
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gdk

PORT = 12347
HOST = "127.0.0.1"


def start_server(w):
    def show_all(w):
        w.show_all()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    try:
        while True:
            try:
                conn, addr = s.accept()
                data = conn.recv(1024)
                GLib.idle_add(show_all, w)
            except socket.error:
                continue
    except KeyboardInterrupt:
        conn.close()


def check_already_running() -> bool:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        return True
    except Exception as e:
        return False


def main():
    def gui() -> Gtk.Window:
        def quit(_w):
            Gtk.main_quit()

        def hide(win, ev):
            keyname = Gdk.keyval_name(ev.keyval)
            if keyname == "Escape":
                win.hide()
        t = Gtk.TextView()
        w = Gtk.Window()
        w.maximize()
        w.add(t)
        w.connect("destroy", quit)
        w.connect("key-press-event", hide)
        w.show_all()
        return w

    def style():
        css = b'''
        textview text {
            background-color: #eafba1;
        }
        textview {
            font-size: 28px;
        }
        '''
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(
            screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def start_server_or_exit(window) -> bool:
        if check_already_running():
            sys.exit()
        else:
            server = Thread(target=start_server, args=(window,))
            server.start()

    window = gui()
    start_server_or_exit(window)
    style()
    Gtk.main()


if __name__ == "__main__":
    main()
