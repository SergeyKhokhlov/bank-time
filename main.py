# -*-coding: utf-8 -*-

from flask import Flask, render_template, redirect
from data import db_session, notes, addNoteForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'info_bank'


@app.route("/")
def redirect_on_main_page():
    session = db_session.create_session()
    all = session.query(notes.Note).all()
    all_names = []
    all_imgs = []
    counter = 0
    all.reverse()
    for i in all:
        counter += 1
        if counter == 6:
            break
        all_names.append(i.name)
        all_imgs.append(i.img)
    return render_template("index.html", notes_list=all_names, all_imgs=all_imgs,
                           next_page=2, back_page=1,
                           title="Bank-Time | Читайте о новостях банков, ипотеках, кредитах у нас!",
                           description="Bank-Time - сайт с новостями банков, "
                                       "ипотеках, кредитах.")


@app.route("/page/<int:num>")
def index(num):
    session = db_session.create_session()
    all = session.query(notes.Note).all()
    all_names = []
    all_imgs = []
    counter = 0
    all.reverse()
    for i in all:
        counter += 1
        if (counter > num * 5 - 5) and (counter < num * 5):
            all_names.append(i.name)
            all_imgs.append(i.img)
    next_page = num + 1
    back_page = num - 1
    if num == 1:
        return redirect("/")
    if len(all_names) < 5:
        next_page = num
    return render_template("index.html", next_page=next_page, back_page=back_page,
                           notes_list=all_names, all_imgs=all_imgs,
                           title="Bank-Time | Читайте о новостях банков, ипотеках, кредитах у нас!",
                           description="Bank-Time - сайт с новостями банков, "
                                       "ипотеках, кредитах.")


@app.route("/note/<int:id_page>")
def page(id_page):
    session = db_session.create_session()
    all_notes = session.query(notes.Note).all()
    all_notes.reverse()
    note = all_notes[id_page - 1]
    return render_template("page.html",
                           name=note.name,
                           text=note.content.split("\n"),
                           title="Bank-Time | " + note.name,
                           description=note.content)


@app.route("/addNote/<int:password>", methods=["GET", "POST"])
def addNote(password):
    if password == 7355608:
        form = addNoteForm.addNote()
        if form.validate_on_submit():
            session = db_session.create_session()
            note = notes.Note(name=form.name.data,
                              content=form.content.data,
                              img=form.img.data)
            session.add(note)
            session.commit()
            return redirect("/")
        return render_template("addNote.html", form=form)
    else:
        return redirect("/")


def main():
    db_session.global_init("db/database.db")
    app.run()


if __name__ == '__main__':
    main()
