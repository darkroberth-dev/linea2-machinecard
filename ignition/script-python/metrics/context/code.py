
class MachineContext(object):
	"""Datos de la maquina que las fuentes necesitan para leer."""

	def __init__(self, machine_id, udt_path, database="", title=""):
		self.machine_id = machine_id
		self.udt_path = udt_path or ""
		self.database = database or ""
		self.title = title or ""

	def get(self, name, default=None):
		values = {
			"machineId": self.machine_id,
			"udtPath": self.udt_path,
			"database": self.database,
			"title": self.title,
		}
		return values.get(name, default)

	@staticmethod
	def from_map(data):
		data = data or {}
		return MachineContext(
			data.get("machineId", data.get("machine_id", "")),
			data.get("udtPath", data.get("udt_path", "")),
			data.get("database", ""),
			data.get("title", data.get("machineTitle", "")),
		)
