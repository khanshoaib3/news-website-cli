import json
import requests
from requests.structures import CaseInsensitiveDict
import account
from terminal_utils import bcolors, clearConsole, getTerminalSize
import posts
import threading
from keyboard_util import keyboardDisable
from time import sleep
import os
import sys
import subprocess
import webbrowser

token = ""

def main():
    t = threading.Thread(target=menu)
    t.start()
    value = 0
    if value == "1":
        clearConsole()
        username = str(input(f"{bcolors.OKBLUE}Enter username:{bcolors.ENDC}\n"))
        password = str(input(f"{bcolors.OKBLUE}Enter password:{bcolors.ENDC}\n"))
        account.login(username,password)
    elif value == "2":
        clearConsole()
        print(f"{bcolors.OKGREEN}1: All posts")
        print(f"2: Post by user")
        print(f"3: Single post")
        value = str(input(f"Enter your choice:{bcolors.ENDC}\n"))
        if(value == "1"):
            clearConsole()
            posts.allPosts()
        elif (value == "2"):
            clearConsole()

            if getToken() == "":
                username = str(input(f"{bcolors.OKBLUE}Enter username:{bcolors.ENDC}\n"))
                password = str(input(f"{bcolors.OKBLUE}Enter password:{bcolors.ENDC}\n"))
            #id = str(input(f"{bcolors.OKGREEN}Enter user id/token{bcolors.ENDC}\n"))
            posts.userPosts(''+getToken())
        elif (value == "3"):
            clearConsole()
            id = str(input(f"{bcolors.OKGREEN}Enter post id/token{bcolors.ENDC}\n"))
            posts.singlePost(id)

def getToken():
    if os.path.exists('.cred'):
        file = open('.cred','r')
        return ""+file.readline()
    else:
        return "notloggedin"

def setToken(newToken):
    file = open('.cred','w')
    file.write(""+newToken)

def menu():
    changed=True
    prevWidth, prevHeight = 0,0
    mainMenu = ["1 :- Account",  "2 :- News", "e/exit :- Exit"]
    accountLIMenu = ["1 :- Sign IN",  "2 :- Sign UP", "b :- Back","e/exit :- Exit"]
    accountMenu = ["1 :- Info",  "2 :- Log Out", "b :- Back","e/exit :- Exit"]
    postMenu = ["1 :- New Post",  "2 :- List Posts", "3 :- Your Posts", "b :- Back","e/exit :- Exit"]
    currentMenu = mainMenu

    while True:
        string = ""
        (width,height) = getTerminalSize()
        height = height-1

        if prevWidth!=width or prevHeight!=height:
            changed=True
            prevWidth = width
            prevHeight = height
        midH = int(height/2)
        midW = int(width/2)

        if changed:
            changed = False
            choice = printMenu(width=width, height=height, midW=midW, midH=midH, strList=currentMenu, message="Enter your choice: ")
            if choice is not None or choice != "":
                changed = True
                if choice == "e" or choice == "exit":
                    sys.exit()
                elif choice == "1" and currentMenu == mainMenu:
                    currentMenu = accountLIMenu
                    if getToken() != 'notloggedin':
                        currentMenu = accountMenu
                elif choice == "2" and currentMenu == mainMenu:
                    currentMenu = postMenu
                elif choice == "b" and (currentMenu==accountMenu or currentMenu==postMenu or currentMenu==accountLIMenu):
                    currentMenu = mainMenu
                elif currentMenu == accountLIMenu:
                    if choice == "1":
                        question = ["Enter your username below"]
                        username = printMenu(width=width, height=height, midW=midW, midH=midH, strList=question, message="")
                        question = ["Enter your password below"]
                        password = printMenu(width=width, height=height, midW=midW, midH=midH, strList=question, message="")
                        mesg = ["Loading..."]
                        printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg)
                        status = account.login(username,password)
                        mesg = [""+status]
                        printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg)
                        sleep(3)
                        currentMenu = accountMenu
                    elif choice == "2":
                        question = ["Enter your email below"]
                        email = printMenu(width=width, height=height, midW=midW, midH=midH, strList=question, message="Email: ")

                        question = ["Enter your username below"]
                        username = printMenu(width=width, height=height, midW=midW, midH=midH, strList=question, message="Username: ")

                        checker = False
                        question = ["Enter your password below"]
                        while not checker:
                            password = printMenu(width=width, height=height, midW=midW, midH=midH, strList=question, message="Password: ")
                            checker = validatePassword(password)
                            if not checker:
                                question = ["Password must:-","1: be atleast 8 char long", "2: contain a alphabet", "3: contain a special character", "4: contain a number"]

                        checker = False
                        question = ["Confirm password below"]
                        while not checker:
                            c_password = printMenu(width=width, height=height, midW=midW, midH=midH, strList=question, message="Confirm pasword: ")
                            if password == c_password:
                                checker = True
                            else:
                                question = ["Password don't match"]


                        question = ["Enter your name below"]
                        name = printMenu(width=width, height=height, midW=midW, midH=midH, strList=question, message="Name: ")

                        mesg = ["Loading..."]
                        printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg)

                        status = account.signup(email=email, username=username, password=password, c_password=c_password, name=name)
                        mesg = [""+status]
                        printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg)

                        sleep(3)
                        currentMenu = accountMenu


                elif currentMenu == accountMenu:
                    if choice == "2":
                        account.logout()
                        mesg = ["Logged Out Successfully"]
                        printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg)
                        sleep(3)
                        currentMenu = accountLIMenu

                elif currentMenu == postMenu:
                    if choice == "2":
                        mesg = ["Loading..."]
                        printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg)
                        data = posts.allPosts()
                        printMultiplePosts(width=width, height=height, midW=midW, midH=midH,data=data)
                    elif choice == "3":
                        mesg = ["Loading..."]
                        printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg)
                        token = getToken()
                        data = posts.userPosts(token)
                        printMultiplePosts(width=width, height=height, midW=midW, midH=midH,data=data)


def printMenu(width, height, midW, midH, strList, message=None):
    clearConsole()
    i = 0
    strLen = len(strList)
    for x in range(height-1):
        if x==0 or x==height-2:
            print(bcolors.ENDC + "+" + ("-"*(width-2)) + "+")
        elif x>=midH-(strLen/2) and x<=midH+(strLen/2) and strLen%2==1:
            string = strList[i]
            i = i+1
            print(bcolors.ENDC + "|" + (" "*int(midW-(len(string)/2) - int(len(string)%2==0))) + string  + (" "*int(midW-(len(string)/2) - int(width%2==0) )) + "|")
        elif x>=midH-(strLen/2)+1 and x<=midH+(strLen/2) and strLen%2==0:
            string = strList[i]
            i = i+1
            print(bcolors.ENDC + "|" + (" "*int(midW-(len(string)/2) - int(len(string)%2==0))) + string  + (" "*int(midW-(len(string)/2) - int(width%2==0) )) + "|")
        else:
            print(bcolors.ENDC + "|" + (" "*(width-2)) + "|")

    if message is not None:
        choice = str(input(message))
        return choice

def validatePassword(password):
    if len(password) >= 8:
        specialCharachter = 0
        number = 0
        word = 0
        for x in password:
            if x=='!' or x=='@' or x=='#' or x=='^' or x=='&' or x=='*' or x=='#' or x=='(' or x==')' or x=='-' or x=='_' or x=='=' or x=='+' or x=='{' or x=='}' or x=='[' or x==']' or x=='|' or x=='\\' or x==';' or x==':' or x=='\'' or x=='"' or x=='<' or x=='>' or x==',' or x=='.' or x=='/' or x=='?' :
                specialCharachter = specialCharachter + 1
            if x>='0' and x<='9' :
                number = number + 1
            if (x>='a' and x<='z') or (x>='A' and x<='Z'):
                word = word + 1
        if specialCharachter > 0 and word > 0 and number > 0 :
            return True
        return False

def printSinglePost(width, height, midW, midH, postId, isAuthor=False):
    printMenu(width=width, height=height, midW=midW, midH=midH, strList=["Loading..."])
    data = posts.singlePost(postId)
    minimalData = []
    minimalData.append('Title: '+data[0][1])
    minimalData.append('Slug: '+data[0][2])
    minimalData.append('Status: '+data[0][9])
    minimalData.append('Created on: '+data[0][7])
    minimalData.append('Updated on: '+data[0][8])
    minimalData.append('Published on: '+data[0][6])
    if isAuthor:
        minimalData.append('i:- Edit Post')
    minimalData.append('o:- Open in browser')
    minimalData.append('b:- Back')
    minimalData.append('e/exit:- Exit')
    while True:
        mesg = minimalData
        choice = printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg, message="Enter your choice: ")
        if choice == "b":
            break
        elif choice == "e" or choice == "exit":
            sys.exit()
        elif choice == "o":
            publish = data[0][6]+""
            publish = publish[:publish.find('T')]
            publish = publish.split('-')
            year = publish[0]
            month = publish[1]
            day = publish[2]
            slug = data[0][2]
            url = f"https://blindcraft.pythonanywhere.com/news/{year}/{month}/{day}/{slug}"
            if sys.platform=='win32':
                os.startfile(url)
            elif sys.platform=='darwin':
                subprocess.Popen(['open', url])
            else:
                try:
                    subprocess.Popen(['xdg-open', url])
                except OSError:
                    webbrowser.open_new(url)
        elif isAuthor and choice == 'i':
            pass


def printMultiplePosts(width, height, midW, midH,data):
    totalPosts = len(data)
    pages = int(len(data)/6)
    paginatedData = []
    postsInPage = []
    j = 0
    try:
        for i in range(pages+1):
            newData = []
            postNumbers = []
            for k in range(5):
                newData.append(str(k+1)+": "+data[j][1])
                postNumbers.append(str(k+1))
                j = j+1
                if j>=totalPosts:
                    break
            if i<pages:
                newData.append("n :- Next Page")
            if i>0:
                newData.append("p :- Previous Page")
            newData.append("b :- Back")
            newData.append("e/exit :- Exit")
            paginatedData.append(newData)
            postsInPage.append(postNumbers)
    except:
        newData = []
        newData.append("No Posts")
        newData.append("b :- Back")
        newData.append("e/exit :- Exit")
        paginatedData.append(newData)
        postsInPage = None
        pages = 0
    currentPage = 0

    while True:
        mesg = paginatedData[currentPage]
        choice = printMenu(width=width, height=height, midW=midW, midH=midH, strList=mesg, message="Enter your choice: ")
        if choice == "b":
            break
        elif choice == "e" or choice == "exit":
            sys.exit()
        elif choice == "n":
            currentPage += 1
            if currentPage >= pages:
                currentPage = pages
        elif choice == "p":
            currentPage -= 1
            if currentPage <= 0:
                currentPage = 0
        elif postsInPage is not None:
            if choice in postsInPage[currentPage]:
                postIndex = ((currentPage*5) + int(choice))-1
                printSinglePost(width=width, height=height, midW=midW, midH=midH, postId=data[postIndex][0])

if __name__ == "__main__":
    main()
