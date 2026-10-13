console.log(exchangeData);
console.log(exchangeData2);

let twd_jpy_line = document.getElementById('chart1');
let twd_jpy_data = JSON.parse(document.getElementById('exchangeData').innerHTML);

let twd_usd_line = document.getElementById('chart2');
let twd_usd_data = JSON.parse(document.getElementById('exchangeData2').innerHTML);

console.log(twd_jpy_data);
let trace1 = {};
trace1.type = "scatter";
trace1.mode = "lines";
trace1.name = "Team A";

trace1.text = [];

trace1.x = [];
trace1.y = [];

console.log(twd_usd_data);
let trace2 = {};
trace2.type = "scatter";
trace2.mode = "lines";
trace2.name = "Team B";

trace2.text = [];

trace2.x = [];
trace2.y = [];


for (let i = 0; i < twd_jpy_data.length; i++) {
    trace1.x[i] = twd_jpy_data[i].date;
    trace1.y[i] = twd_jpy_data[i]['twd-jpy'];
}

for (let i = 0; i < twd_usd_data.length; i++) {
    trace2.x[i] = twd_usd_data[i].date;
    trace2.y[i] = twd_usd_data[i]['twd-usd'];
}

console.log("trace1.x: ", trace1.x);
console.log("trace1.y: ", trace1.y);
console.log("trace2.x: ", trace2.x);
console.log("trace2.y: ", trace2.y);

let data = [];
data.push(trace1);
let data2 = [];
data2.push(trace2);

let layout = {
    margin: {
        t: 0
    },
    xaxis: {
        showline: true
    },
    yaxis: {
        showline: true
    },
    annotations: [
        {
            xref: 'paper',
            yref: 'paper',
            x: 0.5,
            y: 0.1,
            text: `JPY Exchange ${trace1.x[0]}~ ${trace1.x.slice(-1)}`,
            showarrow: false,
            xanchor: 'center',
            yanchor: 'top',
            font: {
                size: 15,
                color: 'gray'
            }
        }
    ]
};
let layout2 = {
    margin: {
        t: 0
    },
    xaxis: {
        showline: true
    },
    yaxis: {
        showline: true
    },
    annotations: [
        {
            xref: 'paper',
            yref: 'paper',
            x: 0.5,
            y: 0.1,
            text: `USD Exchange ${trace2.x[0]}~ ${trace2.x.slice(-1)}`,
            showarrow: false,
            xanchor: 'center',
            yanchor: 'top',
            font: {
                size: 15,
                color: 'gray'
            }
        }
    ]
};

Plotly.newPlot(twd_jpy_line, data, layout);
Plotly.newPlot(twd_usd_line, data2, layout2);