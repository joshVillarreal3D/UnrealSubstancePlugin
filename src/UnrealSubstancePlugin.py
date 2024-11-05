import tkinter.filedialog
from unreal import (ToolMenuContext, ToolMenus, 
                    uclass, 
                    ufunction, 
                    ToolMenuEntryScript)

import os
import sys

import importlib
import tkinter # imports all the important items needed for this script

srcPath = os.path.dirname(os.path.abspath(__file__)) # sets the file as the name srcPath
if srcPath not in sys.path: # checks if the file path is in the correct spot
    sys.path.append(srcPath) # adds the file to the correct spot


import UnrealUtility
importlib.reload(UnrealUtility) # reloads the system with a new import of Unreal Utility

@uclass()
class BuildBaseMaterialEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        UnrealUtility.UnrealUtility().FindOrBuildBaseMaterial()

@uclass()
class LoadMeshEntryScript(ToolMenuEntryScript):
    @ufunction(override=True)
    def execute(self, context: ToolMenuContext) -> None:
        window = tkinter.Tk()
        window.withdraw()
        importDir = tkinter.filedialog.askdirectory()
        window.destroy()
        UnrealUtility.UnrealUtility().ImportFromDir(importDir) # creates a window that closes immediately after  importing the tkinter and tool menu

class UnrealSubstancePlugin:
    def __init__(self):
        self.submenuName="UnrealSubstancePlugin"
        self.submenuLabel="Unreal Substance Plugin"
        self.CreateMenu() # creates submenu with names on the toolbar of UE5

    def CreateMenu(self):
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")

        existing = ToolMenus.get().find_menu(f"LevelEditor.MainMenu.{self.submenuName}")
        if existing:
            print(f"Deleting previous menu: {existing}")
            ToolMenus.get().remove_menu(existing.menu_name)

        self.submenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "UnrealSubstancePlugin", "Unreal Substance Plugin")
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript())
        self.AddEntryScript("LoadFromDirectory", "Load From Directory", LoadMeshEntryScript())
        ToolMenus().get().refresh_all_widgets() # refresh all the widgets needed to make the menus

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript):
        script.init_entry(self.submenu.menu_name, self.submenu.menu_name, "", name, label)
        script.register_menu_entry()

UnrealSubstancePlugin()