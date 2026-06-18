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
        if topic["topic"].lower() == topic_find.lower():
            new_progress=float(input("Enter the new progress :"))
            topic["progress"] = new_progress
            with open("topics.txt","w") as file :
                for topic in topics:
                    file.write(f"{topic['topic']},{topic['progress']}\n")         
            print("progress updated...")
            return
     print("topic not found...")
def delete_topic():
     del_topic= input("Enter the topic to be deleted :")
     for topic in topics:
        if topic["topic"].lower() == del_topic.lower():
            topics.remove(topic)
            with open("topics.txt","w") as file:
                for topic in topics:
                    file.write(f"{topic['topic']},{topic['progress']}\n")
            print("topic deleted successfully...")
            return
     print("topic not found...")
def statistics():
    if len(topics) == 0:
        print("No topic found...")
        return
    total_topic = len(topics)
    print("total topics : ",total_topic)
    total_progress = 0
    for topic in topics:
        total_progress += topic['progress']
    average = total_progress/len(topics)
    print(f"AVERAGE PROGRESS :{average}%")
while True:
    print("=====AI LEARNING TRACKER=====\n\nADD TOPIC        : 1\nVIEW TOPIC       : 2\nUPDATE PROGRESS  : 3\nDELETE TOPIC     : 4\nSTATISTICS       : 5\nEXIT             : 6")
    user_choice = input("Enter your choise: ")
    if   user_choice == "1":
        add()
    elif user_choice == "2":
        view_topics()
    elif user_choice == "3":
        updt_progress()
    elif user_choice == "4":
        delete_topic()
    elif user_choice == "5":
        statistics()
    elif user_choice == "6":
        break
    else:
         print("invelic choice...")

