from datetime import datetime
from tkinter import *
from tkinter import messagebox, filedialog
from database import *
import re, sys, os

dbdirectory = "./database.txt"


def sorting_Toplevel():
    sort_params_hidden = ["name", "surname", "patronymic", "age", "birthdate", "subdivision", "military_speciality"]
    sort_params_shown = ["Ім'я", "Прізвище", "По батькові", "Вік", "День народження", "Підрозділ",
                         "Військова спеціальність"]
    sorting_Top = Toplevel(list_Top)
    sorting_Top.title("Оберіть параметр сортування")

    sorting_Top.geometry("500x600-700+250")

    reverse_sort_var = IntVar()
    sorting_Listbox = Listbox(sorting_Top)
    for param in sort_params_shown:
        sorting_Listbox.insert(END, param)

    sorting_Listbox.bind("<Double-Button>", lambda event: sorting_Button.invoke())
    sorting_Listbox.pack()
    reverse_Checkbutton = Checkbutton(sorting_Top, offvalue=0, onvalue=1, variable=reverse_sort_var, text="Навпаки")
    reverse_Checkbutton.pack()
    sorting_Button = Button(sorting_Top, text="Відсортувати", command=lambda:
    [db.sort(sort_params_hidden[sorting_Listbox.curselection()[0]], True if reverse_sort_var.get() == 1 else False),
     sorting_Top.destroy(), list_Top.destroy(), list_Toplevel()])
    sorting_Button.pack()

    sorting_Top.protocol("WM_DELETE_WINDOW", lambda: [list_Switch_Buttons.invoke(), sorting_Top.destroy()])
    sorting_Top.mainloop()


def list_Toplevel():
    global list_Top
    global list_Top_Buttons
    global filtered_win
    filtered_win = False
    list_Top_Buttons = []
    list_Top = Toplevel()
    list_Top.title("Список")
    list_Top.geometry("700x600-600+250")
    list_Listbox = Listbox(list_Top)
    for person in db.persons:
        list_Listbox.insert(END, person)

    list_Listbox.pack(fill="x")

    list_Exit_Button = Button(list_Top, text="Вихід", command=lambda: [main_win.deiconify(), list_Top.destroy(), db.save()])
    list_Exit_Button.pack()
    list_Select_Button = Button(list_Top, text="Вибрати",
                                command=lambda: user_info_Toplevel(list_Top, list_Listbox.curselection()[0]))
    list_Select_Button.pack()
    list_Sort_Button = Button(list_Top, text="Сортувати",
                              command=lambda: [list_Switch_Buttons.invoke(), sorting_Toplevel()])
    list_Sort_Button.pack()
    list_Filter_Button = Button(list_Top, text="Фільтр",
                                command=lambda: [list_Switch_Buttons.invoke(), select_filter_Toplevel()])
    list_Filter_Button.pack()
    list_Search_Button = Button(list_Top, text="Пошук",
                                command=lambda: [list_Switch_Buttons.invoke(), search_Toplevel()])
    list_Search_Button.pack()
    global list_Switch_Buttons
    list_Switch_Buttons = Button(list_Top, command=lambda:
    [list_Sort_Button.config(state=DISABLED),
     list_Filter_Button.config(state=DISABLED),
     list_Select_Button.config(state=DISABLED),
     list_Search_Button.config(state=DISABLED)]
    if list_Search_Button["state"] in [NORMAL, ACTIVE]
    else
    [list_Sort_Button.config(state=NORMAL),
     list_Filter_Button.config(state=NORMAL),
     list_Select_Button.config(state=NORMAL),
     list_Search_Button.config(state=NORMAL)])

    global list_update_Button
    list_update_Button = Button(list_Top, command=lambda: [list_Top.destroy(), list_Toplevel()])

    list_Top.protocol("WM_DELETE_WINDOW", lambda: [main_win.deiconify(), list_Top.destroy(), db.save()])
    list_Top_Buttons = [list_Exit_Button, list_Filter_Button, list_Select_Button]
    list_Top.mainloop()


def search_Toplevel():
    global search_Top
    search_Top = Toplevel(list_Top)
    search_Top.title("Пошук")
    search_Top.geometry("300x300-800+350")
    search_field_Entry = Entry(search_Top)
    search_field_Entry.pack()

    search_options_hidden = ["name", "surname", "patronymic", "surname+name", "surname+name+patronymic", "position",
                             "education", "subdivision", "military_speciality"]
    search_options_shown = ["Ім'я", "Прізвище", "По батькові", "Прізвище і ім'я", "ПІБ", "Посада",
                            "Освіта", "Підрозділ", "Військова спеціальність"]

    search_options_Listbox = Listbox(search_Top)
    for option in search_options_shown:
        search_options_Listbox.insert(END, option)

    search_options_Listbox.pack()

    search_Button = Button(search_Top, text="Пошук", command=lambda:
    [[search_Top.withdraw(), search_result_Toplevel(search_options_hidden[search_options_Listbox.curselection()[0]],
                                                    search_field_Entry.get())] if isinstance(
        search_options_Listbox.curselection()[0], int)
                                                                                  and search_field_Entry.get() != "" else ()])
    search_Button.pack()

    search_Switch_Button = Button(search_Top, command=lambda: search_Button.config(state=DISABLED)
    if search_Button["state"] == NORMAL
    else
    search_Button.config(state=NORMAL))

    search_Top.protocol("WM_DELETE_WINDOW", lambda: [search_Top.destroy(), list_update_Button.invoke()])

    search_Top.mainloop()


def search_result_Toplevel(search_key, search_value):
    search_value = search_value.lower()
    search_result_id = []
    search_result_Top = Toplevel(list_Top)
    search_result_back_Button = Button(search_result_Top, text="Назад", command=lambda: [search_result_Top.destroy(),
                                                                                         search_Top.deiconify()])
    search_result_Top.geometry("500x500-700+350")
    search_result_Top.title("Результати пошуку")
    search_result_Top.resizable(False, False)

    search_result_Listbox = Listbox(search_result_Top)
    index = 0
    for person in db.persons:
        if search_key == "surname+name":
            try:
                if search_value.split()[0] in getattr(person, search_key.split("+")[0]).lower() \
                        and search_value.split()[1] in getattr(person, search_key.split("+")[1]).lower():
                    search_result_Listbox.insert(END, person)
                    search_result_id.append(index)
            except Exception:
                show_error("Перевірте правильність вводу.")
                search_result_back_Button.invoke()
        elif search_key == "surname+name+patronymic":
            try:
                if search_value.split()[0] in getattr(person, search_key.split("+")[0]).lower() \
                        and search_value.split()[1] in getattr(person, search_key.split("+")[1]).lower() \
                        and search_value.split()[2] in getattr(person, search_key.split("+")[2]).lower():
                    search_result_Listbox.insert(END, person)
                    search_result_id.append(index)
            except Exception:
                show_error("Перевірте правильність вводу.")
                search_result_back_Button.invoke()
        else:
            if search_value in getattr(person, search_key).lower():
                search_result_Listbox.insert(END, person)
                search_result_id.append(index)
        index += 1

    search_result_Listbox.pack(fill="x")
    search_result_select_Button = Button(search_result_Top, text="Вибрати", command=lambda:
    [user_info_Toplevel(search_result_Top, search_result_id[search_result_Listbox.curselection()[0]])])
    search_result_select_Button.pack()
    search_result_Top.protocol("WM_DELETE_WINDOW", lambda: search_result_back_Button.invoke())
    search_result_Top.mainloop()


def select_filter_Toplevel():
    filter_params_hidden = ["Military", "Civil", "reserver"]
    filter_params_shown = ["Військові", "Цивільні", "Офіцери запасу"]
    global select_filter_Top
    select_filter_Top = Toplevel(list_Top)
    select_filter_Top.title("Обрати фільтр")
    select_filter_Top.geometry("500x600-700+250")
    select_filter_Listbox = Listbox(select_filter_Top)
    for i in filter_params_shown:
        select_filter_Listbox.insert(END, i)
    select_filter_Listbox.pack()
    filter_Button = Button(select_filter_Top, text="Показати", command=lambda:
    [list_Top.withdraw(), filter_Button.config(state=DISABLED),
     filtered_Toplevel(filter_params_hidden[select_filter_Listbox.curselection()[0]])])
    filter_Button.pack()

    global select_filter_show_Button
    select_filter_show_Button = Button(select_filter_Top, command=lambda: filter_Button.config(state=NORMAL))

    select_filter_Top.protocol("WM_DELETE_WINDOW", lambda: [select_filter_Top.destroy(), list_update_Button.invoke()])
    select_filter_Top.mainloop()


def filtered_Toplevel(filter_key: str):
    global filtered_Top
    filtered_persons_id = []
    filtered_Top = Toplevel(select_filter_Top)
    filtered_Top.title("Результати з фільтром")
    filtered_Top.geometry("500x600-700+270")
    filtered_Listbox = Listbox(filtered_Top)
    index = 0
    if ["Civil", "Military"].__contains__(filter_key):
        for person in db.persons:
            if person.type() == filter_key:
                filtered_Listbox.insert(END, person)
                filtered_persons_id.append(index)
            index += 1
    else:
        for person in db.persons:
            if isinstance(person, Civil):
                if ["так", "yes", "+", "true", "1"].__contains__(person.reserver.lower()):
                    filtered_Listbox.insert(END, person)
                    filtered_persons_id.append(index)
            index += 1
    filtered_Listbox.pack(fill="x")

    filtered_select_Button = Button(filtered_Top, text="Вибрати", command=lambda:
    user_info_Toplevel(filtered_Top, filtered_persons_id[filtered_Listbox.curselection()[0]]))

    filtered_select_Button.pack()

    global filtered_update_Button
    filtered_update_Button = Button(filtered_Top,
                                    command=lambda: [filtered_Top.destroy(), filtered_Toplevel(filter_key)])

    filtered_Top.protocol("WM_DELETE_WINDOW", lambda: [filtered_Top.destroy(), select_filter_show_Button.invoke()])
    filtered_Top.mainloop()


def user_info_Toplevel(master, id):
    global user_info_Top
    user_info_Top = Toplevel(master)
    user_info_Top.title("Дані")
    user_info_Top.geometry("700x600-600+250")
    person = db.persons[id]
    regex = re.findall("\[(.*?)]", person.str())
    regex.remove(regex[0])
    user_info_Listbox = Listbox(user_info_Top)
    for element in regex:
        user_info_Listbox.insert(END, element)

    user_info_Listbox.pack(fill="x")
    Button(user_info_Top, text="Змінити", command=lambda: edit_user_info_Toplevel(person, id,
                                                                                  user_info_Listbox.curselection()[0],
                                                                                  user_info_Listbox.get(ANCHOR))).pack()
    Button(user_info_Top, text="Видалити людину", command=lambda:
    [db.persons.pop(id), db.save(), user_info_Top.destroy(), [filtered_update_Button.invoke()]
    if "filtered_Top" in globals() else list_update_Button.invoke()]).pack()
    if db.persons[id].type() == "Military":
        Button(user_info_Top, text="Відправити в запас",
               command=lambda: [ToCivil(id), user_info_exit_Button.invoke()]).pack()
    user_info_exit_Button = Button(user_info_Top, text="Вихід", command=lambda:
    [user_info_Top.destroy(), list_Top.destroy(), list_Toplevel()])
    user_info_exit_Button.pack(fill=BOTH)
    user_info_Top.protocol("WM_DELETE_WINDOW", lambda: [user_info_Top.destroy(), list_Top.destroy(), list_Toplevel()])
    user_info_Top.mainloop()


def ToCivil(id: int):
    db.persons[id] = Military.ToCivil(db.persons[id])


def edit_user_info_Toplevel(person, personid: int, attrid, line: str):
    edit_user_info_Top = Toplevel(user_info_Top)
    edit_user_info_Top.title("Редагування")
    Label(edit_user_info_Top, text="Поміняйте значення:").pack()
    edit_info_Entry = Entry(edit_user_info_Top, width=70)
    edit_user_info_Top.geometry("-600+350")
    edit_info_Entry.insert(END, line)
    edit_info_Entry.pack()
    Button(edit_user_info_Top, text="Зберегти", command=lambda:
    [setattr(person, person.__class__.attr_list[attrid], edit_info_Entry.get()),
     (db.save(), edit_user_info_Top.destroy(), user_info_Top.destroy(),
      user_info_Toplevel(user_info_Top.master, personid))
     if not person.__class__.error else ()]).pack()
    Button(edit_user_info_Top, text="Скасувати", command=edit_user_info_Top.destroy).pack()
    edit_user_info_Top.mainloop()


def save_info(type, name, surname, patronymic, day, month, year, height, weight, index, state, district,
              city, street,
              home_num, phone_num, civil_occupation, military_speciality,
              education, rank, rank_assign_date, rank_assign_month,
              rank_assign_year, position, subdivision, duty_form,
              character_note, attitude_to_duty, reserver):
    try:
        person = Civil(name.get(), surname.get(), patronymic.get(), date(int(year.get()), int(month.get()), int(day.get())),
                       height.get(), weight.get(), Location(index.get(), state.get(), district.get(), city.get(), street.get(), home_num.get()),
                       phone_num.get(), education.get(), reserver, civil_occupation.get(), military_speciality.get(), rank.get(),
                       f"{rank_assign_year.get()}/{rank_assign_month.get()}/{rank_assign_date.get()}", position.get(),
                       subdivision.get(), duty_form.get(), character_note.get(), attitude_to_duty.get()) if type.lower() == "civil" else \
            Military(name.get(), surname.get(), patronymic.get(), date(int(year.get()), int(month.get()), int(day.get())),
                       height.get(), weight.get(), Location(index.get(), state.get(), district.get(), city.get(), street.get(), home_num.get()),
                       phone_num.get(), education.get(), military_speciality.get(), rank.get(),
                       f"{rank_assign_year.get()}/{rank_assign_month.get()}/{rank_assign_date.get()}", position.get(),
                       subdivision.get(), duty_form.get(), character_note.get(), attitude_to_duty.get())
    except Exception:
        show_error("Перевірте правильність введених даних")

    try:
        if not person.__class__.error:
            db.persons.append(person)
            if messagebox.showinfo("Результат", "Запис успішно збережено."):
                registration.destroy()
                db.save()
                main_win.deiconify()
        else:
            show_error("Перевірте правильність введених даних.")
            person.__class__.error = False
    except Exception:
        pass


def registration_Toplevel():
    global registration
    registration = Toplevel(main_win)

    registration.title("Регістр")
    registration.geometry("-650+200")

    Label(registration, text="Ім'я: ").grid(row=0, column=0, sticky="w")
    name_Entry = Entry(registration, width=10)
    name_Entry.grid(row=0, column=1, columnspan=3, sticky=N+E+S+W)

    Label(registration, text="Військовий?").grid(row=0, column=5)
    type_Var = IntVar()
    type_Checkbutton = Checkbutton(registration, onvalue=1, offvalue=0, variable=type_Var).grid(row=0, column=6)

    Label(registration, text="Прізвище: ").grid(row=1, column=0, sticky="w")
    surname_Entry = Entry(registration, width=10)
    surname_Entry.grid(row=1, column=1, columnspan=3, sticky=N+E+S+W)

    Label(registration, text="По батькові: ").grid(row=2, column=0, sticky="w")
    patronymic_Entry = Entry(registration, width=10)
    patronymic_Entry.grid(row=2, column=1, columnspan=3, sticky=N+E+S+W)

    Label(registration, text="День народження(дд.мм.рррр): ").grid(row=3, column=0, sticky="w")
    birth_day_Entry = Entry(registration, width=2)
    birth_day_Entry.grid(row=3, column=1, sticky=N+E+S+W)
    birth_month_Entry = Entry(registration, width=2)
    birth_month_Entry.grid(row=3, column=2, sticky=N+E+S+W)
    birth_year_Entry = Entry(registration, width=6)
    birth_year_Entry.grid(row=3, column=3, sticky=N+E+S+W)

    Label(registration, text="Висота: ").grid(row=4, column=0, sticky="w")
    height_Entry = Entry(registration, width=10)
    height_Entry.grid(row=4, column=1, columnspan=3, sticky=N+E+S+W)

    Label(registration, text="Вага: ").grid(row=5, column=0, sticky="w")
    weight_Entry = Entry(registration, width=10)
    weight_Entry.grid(row=5, column=1, columnspan=3, sticky=N+E+S+W)

    Label(registration, text="Місце прописки").grid(row=6, column=1, columnspan=3)

    Label(registration, text="Індекс: ").grid(row=7, column=0, sticky="w")
    index_Entry = Entry(registration, width=2)
    index_Entry.grid(row=7, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Область: ").grid(row=8, column=0, sticky="w")
    state_Entry = Entry(registration, width=10)
    state_Entry.grid(row=8, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Район: ").grid(row=9, column=0, sticky="w")
    district_Entry = Entry(registration, width=10)
    district_Entry.grid(row=9, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Місто: ").grid(row=10, column=0, sticky="w")
    city_Entry = Entry(registration, width=10)
    city_Entry.grid(row=10, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Вулиця: ").grid(row=11, column=0, sticky="w")
    street_Entry = Entry(registration, width=10)
    street_Entry.grid(row=11, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Номер буд.: ").grid(row=12, column=0, sticky="w")
    home_num_Entry = Entry(registration, width=2)
    home_num_Entry.grid(row=12, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Номер тел.: ").grid(row=13, column=0, sticky="w")
    phone_num_Entry = Entry(registration, width=2)
    phone_num_Entry.insert(INSERT, "+380")
    phone_num_Entry.grid(row=13, column=1, sticky=N + E + S + W, columnspan=3)


    Label(registration, text="Цивільна проф.:").grid(row=14, column=0, sticky="w")
    civil_occupation_Entry = Entry(registration, width=2)
    civil_occupation_Entry.grid(row=14, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Військова спец.:").grid(row=15, column=0, sticky="w")
    military_speciality_Entry = Entry(registration, width=2)
    military_speciality_Entry.grid(row=15, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Освіта:").grid(row=16, column=0, sticky="w")
    education_Entry = Entry(registration, width=2)
    education_Entry.grid(row=16, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Звання:").grid(row=17, column=0, sticky="w")
    rank_Entry = Entry(registration, width=2)
    rank_Entry.grid(row=17, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Дата присвоєння:").grid(row=18, column=0, sticky="w")
    rank_assign_day_Entry = Entry(registration, width=2)
    rank_assign_day_Entry.grid(row=18, column=1, sticky=N+E+S+W)
    rank_assign_month_Entry = Entry(registration, width=2)
    rank_assign_month_Entry.grid(row=18, column=2, sticky=N+E+S+W)
    rank_assign_year_Entry = Entry(registration, width=6)
    rank_assign_year_Entry.grid(row=18, column=3, sticky=N+E+S+W)

    Label(registration, text="Посада:").grid(row=19, column=0, sticky="w")
    position_Entry = Entry(registration)
    position_Entry.grid(row=19, column=1, columnspan=3)

    Label(registration, text="Підрозділ:").grid(row=20, column=0, sticky="w")
    subdivision_Entry = Entry(registration, width=2)
    subdivision_Entry.grid(row=20, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Вид служби:").grid(row=21, column=0, sticky="w")
    duty_form_Entry = Entry(registration, width=2)
    duty_form_Entry.grid(row=21, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Особливості характеру:").grid(row=22, column=0, sticky="w")
    character_note_Entry = Entry(registration, width=2)
    character_note_Entry.grid(row=22, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Ставлення до служби:").grid(row=23, column=0, sticky="w")
    attitude_to_duty_Entry = Entry(registration, width=2)
    attitude_to_duty_Entry.grid(row=23, column=1, sticky=N + E + S + W, columnspan=3)

    Label(registration, text="Запас?").grid(row=1, column=5, sticky="w")
    reserver_Var = IntVar()
    reserver_Checkbutton = Checkbutton(registration, onvalue=1, offvalue=0, variable=reserver_Var)
    reserver_Checkbutton.grid(row=1, column=6)

    # registration.geometry("1300x600-300+150")
    registration.resizable(False, False)

    save_Button = Button(registration, text="Зберегти", height=3, command=lambda:
    save_info("civil" if type_Var.get() == 0 else "military", name_Entry, surname_Entry, patronymic_Entry, birth_day_Entry, birth_month_Entry, birth_year_Entry,
              height_Entry, weight_Entry, index_Entry, state_Entry, district_Entry, city_Entry, street_Entry,
              home_num_Entry, phone_num_Entry, civil_occupation_Entry, military_speciality_Entry,
              education_Entry, rank_Entry, rank_assign_day_Entry, rank_assign_month_Entry,
              rank_assign_year_Entry, position_Entry, subdivision_Entry, duty_form_Entry,
              character_note_Entry, attitude_to_duty_Entry, reserver_Var.get()))
    save_Button.grid(row=25, columnspan=7, sticky=N + E + S + W)

    registration.protocol("WM_DELETE_WINDOW", lambda: [main_win.deiconify(), registration.destroy()])

    registration.mainloop()


def main_window():
    global main_win
    main_win = Tk()
    main_win.geometry("300x300-800+350")
    main_win.title("База даних військовослужбовців")
    Label(main_win, text="Оберіть потрібну дію:").pack()
    Button(main_win, text="Відкрити список", command=lambda: [main_win.withdraw(), list_Toplevel()]).pack()
    Button(main_win, text="Зареєструвати", command=lambda: [main_win.withdraw(), registration_Toplevel()]).pack()
    Button(main_win, text="Мобілізаційні списки", command=lambda: [main_win.withdraw(), mobilization_Toplevel()]).pack()
    main_win.protocol("WM_DELETE_WINDOW", lambda: [main_win.destroy(), db.save()])
    main_win.mainloop()


def secure_shell(showed_msg: bool):
    global secure_shell_win
    secure_shell_win = Tk()
    secure_shell_win.title("Виправлення помилок")
    if not showed_msg:
        secure_shell_win.iconify()
        if messagebox.showinfo("Попередження",
                               "У ході зчитування даних виникли помилки, тому вас було перенаправлено сюди. "
                               "Вам потрібно буде переглянути рядки з помилками й усунути їх. Після завершення"
                               " перезапустіть програму."):
            secure_shell_win.deiconify()

    secure_shell_win.geometry("-300+150")

    wrong_line = db.database[db.error_index]
    global line_to_be_changed
    line_to_be_changed = wrong_line
    try:
        line_to_be_changed = re.findall("\[(.*?)]", db.database[db.error_index])
    except Exception:
        db.delete_line(db.database[db.error_index])
    listbox = Listbox(secure_shell_win, width=50, height=20)
    for param in line_to_be_changed:
        listbox.insert(END, param)
    listbox.pack()
    select_Button = Button(secure_shell_win, text="Вибрати", command=lambda:
    secure_shell_editing_Toplevel(listbox.curselection()[0]))
    select_Button.pack()
    save_Button = Button(secure_shell_win, text="Зберегти і вийти", command=lambda:
    [secure_shell_win.destroy(), db.save_after_error(wrong_line)])
    save_Button.pack()
    secure_shell_win.mainloop()


def change_wrong_line_value(id, value):
    line_to_be_changed[id] = value
    db.database[db.error_index] = convert_regex_to_line(line_to_be_changed)


def secure_shell_editing_Toplevel(id):
    showed_msg = True
    secure_shell_editing_Top = Toplevel(secure_shell_win)
    secure_shell_editing_Top.title("Редагування")
    secure_shell_editing_Top.geometry("500x200")
    editing_Entry = Entry(secure_shell_editing_Top, width=70)
    editing_Entry.insert(END, line_to_be_changed[id])
    editing_Entry.pack()
    save_Button = Button(secure_shell_editing_Top, text="Зберегти", command=lambda:
    [change_wrong_line_value(id, editing_Entry.get()), secure_shell_editing_Top.destroy(), secure_shell_win.destroy(),
     secure_shell(True)])
    save_Button.pack()
    secure_shell_editing_Top.mainloop()


def mobilization_new_file_Toplevel():
    global mobilization_params
    mobilization_params = []
    mobilization_new_file_Top = Toplevel()
    mobilization_new_file_Top.title("Створення нового списку")
    mobilization_new_file_Top.geometry("500x700-700+150")

    Label(mobilization_new_file_Top, text="Введіть назву файлу:").grid(row=0, column=0, sticky=W)
    mobilization_name_Entry = Entry(mobilization_new_file_Top)
    mobilization_name_Entry.grid(row=0, column=1, columnspan=3, padx=10)

    Label(mobilization_new_file_Top, text="Введіть обмеження по віку:").grid(row=2, column=0, sticky=W)
    mobilization_min_age_Entry = Entry(mobilization_new_file_Top, width=5)
    mobilization_min_age_Entry.grid(row=2, column=1)
    Label(mobilization_new_file_Top, text="-").grid(row=2, column=2)
    mobilization_max_age_Entry = Entry(mobilization_new_file_Top, width=5)
    mobilization_max_age_Entry.grid(row=2, column=3)

    Label(mobilization_new_file_Top, text="Введіть назву підрозділу:").grid(row=3, column=0, sticky=W)
    mobilization_subdivision_Entry = Entry(mobilization_new_file_Top)
    mobilization_subdivision_Entry.grid(row=3, column=1, columnspan=3, padx=10)

    Label(mobilization_new_file_Top, text="Введіть кількість людей:").grid(row=4, column=0, sticky=W)
    mobilization_amount_Entry = Entry(mobilization_new_file_Top, width=8)
    mobilization_amount_Entry.grid(row=4, column=1, columnspan=3, padx=10, sticky=W)

    mob_reserver_var = IntVar()

    Label(mobilization_new_file_Top, text="Брати людей з запасу?").grid(row=5, column=0, sticky=W)
    mobilization_reserver_Checkbutton = Checkbutton(mobilization_new_file_Top, offvalue=0, onvalue=1,
                                                    variable=mob_reserver_var)
    mobilization_reserver_Checkbutton.grid(row=5, column=1, padx=10, sticky=W)

    Label(mobilization_new_file_Top, text="Примітки щодо списку:").grid(row=6, column=0, sticky=W)
    mobilization_notes_Text = Text(mobilization_new_file_Top, width=20, height=10)
    mobilization_notes_Text.grid(row=6, column=1, columnspan=20, padx=10, sticky=W)

    mobilization_enter_Button = Button(mobilization_new_file_Top, text="Сформувати список", command=lambda:
    [create_mobilization_list(mobilization_name_Entry.get(), mobilization_min_age_Entry.get(),
                             mobilization_max_age_Entry.get(), mobilization_subdivision_Entry.get(),
                             mobilization_amount_Entry.get(),   mob_reserver_var.get(), mobilization_notes_Text.get("1.0", "end-1c")),
     mobilization_new_file_Top.destroy()]
    if isinstance(int(mobilization_min_age_Entry.get()), int) and isinstance(int(mobilization_max_age_Entry.get()), int)
       and isinstance(int(mobilization_amount_Entry.get()), int) and mobilization_name_Entry.get() != "" and
    int(int(mobilization_amount_Entry.get()) > 0) else show_error("Перевірте правильність введени даних"))
    mobilization_enter_Button.grid(row=7, column=0, columnspan=4, rowspan=3, sticky=N+E+S+W)

    Button(mobilization_new_file_Top, text="Підказки щодо вводу", command=lambda:
    messagebox.showinfo("Підказка", "Поля з назвою списку, віком і кількістю - обов'язкові до заповнення. "
                                    "Якщо ви залишите решту полів пустими, то це означатиме, що фільтр просто не застовується. "
                                    "Заборонені символи - [ ] \\n. "
                                    "Заборонено створювати новий рядок.")).grid(columnspan=4, sticky=N+E+S+W)

    mobilization_new_file_Top.protocol("WM_DELETE_WINDOW", lambda: [mobilization_new_file_Top.destroy(),
                                                                    mobilization_Top.destroy(), mobilization_Toplevel(True)])
    mobilization_new_file_Top.mainloop()


def create_mobilization_list(name, min_age, max_age, subdivision, amount, reservers, notes):
    min_age, max_age = int(min_age), int(max_age)
    if int(min_age) > int(max_age):
        min_age, max_age = max_age, min_age
        min_age = int(min_age)
        max_age = int(max_age)

    added_persons = 0
    mobil_persons_list = []
    if reservers:
        for person in db.persons:
            if min_age <= int(getattr(person, "age")) <= max_age and subdivision.lower() in getattr(person, "subdivision").lower():
                if person.type() == "Civil":
                    if getattr(person, "reserver").lower() in ["так", "yes", "+", "true", "1"]:
                        added_persons += 1
                        mobil_persons_list.append(person)
                else:
                    added_persons += 1
                    mobil_persons_list.append(person)
            if added_persons == int(amount):
                break
    else:
        for person in db.persons:
            if min_age <= int(getattr(person, "age")) <= max_age and subdivision.lower() in getattr(person, "subdivision").lower():
                added_persons += 1
                mobil_persons_list.append(person)
            if added_persons == int(amount):
                break

    with open(f"./{name}.txt", "w+") as mobil_list:
        mobil_list.write("#")
        for mobil_param in [name, min_age, max_age, subdivision, reservers, notes]:
            mobil_list.write(f"[{mobil_param}]\t")
        mobil_list.write("\n")
        for mobil_person in mobil_persons_list:
            mobil_list.write(mobil_person.str() + "\n")

    mobilization_Top.deiconify()


def mobilization_Toplevel(asked=False):
    global mobilization_Top
    mobilization_Top = Toplevel(main_win)
    mobilization_Top.protocol("WM_DELETE_WINDOW", lambda: [main_win.deiconify(), mobilization_Top.destroy()])
    mobilization_Top.iconify()
    mobilization_Top.geometry("700x500-600+300")
    mobilization_Top.title("Мобілізаційні списки")
    if not asked:
        if messagebox.askyesno("Файл збереження даних", "Бажаєте створити новий файл з даними мобілізації?",
                               parent=mobilization_Top):
            mobilization_new_file_Toplevel()

    try:
        filename = filedialog.askopenfilename(parent=mobilization_Top)
    except Exception:
        mobilization_Top.destroy()
        main_win.deiconify()
    try:
        mobil_db = Database(filename)
    except Exception:
        mobilization_Top.destroy()
        main_win.deiconify()
    mobil_Listbox = Listbox(mobilization_Top, width=70)
    for person in mobil_db.persons:
        mobil_Listbox.insert(END, person.__str__() + " " + person.number)
    mobil_Listbox.pack()
    mobilization_select_Button = Button(mobilization_Top, text="Вибрати", command=lambda:
    mobil_user_info_Toplevel(mobilization_Top, mobil_Listbox.curselection()[0], mobil_db))
    mobilization_select_Button.pack()
    mobilization_Top.deiconify()
    mobilization_Top.mainloop()


def mobil_user_info_Toplevel(master, id, mobil_db):
    mobil_user_info_Top = Toplevel(master)
    mobil_user_info_Top.title("Дані")
    mobil_user_info_Top.geometry("500x600")
    person = mobil_db.persons[id]
    regex = re.findall("\[(.*?)]", person.str())
    regex.remove(regex[0])
    mobil_user_info_Listbox = Listbox(mobil_user_info_Top)
    for element in regex:
        mobil_user_info_Listbox.insert(END, element)

    mobil_user_info_Listbox.pack()
    user_info_exit_Button = Button(mobil_user_info_Top, text="Вихід", command=lambda: mobil_user_info_Top.destroy())
    user_info_exit_Button.pack(fill=BOTH)
    mobil_user_info_Top.mainloop()


if __name__ == "__main__":
    global db
    tempWin = Tk()
    tempWin.withdraw()
    db = Database(filedialog.askopenfilename())
    tempWin.destroy()
    if db.error:
        secure_shell(False)
    else:
        main_window()
