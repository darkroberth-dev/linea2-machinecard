def open_selector(component):
	params = component.view.params
	selected = list(params.selectedKeys or [])
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


def toggle(options, key, selected):
	rows = []
	for row in list(options or []):
		item = dict(row)
		if item.get("key") == key:
			item["selected"] = True if selected else False
		rows.append(item)
	return rows


def apply(page_self, machine_title, options, context):
	selected = metrics.service.selected_keys(options)
	cards = page_self.getChild("Main").getChild("FlexContainer").getChild("FlexContainer_0").getChild("Cards")
	metrics.service.patch_repeater(cards, machine_title, selected, context)
	return selected
