from predefined import *


class BarGraph(Div):

    GRAPH_TEMPLATE = """
var ctx = document.getElementById("%(name)s").getContext('2d');
var myChart = new Chart(ctx, {
    type: '%(graphType)s',
    data: {
        labels: %(labels)s,
        datasets: [{
            label: '%(name)s',
            data: %(data)s,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
    """

    TYPE = 'bar'

    def __init__(self, name, values, width, height):
        """
        :param name: name of the chart
        :param values: dict of values
        :param width: int
        :param height: int
        """
        super(BarGraph, self).__init__()

        self.addValue(Element('canvas',
                              id=name,
                              width=width,
                              height=height,
                              style='display: block; width: %(width)spx !important; height: %(height)spx !important;' % locals())
                      )

        graphType = self.TYPE
        labels = []
        data = []
        sortedValues = sorted(values)
        sortedValues.reverse()
        for key in sortedValues:
            labels.insert(0, key)
            data.insert(0, values[key])

        self.addValue(Script(self.GRAPH_TEMPLATE % locals()))


class LineGraph(BarGraph):

    TYPE = 'line'