$.get('/api/sales/daily/', function(result, status){

    var sales = [];
    var profit = [];
    var sales_date = [];

    $.each(result.sales_data, function(index, value){

        $('.daily-sales-tbody').append('<tr><td>'+ value.date + '</td><td>' + value.sales + '</td><td>' + value.profit + '</td></tr>');

        sales.push(value.sales);
        profit.push(value.profit);
        sales_date.push(value.date);

    });
    Highcharts.chart('daily_graph', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Daily Sales Weekly'
        },
        subtitle: {
            text: 'Inventory'
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
                text: ''
            },
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        tooltip: {
            split: true,
            valueSuffix: 'Rs'
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
        }]
    });

});

$.get('/api/sales/weekly/', function(result, status){

    var sales = [];
    var profit = [];
    var sales_date = [];

    $.each(result.sales_data, function (index, value) {

        $('.weekly-sales-tbody').append('<tr><td>'+ value.date + '</td><td>' + value.sales + '</td><td>' + value.profit + '</td></tr>');
        sales.push(value.sales);
        profit.push(value.profit);
        sales_date.push(value.date);
    });


    Highcharts.chart('weekly-graph', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Sales Graph Weekly'
        },
        subtitle: {
            text: 'Inventory'
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
                text: ''
            },
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        tooltip: {
            split: true,
            valueSuffix: 'Rs'
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
        }]
    });

});

$.get('/api/sales/monthly/', function (result, status) {
    var sales = [];
    var profit = [];
    var day = [];
    $.each(result.sales_data , function (index, value) {
        $('.monthly-sales-tbody').append('<tr><td>'+ value.day + '</td><td>' + value.sales + '</td><td>' + value.profit + '</td></tr>');


        sales.push(value.sales);
        profit.push(value.profit);
        day.push(value.day);
    });

    Highcharts.chart('monthly-graph', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Monthly Sales Graph'
        },
        subtitle: {
            text: 'Inventory'
        },
        xAxis: {
            categories: day.reverse(),
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                text: 'Billions'
            },
            labels: {
                formatter: function () {
                    return this.value;
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
            name: 'sales',
            data: sales.reverse()
        }]
    });
});

// Dashboard daily profit chart code

var doughnutData = [
    {
        value: 70,
        color:"#68dff0"
    },
    {
        value : 30,
        color : "#fdfdfd"
    }
];
var myDoughnut = new Chart(document.getElementById("todays-sales").getContext("2d")).Doughnut(doughnutData);


// dashboard profit chart code
var doughnutData = [
    {
        value: 20,
        color:"#68dff0"
    },
    {
        value : 80,
        color : "#fdfdfd"
    }
];
var myDoughnut = new Chart(document.getElementById("todays-profit").getContext("2d")).Doughnut(doughnutData);

//dashboard daily loan chart code
var doughnutData = [
    {
        value: 60,
        color:"#68dff0"
    },
    {
        value : 40,
        color : "#fdfdfd"
    }
];
var myDoughnut = new Chart(document.getElementById("serverstatus002").getContext("2d")).Doughnut(doughnutData);