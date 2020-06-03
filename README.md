# website-blocker

This program edits the \Windows\System32\drivers\etc\hosts file with a blacklist of websites.
Access to those websites will be blocked during a set timeframe.
The hosts file must not be read-only.

* Websites can be added/removed in the blacklist
* Select time-range to activate blocker in hours
* when active, hosts file includes blacklisted websites
* when inactive, hosts file reverts back

# webmap-folium

Experimenting with Folium Python module. This program creates an html map (map.html) from a json file
and pinpoints the locations of various volcanoes from a csv file's data.

* Run webmap.py, then open map.html
* Also available as Jupyter notebook

# interactive-english-dictionary

The dictionary data is in resources/dictionary.json

# flask-personal-website

Simple testing of Python & Flask website development. Abandoned project

* needs flask module (pip install flask)

# bookstore-database-gui

First experiment with GUI with tkinter module.

* Main script: book_store_gui.py
* Backend: book_store_database.py (uses sqlite3)
* Database: book_store.db

# mobile-app-kivy

2nd attempt for GUI with Python. Testing **Kivy** cross-platform framework building an app that users can login/sign up to and displays a random quote based on their given mood.

* Kivy installation for Python 3.7:
```
pip install kivy
pip install kivy.deps.glew
pip install docutils pygments pypiwin32 kivy.deps.sdl2
```
* Users login info: files/users.json
* Kivy source GUI: files/gui.kv
* Quotes: files/*.txt
The filename corresponds to the user's specified mood.

For Android deployment, install cython, kivy and buildozer on Linux.
You may use files/kivy-buildozer-installer.sh to install all dependancies.
