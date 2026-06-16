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
def updt_progress():
     topic_find=input("Enter the topic : ")
     for topic in topics:
        if topic["topic"] == topic_find:
            new_progress=float(input("Enter the new progress :"))
            topic["progress"] = new_progress
            with open("topics.txt","w") as file :
                for topic in topics:
                    file.write(f"{topic['topic']},{topic['progress']}\n")         
            print("progress updated...")
            return
     print("topic not found...")

while True:
    print("=====AI LEARNING TRACKER=====\n\nADD TOPIC        : 1\nVIEW TOPIC       : 2\nUPDATE PROGRESS  : 3\nEXIT             : 4")
    user_choise = input("Enter your choise: ")
    if   user_choise == "1":
        add()
    elif user_choise == "2":
        view_topics()
    elif user_choise == "3":
        updt_progress()
    elif user_choise == "4":
        break
    else:
         print("invelic choice...")

