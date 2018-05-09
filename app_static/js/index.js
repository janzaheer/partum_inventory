$.get('/api/sales/daily/', function(result, status){

    var sales = [];
    var profit = [];
    var sales_date = [];

    $.each(result.sales_data, function(index, value){


        sales.push(value.sales);
        profit.push(value.profit);
        sales_date.push(value.date);

    });
    Highcharts.chart('graph01', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Partum Inventory Graph on Daily bases'
        },
        subtitle: {
            text: 'Partum Inventory'
        },
        xAxis: {
            categories: sales_date.reverse(),
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                text: 'Rupees'
            },
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        tooltip: {
            split: true,
            valueSuffix: ' rupees'
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },

        series: [{
            name: 'Sales',
            data: sales.reverse()
        }, {
            name: 'Profit',
            data: profit.reverse()
        }]
    });

});



Highcharts.chart('graph2', {
    chart: {
        type: 'area'
    },
    title: {
        text: 'Partum Inventory Graph on weekly bases'
    },
    subtitle: {
        text: 'Partum Inventory'
    },
    xAxis: {
        categories: ['1750', '1800', '1850', '1900', '1950', '1999', '2050'],
        tickmarkPlacement: 'on',
        title: {
            enabled: false
        }
    },
    yAxis: {
        title: {
            text: 'Rupees'
        },
        labels: {
            formatter: function () {
                return this.value ;
            }
        }
    },
    tooltip: {
        split: true,
        valueSuffix: ' Rupees'
    },
    plotOptions: {
        area: {
            stacking: 'normal',
            lineColor: '#666666',
            lineWidth: 1,
            marker: {
                lineWidth: 1,
                lineColor: '#666666'
            }
        }
    },
    series: [{
        name: 'Sales',
        data: [502, 635, 809, 947, 1402, 3634, 5268]
    }, {
        name: 'Profit',
        data: [106, 107, 111, 133, 221, 767, 1766]
    }, {
        name: 'cash',
        data: [63, 03, 76, 08, 47, 29, 28]
    }]
});




//graph 3 js file is here

 // Create the chart

Highcharts.chart('graph3', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Partum Inventory Sales For The year, 2018'
    },
    subtitle: {
        text: 'Click the columns to view versions. Source: <a href="http://statcounter.com" target="_blank">statcounter.com</a>'
    },
    xAxis: {
        type: 'category'
    },
    yAxis: {
        title: {
            text: 'Total percent market share'
        }

    },
    legend: {
        enabled: false
    },
    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}%'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
    },

    "series": [
        {
            "name": "Browsers",
            "colorByPoint": true,
            "data": [
                {
                    "name": "January",
                    "y": 62.74,
                    "drilldown": "January"
                },
                {
                    "name": "February",
                    "y": 10.57,
                    "drilldown": "February"
                },
                {
                    "name": "March",
                    "y": 7.23,
                    "drilldown": "March"
                },
                {
                    "name": "April",
                    "y": 5.58,
                    "drilldown": "April"
                },
                {
                    "name": "May",
                    "y": 4.02,
                    "drilldown": "May"
                },
                {
                    "name": "June",
                    "y": 1.92,
                    "drilldown": "June"
                },


                {
                    "name" : "July",
                     "y": 2.05,
                     "drildown": "July"

                },
                {
                    "name": "Other",
                    "y": 7.62,
                    "drilldown": null
                }
            ]
        }
    ],
    "drilldown": {
        "series": [
            {
                "name": "January",
                "id": "January",
                "data": [
                    [
                        "v65.0",
                        0.1
                    ],
                    [
                        "v64.0",
                        1.3
                    ],
                    [
                        "v63.0",
                        53.02
                    ],
                    [
                        "v62.0",
                        1.4
                    ],
                    [
                        "v61.0",
                        0.88
                    ],
                    [
                        "v60.0",
                        0.56
                    ],
                    [
                        "v59.0",
                        0.45
                    ],
                    [
                        "v58.0",
                        0.49
                    ],
                    [
                        "v57.0",
                        0.32
                    ],
                    [
                        "v56.0",
                        0.29
                    ],
                    [
                        "v55.0",
                        0.79
                    ],
                    [
                        "v54.0",
                        0.18
                    ],
                    [
                        "v51.0",
                        0.13
                    ],
                    [
                        "v49.0",
                        2.16
                    ],
                    [
                        "v48.0",
                        0.13
                    ],
                    [
                        "v47.0",
                        0.11
                    ],
                    [
                        "v43.0",
                        0.17
                    ],
                    [
                        "v29.0",
                        0.26
                    ]
                ]
            },
            {
                "name": "February",
                "id": "February",
                "data": [
                    [
                        "v58.0",
                        1.02
                    ],
                    [
                        "v57.0",
                        7.36
                    ],
                    [
                        "v56.0",
                        0.35
                    ],
                    [
                        "v55.0",
                        0.11
                    ],
                    [
                        "v54.0",
                        0.1
                    ],
                    [
                        "v52.0",
                        0.95
                    ],
                    [
                        "v51.0",
                        0.15
                    ],
                    [
                        "v50.0",
                        0.1
                    ],
                    [
                        "v48.0",
                        0.31
                    ],
                    [
                        "v47.0",
                        0.12
                    ]
                ]
            },
            {
                "name": "March",
                "id": "March",
                "data": [
                    [
                        "v11.0",
                        6.2
                    ],
                    [
                        "v10.0",
                        0.29
                    ],
                    [
                        "v9.0",
                        0.27
                    ],
                    [
                        "v8.0",
                        0.47
                    ]
                ]
            },
            {
                "name": "April",
                "id": "April",
                "data": [
                    [
                        "v11.0",
                        3.39
                    ],
                    [
                        "v10.1",
                        0.96
                    ],
                    [
                        "v10.0",
                        0.36
                    ],
                    [
                        "v9.1",
                        0.54
                    ],
                    [
                        "v9.0",
                        0.13
                    ],
                    [
                        "v5.1",
                        0.2
                    ]
                ]
            },
            {
                "name": "May",
                "id": "May",
                "data": [
                    [
                        "v16",
                        2.6
                    ],
                    [
                        "v15",
                        0.92
                    ],
                    [
                        "v14",
                        0.4
                    ],
                    [
                        "v13",
                        0.1
                    ]
                ]
            },
            {
                "name": "June",
                "id": "June",
                "data": [
                    [
                        "v50.0",
                        0.96
                    ],
                    [
                        "v49.0",
                        0.82
                    ],
                    [
                        "v12.1",
                        0.14
                    ]
                ]
            },

            {
                "name": "July",
                "id": "July",
                "data": [
                    [
                        "v65.0",
                        0.1
                    ],
                    [
                        "v64.0",
                        1.3
                    ],
                    [
                        "v63.0",
                        53.02
                    ],
                    [
                        "v62.0",
                        1.4
                    ],
                    [
                        "v61.0",
                        0.88
                    ],
                    [
                        "v60.0",
                        0.56
                    ],
                    [
                        "v59.0",
                        0.45
                    ],
                    [
                        "v58.0",
                        0.49
                    ],
                    [
                        "v57.0",
                        0.32
                    ],
                    [
                        "v56.0",
                        0.29
                    ],
                    [
                        "v55.0",
                        0.79
                    ],
                    [
                        "v54.0",
                        0.18
                    ],
                    [
                        "v51.0",
                        0.13
                    ],
                    [
                        "v49.0",
                        2.16
                    ],
                    [
                        "v48.0",
                        0.13
                    ],
                    [
                        "v47.0",
                        0.11
                    ],
                    [
                        "v43.0",
                        0.17
                    ],
                    [
                        "v29.0",
                        0.26
                    ]
                ]
            }
        ]
    }
});

