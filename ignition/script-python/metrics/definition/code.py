
def _text(value):
	if value is None:
		return u"\u2014"
	try:
		return unicode(value)
	except NameError:
		return str(value)


class MetricDefinition(object):
	"""Une la etiqueta de la tarjeta con su fuente y su formato."""

	def __init__(self, key, label, source, icon_left="", icon_right="", metric_type=0, formatter=None):
		self.key = key
		self.label = label
		self.source = source
		self.icon_left = icon_left or ""
		self.icon_right = icon_right or ""
		self.metric_type = metric_type
		self.formatter = formatter or _text

	def read(self, context, previous=None):
		raw = None
		try:
			raw = self.source.read(context)
		except Exception:
			raw = None
		if raw is None and previous is not None:
			shown = previous
		else:
			try:
				shown = self.formatter(raw)
			except Exception:
				shown = u"\u2014"
		return {
			"key": self.key,
			"text": self.label,
			"percent": shown,
			"iconPathLeft": self.icon_left,
			"iconPathRigth": self.icon_right,
			"type": self.metric_type,
			"instancePosition": {"basis": "0px", "grow": 1, "shrink": 1},
			"instanceStyle": {},
		}


class MetricCatalog(object):
	def __init__(self, definitions):
		self._items = list(definitions)
		self._by_key = {}
		for item in self._items:
			self._by_key[item.key] = item

	def keys(self):
		return [item.key for item in self._items]

	def options(self):
		rows = []
		for item in self._items:
			rows.append({
				"key": item.key,
				"label": item.label,
				"source": item.source.kind,
				"selected": False,
			})
		return rows

	def get(self, key):
		return self._by_key.get(key)

	def resolve(self, selected_keys, context, previous=None):
		previous = previous or {}
		rows = []
		for key in list(selected_keys or []):
			item = self.get(key)
			if item is None:
				continue
			rows.append(item.read(context, previous.get(key)))
		return rows
