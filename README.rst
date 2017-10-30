=======
README
=======

This application is created for GlobalSat's 3G GPS tracker TR-313.
There are two purposes for created this.

1. Register latest location.
2. View logging locations.


Installation
-------------

1. Copy sample config file for setting your own googlemap API key and or.

    % cp config.ini.sample development.ini

2. Edit config file.
3. Run

    % PYTHONPATH=".:$PAYTHONPATH" nohup python tr313logger/main.py -c development.ini > std_output.txt 2>&1 &


Limitaion
------------

There are some questions about data format of the tracker, Because I have investigated it.


Link
-------

http://www.globalsat.com.tw/s/2/product-199311/Advance-3G-Personal-Tracker-TR-313.html


License
-------

This program is released under the GPLv3 license.: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.