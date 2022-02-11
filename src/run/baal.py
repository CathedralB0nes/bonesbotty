import math
from pickle import FALSE
from re import search

from char.sorceress import Sorceress
from char.i_char import IChar
from typing import Dict, Tuple, Union, List, Callable
from config import Config
from logger import Logger
import keyboard
from pather import Location, Pather
from typing import Union
from item.pickit import PickIt
from template_finder import TemplateFinder
from town.town_manager import TownManager
from ui import UiManager
from utils.misc import wait
from utils.custom_mouse import mouse
from dataclasses import dataclass
import cv2
import time
from screen import Screen
from char import IChar
import numpy as np
from utils.misc import load_template, list_files_in_folder, alpha_to_mask
import random
import math


class Baal:
    def __init__(
        self,
        screen: Screen,
        template_finder: TemplateFinder,
        pather: Pather,
        town_manager: TownManager,
        ui_manager: UiManager,
        char: IChar,
        pickit: PickIt,

    ):
        self._config = Config()
        self._screen = screen
        self._template_finder = template_finder
        self._pather = pather
        self._town_manager = town_manager
        self._ui_manager = ui_manager
        self._char = char
        self._pickit = pickit
        self._picked_up_items = False
        self._pather = pather
 
    def approach(self, start_loc: Location) -> Union[bool, Location, bool]:
        Logger.info("Run Baal")
        if not self._char.can_teleport():
            raise ValueError("Baal requires teleport")
        if not self._town_manager.open_wp(start_loc):
            return False
        wait(0.4)
        if self._ui_manager.use_wp(5, 8): # Worldstone
            return Location.A5_BAAL_START
        return False

    def stuck(self, corner_picker, x2_m, y2_m, stuck_count, super_stuck, pos_m)-> bool:
        x, y = pos_m
        pos_m2 = x, y
        coordlog = x, y
        Logger.debug(coordlog)
        x, y = self._screen.convert_monitor_to_screen(pos_m2)
        pos_m2 = x, y
        x, y = self._screen.convert_screen_to_abs(pos_m2)                        
        pos_m2 = x, y
        coordlog = x, y
        Logger.debug(coordlog)
        # x, y = self._screen.convert_abs_to_monitor((pos_m2))
        #########################
        if x < 0 and y < 0: # -, - Corner 1 Top Left
            Logger.debug("corner one stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((-600, -350))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                t0 = self._screen.grab()                      
                pos_m2 = self._screen.convert_abs_to_monitor((-600, 350))
                self._char.move(pos_m2, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                if score < .15:
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m * -1))
                    self._char.move(pos_m2, force_tp=True)                              
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m))
                    self._char.move(pos_m2, force_tp=True)
        if x > 0 and y < 0: #corner 2
            Logger.debug("corner two stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((600, -300))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                Logger.debug("corner two stuck")
                t0 = self._screen.grab()                      
                pos_m2 = self._screen.convert_abs_to_monitor((600, 300))
                self._char.move(pos_m2, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                if score < .15:
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m * -1))
                    self._char.move(pos_m2, force_tp=True)                              
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m))
                    self._char.move(pos_m2, force_tp=True)
        if x > 0 and y > 0: #corner 3
            Logger.debug("corner three stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((600, 350))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                Logger.debug("corner three stuck")
                t0 = self._screen.grab()                      
                pos_m2 = self._screen.convert_abs_to_monitor((600, -350))
                self._char.move(pos_m2, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                if score < .15:
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m * -1))
                    self._char.move(pos_m2, force_tp=True)                              
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m))
                    self._char.move(pos_m2, force_tp=True)
        if x < 0 and y > 0: #corner 4
            Logger.debug("corner four stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((-600, 350))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                Logger.debug("corner four stuck")
                t0 = self._screen.grab()                      
                pos_m2 = self._screen.convert_abs_to_monitor((-600, -350))
                self._char.move(pos_m2, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)
                if score < .15:
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m * -1))
                    self._char.move(pos_m2, force_tp=True)                              
                    pos_m2 = self._screen.convert_abs_to_monitor((x2_m * -1, y2_m))
                    self._char.move(pos_m2, force_tp=True)


    def super_stuck(self, corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)-> bool:
        Logger.debug(str(corner_picker) + ": Seems we are super stuck,")
        self._corner_roller(corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)


    def exit_super_stuck(self, pos_m, stuck_count, super_stuck, roomfound)-> bool:
        x, y = pos_m
        pos_m2 = x, y
        coordlog = x, y
        Logger.debug(coordlog)
        x, y = self._screen.convert_monitor_to_screen(pos_m2)
        pos_m2 = x, y
        x, y = self._screen.convert_screen_to_abs(pos_m2)                        
        pos_m2 = x, y
        coordlog = x, y
        Logger.debug(coordlog)
        Logger.debug("SUPER STUCK CLICKER")
        if x < 0 and y < 0: # -, - Corner 1 Top Left
            Logger.debug("SUPER STUCK IN CORNER 1")
            pos_m2 = self._screen.convert_abs_to_monitor((600, 350))
            self._char.move(pos_m2, force_tp=True)
            pos_m2 = self._screen.convert_abs_to_monitor((-20, -300))
            self._char.move(pos_m2, force_tp=True)
            super_stuck += 1
            stuck_count = 0
        if x > 0 and y < 0 and not roomfound: #corner 2
            Logger.debug("STUCK IN ROCNER 2")
            pos_m2 = self._screen.convert_abs_to_monitor((-600, 350))
            self._char.move(pos_m2, force_tp=True)
            pos_m2 = self._screen.convert_abs_to_monitor((20, -300))
            self._char.move(pos_m2, force_tp=True)
            super_stuck += 1
            stuck_count = 0
        if x > 0 and y > 0 and not roomfound: #corner 3
            Logger.debug("stuck in corner 3")
            pos_m2 = self._screen.convert_abs_to_monitor((-600, -350))
            self._char.move(pos_m2, force_tp=True)
            pos_m2 = self._screen.convert_abs_to_monitor((-35, 250))
            self._char.move(pos_m2, force_tp=True)
            super_stuck += 1
            stuck_count = 0
        if x < 0 and y > 0 and not roomfound: #corner 4
            Logger.debug("sutck in corner 4")
            pos_m2 = self._screen.convert_abs_to_monitor((600, -350))
            self._char.move(pos_m2, force_tp=True)
            pos_m2 = self._screen.convert_abs_to_monitor((-35, 250))
            self._char.move(pos_m2, force_tp=True)
            super_stuck += 1
            stuck_count = 0
        if not self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
            keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport
            keyboard.send(self._config.char["minimap"]) #turn on minimap
            Logger.debug("EXIT STUCK /// MAP ON")
        template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9,  time_out=0.5, use_grayscale=False)
        if template_match.valid:
            if self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
                keyboard.send(self._config.char["minimap"]) #turn on minimap
                Logger.debug("EXIT STUCK FOUND MATCH /// MAP OFF")
            template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9,  time_out=0.5, use_grayscale=False)
            pos_m = self._screen.convert_screen_to_monitor(template_match.position)
            if self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.7, time_out=0.1, use_grayscale=False).valid:
                keyboard.send(self._char._skill_hotkeys["teleport"])
                keyboard.send(self._config.char["minimap"])
                Logger.debug("EXIT CLICKER MATCH AND MAP MATCH /// MAP OFF")
            stuck_count = 0
            super_stuck = 0
        elif template_match == False:
            Logger.debug("NO MATCH NO POSITION2222222")                                      
            stuck_count = 0
            super_stuck = 0

    def exit_stuck(self, pos_m, stuck_count, super_stuck, roomfound)-> bool:
        x, y = pos_m
        pos_m2 = x, y
        coordlog = x, y
        Logger.debug(coordlog)
        x, y = self._screen.convert_monitor_to_screen(pos_m2)
        pos_m2 = x, y
        x, y = self._screen.convert_screen_to_abs(pos_m2)                        
        pos_m2 = x, y
        coordlog = x, y
        Logger.debug(coordlog)
        # x, y = self._screen.convert_abs_to_monitor((pos_m2))
        #########################
        if x < 0 and y < 0 and not roomfound: # -, - Corner 1 Top Left
            Logger.debug("corner one stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((-600, -350))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                pos_m2 = self._screen.convert_abs_to_monitor((600, -350))
                self._char.move(pos_m2, force_tp=True)
                pos_m2 = self._screen.convert_abs_to_monitor((0, -350))
                self._char.move(pos_m2, force_tp=True)
        if x > 0 and y < 0 and not roomfound: #corner 2
            Logger.debug("corner two stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((600, -200))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                pos_m2 = self._screen.convert_abs_to_monitor((600, 350))
                self._char.move(pos_m2, force_tp=True)
                pos_m2 = self._screen.convert_abs_to_monitor((0, 200))
                self._char.move(pos_m2, force_tp=True)
        if x > 0 and y > 0 and not roomfound: #corner 3
            Logger.debug("corner three stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((600, 350))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                pos_m2 = self._screen.convert_abs_to_monitor((-600, 350))
                self._char.move(pos_m2, force_tp=True)
                pos_m2 = self._screen.convert_abs_to_monitor((0, 200))
                self._char.move(pos_m2, force_tp=True)
        if x < 0 and y > 0 and not roomfound: #corner 4
            Logger.debug("corner four stuck")
            t0 = self._screen.grab()                      
            pos_m2 = self._screen.convert_abs_to_monitor((-600, 350))
            self._char.move(pos_m2, force_move=True)
            t1 = self._screen.grab()
            # check difference between the two frames to determine if tele was good or not
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            if score < .15:
                pos_m2 = self._screen.convert_abs_to_monitor((-600, 350))
                self._char.move(pos_m2, force_tp=True)
                pos_m2 = self._screen.convert_abs_to_monitor((0, 200))
                self._char.move(pos_m2, force_tp=True)

    def _corner_roller(self, corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)-> bool:
        Logger.debug("corner ROLLER")
        keepernumber = random.randint(1, 4)
        while keepernumber == corner_exclude or keepernumber == corner_picker or keepernumber == exclude1 or keepernumber == exclude2:
            keepernumber = random.randint(1, 4) 
            super_stuck = 0
            stuck_count = 0        
        corner_exclude = corner_picker
        corner_picker = keepernumber
        exclude1 = corner_picker - 2
        exclude2 = corner_picker + 2
        super_stuck = 0
        stuck_count = 0
        if corner_picker == 1:
            Logger.debug("corner ROLLER picked 1")
            self._scout(1, -250, -600, -200, -345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) #top - left
        elif corner_picker == 2:
            Logger.debug("corner ROLLER picked 2")
            self._scout(2, 250, 600, -200, -345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # top - right
        elif corner_picker == 3:
            Logger.debug("corner ROLLER picked 3")
            self._scout(3, 485, 600, 200, 345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # bottom - right
        elif corner_picker == 4:
            Logger.debug("corner ROLLER picked 4")
            self._scout(4, -485, -600, 200, 345, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) # bottom - left

    def _scout(self, corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)-> bool:
        found = False
        if not self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
            keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport
            keyboard.send(self._config.char["minimap"]) #turn on minimap
            Logger.debug("SCOUT /// MAP ON")
        while not found:
            (self, corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber) = (self, corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)
            found = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6", "RED_GOOP_PURPLE5"], best_match=True, threshold=0.9, time_out=0.1, use_grayscale=False).valid
            founder = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6", "RED_GOOP_PURPLE5"], best_match=True, threshold=0.9, time_out=0.1, use_grayscale=False)
            foundname = founder.name
            if founder.valid:
                pos_m = self._screen.convert_screen_to_monitor(founder.position)
            # Logger.debug("EXIT CLICKER 1st FIND/// MAP OFF")
            pos_m = self._screen.convert_abs_to_monitor((random.uniform(x1_m, x2_m), random.uniform(y1_m, y2_m)))
            t0 = self._screen.grab()
            self._char.move(pos_m, force_tp=True, force_move=True)
            t1 = self._screen.grab()
            diff = cv2.absdiff(t0, t1)
            diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
            score = (float(np.sum(mask)) / mask.size) * (1/255.0)
            Logger.debug(str(score) + ": is our current score")
            if self._template_finder.search_and_wait(["BAAL_LVL2_4", "BAAL_LVL2_5", "BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], best_match=True, threshold=0.8,  time_out=0.1, use_grayscale=False).valid:
                pos_m = (0, 0)
                self._exitclicker(pos_m)
            if score < .10:
                stuck_count += 1
                if stuck_count >= 2:
                    super_stuck += 1
                    self.stuck(corner_picker, x2_m, y2_m, stuck_count, super_stuck, pos_m)
                    stuck_count = 0  
                if super_stuck >= 3:
                    self.super_stuck(corner_picker, x1_m, x2_m, y1_m, y2_m, stuck_count, super_stuck, corner_exclude, exclude1, exclude2, keepernumber)
                    super_stuck = 0                                  
                                            
        if found == True:
            Logger.debug("SCOUT EXITING oustside")
            Logger.debug(foundname)
            Logger.debug(founder.score)
            pos_m = self._screen.convert_screen_to_monitor(self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6", "RED_GOOP_PURPLE5"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).position)
            keyboard.send(self._config.char["minimap"]) #turn off minimap
            self._exitclicker(pos_m)
            return True   

    def _exitclicker(self, pos_m)-> bool:
            Logger.debug("EXITCLICKER")
            roomfound = False
            stuck_count = 0
            super_stuck = 0
            mapcheck = self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False)
            template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6", "RED_GOOP_PURPLE5"], best_match=True, threshold=0.9,  time_out=0.1, use_grayscale=False)
            if template_match.valid:
                pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                if self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
                    Logger.debug("EXITCLICKER FOUND TEMPLATE TURNING MAP OFF!")
                    keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport
                    keyboard.send(self._config.char["minimap"]) #turn on minimap
                    # Logger.debug("EXIT CLICKER 1st FIND/// MAP OFF")
            while not roomfound:
                founder = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6"], best_match=True, threshold=0.9,  time_out=0.1, use_grayscale=False)
                if founder.valid:
                    pos_m = self._screen.convert_screen_to_monitor(founder.position)                
                roomfound = self._template_finder.search_and_wait(["BAAL_LVL2_4", "BAAL_LVL2_5", "BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], best_match=True, threshold=0.8,  time_out=0.1, use_grayscale=False).valid
                template_match = self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6", "RED_GOOP_PURPLE5"], best_match=True, threshold=0.9,  time_out=0.1, use_grayscale=False)
                if roomfound == True or template_match.valid:
                    if self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
                        keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport
                        keyboard.send(self._config.char["minimap"]) #turn on minimap
                        Logger.debug("EXIT CLICKER MATCH AND MAP MATCH /// MAP OFF")
                        if self._template_finder.search_and_wait(["RED_GOOP_PURPLE3", "RED_GOOP_PURPLE4", "RED_GOOP_PURPLE6", "RED_GOOP_PURPLE5"], best_match=True, threshold=0.9,  time_out=0.1, use_grayscale=False) == True:
                            pos_m = self._screen.convert_screen_to_monitor(template_match.position)
                            pos_m2 = (template_match.position)#SCREEN                    
                t0 = self._screen.grab()
                self._char.move(pos_m, force_tp=True, force_move=True)
                t1 = self._screen.grab()
                # check difference between the two frames to determine if tele was good or not
                diff = cv2.absdiff(t0, t1)
                diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(diff, 13, 255, cv2.THRESH_BINARY)
                score = (float(np.sum(mask)) / mask.size) * (1/255.0)           
                if score < .15 and not roomfound:
                    stuck_count += 1
                    if stuck_count >= 2:
                        super_stuck += 1
                        self.exit_stuck(pos_m, stuck_count, super_stuck, roomfound)
                    if super_stuck >= 3:
                        Logger.debug("SUPER DUPER STUCK")
                        self.exit_super_stuck(pos_m, stuck_count, super_stuck, roomfound)
                        if self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
                            keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport
                            keyboard.send(self._config.char["minimap"]) #turn on minimap
                            Logger.debug("EXIT CLICKER SUPER STUCK /// MAP OFF")
                        super_stuck = 0
                        stuck_count = 0
            Logger.debug("FOUND EXIT")
            found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
            if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.8, time_out=4):
                # do a random tele jump and try again
                Logger.debug("FOUND EXIT BUT BROKE")
                pos_m = self._screen.convert_abs_to_monitor((315, -150))
                self._char.move(pos_m, force_move=True)
                if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.8, time_out=4):
                    self._char.move(pos_m, force_move=True)
                    if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.8, time_out=4):
                        pos_m = self._screen.convert_abs_to_monitor((-315, -100))
                        self._char.move(pos_m, force_move=True)
                        Logger.debug("CANT GET TO EXIT")
                        if not self._char.select_by_template(["BAAL_LVL2_EXIT", "BAALER2_0", "BAALER2_1"], found_loading_screen_func, threshold=0.8, time_out=4):
                            Logger.debug("ABANDON HOPE!!!")
                            return False
            if self._template_finder.search_and_wait(["BAAL_THRONE_START_0", "BAAL_THRONE_START_1", "BAAL_THRONE_START_2", "BAAL_THRONE_START_3"], threshold=0.8, time_out=.5).valid:
                if self._template_finder.search_and_wait(["BAAL_THRONE_START_0", "BAAL_THRONE_START_1", "BAAL_THRONE_START_2", "BAAL_THRONE_START_3"], threshold=0.8, time_out=1).valid:
                    #throne killd
                    keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport                
                    self._throne_room()                    
            else:
                keyboard.send(self._config.char["minimap"]) #turn off minimap
                self._scout(4, -485, -600, 200, 345, 0, 0, 4, 2, 2, 4) # bottom - left

    def _throne_room(self)-> bool:
        self._char.pre_buff()
        keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport
        Logger.debug("TO MONSTERIN THRONE")
        if not self._template_finder.search_and_wait(["MAP_CHECK"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
            Logger.debug("MAP IS OFF! DO THRONE!")
        else:
            Logger.debug("MAP IS ON TURNING OFF! DO THRONE!")
            keyboard.send(self._config.char["minimap"]) #turn on minimap

        roomfound = False
        while not roomfound:
            roomfound = self._template_finder.search_and_wait(["BAAL_THRONE_ROOM_0", "BAAL_THRONE_ROOM_7", "BAAL_THRONE_ROOM_2", "BAAL_THRONE_ROOM_3", "BAAL_THRONE_ROOM_4", "BAAL_THRONE_ROOM_5", "BAAL_THRONE_ROOM_6"], best_match=True, threshold=0.8,  time_out=0.1, use_grayscale=False).valid
            pos_m = self._screen.convert_abs_to_monitor((550, -340))
            self._char.move(pos_m, force_tp=True)
            self._char.move(pos_m, force_tp=True)
            self._char.move(pos_m, force_tp=True)
        if not self._pather.traverse_nodes([9000], self._char, time_out=3):
            # do a random tele jump and try again
            pos_m = self._screen.convert_abs_to_monitor((250, 220))
            self._char.move(pos_m, force_move=True)
           
        # Cthu: instead of looping to the throne, we just use a static path that ends close to [9000]. The coordinates for the static path are defined in GAME.INI & are called with the function below. You can record your own static paths using utils/static_run_recorder.py -> press F11 and right click where you want to record the x,y of the click to the terminal.
        #if not self._pather.traverse_nodes_fixed("baal_lvl3entrance_throne", self._char): return False #we wrap it around an if block returning false, when it was not successful, to stop the run. 
        #if not self._pather.traverse_nodes([9000], self._char, time_out=3, threshold=0.8): return False



        Logger.debug("CLEAR TRASH IN THRONE")
        corner_count = 0
        while not self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:
            if self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:
                break
            if corner_count < 5:
                if corner_count == 0: #by entrance
                    Logger.debug("MINI ENTRANCE")
                    pos_m = self._screen.convert_abs_to_monitor((-350, 220))
                    self._char.move(pos_m, force_tp=True)        
                    self._char._mini_trash()
                    self._pather.traverse_nodes([9000], self._char, time_out=3)
                    corner_count += 1
                elif corner_count == 1: #top left
                    Logger.debug("MINI TOP LEFT")
                    self._pather.traverse_nodes_fixed("baal_minitrash_tops", self._char)        
                    self._char._mini_trash()
                    self._pather.traverse_nodes_fixed("baal_minitrash_tope", self._char)
                    self._pather.traverse_nodes([9000], self._char, time_out=3)
                    corner_count += 1
                elif corner_count == 2: #top right
                    Logger.debug("MINI TOP RIGHT")
                    self._pather.traverse_nodes_fixed("baal_minitrash_rights", self._char)    
                    self._char._mini_trash()
                    self._pather.traverse_nodes_fixed("baal_minitrash_righte", self._char)
                    self._pather.traverse_nodes([9000], self._char, time_out=3)
                    corner_count += 1
                elif corner_count == 3: # bottom right
                    Logger.debug("MINI BOT RIGHT")
                    self._pather.traverse_nodes_fixed("baal_minitrash_brights", self._char)       
                    self._char._mini_trash()
                    self._pather.traverse_nodes_fixed("baal_minitrash_brighte", self._char)
                    self._pather.traverse_nodes([9000], self._char, time_out=3)
                    corner_count += 1
                elif corner_count == 3: # bottom left
                    Logger.debug("MINI BOT LEFT")
                    self._pather.traverse_nodes_fixed("baal_minitrash_blefts", self._char)          
                    self._char._mini_trash()
                    self._pather.traverse_nodes_fixed("baal_minitrash_blefte", self._char)
                    self._pather.traverse_nodes([9000], self._char, time_out=3)
                    corner_count += 1
                elif corner_count == 4:
                    break
        if not self._pather.traverse_nodes([9000], self._char, time_out=3):
            # do a random tele jump and try again
            pos_m = self._screen.convert_abs_to_monitor((250, 220))
            self._char.move(pos_m, force_move=True)
        Logger.debug("WAITING FOR LAUGH?")
        clearpath = False
        found_loading_screen_func = lambda: self._ui_manager.wait_for_loading_screen(2.0)
        laughcount = 0
        while not self._template_finder.search_and_wait(["BAAL_THRONE_ROOM_CLEAR", "BAAL_THRONE_ROOM_CLEAR_1", "BAAL_THRONE_ROOM_CLEAR_2"], best_match=True, threshold=0.7, time_out=0.1, use_grayscale=False).valid or self._template_finder.search_and_wait(["BAAL_THRONE_ROOM_7"], best_match=True, threshold=0.9, time_out=0.1, use_grayscale=False).valid:
            Logger.debug("LAUGH COUNT :" + str(laughcount))            
            if self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:                
                if not self._pather.traverse_nodes([9000], self._char, time_out=3):
                    # do a random tele jump and try again
                    pos_m = self._screen.convert_abs_to_monitor((250, 220))
                    self._char.move(pos_m, force_move=True) 
                if laughcount == 0:
                    wait(2)
                laughcount += 1
                self._char._kill_throne_trash()   
            if laughcount >= 1 and not self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:
                if self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:
                    break 
                corner_count = corner_count                
                while corner_count > 4:
                    if self._template_finder.search_and_wait(["LAUGHING"], best_match=True, threshold=0.75, time_out=0.1, use_grayscale=False).valid:
                        break
                    if corner_count == 0: #by entrance
                        Logger.debug("MINI ENTRANCE")
                        pos_m = self._screen.convert_abs_to_monitor((-350, 220))
                        self._char.move(pos_m, force_tp=True)        
                        self._char._mini_trash()
                        self._pather.traverse_nodes([9000], self._char, time_out=3)
                        corner_count += 1
                    elif corner_count == 1: #top left
                        Logger.debug("MINI TOP LEFT")
                        self._pather.traverse_nodes_fixed("baal_minitrash_tops", self._char)        
                        self._char._mini_trash()
                        self._pather.traverse_nodes_fixed("baal_minitrash_tope", self._char)
                        self._pather.traverse_nodes([9000], self._char, time_out=3)
                        corner_count += 1
                    elif corner_count == 2: #top right
                        Logger.debug("MINI TOP RIGHT")
                        self._pather.traverse_nodes_fixed("baal_minitrash_rights", self._char)    
                        self._char._mini_trash()
                        self._pather.traverse_nodes_fixed("baal_minitrash_righte", self._char)
                        self._pather.traverse_nodes([9000], self._char, time_out=3)
                        corner_count += 1
                    elif corner_count == 3: # bottom right
                        Logger.debug("MINI BOT RIGHT")
                        self._pather.traverse_nodes_fixed("baal_minitrash_brights", self._char)       
                        self._char._mini_trash()
                        self._pather.traverse_nodes_fixed("baal_minitrash_brighte", self._char)
                        self._pather.traverse_nodes([9000], self._char, time_out=3)
                        corner_count += 1
                    elif corner_count == 3: # bottom left
                        Logger.debug("MINI BOT LEFT")
                        self._pather.traverse_nodes_fixed("baal_minitrash_blefts", self._char)          
                        self._char._mini_trash()
                        self._pather.traverse_nodes_fixed("baal_minitrash_blefte", self._char)
                        self._pather.traverse_nodes([9000], self._char, time_out=3)
                        corner_count += 1
        self._pather.traverse_nodes([9000], self._char, time_out=3)
        if self._template_finder.search_and_wait(["BAAL_THRONE_ROOM_CLEAR", "BAAL_THRONE_ROOM_CLEAR_1", "BAAL_THRONE_ROOM_CLEAR_2"], best_match=True, threshold=0.5, time_out=0.1, use_grayscale=False).valid:
            self._picked_up_items |= self._pickit.pick_up_items(self._char)
            if not self._pather.traverse_nodes([9000], self._char, time_out=3):
                Logger.debug("I GOT LOST BOSS")
            if not self._pather.traverse_nodes([9004], self._char, time_out=3):
                Logger.debug("I GOT LOST BOSS")
            if not self._char.select_by_template(["BAAL_THRONE_ROOM_7"], found_loading_screen_func, threshold=0.5, time_out=4):
                pos_m = self._screen.convert_abs_to_monitor((0, -5))
                self._char.move(pos_m, force_move=True) 
                if not self._char.select_by_template(["BAAL_THRONE_ROOM_7"], found_loading_screen_func, threshold=0.5, time_out=4):
                    if not self._char.select_by_template(["THRONE_ROOMZ_1"], found_loading_screen_func, threshold=0.5, time_out=4):
                        Logger.debug("COULDNT CLICK")
                        return False
 


                    
    
    def battle(self, do_pre_buff: bool) -> Union[bool, tuple[Location, bool]]:
        # TODO: We might need a second template for each option as merc might run into the template and we dont find it then
        if do_pre_buff:
            self._char.pre_buff()
        stuck_count = 0
        keyboard.send(self._char._skill_hotkeys["teleport"]) #switch active skill to teleport
        self._scout(4, -485, -600, 200, 345, stuck_count, 0, 4, 2, 2, 0) #tries to get to exit
        Logger.debug("KILLING BAAL????")
        if not self._pather.traverse_nodes([9001], self._char, time_out=3):
            Logger.debug("I GOT LOST BOSS")
        if not self._pather.traverse_nodes([9002], self._char, time_out=3):
            Logger.debug("I GOT LOST BOSS")
        self._char.kill_baal()
        self._picked_up_items |= self._pickit.pick_up_items(self._char)       

     

