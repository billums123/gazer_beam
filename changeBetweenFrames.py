def change_to_select_difficulty():
    #changes frame, forget() hidesframe, pack() shows frame
    select_song_menu_frame2.forget()
    select_difficulty_frame3.pack(fill='both', expand=1)


def change_to_select_song():
    select_song_menu_frame2.pack(fill='both', expand=1)
    select_difficulty_frame3.forget()