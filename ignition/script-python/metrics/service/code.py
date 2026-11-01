def catalog():
	return metrics.catalog.default_catalog()


def options():
	return catalog().options()


def normalize_selection(selected_keys):
	allowed = {}
	for key in catalog().keys():
		allowed[key] = True
	clean = []
	for key in list(selected_keys or []):
		if allowed.get(key) and key not in clean:
			clean.append(key)
	return clean


def selection_rows(selected_keys):
	chosen = {}
	for key in normalize_selection(selected_keys):
		chosen[key] = True
	rows = []
	for row in options():
		item = dict(row)
		item["selected"] = True if chosen.get(item.get("key")) else False
		rows.append(item)
	return rows


def selected_keys(rows):
	keys = []
	for row in rows or []:
		if row.get("selected"):
			keys.append(row.get("key"))
	return normalize_selection(keys)


def _clone(value):
	return system.util.jsonDecode(system.util.jsonEncode(value))


def _previous_by_key(metric_rows):
	previous = {}
	for row in metric_rows or []:
		key = row.get("key") or metrics.catalog.LABEL_TO_KEY.get(row.get("text"))
		if key:
			previous[key] = row.get("percent")
	return previous


def build(selected_keys, context, previous=None):
	machine = context if hasattr(context, "get") else metrics.context.MachineContext.from_map(context)
	return catalog().resolve(normalize_selection(selected_keys), machine, previous)


def _pick(obj, name, default=None):
	if obj is None:
		return default
	try:
		value = obj[name]
	except Exception:
		try:
			value = obj.get(name)
		except Exception:
			return default
	if value is None:
		return default
	return value


def _same(data, machine_title, context):
	wanted = _pick(context, "machineId", "")
	if wanted not in ("", None):
		current = _pick(data, "machineId", "")
		try:
			if int(current) == int(wanted):
				return True
		except Exception:
			if str(current) == str(wanted):
				return True
	left = " ".join(str(_pick(data, "title", "")).split())
	right = " ".join(str(machine_title or "").split())
	return left != "" and left == right


def patch_instances(instances, machine_title, selected_keys, context):
	selected = normalize_selection(selected_keys)
	rows = []
	for raw in list(instances or []):
		data = _clone(raw)
		if not _same(data, machine_title, context or {}):
			rows.append(data)
			continue
		machine = metrics.context.MachineContext.from_map({
			"machineId": _pick(context, "machineId", _pick(data, "machineId", "")),
			"udtPath": _pick(context, "udtPath", _pick(data, "udtPath", "")),
			"database": _pick(context, "database", _pick(data, "database", "")),
			"title": _pick(data, "title", machine_title),
		})
		data["selectedKeys"] = selected
		data["metrics"] = build(selected, machine, _previous_by_key(data.get("metrics")))
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
	return rows


def patch_repeater(repeater, machine_title, selected_keys, context):
	repeater.props.instances = patch_instances(repeater.props.instances, machine_title, selected_keys, context)


def refresh_instances(instances):
	rows = []
	for raw in list(instances or []):
		data = _clone(raw)
		selected = data.get("selectedKeys")
		if selected:
			data["metrics"] = build(selected, metrics.context.MachineContext.from_map(data), _previous_by_key(data.get("metrics")))
		rows.append(data)
	return rows


def refresh_repeater(repeater):
	repeater.props.instances = refresh_instances(repeater.props.instances)
