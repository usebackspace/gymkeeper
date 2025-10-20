
README

 Starting the Django Server

This project uses a batch script to launch the Django development server and open your default browser to the local address automatically.

 How to Run

1. Make sure you have your Python virtual environment set up in the `env` folder inside the project directory.

2. Double-click the batch file `hanix-gymkeeper.bat` located in the root of your project (`C:\gymkeeper`).

3. The batch script will:

   * Activate the virtual environment.
   * Start the Django development server.
   * Wait a few seconds for the server to boot.
   * Open your default web browser at [http://127.0.0.1:8000](http://127.0.0.1:8000).

4. A command window will remain open showing the server logs. To stop the server, press `Ctrl + C` in the command window, then close it.

---

 Notes

* If the browser opens before the server is fully ready, refresh the page after a few seconds.
* If you modify your Django code while the server is running, it will auto-restart.
* Make sure your virtual environment and dependencies are properly installed.

---

 Troubleshooting

* If the script fails to activate the virtual environment, verify the `env` folder and virtual environment are set up correctly.
* If the server doesn't start or shows errors, run `python manage.py runserver` manually inside the activated environment to debug.

---

Enjoy working on your Django project! 🚀

---


| Step                       | What to Do                        |
| -------------------------- | --------------------------------- |
| On new system:             | Install Python                    |
| Transfer project files     | Copy your Django project folder   |
| Create virtual environment | `python -m venv env`              |
| Activate environment       | `env\Scripts\activate`            |
| Install dependencies       | `pip install -r requirements.txt` |
| Run server                 | `python manage.py runserver`      |
