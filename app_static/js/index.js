function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

$.get('/api/sales/daily/').done(function(result){

    var sales = [];
    var profit = [];
    var sales_date = [];

    $.each(result.sales_data, function(index, value){
        $('.daily-sales-tbody').append(
            '<tr><td>'+ escapeHtml(value.date) + '</td><td>' +
            escapeHtml(value.sales) + '</td><td>' +
            escapeHtml(value.profit) + '</td></tr>'
        );

        sales.push(value.sales);
        profit.push(value.profit);
        sales_date.push(value.date);
    });

    if (typeof Highcharts !== 'undefined' && document.getElementById('daily_graph')) {
        Highcharts.chart('daily_graph', {
            chart: { type: 'area' },
            title: { text: 'Daily Sales Weekly' },
            subtitle: { text: 'Inventory' },
            xAxis: {
                categories: sales_date.reverse(),
                tickmarkPlacement: 'on',
                title: { enabled: false }
            },
            yAxis: {
                title: { text: '' },
                labels: { formatter: function () { return this.value; } }
            },
            tooltip: { split: true, valueSuffix: 'Rs' },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: { lineWidth: 1, lineColor: '#666666' }
                }
            },
            series: [
                { name: 'Sales', data: sales.reverse() },
                { name: 'Profit', data: profit.reverse() }
            ]
        });
    }
}).fail(function() {
    $('.daily-sales-tbody').append('<tr><td colspan="3">Failed to load daily sales data</td></tr>');
});

$.get('/api/sales/weekly/').done(function(result){

    var sales = [];
    var profit = [];
    var sales_date = [];

    $.each(result.sales_data, function (index, value) {
        $('.weekly-sales-tbody').append(
            '<tr><td>'+ escapeHtml(value.date) + '</td><td>' +
            escapeHtml(value.sales) + '</td><td>' +
            escapeHtml(value.profit) + '</td></tr>'
        );
        sales.push(value.sales);
        profit.push(value.profit);
        sales_date.push(value.date);
    });

    if (typeof Highcharts !== 'undefined' && document.getElementById('weekly-graph')) {
        Highcharts.chart('weekly-graph', {
            chart: { type: 'area' },
            title: { text: 'Sales Graph Weekly' },
            subtitle: { text: 'Inventory' },
            xAxis: {
                categories: sales_date.reverse(),
                tickmarkPlacement: 'on',
                title: { enabled: false }
            },
            yAxis: {
                title: { text: '' },
                labels: { formatter: function () { return this.value; } }
            },
            tooltip: { split: true, valueSuffix: 'Rs' },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: { lineWidth: 1, lineColor: '#666666' }
                }
            },
            series: [
                { name: 'Sales', data: sales.reverse() },
                { name: 'Profit', data: profit.reverse() }
            ]
        });
    }
}).fail(function() {
    $('.weekly-sales-tbody').append('<tr><td colspan="3">Failed to load weekly sales data</td></tr>');
});

$.get('/api/sales/monthly/').done(function(result) {
    var sales = [];
    var profit = [];
    var day = [];

    $.each(result.sales_data , function (index, value) {
        $('.monthly-sales-tbody').append(
            '<tr><td>'+ escapeHtml(value.day) + '</td><td>' +
            escapeHtml(value.sales) + '</td><td>' +
            escapeHtml(value.profit) + '</td></tr>'
        );

        sales.push(value.sales);
        profit.push(value.profit);
        day.push(value.day);
    });

    if (typeof Highcharts !== 'undefined' && document.getElementById('monthly-graph')) {
        Highcharts.chart('monthly-graph', {
            chart: { type: 'area' },
            title: { text: 'Monthly Sales Graph' },
            subtitle: { text: 'Inventory' },
            xAxis: {
                categories: day.reverse(),
                tickmarkPlacement: 'on',
                title: { enabled: false }
            },
            yAxis: {
                title: { text: '' },
                labels: { formatter: function () { return this.value; } }
            },
            tooltip: { split: true, valueSuffix: ' Rs' },
            plotOptions: {
                area: {
                    stacking: 'normal',
                    lineColor: '#666666',
                    lineWidth: 1,
                    marker: { lineWidth: 1, lineColor: '#666666' }
                }
            },
            series: [
                { name: 'Sales', data: sales.reverse() },
                { name: 'Profit', data: profit.reverse() }
            ]
        });
    }
}).fail(function() {
    $('.monthly-sales-tbody').append('<tr><td colspan="3">Failed to load monthly sales data</td></tr>');
});

$(document).ready(function() {
    var todaySalesEl = document.getElementById("todays-sales");
    var todaysProfitEl = document.getElementById("todays-profit");
    var serverStatusEl = document.getElementById("serverstatus002");

    if (typeof Chart !== 'undefined') {
        if (todaySalesEl) {
            var todaySalesVal = parseInt(todaySalesEl.getAttribute('data-value') || '0', 10);
            var remaining = Math.max(0, 100 - todaySalesVal);
            new Chart(todaySalesEl.getContext("2d")).Doughnut([
                { value: todaySalesVal || 1, color: "#68dff0" },
                { value: remaining || 1, color: "#fdfdfd" }
            ]);
        }
        if (todaysProfitEl) {
            var todayProfitVal = parseInt(todaysProfitEl.getAttribute('data-value') || '0', 10);
            var profitRemaining = Math.max(0, 100 - todayProfitVal);
            new Chart(todaysProfitEl.getContext("2d")).Doughnut([
                { value: todayProfitVal || 1, color: "#68dff0" },
                { value: profitRemaining || 1, color: "#fdfdfd" }
            ]);
        }
        if (serverStatusEl) {
            new Chart(serverStatusEl.getContext("2d")).Doughnut([
                { value: 60, color: "#68dff0" },
                { value: 40, color: "#fdfdfd" }
            ]);
        }
    }
});
