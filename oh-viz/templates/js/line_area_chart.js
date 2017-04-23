$(function () {
        Highcharts.setOptions({
            lang: {
                thousandsSep: ','
            }
        });

        // console.log(charts)
        $.each(charts, function (i, chart) {
          // unpack multiple series per chart
            // console.log(chart.series[0].name)
            var chart_series = [],
                len = chart.series.length,
                i = 0,
                chart_id = chart._id;

            for(i;i<len;i++){
              // console.log(chart.series[i]);
              chart_series.push({
                name: chart.series[i].name,
                type: chart.series[i].type,
                data: chart.series[i].data,
                showInLegend: chart.series[i].showInLegend,
                visible: chart.series[i].visible,
                tooltip: {
                    valueDecimals:0,
                    pointFormat: chart.series[i].pointFormat
                }
              })
            }
          console.log('#' + chart._id)
          // iteratively draw charts
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
        });
});
