#!/usr/bin/env python
import wx, wx.lib.intctrl

''' Note:
I created this little thing for my own use..
it's not the best thing in the world, but it
works for me! If you can / want to edit or
improve it in any way, please do so! As such,
I've thrown this under the GPL.. but I would
really appreciate it if you send me any updates
or fixes etc (kentonh@gmail.com). I'm still
rather new to wxPython, so many things I wanted
to get working I couldn't.

Anyway, here's the standard spiel:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

class TFTColourPicker(wx.Frame):
	def __init__(self, parent, title):
		# init the frame
		super(TFTColourPicker, self).__init__(parent, title=title, size=(440, 110))
		
		# create the panel and sizers..
		panel = wx.Panel(self, -1)
		bgbox = wx.BoxSizer(wx.VERTICAL)
		boxMain = wx.BoxSizer(wx.HORIZONTAL)
		boxSliders = wx.GridBagSizer(2, 2)
		
		# set up the controls
		# colour display
		self.colourBox = wx.Panel(panel, -1, size=(100,100), style=wx.SUNKEN_BORDER)
		self.colourBox.SetBackgroundColour(wx.Colour(0, 0, 0))
		boxMain.Add(self.colourBox, 1, wx.EXPAND)
		
		# red colour slider
		boxSliders.Add(wx.StaticText(panel, label="Red:"), (0,0))
		self.rSlider = wx.Slider(panel, -1, 0, 0, 255, wx.DefaultPosition, (100, -1), wx.SL_HORIZONTAL)
		boxSliders.Add(self.rSlider, (0,1), flag=wx.EXPAND)
		
		# red colour input box
		self.rLabel = wx.lib.intctrl.IntCtrl(panel, 100, 0, size=(30, -1), min=0, max=255)
		boxSliders.Add(self.rLabel, (0,2), flag=wx.EXPAND)
		
		# hex888 display
		boxSliders.Add(wx.StaticText(panel, label="Hex888:"), (0,3))
		#self.hex888 = wx.lib.masked.TextCtrl(panel, 200, '0x000000', size=(65, -1), mask = '0x|######', includeChars='abcdefABCDEF')
		self.hex888 = wx.TextCtrl(panel, -1, value="0x000000", size=(65, -1), style=wx.TE_READONLY)
		self.hex888.SetBackgroundColour(wx.Colour(200, 200, 200))
		boxSliders.Add(self.hex888, (0,4))
		
		# green colour slider
		boxSliders.Add(wx.StaticText(panel, label="Green:"), (1,0))
		self.gSlider = wx.Slider(panel, -1, 0, 0, 255, wx.DefaultPosition, (100, -1), wx.SL_HORIZONTAL)
		boxSliders.Add(self.gSlider, (1,1), flag=wx.EXPAND)
		
		# green colour input box
		self.gLabel = wx.lib.intctrl.IntCtrl(panel, 101, 0, size=(30, -1), min=0, max=255)
		boxSliders.Add(self.gLabel, (1,2), flag=wx.EXPAND)
		
		# hex565 display
		boxSliders.Add(wx.StaticText(panel, label="Hex565:"), (1,3))
		#self.hex565 = wx.lib.masked.TextCtrl(panel, 201, '0x0000', size=(65, -1), mask = '0x|####', includeChars='abcdefABCDEF')
		#self.hex565 = wx.StaticText(panel, label="0x0000")
		self.hex565 = wx.TextCtrl(panel, -1, value="0x0000", size=(65, -1), style=wx.TE_READONLY)
		self.hex565.SetBackgroundColour(wx.Colour(200, 200, 200))
		boxSliders.Add(self.hex565, (1,4))
		
		# blue colour slider
		boxSliders.Add(wx.StaticText(panel, label="Blue:"), (2,0))
		self.bSlider = wx.Slider(panel, -1, 0, 0, 255, wx.DefaultPosition, (100, -1), wx.SL_HORIZONTAL)
		boxSliders.Add(self.bSlider, (2,1), flag=wx.EXPAND)
		
		# blue colour input box
		self.bLabel = wx.lib.intctrl.IntCtrl(panel, 102, 0, size=(30, -1), min=0, max=255)
		boxSliders.Add(self.bLabel, (2,2), flag=wx.EXPAND)
		
		# copy to clipboard button!
		self.copyToClipboard = wx.Button(panel, 300, label="Copy Hex565")
		boxSliders.Add(self.copyToClipboard, (2,3), span=(1,2), flag=wx.EXPAND)
		
		# add the sizer to the list
		boxSliders.AddGrowableCol(1)
		boxMain.Add(boxSliders, 2, wx.EXPAND)
		
		# bind the events
		self.Bind(wx.EVT_BUTTON, self.OnCopy, id=300)
		self.Bind(wx.EVT_SLIDER, self.SliderUpdate)
		self.Bind(wx.EVT_TEXT, self.TextUpdate)
		
		# set up the keyboard accelerator
		# (for Ctrl+C to copy!)
		# NOTE: NOT WORKING FOR SOME REASON :/
		copyId = wx.NewId()
		self.Bind(wx.EVT_MENU, self.OnCopy, id=copyId)
		acceleratorTable = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('C'), copyId)])
		self.SetAcceleratorTable(acceleratorTable)

		# setup the window
		panel.SetSizer(boxMain)
		bgbox.Add(panel, 1, wx.EXPAND)
		self.SetAutoLayout(True)
		self.SetSizer(bgbox)
	
	# called whenever the slider updates..
	def SliderUpdate(self, event):
		# get the slider values
		self.red = self.rSlider.GetValue()
		self.green = self.gSlider.GetValue()
		self.blue = self.bSlider.GetValue()
		
		# update the text box labels
		self.rLabel.SetValue(self.red)
		self.gLabel.SetValue(self.green)
		self.bLabel.SetValue(self.blue)
		self.UpdateHexCodes()
		
		# update the colour
		self.colourBox.SetBackgroundColour(wx.Colour(self.red, self.green, self.blue))
		self.colourBox.Refresh()
		
	# called when the text boxes get updated
	def TextUpdate(self, event):
		# make sure it's one of the text boxes we're looking for
		if event.GetId() == 100 or event.GetId() == 101 or event.GetId() == 102:
			# get the values			
			self.red = self.rLabel.GetValue()
			self.green = self.gLabel.GetValue()
			self.blue = self.bLabel.GetValue()
			
			# update the sliders
			self.rSlider.SetValue(self.red)
			self.gSlider.SetValue(self.green)
			self.bSlider.SetValue(self.blue)
			
			# and update the hex codes
			self.UpdateHexCodes()
		
			# update the colour
			self.colourBox.SetBackgroundColour(wx.Colour(self.red, self.green, self.blue))
			self.colourBox.Refresh()
			
	def UpdateHexCodes(self):
		# just format the hex value
		self.hex888.SetValue("0x%0.6X" % ((self.red << 16) | (self.green << 8) | (self.blue)))
		# convert from rgb888 to rgb565
		self.hex565.SetValue("0x%0.4X" % ((int(float(self.red) / 255 * 31) << 11) | (int(float(self.green) / 255 * 63) << 5) | (int(float(self.blue) / 255 * 31))))
			
	# copy the hex565 to the clipboard!
	def OnCopy(self, event):
		# copy it to the clipboard!
		clipdata = wx.TextDataObject()
		clipdata.SetText(self.hex565.GetValue())
		wx.TheClipboard.Open()
		wx.TheClipboard.SetData(clipdata)
		wx.TheClipboard.Close()
		
if __name__ == '__main__':
	# start the frame running up
	app = wx.App()
	frame = TFTColourPicker(None, 'TFT Colour Picker')
	frame.Centre()
	frame.Show()
	app.MainLoop()