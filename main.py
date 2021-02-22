#This will be the file to run
from Pages import HomePage
from Pages.HomePage import HomePage
from Pages.JsonFiles.LoadUserData import LoadUserData


def main():
    user = LoadUserData.loadUserData()  #load user object
    HomePage.openHomePage()


if __name__ == "__main__":
    main()