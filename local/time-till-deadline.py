import datetime

user_input = input("Please enter your goal with a deadline separated by a colon\n")
input_list = user_input.split(":")

goal = input_list[0]
deadline = input_list[1]

deadline_date = datetime.datetime.strptime(deadline, "%d.%m.%Y")
today_date = datetime.datetime.today()

#calculation how many days from now till the deadline

time_till = deadline_date - today_date

print(f"Dear user! time remaining for your goal: {goal} is {time_till.days} days")