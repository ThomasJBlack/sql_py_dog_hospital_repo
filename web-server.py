# export FLASK_APP=werb-server.py
# export FLASK_ENV=development
# flask run

from typing import TYPE_CHECKING
from flask import Flask, render_template, request
import pymysql
# import databaseStuff


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

if __name__ == "__main__":
    app.run(debug=True)
db = pymysql.connect(
    host="freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com",
    user="thomas",
    password="changeme"
)
cursor = db.cursor()


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/dogs", methods=["POST", "GET"])
def dogs():
    form_data = request.form
    if form_data["updating_dog"] is True:
        # save submit changes
        data = {
            "id": form_data["id"],
            "name": form_data["name"],
            "doctor": form_data["doctor"],
            "malady": form_data["malady"],
            "breed": form_data["breed"]
        }
        updateData(type="dogs", data=data)
    else:
        all_data = readData("dogs")

        return render_template("dogs.html", all_data=all_data)


def readData(type):
    table_dict = {}
    if type == "dogs":
        sql = """SELECT dog_table.id as id, dog_table.name AS Dog, dr_table.name AS Doctor, malady_table.malady AS Malady, breed_table.breed AS Breed
                FROM Thomas_Black.dog_table
                JOIN Thomas_Black.dr_table ON dr_table.id = dog_table.id
                JOIN Thomas_Black.malady_table ON malady_table.id = dog_table.malady_id
                JOIN Thomas_Black.breed_table ON breed_table.id = dog_table.breed_id;"""
        cursor.execute(sql)
        while True:
            row = cursor.fetchone()
            print(row)
            if row == None:
                break
            table_dict[row[0]] = {
                "Name": row[1],
                "Doctor": row[2],
                "Malady": row[3],
                "Breed": row[4]
            }
        return table_dict
    if type == "table":
        # get other table
        return("finish me")
    return table_dict


def updateData(type, data):
    if type == "dog":
        # update a dog
        sql = f"""
                UPDATE dog_table
                SET name = {data.name},
                    dogs_doctor_id = dr_table.id ON {data.doctor} LIKE dr_table.name,
                    malady_id = malady_table.id ON {data.malady} LIKE malady_table.malady,
                    breed_id = breed_table.id ON {data.breed} LIKE breed_table.breed,
                WHERE id = {data.id};
                """
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    if type == "doctor":
        # update a doctor
        cursor.execute(sql)
