#! /usr/bin/python

# Special Functions

# specialfunctions.py is part of Sentience in Space.
#
# Sentience in Space is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sentience in Space is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sentience in Space.  If not, see <http://www.gnu.org/licenses/>.

# Turn an integer into a big endian hex string
makehex = lambda value, size = 1: eval(('"%.' + str(size)) + 'x"%' + str(value))

# parse a "journal entry" formatted file
def parsejournal(file_name):
    f = open(file_name, 'r')
    j = f.read()
    f.close()

    j = j.split('\n')

    out = []# returned data
    data = []# temporary storage
    store = False
    for entry in j:
        if not store:
            if entry == '-----BEGIN ENTRY-----':
                store = True
                data = []
        else:
            if entry == '-----END ENTRY-----':
                store = False
                out += [[data[0], data[1:]]]
                data = []
            else:
                data += [entry]
    return out
