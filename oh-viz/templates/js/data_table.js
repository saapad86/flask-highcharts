$(function () {
        Highcharts.setOptions({
            lang: {
                thousandsSep: ','
            }
        });

        // console.log(charts)
        $.each(tables, function (i, table) {
            $('#example').DataTable( {
                    data: table.data,
                    columns: [
                        { title: "Name" },
                        { title: "Position" },
                        { title: "Office" },
                        { title: "Extn." },
                        { title: "Start date" },
                        { title: "Salary" }
                    ]
                } );
        });

            $(document).ready(function() {
    
});

    $('<div>')
            .appendTo('#' + chart._id)
            .highcharts({
                chart: {
                  zoomType: 'x'
                },
                plotOptions: {
                    series: {
                        connectNulls: false,
                        marker: {
                            enabled: false
                        }
                     }
                 },
                title: {
                    text: chart.title
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                            'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'datetime'
                },
                yAxis: {
                    title: {
                        text: chart.ylabel
                    }
                },
                credits: {
                    enabled: false
                },
                tooltip: {
                    shared: true
                },
                series: chart_series
            });