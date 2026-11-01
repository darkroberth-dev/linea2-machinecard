
def info(header,text,_type,timeout=3):
	#type success,info, danger
	system.perspective.openPopup(id="popupBanner", view="Components/notification/banner", params = {"text":text,"header":header,"type":_type, "timeout":timeout}, position={'right':15,'top':10}, draggable = False, showCloseIcon= False, resizable=False, classes="popup-banner")
	
	
