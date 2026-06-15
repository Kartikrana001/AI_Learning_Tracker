topics=[]
try:
    with open("topics.txt","r") as file:
        lines = file.readlines()
    for line in lines:
        topic,progress= line.strip().split(",")
        topics.append(({"topic":topic,"progress": float(progress)}))
except FileNotFoundError:
     print("previous data is not present...")
def add():
        new_topic=input("Enter the topic: ")
        progress= float(input("Enter how much percent it is complete: "))
        topics.append({"topic": new_topic,"progress": progress})
        with open("topics.txt","a") as file:
            file.write(f"{new_topic},{progress}\n")
def view_topics():
    if len(topics) == 0:
             print("No topic found...")
    else:
        for item in topics:
            print(item["topic"], "-", item["progress"], "%")
while True:
    print("=====AI LEARNING TRACKER=====\n\nADD TOPIC  : 1\nVIEW TOPIC : 2\nEXIT       : 3")
    user_choise = int(input("Enter your choise: "))
    if user_choise == 1:
        add()
    elif user_choise == 2:
        view_topics()
    elif user_choise == 3:
        break
    else:
         print("invelic choice...")

