from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import PySimpleGUI as gui 
import numpy as np
import matplotlib
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

def chartSelectionPage():
    chartSelectionContent = [[gui.Column(
                            [[gui.Text("Which Chart Type?", font=("Helvetica", 40))],
                            [gui.Button("Bar Chart Of Penguin", font=("Helvetica", 25)), gui.Button("Scatter Plot Of Attribute", font=("Helvetica", 25)), gui.Button("Scatter Plot Mean", font=("Helvetica", 25))],
                            [gui.Button("Back", font=("Helvetica", 25), button_color="red")]], 
                        element_justification="c")]]


    return gui.Window("PAA - Which Chart", chartSelectionContent, finalize=True)

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

def barChartPage():
    barChartContent = [[gui.Text("Bar Chart - Penguin", font=("Helvetica", 40))],
                    [gui.Column([
                        [gui.Text("Search By ID:", font=("Helvetica", 15))],
                        [gui.In(key="IdSearch", font=("Helvetica", 20), size=(21)), gui.Button("Search", font=("Helvetica", 20), button_color="green")],
                        [gui.Listbox(data, key="ScrollableList", size=(36, 15), font=("Helvetica", 15), select_mode="LISTBOX_SELECT_MODE_SINGLE", enable_events=True)],
                        [gui.ColorChooserButton("Bar Colour Chooser", font=("Helvetica", 20), target="colourText"), gui.In(key="colourText", visible=False, enable_events=True)]], 
                    element_justification="left"), 
                    gui.Column([
                        [gui.Text("Output:", font=("Helvetica", 15))],
                        [gui.Canvas(key='chatView')]],
                    element_justification="left", vertical_alignment="top")], 
                    [gui.VPush()],
                    [gui.Button("Back", font=("Helvetica", 25), button_color="red", size=10)]]

    return gui.Window("PAA - Bar Chart", barChartContent, finalize=True)

def scatterGraphPage():
    scatterGraphContent = [[gui.Text("Scatter Graph - Attribute", font=("Helvetica", 40))],
                            [gui.Canvas(key='scatterView')],
                            [gui.Text("Select 2 Attributes:", font=("Helvetica", 20))],
                            [gui.Combo(list(data[0].keys()), default_value='bill_length_mm', font=("Helvetica", 20), enable_events=True, key='a1')],
                            [gui.Combo(list(data[0].keys()), default_value='bill_depth_mm', font=("Helvetica", 20), enable_events=True, key='a2')],
                            [[gui.ColorChooserButton("Dot Colour Chooser", font=("Helvetica", 20), target="colourText"), gui.In(key="colourText", visible=False, enable_events=True)],
                            [gui.VPush()],
                            [gui.Button("Back", font=("Helvetica", 25), button_color="red", size=10)]]]

    return gui.Window("PAA - Scatter Graph", scatterGraphContent, finalize=True)

def scatterGraphMeanPage():
    keys = list(data[0].keys())
    keys.pop(0)
    keys.pop(0)

    scatterGraphMeanContent = [[gui.Text("Scatter Graph - Mean", font=("Helvetica", 40))],
                            [gui.Canvas(key='scatterView')],
                            [gui.Text("Select Attribute To Compare:", font=("Helvetica", 20))],
                            [gui.Combo(keys, default_value='bill_length_mm', font=("Helvetica", 20), enable_events=True, key='attributeNotMean')],
                            [[gui.ColorChooserButton("Dot Colour Chooser", font=("Helvetica", 20), target="colourText"), gui.In(key="colourText", visible=False, enable_events=True)],
                            [gui.VPush()],
                            [gui.Button("Back", font=("Helvetica", 25), button_color="red", size=10)]]]

    return gui.Window("PAA - Scatter Graph", scatterGraphMeanContent, finalize=True)



def dictToFormatedString(dict):
    finalString = ""
    
    for item in dict:
        if item == "id":
            continue
        
        semi_string = item.replace("_", " ").title() + ": " + str(dict[item]) + "\n"
        finalString += semi_string

    return finalString

def genrateBarChart(dictData, colour):
    print(dictData)

    fig = plt.figure(figsize=(7,4))
    
    plt.title(dictData["species"] + " - " + str(dictData["id"]))
    plt.xlabel("Attribute")
    plt.ylabel("Value")


    attributes = list(dictData.keys())
    values = list(dictData.values())

    attributes.pop(0)
    attributes.pop(0)

    values.pop(0)
    values.pop(0)

    for i in range(0, len(values)):
        values[i] =  int(values[i])

    plt.ylim([0, 240])
    plt.bar(attributes, values, color=colour, edgecolor='black')
 
    return fig

def genrateScatterChart(data, colour, a1, a2):

    fig = plt.figure(figsize=(7,4))

    plt.title("Comparison of: " + a1 + " & " + a2)
    plt.xlabel(a1)
    plt.ylabel(a2)

    a1Data = []
    a2Data = []
    
    for record in data:
        a1Data.append(record[a1])
        a2Data.append(record[a2])

    # americans can't spell grrr
    plt.scatter(a1Data, a2Data, color=colour) 

    return fig

def genrateScatterMeanChart(data, colour, aName):

    fig = plt.figure(figsize=(7,4))

    plt.title("Comparison of: " + aName + " & Mean")
    plt.xlabel(aName)
    plt.ylabel("Mean")

    ax = plt.axes()
    # next line is from stackoverflow cuz its so clean
    ax.plot([0,1],[0,1], transform=ax.transAxes)
    # limits graph to axes to reproduce brief's graph
    plt.ylim([0, 150])
    plt.xlim([0, 250])

    # americans can't spell grrr
    plt.scatter(data[0], data[1], color=colour) 

    return fig

# this function is from a demo piece of code for PySimpleGUI
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    
    return figure_canvas_agg



mainPageWindow, viaIdWindow, chartSelectionWindow, barChartWindow, scatterGraphWindow, scatterGraphMeanWindow = mainPage(), None, None, None, None, None
currentWindow = 0
currentColour = "#ff0000"

while True:
    allOtherWindows = [viaIdWindow, chartSelectionWindow, barChartWindow, scatterGraphWindow, scatterGraphMeanWindow]
    window, event, values = gui.read_all_windows()
    # print(event)
    # print(values)

    # Relevent for all windows
    if (event == gui.WIN_CLOSED) or (event == "Exit"): # if exit button or window x button used
        break
    if (event == "Back"):
        for window in allOtherWindows:
            try:
                window.close()
            except:
                print("trying to close all other windows")
            
        mainPageWindow = mainPage()
        currentWindow = 0
    
    # Main Page Window
    if (event == "Display Via ID"):
        mainPageWindow.close()
        viaIdWindow = byIdPage()
        currentWindow = 1

    # Chart selection window
    if (event == "Show Charts"):
        mainPageWindow.close()
        chartSelectionWindow = chartSelectionPage()
        currentWindow = 2
    
    if (event == "Bar Chart Of Penguin"):
        chartSelectionWindow.close()
        barChartWindow = barChartPage()
        currentWindow = 3

        fig_canvas_agg = draw_figure(barChartWindow['chatView'].TKCanvas, genrateBarChart(data[0], currentColour))

    if (event == "Scatter Plot Of Attribute"):
        chartSelectionWindow.close()
        scatterGraphWindow = scatterGraphPage()
        currentWindow = 4

        fig_canvas_agg = draw_figure(scatterGraphWindow['scatterView'].TKCanvas, genrateScatterChart(data, currentColour, "flipper_length_mm", "bill_depth_mm"))

    if (event == "Scatter Plot Mean"):
        chartSelectionWindow.close()
        scatterGraphMeanWindow = scatterGraphMeanPage()
        currentWindow = 5

        fig_canvas_agg = draw_figure(scatterGraphMeanWindow['scatterView'].TKCanvas, genrateScatterMeanChart([[1],[1]], currentColour, "None (Generate New Graph)"))

    # By ID window / Bar Chart
    if (event == "Search"):
        # Get value from input box
        # Validation, to make sure erroneous data isn't entered
        try:
            valueWanted = int(values['IdSearch'])
            print(currentWindow)

            # Clear output box and display data, select said data in scrollable list

            if currentWindow == 1:
                window['Output'].Update('')
                window['ScrollableList'].Update(set_to_index=[valueWanted-1], scroll_to_index=valueWanted-1)
            

                # whatever is printed is displayed in output window 
                print("Value Searched For: " + str(valueWanted) + "\n")
                print(dictToFormatedString(data[valueWanted-1]))
            elif currentWindow == 3:
                fig_canvas_agg.get_tk_widget().forget()
                fig_canvas_agg = draw_figure(barChartWindow['chatView'].TKCanvas, genrateBarChart(dict(data[valueWanted-1]), currentColour))
                window['ScrollableList'].Update(set_to_index=[valueWanted-1], scroll_to_index=valueWanted-1)

        except:
            if currentWindow == 1:
                window['Output'].Update('')
                print("Error! Please try a diffrent input.")
            else:
                gui.popup("Error! Please try a diffrent input.")

    # Item change in scrollable list
    if (event == "ScrollableList"):
        itemDict = dict(values["ScrollableList"][0])
        itemId = int(itemDict["id"])

        if currentWindow == 1:
            window['Output'].Update('')
            print("Value Selected: " + str(itemId) + "\n")
            print(dictToFormatedString(data[itemId-1]))
        elif currentWindow == 3:
            fig_canvas_agg.get_tk_widget().forget()
            fig_canvas_agg = draw_figure(barChartWindow['chatView'].TKCanvas, genrateBarChart(dict(data[itemId-1]), currentColour))

    if (event == "colourText"):
        print(currentColour)
        currentColour = values["colourText"]
        print(currentColour)

        fig_canvas_agg.get_tk_widget().forget()
        gui.popup("Please generate a new graph...", font=("Helvetica", 25))

    # Scatter graph page
    if (event == "a1") or (event == "a2"):
        a1 = values["a1"]
        a2 = values["a2"]

        fig_canvas_agg.get_tk_widget().forget()
        fig_canvas_agg = draw_figure(scatterGraphWindow['scatterView'].TKCanvas, genrateScatterChart(data, currentColour, a1, a2))

    # Scatter Graph Mean Page 
    if (event == "attributeNotMean"):
        attributeChosen = values["attributeNotMean"]
        otherAttributes = list(data[0].keys())
        
        otherAttributes.pop(0)
        otherAttributes.pop(0)
        otherAttributes.remove(attributeChosen)

        meanOfDatum = []
        chosenData = []


        for record in data:
            chosenData.append(record[attributeChosen])

            currentP = 0
            for a in otherAttributes:
                currentP = currentP + int(record[a])
            currentP = currentP / 3
    
            meanOfDatum.append(currentP)
        # print(otherData, len(otherData))
        # print(meanOfDatum, len(meanOfDatum))

        aggergateData = [chosenData, meanOfDatum]
        fig_canvas_agg.get_tk_widget().forget()
        fig_canvas_agg = draw_figure(scatterGraphMeanWindow['scatterView'].TKCanvas, genrateScatterMeanChart(aggergateData, currentColour, attributeChosen))

window.close()