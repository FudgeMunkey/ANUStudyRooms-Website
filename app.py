import datetime

from flask import Flask, render_template, request
import json

app = Flask(__name__)

DAYS_NUM = 11
BUILDINGS = ["Chifley", "Hancock", "Law", "Menzies"]


# Generate a list of dates in the format: YYYY-MM-DD
def generateDates(num_days):
    date_list = []

    start_date = datetime.datetime.today()

    for n in range(num_days):
        date = start_date + datetime.timedelta(days=n)
        date = date.strftime("%Y-%m-%d")
        date_list.append(date)

    return date_list


# Convert times to minutes for easier comparison
def convertStringToMinutes(time_list):
    new_list = []

    for t in time_list:
        split = t.split(':')
        hours = int(split[0]) * 60
        minutes = int(split[1])
        new_list.append(hours + minutes)

    return new_list


# This function is passed through to the HTML form to help convert minutes to time strings
@app.context_processor
def utility_processor():
    def convertMinutesToString(mins):
        hours = int(mins / 60)
        minutes = int(mins - hours * 60)
        outStr = str(hours).zfill(2) + ':' + str(minutes).zfill(2)
        return outStr
    return dict(convertMinutesToString=convertMinutesToString)


@app.route('/')
def home():
    return render_template('home.html', buildingList=BUILDINGS, dateList=generateDates(DAYS_NUM))


@app.route('/', methods=['POST'])
def filter():
    selected_building = request.form['building']
    selected_date = request.form['date']

    # Read in values
    text = open("static/data/scan.json", "r")
    my_content = text.read()
    text.close()

    # Convert text to json and slice relevant info
    parsed_json = (json.loads(my_content))
    sliced_json = parsed_json[selected_building][selected_date]
    for room in sliced_json:
        sliced_json[room] = convertStringToMinutes(sliced_json[room])
    # print(json.dumps(sliced_json, indent=4, sort_keys=True))

    # Generate Boolean table
    bool_array = []

    # Go through each time slot (i.e. 00:00-00:15, 00:15-00:30, etc)
    time_start = 0
    # time_start = 540
    time_end = 1425
    increment = 15
    for c in range(int(time_end / 15) + 1 - int(time_start / 15)):
        bool_row = []

        # Go through each of the rooms
        for room in sliced_json:
            booked = False

            # Grab pairs of times and see if we are within the range
            for i in range(0, len(sliced_json[room]), 2):
                start = sliced_json[room][i]
                end = sliced_json[room][i + 1]

                time_current = time_start + c * increment

                if start <= time_current < end:
                    booked = True
                    break

            bool_row.append(booked)
        bool_array.append(bool_row)

    return render_template('home.html', buildingList=BUILDINGS, dateList=generateDates(DAYS_NUM),
                           buildingSelected=selected_building, dateSelected=selected_date,
                           startTime=time_start, titles=sliced_json.keys(), bool_booked=bool_array)


if __name__ == '__main__':
    app.debug = True
    app.run()
