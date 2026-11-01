
_REPEATER = ("root", "Main", "FlexContainer", "FlexContainer_0", "Cards")


def catalog():
	return metrics.catalog.default_catalog()


def options():
	return catalog().options()


def keys_from_labels(labels):
	found = []
	for label in labels or []:
		key = metrics.catalog.LABEL_TO_KEY.get(label)
		if key and key not in found:
			found.append(key)
	return found


def normalize_selection(selected_keys):
	known = catalog().keys()
	allowed = {}
	for key in known:
		allowed[key] = True
	clean = []
	for key in list(selected_keys or []):
		if allowed.get(key) and key not in clean:
			clean.append(key)
	return clean


def _previous_by_key(metric_rows):
	previous = {}
	for row in metric_rows or []:
		key = row.get("key") or metrics.catalog.LABEL_TO_KEY.get(row.get("text"))
		if key:
			previous[key] = row.get("percent")
	return previous


def resolve(selected_keys, context, previous=None):
	machine = context if hasattr(context, "get") else metrics.context.MachineContext.from_map(context)
	return catalog().resolve(normalize_selection(selected_keys), machine, previous)


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
		},
		title="Metricas",
		modal=True,
		overlayDismiss=True,
		showCloseIcon=True,
		resizable=False,
		position={"width": 440, "height": 560},
	)


def _cards(page):
	node = page
	for name in _REPEATER:
		node = node.getChild(name)
	return node


def apply_selection(page, machine_title, selected_keys, context):
	selected = normalize_selection(selected_keys)
	repeater = _cards(page)
	rows = []
	built = []
	for row in list(repeater.props.instances):
		data = dict(row)
		if data.get("title") == machine_title:
			machine = metrics.context.MachineContext.from_map({
				"machineId": context.get("machineId", data.get("machineId", "")),
				"udtPath": context.get("udtPath", data.get("udtPath", "")),
				"database": context.get("database", data.get("database", "")),
				"title": machine_title,
			})
			built = resolve(selected, machine, _previous_by_key(data.get("metrics")))
			data["selectedKeys"] = selected
			data["metrics"] = built
			data["udtPath"] = machine.udt_path
			data["machineId"] = machine.machine_id
			data["database"] = machine.database
			actions = []
			for action in list(data.get("actions") or []):
				item = dict(action)
				if item.get("role") == "select-metrics":
					item["selectedKeys"] = selected
					item["udtPath"] = machine.udt_path
					item["machineId"] = machine.machine_id
					item["database"] = machine.database
				actions.append(item)
			data["actions"] = actions
		rows.append(data)
	repeater.props.instances = rows
	return built


def refresh(page):
	repeater = _cards(page)
	rows = []
	for row in list(repeater.props.instances):
		data = dict(row)
		selected = data.get("selectedKeys")
		if selected:
			machine = metrics.context.MachineContext.from_map(data)
			data["metrics"] = resolve(selected, machine, _previous_by_key(data.get("metrics")))
		rows.append(data)
	repeater.props.instances = rows
