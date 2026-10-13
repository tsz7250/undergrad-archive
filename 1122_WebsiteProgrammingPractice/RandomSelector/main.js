window.onload = function() {
    //document.write("Hello, JavaScript!");
    $(function() {
        $("input").on("click", function() {
            //alert("Hi");

            //random select the food
            // var numOfListItem = $("li").length;
            // var randomChildNumber = Math.floor(Math.random() * numOfListItem);
            // $("#ans").text($("li").eq(randomChildNumber).text());


            //test the random number
            var noodle=0, rice=0, dumpling=0;
            for(var i=0;i<1000;++i){  
                var numOfListItem = $("li").length;
                var randomChildNumber = Math.floor(Math.random() * numOfListItem);
                if(randomChildNumber==0){
                    noodle++;
                }else if(randomChildNumber==1){
                    rice++;
                }else if(randomChildNumber==2){
                    dumpling++;
                }
            }
            $("#ran").text("拉麵:"+noodle+" 滷肉飯:"+rice+" 水餃:"+dumpling);

            //show photo of the food
            // var selectedFood = $("li").eq(randomChildNumber).text();
            // if (selectedFood == "拉麵") {
            //     $("#pic").attr("src", "noodle.jpg");
            // } else if (selectedFood == "滷肉飯") {
            //     $("#pic").attr("src", "rice.jpg");
            // } else if (selectedFood == "水餃") {
            //     $("#pic").attr("src", "dumpling.jpg");
            // }
        });
    });
}