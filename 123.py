from tkinter import *
from tkinter import ttk

my_window = Tk()
# frame_name = Frame(my_window)

my_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
           '12', '13', '14', '15', '16', '17', '18', '19', '20']
my_list2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
            '12', '13', '14', '15', '16', '17', '18', '19', '20']


# listbox_object = Listbox(my_window)
# listbox_object2 = Listbox(my_window)
# # listbox.pack()
# listbox_object.grid(row=0, column=1)
# listbox_object2.grid(row=0, column=3)
#
# scrollbar_object = Scrollbar(my_window)
# scrollbar_object2 = Scrollbar(my_window)
# # scrollbar.pack(side=RIGHT, fill=Y)
# scrollbar_object.grid(row=0, column=2, sticky='ns')
# scrollbar_object2.grid(row=0, column=4, sticky='ns')
#
# for item in my_list:
#     listbox_object.insert(END, item)
#
# for item in my_list2:
#     listbox_object2.insert(END, item)
#
# # attach listbox to scrollbar
# listbox_object.config(yscrollcommand=scrollbar_object.set)
# listbox_object2.config(yscrollcommand=scrollbar_object2.set)
# scrollbar_object.config(command=listbox_object.yview)
# scrollbar_object2.config(command=listbox_object2.yview)
# mainloop()


main_frame = Frame(my_window)
main_frame.grid(row=0, column=0, sticky="nswe")

left_frame = Frame(main_frame)
left_frame.grid(row=0, column=0, sticky="nswe")

# Button added just to see that there is a left frame, otherwise it will shrink
button_object = Button(left_frame, text="My Button")
button_object.grid(row=0, column=0)

right_frame = Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nswe")

listbox_object = Listbox(right_frame)
listbox_object2 = Listbox(right_frame)
listbox_object.grid(row=0, column=0)
listbox_object2.grid(row=0, column=2)

scrollbar_object = Scrollbar(right_frame)
scrollbar_object2 = Scrollbar(right_frame)
scrollbar_object.grid(row=0, column=1, sticky='ns')
scrollbar_object2.grid(row=0, column=3, sticky='ns')
mainloop()