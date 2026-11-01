
class MetricSource(object):
	"""Lee el valor crudo de una metrica. Las subclases deciden el origen."""

	kind = "base"

	def __init__(self, key):
		self.key = key

	def read(self, context):
		raise NotImplementedError("read")


class UdtTagSource(MetricSource):
	"""Lee un miembro del UDT de la maquina.

	udtPath en el contexto es la instancia, por ejemplo [default]Lineas/Linea1.
	relative_path es el miembro, por ejemplo SKU o Produccion/Piezas.
	"""

	kind = "udt"

	def __init__(self, key, relative_path):
		MetricSource.__init__(self, key)
		self.relative_path = relative_path

	def tag_path(self, context):
		base = str(context.get("udtPath", "") or "").rstrip("/")
		relative = str(self.relative_path or "").lstrip("/")
		if not base:
			return relative
		if not relative:
			return base
		return base + "/" + relative

	def read(self, context):
		path = self.tag_path(context)
		if not path:
			return None
		try:
			qualified = system.tag.readBlocking([path])[0]
		except Exception:
			return None
		if not _quality_good(qualified):
			return None
		return qualified.value


class DatabaseSource(MetricSource):
	"""Lee un escalar con una consulta preparada.

	La consulta usa ? y param_names salen del contexto (machineId, udtPath).
	database vacio usa la conexion por defecto del proyecto.
	"""

	kind = "database"

	def __init__(self, key, query, value_column=0, param_names=None):
		MetricSource.__init__(self, key)
		self.query = query
		self.value_column = value_column
		self.param_names = list(param_names or ["machineId"])

	def read(self, context):
		args = [context.get(name) for name in self.param_names]
		database = context.get("database", "") or ""
		try:
			if database:
				rows = system.db.runPrepQuery(self.query, args, database)
			else:
				rows = system.db.runPrepQuery(self.query, args)
		except Exception:
			return None
		if not rows:
			return None
		try:
			return rows[0][self.value_column]
		except Exception:
			return None


def _quality_good(qualified):
	quality = getattr(qualified, "quality", None)
	if quality is None:
		return False
	is_good = getattr(quality, "isGood", None)
	if callable(is_good):
		try:
			return bool(is_good())
		except Exception:
			return False
	return str(quality).lower().startswith("good")
