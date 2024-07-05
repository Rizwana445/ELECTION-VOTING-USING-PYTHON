import mysql.connector
from datetime import datetime

# Establish database connection
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="election_db"
    )
    mycursor = mydb.cursor()
    print("Connected to MySQL database")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

# Define the list of valid candidates
valid_candidates = ["Arun", "Kalai", "Madhu", "Deepa", "Nazeer", "Akash"]

def insert_voterdata():
    try:
        sql = "INSERT INTO voter_details (voter_name, aadhaar_no, date_of_birth, voter_id_no, mobile_no, email_id) VALUES (%s, %s, %s, %s, %s, %s)"
        
        voter_name = input("Enter voter name: ")
        aadhaar_no = input("Enter your Aadhaar number: ")

        if not aadhaar_no.isdigit() or len(aadhaar_no) != 12:
            print("Aadhaar number must be a 12-digit number")
            return
        else:
            aadhaar_no = int(aadhaar_no)  # Convert to integer after validation

        date_of_birth_str = input("Enter date of birth (YYYY-MM-DD): ")
        try:
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        except ValueError:
            print("Incorrect date format, should be YYYY-MM-DD")
            return
        
        # Calculate age
        today = datetime.today().date()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        
        if age < 18:
            print("You cannot vote. You must be at least 18 years old to register.")
            return
        else:
            print("You can vote")    
        voter_id_number = input("Enter your voter ID number: ")
        mobile_no = input("Enter mobile number: ")
        email_id = input("Enter email ID: ")
        
        val = (voter_name, aadhaar_no, date_of_birth, voter_id_number, mobile_no, email_id)
        mycursor.execute(sql, val)
        mydb.commit()  # Committing the transaction
        print("\nVoter data saved successfully")

    except mysql.connector.Error as err:
        mydb.rollback()  # Rollback the transaction if there's an error
        print(f"Error: {err}")

def insert_vote_data():
    try:
        # Input from user
        voter_name = input("Enter voter name: ")
        voting_candidate = input("Enter the candidate's name you are voting for: ")

        # Check if the voting candidate is in the valid candidates list
        if voting_candidate not in valid_candidates:
            print(f"Candidate {voting_candidate} is not in the valid candidates list.")
            return

        # Specify the voting date (for example)
        voting_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert vote details into vote_details table
        sql_insert_vote = "INSERT INTO vote_details (voter_name, candidate_name, voting_date) VALUES (%s, %s, %s)"
        val_insert_vote = (voter_name, voting_candidate, voting_date_str)
        mycursor.execute(sql_insert_vote, val_insert_vote)

        # Update vote_count in candidates table
        sql_update_vote_count = "UPDATE candidates SET vote_count = vote_count + 1 WHERE candidate_name = %s"
        val_update_vote_count = (voting_candidate,)
        mycursor.execute(sql_update_vote_count, val_update_vote_count)

        mydb.commit()  # Committing the transaction
        # Print success message with voting details
        print("\nVote data saved successfully")

    except mysql.connector.Error as err:
        mydb.rollback()  # Rollback the transaction if there's an error
        print(f"Error: {err}")

def insert_candidate_and_vote(voting_candidate):
    try:
        # Insert candidate into candidates table (if not exists)
        sql_insert_candidate = "INSERT INTO candidates (candidate_name) VALUES (%s) ON DUPLICATE KEY UPDATE candidate_name=candidate_name"
        val_insert_candidate = (voting_candidate,)
        mycursor.execute(sql_insert_candidate, val_insert_candidate)

        # Increment vote_count for the candidate if it matches specific names
        if voting_candidate in valid_candidates:
            sql_update_vote_count = "UPDATE candidates SET vote_count = vote_count + 1 WHERE candidate_name = %s"
            val_update_vote_count = (voting_candidate,)
            mycursor.execute(sql_update_vote_count, val_update_vote_count)

        mydb.commit()  # Committing the transaction

    except mysql.connector.Error as err:
        mydb.rollback()  # Rollback the transaction if there's an error
        print(f"Error: {err}")

def print_voter_data():
    try:
        # Retrieve and print voter data
        sql_select_voter = "SELECT * FROM voter_details ORDER BY voter_id DESC LIMIT 1"
        mycursor.execute(sql_select_voter)
        result = mycursor.fetchone()
        if result:
            print("\nRecent Voter Data:")
            print(f"Voter Name: {result[1]}")
            print(f"Aadhaar Number: {result[2]}")
            print(f"Date of Birth: {result[3]}")
            print(f"Voter ID Number: {result[4]}")
            print(f"Mobile Number: {result[5]}")
            print(f"Email ID: {result[6]}")
        else:
            print("\nNo voter data found")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def print_vote_data():
    try:
        # Retrieve and print vote data
        sql_select_vote = "SELECT * FROM vote_details ORDER BY vote_id DESC LIMIT 1"
        mycursor.execute(sql_select_vote)
        result = mycursor.fetchone()
        if result:
            print("\nRecent Vote Data:")
            print(f"Voter Name: {result[1]}")
            print(f"Candidate Voted: {result[2]}")
            print(f"Voting Date: {result[3]}")
        else:
            print("\nNo vote data found")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def print_candidate_data():
    try:
        # Retrieve and print candidate data with vote counts
        sql_select_candidates = "SELECT * FROM candidates"
        mycursor.execute(sql_select_candidates)
        results = mycursor.fetchall()
        
        if results:
            print("\nCandidate Data:")
            for row in results:
                print(f"Candidate Name: {row[0]} | Vote Count: {row[1]}")
        else:
            print("\nNo candidate data found")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def print_voting_results():
    try:
        print("\nVoting Results:")
        # Retrieve and print candidate data with vote counts
        sql_select_candidates = "SELECT * FROM candidates ORDER BY vote_count DESC"
        mycursor.execute(sql_select_candidates)
        results = mycursor.fetchall()
        
        if results:
            for rank, row in enumerate(results, start=1):
                print(f"{rank}. Candidate Name: {row[0]} | Vote Count: {row[1]}")
        else:
            print("No voting results found")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def print_winning_candidate():
    try:
        sql_select_winner = "SELECT candidate_name, vote_count FROM candidates ORDER BY vote_count DESC LIMIT 1"
        mycursor.execute(sql_select_winner)
        result = mycursor.fetchone()

        if result:
            print(f"\nWinner: {result[0]} with {result[1]} votes")
        else:
            print("\nNo winner found")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def main():
    try:
        # Insert candidate names into candidates table
        candidate_names = valid_candidates
        
        for candidate_name in candidate_names:
            insert_candidate_and_vote(candidate_name)

        # Insert voter data
        insert_voterdata()

        # Insert vote data
        insert_vote_data()

        # Print voter data
        print_voter_data()

        # Print vote data
        print_vote_data()

        # Print candidate data
        print_candidate_data()
        # Print voting results and winning candidate
        print_voting_results()
        print_winning_candidate()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close cursor and database connection
        mycursor.close()
        mydb.close()
        print("\nDatabase connection closed.")

# Entry point of the script
print(f"ELECTION VOTING PROCESS")
main()
