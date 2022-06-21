def white(sg):

    white = {
    	'BACKGROUND': '#ffffff',
    	'TEXT': 'black',
    	'INPUT': '#eeeeee',
    	'SCROLL': '#4169e1',
    	'TEXT_INPUT': '#4169e1',
    	'BUTTON': ('white', '#4169e1'),
    	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    	'BORDER': 0,
    	'SLIDER_DEPTH': 0,
    	'PROGRESS_DEPTH': 0
    }

    return white

def dark(sg):

    dark = {
    	'BACKGROUND': '#000000',
    	'TEXT': 'white',
    	'INPUT': '#1e1e1e',
    	'SCROLL': '#1e1e1e',
    	'TEXT_INPUT': '#4169e1',
    	'BUTTON': ('white', '#1e1e1e'),
    	'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    	'BORDER': 0,
    	'SLIDER_DEPTH': 0,
    	'PROGRESS_DEPTH': 0
    }

    return dark
