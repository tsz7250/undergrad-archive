let category = document.getElementById('category');
let categoryData = JSON.parse(document.getElementById('categoryData').innerHTML);
let product = document.getElementById('product');
let productData = JSON.parse(document.getElementById('productData').innerHTML);

console.log(categoryData);

let trace1 = {
    type : "pie",
    labels : [],
    values : [],
    textinfo : "label",
    // domain :{
    //     row : 0, column : 0
    // },
}

trace1.values.push(categoryData[0]['套餐']);
trace1.values.push(categoryData[0]['麵']);
trace1.values.push(categoryData[0]['飯']);
trace1.values.push(categoryData[0]['潛艇堡']);
trace1.values.push(categoryData[0]['吐司']);
trace1.values.push(categoryData[0]['沙拉']);
trace1.values.push(categoryData[0]['三明治']);
trace1.values.push(categoryData[0]['鬆餅']);

trace1.labels.push('套餐');
trace1.labels.push('麵');
trace1.labels.push('飯');
trace1.labels.push('潛艇堡');
trace1.labels.push('吐司');
trace1.labels.push('沙拉');
trace1.labels.push('三明治');
trace1.labels.push('鬆餅');

console.log(trace1);

let data1 = [];
data1.push(trace1);

let trace2 = {};
trace2.type = "pie";
trace2.labels = [];
trace2.values = [];

for (let i = 0; i < productData.length; i++){
    if ('名稱' in productData[i]) {
        trace2.labels.push(productData[i]['名稱']);
    } else {
        console.log('名稱 not found in productData[' + i + ']');
    }
    if ('賣出/份' in productData[i]) {
        trace2.values.push(productData[i]['賣出/份']);
    } else {
        console.log('賣出/份 not found in productData[' + i + ']');
    }
}

console.log(trace2);

let threshold = 0.019;  // 設定閾值

let filteredLabels = [];
let filteredValues = [];

for (let i = 0; i < trace2.labels.length; i++){
    let proportion = trace2.values[i] / trace2.values.reduce((a, b) => a + b, 0);
    if (proportion > threshold) {
        filteredLabels.push(trace2.labels[i]);
        filteredValues.push(trace2.values[i]);
    }
}

let filteredTrace2 = {
    type: "pie",
    labels: filteredLabels,
    values: filteredValues,
    textinfo: "label",
    // domain: {
    //     row: 0, column: 1
    // }
};

console.log(filteredTrace2);

let data2 = [];
data2.push(filteredTrace2);

let layout1 = {
    title: "上個月暢銷類別比例圖",
    autosize: true,
    margin: {
        t: 80
    },
    height: 650,
    width: 650,
    font: {
        size: 19,
        color: 'black'
    },
};

let layout2 = {
    title: "上個月暢銷商品比例圖",
    autosize: true,
    margin: {
        t: 80
    },
    height: 690,
    width: 690,
    font: {
        size: 19,
        color: 'black'
    },
};


Plotly.newPlot(category, data1, layout1);
Plotly.newPlot(product, data2, layout2);