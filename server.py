from flask import Flask, render_template, url_for, request, redirect
import csv
import os


app = Flask(__name__)
print(__name__)

_CONTACTS_TXT = './contacts.txt'
_CONTACTS_DB = './contacts.csv'

def save_contact_to_file(data):
    try:
        with open(_CONTACTS_TXT, mode='a') as my_file:
            out = ''
            for key in data:
                out = out + data[key] + ','
            # rememer to strip last last ,
            out = out[:len(out)-1] + '\n'
            my_file.write(out)
    except FileNotFoundError as err:
        print("can't find the file")
        raise err
    except IOError as err:
        print("IO Error")
        raise err


def save_contact_to_csv(data):
    try:
        fieldnames=['email', 'subject', 'message']
        with open(_CONTACTS_DB, mode='a+', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            # if new file then add header then add it
            if os.path.getsize(_CONTACTS_DB) == 0:
                csv_writer.writeheader()
            csv_writer.writerow(data)
    except FileNotFoundError as err:
        print("can't find the file")
        raise err
    except IOError as err:
        print("IO Error")
        raise err



@app.route('/')
@app.route('/<page_name>')
def home(page_name='index.html'):
     return render_template(page_name)        # templates need to go in templates directory

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == "POST":
        data = request.form.to_dict()
        print(data)
        save_contact_to_csv(data)
        return redirect('./thankyou.html')
    else:
        return request.method

