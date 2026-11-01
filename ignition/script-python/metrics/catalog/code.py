
def _text(value):
	if value is None:
		return u"\u2014"
	try:
		return unicode(value)
	except NameError:
		return str(value)


def _percent(value):
	if value is None:
		return u"\u2014"
	return u"%s%%" % _text(value)


def _temperature(value):
	if value is None:
		return u"\u2014"
	return u"%s \u00b0C" % _text(value)


def _minutes(value):
	if value is None:
		return u"\u2014"
	try:
		total = int(float(value))
	except Exception:
		return _text(value)
	return u"%sh %sm" % (total // 60, total % 60)


def default_catalog():
	source = metrics.source
	definition = metrics.definition
	udt = source.UdtTagSource
	db = source.DatabaseSource
	item = definition.MetricDefinition
	return definition.MetricCatalog([
		item("sku", "SKU", udt("sku", "SKU"), icon_left="material/qr_code_scanner"),
		item("clr", "CLR", udt("clr", "CLR"), icon_left="material/layers"),
		item("lastState", "Ultimo estado", udt("lastState", "UltimoEstado"), icon_left="material/access_time"),
		item("dryerTemp", "Piezas salida secador", udt("dryerTemp", "TemperaturaSecador"), icon_left="ignition/heat_exchanger", formatter=_temperature),
		item("availability", "DISPONIBILIDAD", db("availability", "SELECT availability FROM machine_metrics WHERE machine_id = ?", 0, ["machineId"]), icon_right="material/show_chart", formatter=_percent),
		item("downtime", "TIEMPO EN PARO", db("downtime", "SELECT downtime_min FROM machine_metrics WHERE machine_id = ?", 0, ["machineId"]), icon_right="material/show_chart", formatter=_minutes),
		item("stops", "PAROS", udt("stops", "Paros"), icon_right="material/show_chart"),
		item("performance", "RENDIMIENTO", udt("performance", "Rendimiento"), icon_right="material/show_chart", formatter=_percent),
		item("speed", "VELOCIDAD PROMEDIO", udt("speed", "VelocidadPromedio"), icon_right="material/show_chart"),
		item("total", "PRODUCTOS TOTALES", db("total", "SELECT total_pieces FROM machine_metrics WHERE machine_id = ?", 0, ["machineId"]), icon_right="material/show_chart"),
		item("good", "PRODUCTOS CORRECTOS", udt("good", "ProductosCorrectos"), icon_right="material/show_chart"),
		item("runTime", "TIEMPO EN PRODUCCI\u00d3N", udt("runTime", "TiempoProduccion"), icon_right="material/show_chart", formatter=_minutes),
		item("defects", "DEFECTOS", udt("defects", "Defectos"), icon_right="material/show_chart"),
		item("oee", "OEE", udt("oee", "OEE"), icon_right="material/show_chart", formatter=_percent),
		item("rate", "PRODUCCION / MINUTO", udt("rate", "PiezasPorMinuto"), metric_type=1),
	])


LABEL_TO_KEY = {
	"SKU": "sku",
	"CLR": "clr",
	"Ultimo estado": "lastState",
	"Piezas salida secador": "dryerTemp",
	"DISPONIBILIDAD": "availability",
	"TIEMPO EN PARO": "downtime",
	"PAROS": "stops",
	"RENDIMIENTO": "performance",
	"VELOCIDAD PROMEDIO": "speed",
	"PRODUCTOS TOTALES": "total",
	"PRODUCTOS CORRECTOS": "good",
	"TIEMPO EN PRODUCCI\u00d3N": "runTime",
	"TIEMPO EN PRODUCCION": "runTime",
	"DEFECTOS": "defects",
	"OEE": "oee",
	"PRODUCCION / MINUTO": "rate",
}
