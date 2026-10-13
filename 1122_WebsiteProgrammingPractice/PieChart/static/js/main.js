let survived_pie = document.getElementById('pie1');
let sex_pie = document.getElementById('pie2');
let embarked_pie = document.getElementById('pie3');

let survived_count = JSON.parse(document.getElementById('survived_count').textContent);
let sex_count = JSON.parse(document.getElementById('sex_count').textContent);
let embarked_count = JSON.parse(document.getElementById('embarked_count').textContent);

console.log(survived_count);
console.log(sex_count);
console.log(embarked_count);

let trace1 = {};
trace1.type = "pie";
trace1.title = "Survived vs Not Survived";
trace1.labels = [
    "Not Survived",
    "Survived"
];
trace1.values = [
    survived_count[0],
    survived_count[1]
];
trace1.domain = {
    row: 0,
    column: 0
};
trace1.text = [
    survived_count[0],
    survived_count[1]
];

let trace2 = {};
trace2.type = "pie";
trace2.title = "Male vs Female";
trace2.labels = [
    "Male",
    "Female"
];
trace2.values = [
    sex_count["male"],
    sex_count["female"]
];
trace2.domain = {
    row: 0,
    column: 0
};
trace2.text = [
    sex_count["male"],
    sex_count["female"]
];

let trace3 = {};
trace3.type = "pie";
trace3.title = "Embarked: S/C/Q";
trace3.labels = [
    "S",
    "C",
    "Q"
];
trace3.values = [
    embarked_count["S"],
    embarked_count["C"],
    embarked_count["Q"]
];
trace3.domain = {
    row: 0,
    column: 0
};
trace3.text = [
    embarked_count["S"],
    embarked_count["C"],
    embarked_count["Q"]
];

let data1 = [trace1];
let data2 = [trace2];
let data3 = [trace3];

let layout = {
    margin: {
        t: 10,
        l: 0,
    }
};

Plotly.newPlot(survived_pie, data1, layout);
Plotly.newPlot(sex_pie, data2, layout);
Plotly.newPlot(embarked_pie, data3, layout);

