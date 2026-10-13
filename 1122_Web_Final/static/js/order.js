document.addEventListener("DOMContentLoaded", function() {
    const c = document.getElementById("myCanvas");
    const ctx = c.getContext("2d");

    // 創建圖片
    const imgMain = new Image();
    // 使用相對路徑，從 JS 檔案位置 (static/js/) 向上兩層到根目錄，再進入 static/images/
    imgMain.src = '../images/webcanvas.png';

    // 圖片加載後畫到Canvas
    imgMain.onload = function() {   //寬183 長136 間隔4

    //(原圖x, 原圖y, 原圖要畫多少x, 原圖要畫多少y, canvas上x, canvas上y, canvas上畫多少x, canvas上畫多少y)

        ctx.drawImage(imgMain, 0, 0, 183, 136,0,0,183,136);
        ctx.drawImage(imgMain, 187.5, 0, 183, 136,183,0,183,136);
        ctx.drawImage(imgMain, 0, 142, 183, 136,366,0,183,136);
        ctx.drawImage(imgMain, 187.5, 142, 183, 136,549,0,183,136);

        ctx.drawImage(imgMain, 0, 278, 183, 136,0,136,183,136);
        ctx.drawImage(imgMain, 187, 278, 183, 136,183,136,183,136);
        ctx.drawImage(imgMain, 0, 424.5, 183, 136,366,136,183,138);
        ctx.drawImage(imgMain, 187.5, 424.5, 183, 136,549,136,183,138);
    };
});