function calculateDays() {
    var start = new Date(document.getElementById('Start').value);
    var end = new Date(document.getElementById('End').value);
    var diffTime = Math.abs(end.getTime() - start.getTime());
    var diffDays = (diffTime / (1000 * 60 * 60 * 24));
    document.getElementById('result').innerHTML = `一共 ${diffDays.toFixed(3)} 天，所以要買 ${Math.ceil(diffDays)} 天的sim卡量`;
}