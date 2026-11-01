def open_selector(component):
	params = component.view.params
	selected = []
	for key in list(params.selectedKeys or []):
		selected.append(str(key))
	component.session.custom.metricDraftKeys = selected
	system.perspective.openPopup(
		"metricSelector",
		"Popups/MetricSelector",
		params={
			"machineTitle": params.machineTitle,
			"udtPath": params.udtPath,
			"machineId": params.machineId,
			"database": params.database,
			"selectedKeys": selected,
			"options": metrics.service.selection_rows(selected),
		},
		title="Metricas",
		modal=True,
		overlayDismiss=True,
		showCloseIcon=True,
		resizable=False,
		position={"width": 440, "height": 560},
	)


def remember(session, key, selected, fallback=None):
	keys = []
	current = session.custom.metricDraftKeys
	if current:
		for item in current:
			text = str(item)
			if text not in keys:
				keys.append(text)
	elif fallback:
		for item in fallback:
			text = str(item)
			if text not in keys:
				keys.append(text)
	key = str(key)
	if selected:
		if key not in keys:
			keys.append(key)
	else:
		keys = [item for item in keys if item != key]
	session.custom.metricDraftKeys = keys
	return keys
