from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.legends import Legend
from reportlab.lib.styles import ParagraphStyle

class PDFReportGenerator:
	def __init__(self, filename="weather_report.pdf"):
		self.filename = filename
		self.styles = getSampleStyleSheet()

	def create_report(self, weather_data, city):
		doc = SimpleDocTemplate(
			self.filename,
			pagesize=letter,
			rightMargin=72,
			leftMargin=72,
			topMargin=72,
			bottomMargin=72
		)

		elements = []
		elements.append(self._create_title(city))
		elements.append(self._create_table(weather_data))
		elements.append(self._create_line_chart(weather_data))

		doc.build(elements)

	# TITLE CREATION
	def _create_title(self, city):
		heading_style = ParagraphStyle(
			'HeadingStyle',
			parent=self.styles['Heading1'],
			alignment=1,
			fontSize=18,
			spaceAfter=25,
		)
		return Paragraph(f"Weather Report for {city}", heading_style)

	# TABLE CREATION
	def _create_table(self, weather_data):
		table_data = self._prepare_table_data(weather_data)
		table = Table(table_data)
		table.setStyle(TableStyle([
			('BACKGROUND', (0, 0), (-1, 0), colors.grey),
			('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
			('FONTSIZE', (0, 0), (-1, 0), 12),
			('BOTTOMPADDING', (0, 0), (-1, 0), 12),
			('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
			('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
			('FONTSIZE', (0, 1), (-1, -1), 10),
			('GRID', (0, 0), (-1, -1), 1, colors.black)
		]))
		return table

	def _prepare_table_data(self, weather_data):
		table_data = [['Date', 'Average Temperature (°C)', 'Min Hourly Temp', 'Max Hourly Temp']]

		for date, data in weather_data.items():
			hourly_temps = data['hourly_temps']
			row = [
				date,
				f"{data['daily_avg_temp']}°C",
				f"{min(hourly_temps)}°C",
				f"{max(hourly_temps)}°C"
			]
			table_data.append(row)
		return table_data

	# LINE CHART CREATION
	def _create_line_chart(self, weather_data):
		drawing = Drawing(600, 300)

		line_chart = HorizontalLineChart()
		line_chart.x = 25
		line_chart.y = 50
		line_chart.width = 400
		line_chart.height = 200

		line_chart.categoryAxis.categoryNames = [str(i) for i in range(24)]
		data = self._prepare_line_chart_data(weather_data)
		line_chart.data = data

		line_chart.lines[0].strokeColor = colors.green
		line_chart.lines[1].strokeColor = colors.blue
		line_chart.lines[2].strokeColor = colors.red
		line_chart.lines.strokeWidth = 2

		line_chart.valueAxis.valueMin = min(data[1]) - 2
		line_chart.valueAxis.valueMax = max(data[2]) + 2
		line_chart.valueAxis.valueStep = 2
		line_chart.valueAxis.labelTextFormat = '%d°C'

		legend = Legend()
		legend.x = 170
		legend.y = 30
		legend.fontName = 'Helvetica'
		legend.fontSize = 8
		legend.deltax = 150

		legend.colorNamePairs = [
			(colors.red, 'Maximum Temperature'),
			(colors.green, 'Average Temperature'),
			(colors.blue, 'Minimum Temperature'),
		]

		drawing.add(line_chart)
		drawing.add(legend)
		return drawing

	def _prepare_line_chart_data(self, weather_data):
		hourly_mins = [float('inf')] * 24
		hourly_maxs = [float('-inf')] * 24
		hourly_sums = [0.0] * 24
		day_count = len(weather_data)

		for data in weather_data.values():
			hourly_temps = data['hourly_temps']
			for hour, temp in enumerate(hourly_temps):
				hourly_mins[hour] = min(hourly_mins[hour], temp)
				hourly_maxs[hour] = max(hourly_maxs[hour], temp)
				hourly_sums[hour] += temp

		hourly_avgs = [sum_temp / day_count for sum_temp in hourly_sums]

		data = []
		data.append(hourly_avgs)
		data.append(hourly_mins)
		data.append(hourly_maxs)

		return data