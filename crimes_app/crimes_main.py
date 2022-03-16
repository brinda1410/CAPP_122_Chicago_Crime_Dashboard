import crimes_app
from crimes_app import data_collection

'''
This is an application module that allows a user to select to download data
from the Chicago Data Portal through an API, and then run the application.
'''

MENU = '''
********* Crime Visualization Module *********
Welcome to the crime visualization application! Please choose
an option to perform a task.
(1) Update Data from Source
(2) Open the visualizations
(3) Quit the program
'''
START = 1
END = 3

def retrieve_task():
    option = -1
    while True:
        print(MENU)
        option = int(input("Option: "))
        if option >= START and option <= END:
            break
        else:
            print(f"Invalid option({option})")
    return option

OPTIONS_HANDLER = {
    1: lambda: update_data(),
    2: lambda: run_app()
}

def update_data():
    import crimes_app.data_collection.api_collection
    import crimes_app.data_collection.join_data

def run_app():
    import crimes_app.dashboard.app

def main():
    while True:
        option = retrieve_task()
        if option == 3:
            break
        else:
            handler = OPTIONS_HANDLER[option]
            handler()

if __name__ == "__main__":
    main()