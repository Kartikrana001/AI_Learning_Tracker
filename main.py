topics=[]
def add():
        new_topic=input("Enter the topic: ")
        progress= float(input("Enter how much percent it is complete: "))
        topics.append({"topic": new_topic,"progress": progress})
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

