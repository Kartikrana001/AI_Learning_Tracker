import database
database.create_table()
# Show learning status
def statistics():
    topic_data = database.view_topics()
    if len(topic_data) == 0:
        print("data not found...")
        return
    sum_progress = 0
    completed_topic = 0
    for progress in topic_data:
        sum_progress += progress[2]
        if progress[2] == 100:
            completed_topic +=1
    average_progress = sum_progress/ len(topic_data)
    high_progress = topic_data[0]
    low_progress =  topic_data[0]
    for progress in topic_data:
        if high_progress[2] < progress[2]:
            high_progress =progress
        if low_progress[2] > progress[2]:
            low_progress = progress
    print(f"TOTAL TOPICS    : {len(topic_data)}")
    print(f"AVERAGE PROGRESS: {average_progress}")
    print(f"COMPLETED TOPIC : {completed_topic}")
    print(f"HIGHEST PROGRESS: {high_progress[1]} {high_progress[2]}")
    print(f"LOWEST PROGRESS : {low_progress[1]} {low_progress[2]}")

# Main menu loop
while True:
    print("=====AI LEARNING TRACKER=====\n\nADD TOPIC        : 1\nVIEW TOPIC       : 2\nUPDATE PROGRESS  : 3\nDELETE TOPIC     : 4\nSTATISTICS       : 5\nSEARCH TOPIC     : 6\nEXIT             : 7")
    user_choice = input("Enter your choise: ")
    if   user_choice == "1":
        topic = input("Enter the topic: ")
        progress = float(input("Enter the progress: "))
        database.add_topic(topic,progress)

    elif user_choice == "2":
        c = database.view_topics()
        for topic in c:
            print(f"{topic[0]} {topic[1]}: {topic[2]}%")
    elif user_choice == "3":
        topic = input("Enter the topic: ")
        progress = float(input("Enter the progress: "))
        database.update_topic(topic,progress)
    elif user_choice == "4":
        topic = input("Enter the topic: ")
        database.delete_topic(topic)
    elif user_choice == "5":
        statistics()

    elif user_choice == "6":
        topic = input("Enter the topic: ")
        print(database.search_topic(topic))
    elif user_choice == "7":
        break
    else:
         print("invelic choice...")

