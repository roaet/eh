# Copyright (c) 2016 Justin L. Hammond
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from eh import base_subject as base

class BashKeyboardShortcutsSubject(base.BaseSubject):
    keys = ['bash']
    versions = ['1.0']

    def output(self):
        output = """
Keyboard shortcuts for bash cursor movement:
"""
        b2c = self.bullet2col
        output += b2c("Ctrl + A", "Go to the beginning of the line you are currently typing on")
        output += b2c("Ctrl + E", "Go to the end of the line you are currently typing on")
        output += b2c("Ctrl + L", "Clears the Screen, similar to the clear command")
        output += b2c("Ctrl + U", "Clears the line before the cursor position. If you are at the end of the line, clears the entire line.")
        output += b2c("Ctrl + H", "Same as backspace")
        output += b2c("Ctrl + R", "Let's you search through previously used commands")
        output += b2c("Ctrl + C", "Kill whatever you are running")
        output += b2c("Ctrl + D", "Exit the current shell")
        output += b2c("Ctrl + Z", "Puts whatever you are running into a suspended background process. fg restores it.")
        output += b2c("Ctrl + W", "Delete the word before the cursor")
        output += b2c("Ctrl + K", "Clear the line after the cursor")
        output += b2c("Ctrl + T", "Swap the last two characters before the cursor")
        output += b2c("Esc + T", "Swap the last two words before the cursor")
        output += b2c("Alt + F", "Move cursor forward one word on the current line")
        output += b2c("Alt + B", "Move cursor backward one word on the current line")
        return output
