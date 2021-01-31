#!/bin/python
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GLib
import sys
import socket
from threading import Thread

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
    def quit(w):
        Gtk.main_quit()

    t = Gtk.TextView()
    w = Gtk.Window()
    w.add(t)
    w.connect("destroy", quit)

    if check_already_running():
        return
    else:
        server = Thread(target=start_server, args=(w,))
        server.start()

    def hide(win, ev):
        keyname = Gdk.keyval_name(ev.keyval)
        if keyname == "Escape":
            win.hide()

    w.connect("key-press-event", hide)
    w.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
