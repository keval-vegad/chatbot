import BookTicket as bt
import Contingency as C


def start_main_chat():
    selection = get_input()
    if selection == 1:
        # handle_option1()
        print("1")
        object_BookTicket = bt.BookTicket()
        object_BookTicket.start_chat()
    elif selection == 2:
        # handle_option2()
        print("2")

    elif selection == 3:

    #     # some = code + that
    #     # [does(something) for something in range(0, 3)]
        print("3")
        object_Contingency = C.Contingency()
        object_Contingency.start_chat()
    # else:
    #     # print("3")
    #     break

def get_input():
    print("1. book a ticket"),
    # print("\n"),
    print("2. check for delay"),
    # print("\n"),
    print("3. check for contingency plan"),
    # print("\n"),
    print("0. for exit")
    user_selection = int(input("Please select from above options: "))
    if user_selection not in range(0,4):
        print("Please select valid options ")
    else:
        return user_selection

if __name__ == '__main__':
    start_main_chat()
