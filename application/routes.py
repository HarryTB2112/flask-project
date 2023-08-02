from application import app, db
from flask import request, jsonify, render_template, redirect
from application.models import FriendsCharacter
from application.forms import AddCharacterForm


def format_character(character):
    return {
        "id": character.id,
        "name": character.name,
        "age": character.age,
        "catch_phrase": character.catch_phrase,
    }


@app.route("/")
def index():
    return "Index Page"


@app.route("/characters/", methods=["GET", "POST"])
def get_characters():
    form = AddCharacterForm()
    if request.method == "GET":
        characters = FriendsCharacter.query.all()
        character_list = []
        for character in characters:
            character_list.append(format_character(character))
        return render_template(
            "characters.html",
            characters=character_list,
            title="Friends Characters",
            form=form,
        )
    else:
        if form.validate_on_submit():
            character = FriendsCharacter(
                form.name.data, form.age.data, form.catch_phrase.data
            )
            db.session.add(character)
            db.session.commit()
            return redirect("/")
        # data = request.json
        # character = FriendsCharacter(data["name"], data["age"], data["catch_phrase"])
        # db.session.add(character)
        # db.session.commit()
        # return jsonify(
        #     id=character.id,
        #     name=character.name,
        #     age=character.age,
        #     catch_phrase=character.catch_phrase,
        # )


@app.route("/characters/<id>", methods=["GET"])
def get_character(id):
    character = FriendsCharacter.query.filter_by(id=id).first()
    return render_template("character.html", character=character)


@app.route("/characters/<id>", methods=["DELETE"])
def delete_character(id):
    character = FriendsCharacter.query.filter_by(id=id).first()
    db.session.delete(character)
    db.session.commit()
    return f"{character.name} deleted"


@app.route("/characters/<id>", methods=["PATCH"])
def update_character(id):
    character = FriendsCharacter.query.filter_by(id=id)
    data = request.json
    character.update(
        dict(name=data["name"], age=data["age"], catch_phrase=data["catch_phrase"])
    )
    db.session.commit()
    updated_character = character.first()
    return jsonify(
        id=updated_character.id,
        name=updated_character.name,
        age=updated_character.age,
        catch_phrase=updated_character.catch_phrase,
    )
