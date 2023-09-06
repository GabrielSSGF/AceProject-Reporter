<h1 align="center">
  <br>
  <a href="https://www.aceproject.com/"><img src="https://dtyoc.files.wordpress.com/2015/11/aceproject-logo.png" alt="Ace Project" width="200"></a>
  <br>
  AceProject Reporter
  <br>
</h1>

<h4 align="center">Report generator and email sender for monitoring time registering.</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#credits">Credits</a>
</p>

# Key Features
Generates two reports containing the information regarding the time registered by each employee with their respective tasks and projects. The reports are sended over to HR and employees that dont register their hours will receive an email requesting them to register it. In the afternoon, a last email will be sent to the managers with a list of employees whose timesheets are waiting for approval and another list of employees that didnt submit their working hours.
The list of periods of email sending are as follows:
- 9 AM - Reminds the employees to register their working hours from last week;
- 12 PM:
  - Final reminder for employees to register their working hours;
  - Excel reports for HR.
- 5 PM:
  - Final excel reports for HR.
  - Sends to the managers two lists of employess (submitted/waiting for approval and pending).

# How To Use
To clone and run this application, you'll need [Git](https://git-scm.com) and [Python 3](https://www.python.org/downloads/). From your command line:


```bash
# Clone this repository
$ git clone https://github.com/GabrielSSGF/AceProject-Reporter

# Go into the repository
$ cd AceProject-Reporter

```

Before running it, modify the code with the necessary information regarding the authentication of AceProject, email sender, HR email, managers emails, corporate email and a file path for the reports.
After the modifications are made:

```bash
# Install dependencies
$ pip install pandas xlsxwriter

# Run the app
$ python3 main.py
```

# Credits

This software uses the following Python libraries:

- [Pandas](https://pandas.pydata.org/) - For data analysis;
- [XLSXWriter](https://xlsxwriter.readthedocs.io/index.html) - For Excel exportation.
