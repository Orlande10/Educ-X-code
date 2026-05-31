from storage import read_data, write_data

def run_quiz():
    data = read_data()
    
    questions = data.get("questions", [])
    
    user = data.get("user", {})
    
    if not user.get("name"): 
        user["name"] = input("Enter your name: ")
        
        score = 0
        
        for q in questions: 
            print("/n" + q["question"])
            answer = input("Your Answer : ")
            
            if answer.lower() == q["answer"].lower():
                print("Correct!")
                score += 1
            else:
                print("Wrong!")
                
                print(f"\nFinal score: {score}/ {len(questions)}")
                
                user["score"] = score
                user["history"].append(score)
                
                data["user"] = user
                
                write_data(data)
                print("Data saved")
                
                if __name__ == "__main__":
                    run_quiz()
                