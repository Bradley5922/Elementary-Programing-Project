import matplotlib as plot
import PySimpleGUI as gui 
import csv

# init data array
data = []

# open data file and store as array of items
file = open("clean_penguins.csv", "r")
reader = csv.reader(file)
arrayForm = list(reader)

for data_RAW in arrayForm:
    # ignore first row, as they are column
    # this code could be adapted to use the column names to create the structured list
    if data_RAW[0] == "id":
        continue # skip to next loop

    # Fetch and cast all the data
    id = int(data_RAW[0])
    species = str(data_RAW[1])
    bill_length_mm = float(data_RAW[2])
    bill_depth_mm = float(data_RAW[3])
    flipper_length_mm = float(data_RAW[4])
    body_mass_g = float(data_RAW[5])

    # format data into a dictionary for easy access later
    structured_data = {
        "id": id,
        "species": species,
        "bill_length_mm": bill_length_mm,
        "bill_depth_mm": bill_depth_mm,
        "flipper_length_mm": flipper_length_mm,
        "body_mass_g/100": body_mass_g
    }

    # Add structured data (dic) to the list
    data.append(structured_data)

# for item in data:
#     print(item)

# GUI
# References made from the documentation, but that should be obvious
gui.theme("DarkGreen3")

def mainPage():
    mainPageContent = [[gui.Column(
                            [[gui.Text("Penguin Attribute Analysis", font=("Helvetica", 40))],
                            [gui.Button("Display Via ID", font=("Helvetica", 25)), gui.Button("Show Charts", font=("Helvetica", 25))],
                            [gui.Button("Exit", font=("Helvetica", 25), button_color="red")]], 
                        element_justification="c")]]


    return gui.Window("Penguin Attribute Analysis", mainPageContent, finalize=True)

def byIdPage():
    viaIdContent = [[gui.Text("View All Data", font=("Helvetica", 40))],
                    [gui.Column([
                        [gui.Text("Search By ID:", font=("Helvetica", 15))],
                        [gui.In(key="IdSearch", font=("Helvetica", 20), size=(21)), gui.Button("Search", font=("Helvetica", 20), button_color="green")],
                        [gui.Listbox(data, key="ScrollableList", size=(36, 15), font=("Helvetica", 15), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)]], 
                    element_justification="left"), 
                    gui.Column([
                        [gui.Text("Output:", font=("Helvetica", 15))],
                        [gui.Output(key='Output', font=("Helvetica", 20), size=(30, 10))]],
                    element_justification="left", vertical_alignment="top")], 
                    [gui.VPush()],
                    [gui.Button("Back", font=("Helvetica", 25), button_color="red", size=10)]]

    return gui.Window("PAA - By ID", viaIdContent, finalize=True)


mainPageWindow, viaIdWindow = mainPage(), None

while True:
    window, event, values = gui.read_all_windows()
    # print(window, event, values)

    # Relevent for all windows
    if (event == gui.WIN_CLOSED) or (event == "Exit"): # if exit button or window x button used
        break
    if (event == "Back"):
        viaIdWindow.close()
        # mainPageWindow.close()
        mainPageWindow = mainPage()
    
    # Main Page Window
    if (event == "Display Via ID"):
        mainPageWindow.close()
        viaIdWindow = byIdPage()

    # By ID window
    if (event == "Search"):
        valueWanted = int(values['IdSearch'])

        viaIdWindow['Output'].Update('')
        viaIdWindow['ScrollableList'].Update(set_to_index=[valueWanted-1], scroll_to_index=valueWanted-1)
        print("Value Entered: " + str(valueWanted))
        print(data[valueWanted])


window.close()