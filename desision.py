def determine_winner(user_choice, ai_choice):
    if user_choice == ai_choice:
        return 0
    elif (user_choice == 1 and ai_choice == 3) or \
         (user_choice == 3 and ai_choice == 2) or \
         (user_choice == 2 and ai_choice == 1):
        return 1
    else:
        return 2
    